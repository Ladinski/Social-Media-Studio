from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.schedule_repository import ScheduleRepository
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleResponse,
)
from app.services.scheduling import SchedulingService


router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
)


@router.post(
    "/variants/{variant_id}",
    response_model=ScheduleResponse,
    status_code=201,
)
def schedule_variant(
    variant_id: int,
    payload: ScheduleCreate,
    db: Session = Depends(get_db),
):
    return SchedulingService.schedule_variant(
        db,
        variant_id=variant_id,
        scheduled_for=payload.scheduled_for,
    )


@router.get(
    "/{schedule_id}",
    response_model=ScheduleResponse,
)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
):
    schedule = ScheduleRepository.get_by_id(
        db,
        schedule_id,
    )

    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found.",
        )

    return schedule