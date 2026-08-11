from enum import Enum

from pydantic import BaseModel


class ScamLevel(str, Enum):
    SAFE = "SAFE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class AIResponseSchema(BaseModel):
    summary: str
    scam_level: ScamLevel
    description: str
    solution: str | None = None
    reassurance: str | None = None



ai_response = AIResponseSchema(summary="None",scam_level="SAFE",description="None",solution="None",reassurance="None")