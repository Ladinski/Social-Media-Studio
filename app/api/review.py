from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.review import VariantEditRequest
from app.schemas.variant import VariantResponse
from app.services.review import ReviewService


router = APIRouter(
    prefix="/variants",
    tags=["review"],
)


@router.patch(
    "/{variant_id}/edit",
    response_model=VariantResponse,
)
def edit_variant(
    variant_id: int,
    payload: VariantEditRequest,
    db: Session = Depends(get_db),
):
    return ReviewService.edit(
        db,
        variant_id,
        payload.content,
    )


@router.post(
    "/{variant_id}/approve",
    response_model=VariantResponse,
)
def approve_variant(
    variant_id: int,
    db: Session = Depends(get_db),
):
    return ReviewService.approve(
        db,
        variant_id,
    )


@router.post(
    "/{variant_id}/reject",
    response_model=VariantResponse,
)
def reject_variant(
    variant_id: int,
    db: Session = Depends(get_db),
):
    return ReviewService.reject(
        db,
        variant_id,
    )