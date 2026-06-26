from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.achievement import (
    AchievementCreate,
    AchievementRead,
    RefreshUserAchievementsRequest,
    RefreshUserAchievementsResponse,
)
from app.services.achievement_service import create_achievement, update_user_achievements

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.post("", response_model=AchievementRead)
async def create_achievement_route(payload: AchievementCreate, db: AsyncSession = Depends(get_db)):
    return await create_achievement(payload, db)


@router.post("/refresh", response_model=RefreshUserAchievementsResponse)
async def refresh_user_achievements_route(payload: RefreshUserAchievementsRequest, db: AsyncSession = Depends(get_db)):
    unlocked_ids = await update_user_achievements(payload.user_id, db)
    return RefreshUserAchievementsResponse(unlocked_achievement_ids=unlocked_ids)
