from datetime import datetime

from sqlalchemy import DateTime, Integer, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255))

    source_type: Mapped[str] = mapped_column(String(50))
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    content: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    variants = relationship(
        "Variant",
        back_populates="post",
        cascade="all, delete-orphan",
    )