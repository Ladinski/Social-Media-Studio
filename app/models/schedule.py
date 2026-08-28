from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ScheduleSlot(Base):
    __tablename__ = "schedule_slots"

    __table_args__ = (
        UniqueConstraint(
            "variant_id",
            "scheduled_for",
            name="uq_variant_schedule_slot",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    variant_id: Mapped[int] = mapped_column(
        ForeignKey("variants.id", ondelete="CASCADE"),
        index=True,
    )

    scheduled_for: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        index=True,
    )

    idempotency_key: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    variant = relationship(
        "Variant",
        back_populates="schedules",
    )

    publish_attempts = relationship(
        "PublishAttempt",
        back_populates="schedule_slot",
        cascade="all, delete-orphan",
    )