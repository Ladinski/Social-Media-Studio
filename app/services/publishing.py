from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.publishers.factory import PublisherFactory
from app.repositories.publish_attempt_repository import (
    PublishAttemptRepository,
)
from app.repositories.schedule_repository import ScheduleRepository


class PublishingService:
    @staticmethod
    def publish_schedule(
        db: Session,
        schedule_id: int,
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

        existing_success = (
            PublishAttemptRepository.get_successful_for_schedule(
                db,
                schedule.id,
            )
        )

        if existing_success:
            return existing_success

        variant = schedule.variant

        if variant.status != "approved":
            raise HTTPException(
                status_code=400,
                detail=(
                    "Only approved variants can be published. "
                    f"Current status: {variant.status}."
                ),
            )

        publisher = PublisherFactory.get_publisher(
            variant.platform
        )

        try:
            result = publisher.publish(
                content=variant.content,
                idempotency_key=schedule.idempotency_key,
            )
        except Exception as exc:
            return PublishAttemptRepository.create(
                db,
                schedule_slot_id=schedule.id,
                platform=variant.platform,
                status="failed",
                error_message=str(exc),
            )

        if not result.success:
            return PublishAttemptRepository.create(
                db,
                schedule_slot_id=schedule.id,
                platform=variant.platform,
                status="failed",
                error_message=result.error_message,
            )

        attempt = PublishAttemptRepository.create(
            db,
            schedule_slot_id=schedule.id,
            platform=variant.platform,
            status="success",
            external_post_id=result.external_post_id,
            external_url=result.external_url,
        )

        schedule.status = "published"
        variant.status = "published"

        db.commit()

        return attempt