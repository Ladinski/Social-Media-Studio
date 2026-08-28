from fastapi import FastAPI

from app.core.database import Base, engine
import app.models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Social Media Studio",
    description="Generate, review, schedule, and publish social media campaign variants.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Social Media Studio API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}