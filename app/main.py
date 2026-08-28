from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models
from app.api.posts import router as posts_router
from app.api.publish import router as publish_router
from app.api.review import router as review_router
from app.api.schedules import router as schedules_router
from app.api.variants import router as variants_router
from app.core.database import Base, engine
from app.api.history import router as history_router
from app.services.scheduler import (
    start_scheduler,
    stop_scheduler,
)


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()

    yield

    stop_scheduler()


app = FastAPI(
    title="Social Media Studio",
    description=(
        "Generate, review, schedule, and publish "
        "social media campaign variants."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(posts_router)
app.include_router(variants_router)
app.include_router(review_router)
app.include_router(schedules_router)
app.include_router(publish_router)
app.include_router(history_router)

@app.get("/")
def root():
    return {
        "message": "Social Media Studio API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }