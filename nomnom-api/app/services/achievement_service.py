from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.achievement import Achievement
from app.models.dish import Dish
from app.models.dish_review import DishReview
from app.models.user import User
from app.models.user_achievement import UserAchievement
from app.schemas.achievement import AchievementCreate

ARRAY_FIELDS = {"material_tag", "taste_tag"}
RECENT_REVIEW_WINDOW_HOURS = 24


async def create_achievement(payload: AchievementCreate, db: AsyncSession) -> Achievement:
    achievement = Achievement(
        title=payload.title,
        description=payload.description,
        icon_object_name=payload.icon_object_name,
        criteria=payload.criteria.model_dump(mode="json"),
    )
    db.add(achievement)
    await db.commit()
    await db.refresh(achievement)
    return achievement


async def _has_recent_dish_review(user_id: int, db: AsyncSession) -> bool:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=RECENT_REVIEW_WINDOW_HOURS)
    result = await db.execute(
        select(func.count())
        .select_from(DishReview)
        .where(DishReview.user_id == user_id, DishReview.created_at >= cutoff)
    )
    return result.scalar_one() > 0


async def _check_tag_value_count(user_id: int, criteria: dict, db: AsyncSession) -> bool:
    column = getattr(Dish, criteria["field"])
    condition = column.any(criteria["value"]) if criteria["field"] in ARRAY_FIELDS else column == criteria["value"]

    result = await db.execute(
        select(func.count())
        .select_from(DishReview)
        .join(Dish, Dish.id == DishReview.dish_id)
        .where(DishReview.user_id == user_id, condition)
    )
    return result.scalar_one() >= criteria["min_count"]


async def _check_distinct_value_count(user_id: int, criteria: dict, db: AsyncSession) -> bool:
    column = getattr(Dish, criteria["field"])
    distinct_expr = func.unnest(column) if criteria["field"] in ARRAY_FIELDS else column

    result = await db.execute(
        select(func.count(func.distinct(distinct_expr)))
        .select_from(DishReview)
        .join(Dish, Dish.id == DishReview.dish_id)
        .where(DishReview.user_id == user_id, column.is_not(None))
    )
    return result.scalar_one() >= criteria["min_distinct"]


async def _check_review_count(user_id: int, criteria: dict, db: AsyncSession) -> bool:
    result = await db.execute(select(func.count()).select_from(DishReview).where(DishReview.user_id == user_id))
    return result.scalar_one() >= criteria["min_count"]


async def _check_consecutive_days(user_id: int, criteria: dict, db: AsyncSession) -> bool:
    result = await db.execute(
        select(func.distinct(func.date(DishReview.created_at)))
        .where(DishReview.user_id == user_id)
        .order_by(func.date(DishReview.created_at).desc())
    )
    review_dates = result.scalars().all()

    min_days = criteria["min_days"]
    if len(review_dates) < min_days:
        return False

    streak = 1
    for i in range(len(review_dates) - 1):
        if review_dates[i] - review_dates[i + 1] == timedelta(days=1):
            streak += 1
            if streak >= min_days:
                return True
        else:
            streak = 1

    return False


_CRITERIA_CHECKERS = {
    "tag_value_count": _check_tag_value_count,
    "distinct_value_count": _check_distinct_value_count,
    "review_count": _check_review_count,
    "consecutive_days": _check_consecutive_days,
}


async def _check_achievement_criteria(user_id: int, achievement: Achievement, db: AsyncSession) -> bool:
    checker = _CRITERIA_CHECKERS[achievement.criteria["type"]]
    return await checker(user_id, achievement.criteria, db)


async def update_user_achievements(user_id: int, db: AsyncSession) -> list[int]:
    if not await _has_recent_dish_review(user_id, db):
        return []

    result = await db.execute(select(Achievement))
    achievements = result.scalars().all()

    unlocked_ids = []
    for achievement in achievements:
        if not await _check_achievement_criteria(user_id, achievement, db):
            continue

        stmt = (
            insert(UserAchievement)
            .values(user_id=user_id, achievement_id=achievement.id)
            .on_conflict_do_nothing(index_elements=["user_id", "achievement_id"])
        )
        await db.execute(stmt)
        unlocked_ids.append(achievement.id)

    await db.commit()
    return unlocked_ids


async def update_all_users_achievements(db: AsyncSession) -> int:
    result = await db.execute(select(User.id))
    user_ids = result.scalars().all()

    updated_count = 0
    for user_id in user_ids:
        unlocked_ids = await update_user_achievements(user_id, db)
        if unlocked_ids:
            updated_count += 1

    return updated_count
