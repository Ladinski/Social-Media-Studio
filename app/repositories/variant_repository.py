from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.variant import Variant


class VariantRepository:
    @staticmethod
    def create(
        db: Session,
        *,
        post_id: int,
        platform: str,
        content: str,
    ) -> Variant:
        variant = Variant(
            post_id=post_id,
            platform=platform,
            content=content,
            status="draft",
        )

        db.add(variant)
        db.commit()
        db.refresh(variant)

        return variant

    @staticmethod
    def get_by_id(db: Session, variant_id: int) -> Variant | None:
        return db.get(Variant, variant_id)

    @staticmethod
    def get_by_post(db: Session, post_id: int) -> list[Variant]:
        stmt = select(Variant).where(
            Variant.post_id == post_id
        )

        return list(
            db.scalars(stmt).all()
        )