from fastapi import HTTPException

from app.core.constraints import PLATFORM_CONSTRAINTS


class VariantValidator:
    @staticmethod
    def validate(platform: str, content: str) -> None:
        profile = PLATFORM_CONSTRAINTS.get(platform)

        if not profile:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown platform: {platform}",
            )

        max_length = profile["max_length"]
        max_hashtags = profile["max_hashtags"]

        if len(content) > max_length:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"{platform} maximum length exceeded: "
                    f"{len(content)}/{max_length} characters."
                ),
            )

        hashtag_count = len(
            [
                word
                for word in content.split()
                if word.startswith("#")
            ]
        )

        if hashtag_count > max_hashtags:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"{platform} hashtag limit exceeded: "
                    f"{hashtag_count}/{max_hashtags}."
                ),
            )

        VariantValidator._validate_tone(
            platform=platform,
            content=content,
        )

    @staticmethod
    def _validate_tone(
        platform: str,
        content: str,
    ) -> None:
        lowered = content.lower()

        if platform == "x":
            if "\n\n\n" in content:
                raise HTTPException(
                    status_code=400,
                    detail="x tone rule violated: post must be concise.",
                )

        if platform == "linkedin":
            banned_phrases = [
                "lol",
                "lmao",
                "omg",
            ]

            for phrase in banned_phrases:
                if phrase in lowered:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "linkedin tone rule violated: "
                            "post must use a professional tone."
                        ),
                    )