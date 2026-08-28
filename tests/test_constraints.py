import pytest
from fastapi import HTTPException

from app.services.variant_validator import VariantValidator


def test_x_variant_over_character_limit_is_blocked():
    content = "a" * 281

    with pytest.raises(HTTPException) as exc:
        VariantValidator.validate(
            "x",
            content,
        )

    assert exc.value.status_code == 400
    assert "maximum length exceeded" in exc.value.detail


def test_x_variant_over_hashtag_limit_is_blocked():
    content = (
        "Useful software engineering post "
        "#backend #python #fastapi"
    )

    with pytest.raises(HTTPException) as exc:
        VariantValidator.validate(
            "x",
            content,
        )

    assert exc.value.status_code == 400
    assert "hashtag limit exceeded" in exc.value.detail


def test_valid_x_variant_passes():
    content = (
        "Reliable systems need clear constraints. "
        "#backend #python"
    )

    VariantValidator.validate(
        "x",
        content,
    )