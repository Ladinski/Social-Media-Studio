from fastapi import HTTPException

from app.publishers.base import SocialPublisher
from app.publishers.discord import DiscordPublisher
from app.publishers.mock_linkedin import MockLinkedInPublisher
from app.publishers.mock_x import MockXPublisher


class PublisherFactory:
    @staticmethod
    def get_publisher(platform: str) -> SocialPublisher:
        publishers = {
            "discord": DiscordPublisher,
            "x": MockXPublisher,
            "linkedin": MockLinkedInPublisher,
        }

        publisher_class = publishers.get(platform)

        if not publisher_class:
            raise HTTPException(
                status_code=400,
                detail=f"No publisher configured for platform: {platform}",
            )

        return publisher_class()