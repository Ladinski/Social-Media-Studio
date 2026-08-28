import re

from sqlalchemy.orm import Session

from app.repositories.post_repository import PostRepository
from app.repositories.variant_repository import VariantRepository
from app.services.variant_validator import VariantValidator


class VariantGeneratorService:
    @staticmethod
    def generate_for_post(
        db: Session,
        post_id: int,
    ):
        post = PostRepository.get_by_id(db, post_id)

        if not post:
            return None

        x_content = VariantGeneratorService._generate_x(
            post.title,
            post.content,
        )

        linkedin_content = VariantGeneratorService._generate_linkedin(
            post.title,
            post.content,
        )

        VariantValidator.validate(
            "x",
            x_content,
        )

        VariantValidator.validate(
            "linkedin",
            linkedin_content,
        )

        x_variant = VariantRepository.create(
            db,
            post_id=post.id,
            platform="x",
            content=x_content,
        )

        linkedin_variant = VariantRepository.create(
            db,
            post_id=post.id,
            platform="linkedin",
            content=linkedin_content,
        )

        return [
            x_variant,
            linkedin_variant,
        ]

    @staticmethod
    def _clean_markdown(content: str) -> str:
        content = re.sub(
            r"^#{1,6}\s+",
            "",
            content,
            flags=re.MULTILINE,
        )

        content = re.sub(
            r"\*\*(.*?)\*\*",
            r"\1",
            content,
        )

        content = re.sub(
            r"\*(.*?)\*",
            r"\1",
            content,
        )

        return " ".join(content.split())

    @staticmethod
    def _generate_x(
        title: str,
        content: str,
    ) -> str:
        excerpt = VariantGeneratorService._clean_markdown(
            content
        )

        if len(excerpt) > 170:
            excerpt = excerpt[:167].rstrip() + "..."

        return (
            f"{title}\n\n"
            f"{excerpt}\n\n"
            "#software #backend"
        )

    @staticmethod
    def _generate_linkedin(
        title: str,
        content: str,
    ) -> str:
        excerpt = VariantGeneratorService._clean_markdown(
            content
        )

        if len(excerpt) > 800:
            excerpt = excerpt[:797].rstrip() + "..."

        return (
            f"{title}\n\n"
            f"{excerpt}\n\n"
            "A useful reminder that reliable software depends "
            "on clear constraints and predictable behavior.\n\n"
            "#SoftwareEngineering #BackendDevelopment #AI"
        )