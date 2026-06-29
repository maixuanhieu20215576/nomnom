from fastapi import APIRouter, Depends

from app.core.scheduler import run_recompute_personal_vectors, run_update_dish_rating
from app.core.security import require_admin

router = APIRouter(prefix="/jobs", tags=["jobs"], dependencies=[Depends(require_admin)])


@router.post("/update-dish-rating")
async def trigger_update_dish_rating_route():
    await run_update_dish_rating()
    return {"status": "ok"}


@router.post("/recompute-personal-vector")
async def trigger_recompute_personal_vectors_route():
    await run_recompute_personal_vectors()
    return {"status": "ok"}
