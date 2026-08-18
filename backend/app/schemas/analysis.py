from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from backend.app.enums.analysis import AnalysisStatus
from backend.app.enums.risk_factor import RiskFactor
from backend.app.enums.risk_level import RiskLevel


class CreateAnalysisResponse(BaseModel):
    analysis_id: UUID
    upload_id: UUID
    status: AnalysisStatus
    message: str


class RiskScoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    risk_factor: RiskFactor
    score: float
    explanation: str


class AIResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    summary: str
    explanation: str
    guidance: str
    reassurance: str
    risk_level: RiskLevel


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    analysis_id: UUID = Field(validation_alias="id")
    upload_id: UUID
    status: AnalysisStatus
    started_at: datetime | None
    completed_at: datetime | None
    ai_result: AIResultResponse | None
    risk_scores: list[RiskScoreResponse]