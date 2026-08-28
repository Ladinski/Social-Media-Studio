from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.publish import PublishAttemptResponse
from app.services.publishing import PublishingService


router = APIRouter(
    prefix="/publish",
    tags=["publish"],
)


@router.post(
    "/schedules/{schedule_id}",
    response_model=PublishAttemptResponse,
)
def publish_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
):
    return PublishingService.publish_schedule(
        db,
        schedule_id,
    )