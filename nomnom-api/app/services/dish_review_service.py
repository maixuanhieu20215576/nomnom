from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dish_review import DishReview
from app.services.user_service import get_first_admin


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
