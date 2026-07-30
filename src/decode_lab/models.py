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
