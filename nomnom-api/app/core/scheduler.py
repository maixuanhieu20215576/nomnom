import logging
from enum import StrEnum

from apscheduler.events import EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.database import AsyncSessionLocal
from app.services.dish_review_service import update_dish_rating
from app.services.personal_vector_service import recompute_all_personal_vectors

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


class JobId(StrEnum):
    UPDATE_DISH_RATING = "update_dish_rating"
    RECOMPUTE_PERSONAL_VECTOR = "recompute_personal_vector"


async def run_update_dish_rating() -> None:
    async with AsyncSessionLocal() as db:
        updated_count = await update_dish_rating(db)
        logger.info("update_dish_rating: updated %d dish(es)", updated_count)


async def run_recompute_personal_vectors() -> None:
    async with AsyncSessionLocal() as db:
        updated_count = await recompute_all_personal_vectors(db)
        logger.info("recompute_personal_vector: updated %d user(s)", updated_count)


def _on_job_error(event: JobExecutionEvent) -> None:
    logger.error("Scheduled job %s failed", event.job_id, exc_info=event.exception)
    raise event.exception


def start_scheduler() -> None:
    scheduler.add_listener(_on_job_error, EVENT_JOB_ERROR)
    scheduler.add_job(
        run_update_dish_rating,
        trigger="interval",
        hours=3,
        id=JobId.UPDATE_DISH_RATING,
        replace_existing=True,
    )
    scheduler.add_job(
        run_recompute_personal_vectors,
        trigger="interval",
        minutes=5,
        id=JobId.RECOMPUTE_PERSONAL_VECTOR,
        replace_existing=True,
    )
    scheduler.start()


def shutdown_scheduler() -> None:
    scheduler.shutdown(wait=False)
