from enum import Enum

from pydantic import BaseModel
from backend.app.enums.risk_level import RiskLevel


class AIResponseSchema(BaseModel):
    summary: str
    risk_level: RiskLevel
    description: str
    solution: str
    reassurance: str



ai_response = AIResponseSchema(summary="None",risk_level=RiskLevel.SAFE, description="None",solution="None",reassurance="None")