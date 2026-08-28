from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VariantResponse(BaseModel):
    id: int
    post_id: int
    platform: str
    content: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)