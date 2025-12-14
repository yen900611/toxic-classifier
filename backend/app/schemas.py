from pydantic import BaseModel
from typing import Dict

class ToxicRequest(BaseModel):
    text: str

class ToxicResponse(BaseModel):
    # Returns a dictionary like {"toxic": 0.95, "threat": 0.01}
    results: Dict[str, float]