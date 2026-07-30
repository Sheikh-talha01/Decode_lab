from pydantic import BaseModel, validator
from typing import Optional


class OutputSchema(BaseModel):
    generated: str
    platform: Optional[str] = None
    processed: Optional[str] = None
    truncated: bool = False

    @validator("processed", always=True)
    def ensure_processed(cls, v, values):
        # if processed not provided, default to generated
        if v:
            return v
        return values.get("generated")


class TextOutput(BaseModel):
    id: Optional[str]
    product: Optional[str]
    name: Optional[str]
    tone: Optional[str]
    platform: Optional[str]
    generated: str
    processed: str
    truncated: bool = False
    filter_reason: Optional[str]
    unsafe: bool = False

    @validator("processed")
    def non_empty_processed(cls, v):
        if not v or not v.strip():
            raise ValueError("processed text must not be empty")
        return v

