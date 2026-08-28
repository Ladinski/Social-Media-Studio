import httpx

from app.core.config import settings
from app.publishers.base import PublishResult, SocialPublisher


class DiscordPublisher(SocialPublisher):
    def publish(
        self,
        *,
        content: str,
        idempotency_key: str,
    ) -> PublishResult:
        if not settings.discord_webhook_url:
            return PublishResult(
                success=False,
                error_message="Discord webhook URL is not configured.",
            )

        try:
            response = httpx.post(
                settings.discord_webhook_url,
                params={"wait": "true"},
                json={
                    "content": content,
                },
                timeout=10.0,
            )

            response.raise_for_status()

        except httpx.HTTPError as exc:
            return PublishResult(
                success=False,
                error_message=f"Discord publish failed: {exc}",
            )

        data = response.json()

        message_id = data.get("id")
        channel_id = data.get("channel_id")
        guild_id = data.get("guild_id")

        external_url = None

        if message_id and channel_id and guild_id:
            external_url = (
                f"https://discord.com/channels/"
                f"{guild_id}/{channel_id}/{message_id}"
            )

        return PublishResult(
            success=True,
            external_post_id=message_id,
            external_url=external_url,
        )