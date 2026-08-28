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

        generated = {
            "x": VariantGeneratorService._generate_x(
                post.title,
                post.content,
            ),
            "linkedin": VariantGeneratorService._generate_linkedin(
                post.title,
                post.content,
            ),
            "discord": VariantGeneratorService._generate_discord(
                post.title,
                post.content,
            ),
        }

        variants = []

        for platform, content in generated.items():
            VariantValidator.validate(
                platform,
                content,
            )

            variant = VariantRepository.create(
                db,
                post_id=post.id,
                platform=platform,
                content=content,
            )

            variants.append(variant)

        return variants

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

    @staticmethod
    def _generate_discord(
        title: str,
        content: str,
    ) -> str:
        excerpt = VariantGeneratorService._clean_markdown(
            content
        )

        if len(excerpt) > 1200:
            excerpt = excerpt[:1197].rstrip() + "..."

        return (
            f"**{title}**\n\n"
            f"{excerpt}\n\n"
            "What do you think?"
        )