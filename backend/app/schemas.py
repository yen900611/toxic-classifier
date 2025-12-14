from pydantic import BaseModel
from typing import Dict, List

# Single Request (Keep this)
class ToxicRequest(BaseModel):
    text: str

# Single Response (Keep this)
class ToxicResponse(BaseModel):
    results: Dict[str, float]

class ToxicBatchRequest(BaseModel):
    texts: List[str]  # e.g. ["Comment 1", "Comment 2", ...]

class ToxicBatchResponse(BaseModel):
    results: List[Dict[str, float]] # Returns a list of result dictionaries