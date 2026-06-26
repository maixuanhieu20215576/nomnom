import math
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dish import Dish
from app.models.user import User
from app.models.user_dish_interaction import UserDishInteraction

# score = (w_time*log(1 + timeSpentMs/1000) + w_reaction*reactioned + w_share*shared) * decay
# decay = min(days_since_last_order / RECENCY_DECAY_WINDOW_DAYS, 1), or 1 if never ordered
# Linear decay penalizes dishes ordered recently so they're not re-recommended right away,
# fading out after RECENCY_DECAY_WINDOW_DAYS days.
TIME_SPENT_WEIGHT = 1.0
REACTION_WEIGHT = 3.0
SHARE_WEIGHT = 5.0
RECENCY_DECAY_WINDOW_DAYS = 7

# Only interactions updated within this window are considered on each run, and the
# resulting vector is blended into the existing personal_vector via EMA, instead of
# recomputing from a user's entire interaction history every time.
INTERACTION_LOOKBACK_MINUTES = 15
PERSONAL_VECTOR_EMA_ALPHA = 0.3


def _compute_interaction_score(interaction: UserDishInteraction) -> float:
    raw_score = (
        TIME_SPENT_WEIGHT * math.log1p(interaction.time_spent_on_post_ms / 1000)
        + REACTION_WEIGHT * interaction.reactioned
        + SHARE_WEIGHT * interaction.shared
    )

    if interaction.last_order_at is None:
        decay = 1.0
    else:
        last_order_at = interaction.last_order_at
        if last_order_at.tzinfo is None:
            last_order_at = last_order_at.replace(tzinfo=timezone.utc)
        days_since_order = (datetime.now(timezone.utc) - last_order_at).total_seconds() / 86400
        decay = min(max(days_since_order, 0) / RECENCY_DECAY_WINDOW_DAYS, 1.0)

    return raw_score * decay


# vector_from_recent_interactions = sum(score_i * food_vector_i) / sum(score_i) over
# dishes the user interacted with in the last INTERACTION_LOOKBACK_MINUTES minutes
# (weighted average of food_vector by interaction score).
async def _compute_vector_from_recent_interactions(user_id: int, db: AsyncSession) -> list[float] | None:
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=INTERACTION_LOOKBACK_MINUTES)

    result = await db.execute(
        select(UserDishInteraction, Dish)
        .join(Dish, Dish.id == UserDishInteraction.dish_id)
        .where(
            UserDishInteraction.user_id == user_id,
            UserDishInteraction.updated_at >= cutoff,
            Dish.food_vector.is_not(None),
        )
    )
    rows = result.all()

    weighted_sum: list[float] | None = None
    total_score = 0.0

    for interaction, dish in rows:
        score = _compute_interaction_score(interaction)
        if score <= 0:
            continue

        if weighted_sum is None:
            weighted_sum = [0.0] * len(dish.food_vector)

        for i, value in enumerate(dish.food_vector):
            weighted_sum[i] += score * value
        total_score += score

    if weighted_sum is None or total_score == 0:
        return None

    return [value / total_score for value in weighted_sum]


# personal_vector_new = alpha * vector_from_recent_interactions + (1 - alpha) * personal_vector_old
# Exponential moving average: blends the latest signal into the existing personal_vector
# instead of discarding history, so a single 15-minute batch doesn't overwrite it.
def _blend_with_ema(old_vector: list[float] | None, new_vector: list[float]) -> list[float]:
    if old_vector is None:
        return new_vector

    return [
        PERSONAL_VECTOR_EMA_ALPHA * new_value + (1 - PERSONAL_VECTOR_EMA_ALPHA) * old_value
        for new_value, old_value in zip(new_vector, old_vector)
    ]


async def recompute_personal_vector(user_id: int, db: AsyncSession) -> list[float] | None:
    user = await db.get(User, user_id)
    if user is None:
        return None

    new_vector = await _compute_vector_from_recent_interactions(user_id, db)
    if new_vector is None:
        return None

    old_vector = list(user.personal_vector) if user.personal_vector is not None else None
    return _blend_with_ema(old_vector, new_vector)


async def recompute_all_personal_vectors(db: AsyncSession) -> int:
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=INTERACTION_LOOKBACK_MINUTES)

    result = await db.execute(
        select(UserDishInteraction.user_id).where(UserDishInteraction.updated_at >= cutoff).distinct()
    )
    user_ids = result.scalars().all()

    updated_count = 0
    for user_id in user_ids:
        personal_vector = await recompute_personal_vector(user_id, db)
        if personal_vector is None:
            continue

        user = await db.get(User, user_id)
        user.personal_vector = personal_vector
        updated_count += 1

    await db.commit()
    return updated_count
