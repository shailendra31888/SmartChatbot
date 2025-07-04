from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Schema for the incoming user query."""
    input: str  # The question or statement provided by the user


class ChatResponse(BaseModel):
    """Schema for the outgoing response to the user."""
    response: str  # The response generated by the chatbot
    category: Optional[str] = None  # Optional field for categorizing the response, e.g., 'Trades', 'News', etc.
