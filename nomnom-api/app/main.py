from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging_config import setup_logging
from app.core.scheduler import shutdown_scheduler, start_scheduler
from app.routers import achievement, auth, dish, image, job, log, user_dish_interaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    start_scheduler()
    yield
    shutdown_scheduler()


app = FastAPI(title="Nomnom API", version="0.1.0", lifespan=lifespan)

app.include_router(achievement.router)
app.include_router(auth.router)
app.include_router(dish.router)
app.include_router(image.router)
app.include_router(job.router)
app.include_router(log.router)
app.include_router(user_dish_interaction.router)

@app.get("/health")
async def health():
    return {"status": "ok"}