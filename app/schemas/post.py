from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class PostCreate(BaseModel):
    title: str
    markdown: str | None = None
    url: HttpUrl | None = None


class PostResponse(BaseModel):
    id: int
    title: str
    source_type: str
    source_url: str | None
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)