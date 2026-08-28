from pydantic import BaseModel


class VariantEditRequest(BaseModel):
    content: str