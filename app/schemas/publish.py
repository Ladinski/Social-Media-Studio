from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PublishAttemptResponse(BaseModel):
    id: int
    schedule_slot_id: int
    platform: str
    status: str
    external_post_id: str | None
    external_url: str | None
    error_message: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)