import uuid

from app.publishers.base import PublishResult, SocialPublisher


class MockXPublisher(SocialPublisher):
    def publish(
        self,
        *,
        content: str,
        idempotency_key: str,
    ) -> PublishResult:
        external_id = f"mock-x-{uuid.uuid4()}"

        return PublishResult(
            success=True,
            external_post_id=external_id,
            external_url=f"mock://x/{external_id}",
        )