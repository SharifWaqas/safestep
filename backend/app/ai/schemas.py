from pydantic import BaseModel, Field

from backend.app.enums.risk_factor import RiskFactor
from backend.app.enums.risk_level import RiskLevel


class RiskFactorResult(BaseModel):
    risk_factor: RiskFactor
    value: float = Field(ge=0.0, le=1.0)
    description: str


class AIResponseSchema(BaseModel):
    summary: str
    risk_level: RiskLevel
    description: str
    solution: str
    reassurance: str
    risk_factors: list[RiskFactorResult]
    


ai_response = AIResponseSchema(summary="None",risk_level=RiskLevel.SAFE, description="None",solution="None",reassurance="None", risk_factors=[])