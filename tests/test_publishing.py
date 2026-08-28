from datetime import datetime, timedelta, timezone

from app.models.post import Post
from app.models.variant import Variant
from app.repositories.publish_attempt_repository import (
    PublishAttemptRepository,
)
from app.services.publishing import PublishingService
from app.services.scheduling import SchedulingService


def test_repeated_publish_returns_one_success(db):
    post = Post(
        title="Idempotency Test",
        source_type="markdown",
        content="Testing idempotent publishing.",
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    variant = Variant(
        post_id=post.id,
        platform="x",
        content="Testing idempotent publishing. #backend",
        status="approved",
    )

    db.add(variant)
    db.commit()
    db.refresh(variant)

    scheduled_for = (
        datetime.now(timezone.utc)
        + timedelta(minutes=5)
    )

    schedule = SchedulingService.schedule_variant(
        db,
        variant_id=variant.id,
        scheduled_for=scheduled_for,
    )

    first = PublishingService.publish_schedule(
        db,
        schedule.id,
    )

    second = PublishingService.publish_schedule(
        db,
        schedule.id,
    )

    assert first.id == second.id

    attempts = (
        PublishAttemptRepository.get_for_schedule(
            db,
            schedule.id,
        )
    )

    successful_attempts = [
        attempt
        for attempt in attempts
        if attempt.status == "success"
    ]

    assert len(successful_attempts) == 1