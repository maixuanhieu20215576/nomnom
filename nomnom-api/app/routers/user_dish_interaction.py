from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user_dish_interaction import ReactionRequest, StopInteractionRequest, UserDishInteractionRead
from app.services.user_dish_interaction_service import add_time_spent, set_reaction

router = APIRouter(tags=["user-dish-interaction"])


@router.post("/stop-interaction", response_model=UserDishInteractionRead)
async def stop_interaction_route(payload: StopInteractionRequest, db: AsyncSession = Depends(get_db)):
    interaction = await add_time_spent(payload.user_id, payload.dish_id, payload.time_spent_on_post_ms, db)
    return interaction


@router.post("/reaction", response_model=UserDishInteractionRead)
async def reaction_route(payload: ReactionRequest, db: AsyncSession = Depends(get_db)):
    interaction = await set_reaction(payload.user_id, payload.dish_id, payload.reactioned, db)
    return interaction
