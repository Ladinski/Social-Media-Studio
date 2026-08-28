from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from app.models.post import Post
from app.models.variant import Variant
from app.services.scheduling import SchedulingService


def test_unapproved_variant_cannot_be_scheduled(db):
    post = Post(
        title="Scheduling Test",
        source_type="markdown",
        content="Test content",
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    variant = Variant(
        post_id=post.id,
        platform="x",
        content="Test post #python",
        status="draft",
    )

    db.add(variant)
    db.commit()
    db.refresh(variant)

    scheduled_for = (
        datetime.now(timezone.utc)
        + timedelta(minutes=5)
    )

    with pytest.raises(HTTPException) as exc:
        SchedulingService.schedule_variant(
            db,
            variant_id=variant.id,
            scheduled_for=scheduled_for,
        )

    assert exc.value.status_code == 400
    assert "Only approved variants" in exc.value.detail