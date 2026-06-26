from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.vectorUtils import foodVectorGenerate
from app.models.dish import Dish
from app.models.dish_job import DishJob
from app.schemas.dish import DishCreate
from app.services.dish_review_service import calculate_avg_rating, create_dish_reviews_for_new_dishes


async def create_dish_job(payload: DishCreate, db: AsyncSession) -> DishJob:
    job = DishJob(status="pending", payload=payload.model_dump(mode="json"))
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_dish_job(job_id: int, db: AsyncSession) -> DishJob | None:
    result = await db.execute(select(DishJob).where(DishJob.id == job_id))
    return result.scalar_one_or_none()


async def process_dish_job(job_id: int) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(DishJob).where(DishJob.id == job_id))
        job = result.scalar_one_or_none()
        if job is None:
            return

        payload = DishCreate.model_validate(job.payload)
        try:
            food_vector = foodVectorGenerate(payload.description)
            dish = Dish(
                name=payload.name,
                description=payload.description,
                address_text=payload.address_text,
                district=payload.district,
                country=payload.country,
                price=payload.price,
                material_tag=payload.material_tag,
                taste_tag=payload.taste_tag,
                location=f"POINT({payload.location.longitude} {payload.location.latitude})",
                food_vector=food_vector,
            )
            session.add(dish)
            await session.flush()

            await create_dish_reviews_for_new_dishes(dish.id, payload.image_object_names, payload.rating, session)
            await session.flush()

            dish.avg_rating = await calculate_avg_rating(dish.id, session)

            job.status = "done"
            job.dish_id = dish.id
            await session.commit()
        except Exception as exc:
            await session.rollback()
            result = await session.execute(select(DishJob).where(DishJob.id == job_id))
            job = result.scalar_one_or_none()
            if job is not None:
                job.status = "failed"
                job.error = str(exc)
                await session.commit()
