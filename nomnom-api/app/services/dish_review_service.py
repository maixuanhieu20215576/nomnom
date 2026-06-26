from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dish import Dish
from app.models.dish_review import DishReview
from app.services.user_service import get_first_admin

DISH_RATING_LOOKBACK_HOURS = 12


async def create_dish_reviews_for_new_dishes(
    dish_id: int, image_object_names: list[str], rating: Decimal, db: AsyncSession
) -> None:
    admin = await get_first_admin(db)
    if admin is None:
        raise ValueError("No admin user found to attribute dish reviews to")

    for image_object_name in image_object_names:
        db.add(
            DishReview(
                user_id=admin.id,
                dish_id=dish_id,
                image_object_name=image_object_name,
                rating=rating,
                caption=None,
            )
        )


async def calculate_avg_rating(dish_id: int, db: AsyncSession) -> Decimal | None:
    result = await db.execute(select(func.avg(DishReview.rating)).where(DishReview.dish_id == dish_id))
    return result.scalar()


async def update_dish_rating(db: AsyncSession) -> int:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=DISH_RATING_LOOKBACK_HOURS)

    result = await db.execute(
        select(DishReview.dish_id).where(DishReview.created_at >= cutoff).distinct()
    )
    dish_ids = result.scalars().all()

    updated_count = 0
    for dish_id in dish_ids:
        avg_rating = await calculate_avg_rating(dish_id, db)
        dish = await db.get(Dish, dish_id)
        if dish is None:
            continue
        dish.avg_rating = avg_rating
        updated_count += 1

    await db.commit()
    return updated_count
