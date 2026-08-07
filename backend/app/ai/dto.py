from enum import Enum

from pydantic import BaseModel


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalysisResultDTO(BaseModel):
    """
    Represents the final structured analysis produced by the AI subsystem.
    """

    risk_level: RiskLevel
    summary: str
    explanation: str
    guidance: str
    reassurance: str