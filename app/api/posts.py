from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostResponse
from app.services.ingestion import IngestionService


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.post("", response_model=PostResponse, status_code=201)
def create_post(
    payload: PostCreate,
    db: Session = Depends(get_db),
):
    return IngestionService.ingest(db, payload)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = PostRepository.get_by_id(db, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found.",
        )

    return post