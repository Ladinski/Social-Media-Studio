from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Variant(Base):
    __tablename__ = "variants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
        index=True,
    )

    platform: Mapped[str] = mapped_column(String(50))

    content: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    post = relationship(
        "Post",
        back_populates="variants",
    )

    schedules = relationship(
        "ScheduleSlot",
        back_populates="variant",
        cascade="all, delete-orphan",
    )