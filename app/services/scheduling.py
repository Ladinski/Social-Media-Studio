import hashlib
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.schedule_repository import ScheduleRepository
from app.repositories.variant_repository import VariantRepository


class SchedulingService:
    @staticmethod
    def schedule_variant(
        db: Session,
        *,
        variant_id: int,
        scheduled_for: datetime,
    ):
        variant = VariantRepository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            raise HTTPException(
                status_code=404,
                detail="Variant not found.",
            )

        if variant.status != "approved":
            raise HTTPException(
                status_code=400,
                detail=(
                    "Only approved variants can be scheduled. "
                    f"Current status: {variant.status}."
                ),
            )

        now = datetime.now(timezone.utc)

        if scheduled_for.tzinfo is None:
            scheduled_for = scheduled_for.replace(
                tzinfo=timezone.utc
            )

        if scheduled_for <= now:
            raise HTTPException(
                status_code=400,
                detail="scheduled_for must be in the future.",
            )

        existing = (
            ScheduleRepository.get_by_variant_and_time(
                db,
                variant_id,
                scheduled_for,
            )
        )

        if existing:
            return existing

        idempotency_key = (
            SchedulingService._build_idempotency_key(
                variant_id,
                scheduled_for,
            )
        )

        return ScheduleRepository.create(
            db,
            variant_id=variant_id,
            scheduled_for=scheduled_for,
            idempotency_key=idempotency_key,
        )

    @staticmethod
    def _build_idempotency_key(
        variant_id: int,
        scheduled_for: datetime,
    ) -> str:
        raw = (
            f"variant:{variant_id}:"
            f"slot:{scheduled_for.isoformat()}"
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()