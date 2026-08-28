from fastapi import FastAPI

import app.models
from app.api.posts import router as posts_router
from app.api.review import router as review_router
from app.api.variants import router as variants_router
from app.core.database import Base, engine
from app.api.schedules import router as schedules_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Social Media Studio",
    description="Generate, review, schedule, and publish social media campaign variants.",
    version="1.0.0",
)

app.include_router(posts_router)
app.include_router(variants_router)
app.include_router(review_router)
app.include_router(schedules_router)

@app.get("/")
def root():
    return {
        "message": "Social Media Studio API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}