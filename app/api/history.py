from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.publish_attempt_repository import (
    PublishAttemptRepository,
)
from app.schemas.publish import PublishAttemptResponse


router = APIRouter(
    prefix="/history",
    tags=["history"],
)


@router.get(
    "",
    response_model=list[PublishAttemptResponse],
)
def get_publish_history(
    db: Session = Depends(get_db),
):
    return PublishAttemptRepository.get_all(db)


@router.get(
    "/schedules/{schedule_id}",
    response_model=list[PublishAttemptResponse],
)
def get_schedule_history(
    schedule_id: int,
    db: Session = Depends(get_db),
):
    return PublishAttemptRepository.get_for_schedule(
        db,
        schedule_id,
    )