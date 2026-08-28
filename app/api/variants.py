from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.variant_repository import VariantRepository
from app.schemas.variant import VariantResponse
from app.services.variant_generator import VariantGeneratorService


router = APIRouter(
    prefix="/variants",
    tags=["variants"],
)


@router.post(
    "/generate/{post_id}",
    response_model=list[VariantResponse],
)
def generate_variants(
    post_id: int,
    db: Session = Depends(get_db),
):
    variants = VariantGeneratorService.generate_for_post(
        db,
        post_id,
    )

    if variants is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found.",
        )

    return variants


@router.get(
    "/post/{post_id}",
    response_model=list[VariantResponse],
)
def get_post_variants(
    post_id: int,
    db: Session = Depends(get_db),
):
    return VariantRepository.get_by_post(
        db,
        post_id,
    )


@router.get(
    "/{variant_id}",
    response_model=VariantResponse,
)
def get_variant(
    variant_id: int,
    db: Session = Depends(get_db),
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

    return variant