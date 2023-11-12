import typing


from pydantic import BaseModel

class RequestModel(BaseModel):
    """Simple message model."""
    model: str
    messages: list[dict[str, str]]
    temperature: float
