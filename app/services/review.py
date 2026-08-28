from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.variant_repository import VariantRepository
from app.services.variant_validator import VariantValidator


class ReviewService:
    @staticmethod
    def approve(
        db: Session,
        variant_id: int,
    ):
        variant = VariantRepository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            raise HTTPException(
                status_code=404,
                detail="Variant not found.",
            )

        if variant.status == "published":
            raise HTTPException(
                status_code=400,
                detail="Published variants cannot be approved again.",
            )

        VariantValidator.validate(
            variant.platform,
            variant.content,
        )

        variant.status = "approved"

        db.commit()
        db.refresh(variant)

        return variant

    @staticmethod
    def reject(
        db: Session,
        variant_id: int,
    ):
        variant = VariantRepository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            raise HTTPException(
                status_code=404,
                detail="Variant not found.",
            )

        if variant.status == "published":
            raise HTTPException(
                status_code=400,
                detail="Published variants cannot be rejected.",
            )

        variant.status = "rejected"

        db.commit()
        db.refresh(variant)

        return variant

    @staticmethod
    def edit(
        db: Session,
        variant_id: int,
        content: str,
    ):
        variant = VariantRepository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            raise HTTPException(
                status_code=404,
                detail="Variant not found.",
            )

        if variant.status == "published":
            raise HTTPException(
                status_code=400,
                detail="Published variants cannot be edited.",
            )

        content = content.strip()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Variant content cannot be empty.",
            )

        VariantValidator.validate(
            variant.platform,
            content,
        )

        variant.content = content

        # Editing requires human approval again.
        variant.status = "draft"

        db.commit()
        db.refresh(variant)

        return variant