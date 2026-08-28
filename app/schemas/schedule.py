from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ScheduleCreate(BaseModel):
    scheduled_for: datetime


class ScheduleResponse(BaseModel):
    id: int
    variant_id: int
    scheduled_for: datetime
    status: str
    idempotency_key: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)