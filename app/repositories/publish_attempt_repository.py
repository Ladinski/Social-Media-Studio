from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.publish_attempt import PublishAttempt


class PublishAttemptRepository:
    @staticmethod
    def create(
        db: Session,
        *,
        schedule_slot_id: int,
        platform: str,
        status: str,
        external_post_id: str | None = None,
        external_url: str | None = None,
        error_message: str | None = None,
    ) -> PublishAttempt:
        attempt = PublishAttempt(
            schedule_slot_id=schedule_slot_id,
            platform=platform,
            status=status,
            external_post_id=external_post_id,
            external_url=external_url,
            error_message=error_message,
        )

        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        return attempt

    @staticmethod
    def get_successful_for_schedule(
        db: Session,
        schedule_slot_id: int,
    ) -> PublishAttempt | None:
        stmt = select(PublishAttempt).where(
            PublishAttempt.schedule_slot_id == schedule_slot_id,
            PublishAttempt.status == "success",
        )

        return db.scalar(stmt)

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[PublishAttempt]:
        stmt = (
            select(PublishAttempt)
            .order_by(PublishAttempt.created_at.desc())
        )

        return list(db.scalars(stmt).all())

    @staticmethod
    def get_for_schedule(
        db: Session,
        schedule_slot_id: int,
    ) -> list[PublishAttempt]:
        stmt = (
            select(PublishAttempt)
            .where(
                PublishAttempt.schedule_slot_id
                == schedule_slot_id
            )
            .order_by(PublishAttempt.created_at.desc())
        )

        return list(db.scalars(stmt).all())