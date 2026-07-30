from pydantic import BaseModel
from typing import List, Optional


class CreateSessionResponse(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    history: Optional[List[dict]] = None
