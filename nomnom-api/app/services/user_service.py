from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_first_admin(db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.role == "admin").order_by(User.id).limit(1))
    return result.scalar_one_or_none()
