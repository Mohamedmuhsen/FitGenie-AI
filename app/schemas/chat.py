from pydantic import BaseModel, Field
from typing import Any

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message")
    user_context: dict[str, Any] | None = Field(default=None, description="Optional user profile/context")

class ChatResponse(BaseModel):
    response: str
    agents_used: list[str] = Field(default_factory=list)
    data: dict[str, Any] | None = None
