from pydantic import BaseModel

class ToxicRequest(BaseModel):
    text: str

class ToxicResponse(BaseModel):
    is_toxic: bool
    confidence: float