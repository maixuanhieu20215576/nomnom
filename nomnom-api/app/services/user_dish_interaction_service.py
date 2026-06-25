from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_dish_interaction import UserDishInteraction


async def add_time_spent(user_id: int, dish_id: int, time_spent_on_post_ms: int, db: AsyncSession) -> UserDishInteraction:
    stmt = (
        insert(UserDishInteraction)
        .values(user_id=user_id, dish_id=dish_id, time_spent_on_post_ms=time_spent_on_post_ms)
        .on_conflict_do_update(
            index_elements=["user_id", "dish_id"],
            set_={
                "time_spent_on_post_ms": UserDishInteraction.time_spent_on_post_ms + time_spent_on_post_ms,
            },
        )
        .returning(UserDishInteraction)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one()


async def set_reaction(user_id: int, dish_id: int, reactioned: bool, db: AsyncSession) -> UserDishInteraction:
    stmt = (
        insert(UserDishInteraction)
        .values(user_id=user_id, dish_id=dish_id, reactioned=reactioned)
        .on_conflict_do_update(
            index_elements=["user_id", "dish_id"],
            set_={"reactioned": reactioned},
        )
        .returning(UserDishInteraction)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one()
