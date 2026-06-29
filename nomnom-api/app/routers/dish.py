from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from geoalchemy2.shape import to_shape
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.dish import Dish
from app.schemas.dish import (
    DishCreate,
    DishJobCreated,
    DishJobStatus,
    DishListResponse,
    DishRead,
    Location,
)
from app.services.dish_service import (
    create_dish_job,
    get_dish_image_urls,
    get_dish_job,
    list_dishes_for_admin,
    process_dish_job,
)

router = APIRouter(prefix="/dishes", tags=["dishes"])


def _to_dish_read(dish: Dish, image_urls: list[str] | None = None) -> DishRead:
    point = to_shape(dish.location)
    return DishRead(
        id=dish.id,
        name=dish.name,
        description=dish.description,
        address_text=dish.address_text,
        district=dish.district,
        country=dish.country,
        price=dish.price,
        material_tag=dish.material_tag,
        taste_tag=dish.taste_tag,
        location=Location(latitude=point.y, longitude=point.x),
        food_vector=dish.food_vector,
        avg_rating=dish.avg_rating,
        image_urls=image_urls or [],
        created_at=dish.created_at,
        updated_at=dish.updated_at,
    )


@router.post("", response_model=DishJobCreated, status_code=202)
async def create_dish_route(
    payload: DishCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)
):
    job = await create_dish_job(payload, db)
    background_tasks.add_task(process_dish_job, job.id)
    return DishJobCreated(job_id=job.id)


@router.get("", response_model=DishListResponse)
async def list_dishes_route(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    dishes, total = await list_dishes_for_admin(page, page_size, db)
    return DishListResponse(
        items=[_to_dish_read(dish) for dish in dishes],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/jobs/{job_id}", response_model=DishJobStatus)
async def get_dish_job_route(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await get_dish_job(job_id, db)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    dish_read = None
    if job.dish_id is not None:
        result = await db.get(Dish, job.dish_id)
        if result is not None:
            dish_read = _to_dish_read(result)

    return DishJobStatus(job_id=job.id, status=job.status, dish=dish_read, error=job.error)


@router.get("/{dish_id}", response_model=DishRead)
async def get_dish_route(dish_id: int, db: AsyncSession = Depends(get_db)):
    dish = await db.get(Dish, dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    image_urls = await get_dish_image_urls(dish_id, db)
    return _to_dish_read(dish, image_urls)
