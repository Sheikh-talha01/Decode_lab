from pydantic import BaseModel


class OutputSchema(BaseModel):
    generated: str
