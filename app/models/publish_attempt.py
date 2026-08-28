from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PublishAttempt(Base):
    __tablename__ = "publish_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    schedule_slot_id: Mapped[int] = mapped_column(
        ForeignKey("schedule_slots.id", ondelete="CASCADE"),
        index=True,
    )

    platform: Mapped[str] = mapped_column(
        String(50),
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        index=True,
    )

    external_post_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    external_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    schedule_slot = relationship(
        "ScheduleSlot",
        back_populates="publish_attempts",
    )