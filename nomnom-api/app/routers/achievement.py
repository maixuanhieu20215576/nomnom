from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.models.user import User
from app.schemas.achievement import (
    AchievementCreate,
    AchievementRead,
    RefreshUserAchievementsResponse,
)
from app.services.achievement_service import create_achievement, update_user_achievements

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.post("", response_model=AchievementRead, dependencies=[Depends(require_admin)])
async def create_achievement_route(payload: AchievementCreate, db: AsyncSession = Depends(get_db)):
    return await create_achievement(payload, db)


@router.post("/refresh", response_model=RefreshUserAchievementsResponse)
async def refresh_user_achievements_route(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    unlocked_ids = await update_user_achievements(current_user.id, db)
    return RefreshUserAchievementsResponse(unlocked_achievement_ids=unlocked_ids)
