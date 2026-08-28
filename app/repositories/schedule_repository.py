from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.schedule import ScheduleSlot


class ScheduleRepository:
    @staticmethod
    def create(
        db: Session,
        *,
        variant_id: int,
        scheduled_for,
        idempotency_key: str,
    ) -> ScheduleSlot:
        schedule = ScheduleSlot(
            variant_id=variant_id,
            scheduled_for=scheduled_for,
            status="pending",
            idempotency_key=idempotency_key,
        )

        db.add(schedule)
        db.commit()
        db.refresh(schedule)

        return schedule

    @staticmethod
    def get_by_id(
        db: Session,
        schedule_id: int,
    ) -> ScheduleSlot | None:
        return db.get(ScheduleSlot, schedule_id)

    @staticmethod
    def get_by_variant_and_time(
        db: Session,
        variant_id: int,
        scheduled_for,
    ) -> ScheduleSlot | None:
        stmt = select(ScheduleSlot).where(
            ScheduleSlot.variant_id == variant_id,
            ScheduleSlot.scheduled_for == scheduled_for,
        )

        return db.scalar(stmt)

    @staticmethod
    def get_due(
        db: Session,
        now: datetime,
    ) -> list[ScheduleSlot]:
        stmt = (
            select(ScheduleSlot)
            .where(
                ScheduleSlot.status == "pending",
                ScheduleSlot.scheduled_for <= now,
            )
            .order_by(ScheduleSlot.scheduled_for)
        )

        return list(db.scalars(stmt).all())