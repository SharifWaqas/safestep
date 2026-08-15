from uuid import UUID

from pydantic import BaseModel

from backend.app.enums.analysis import AnalysisStatus


class CreateAnalysisResponse(BaseModel):
    analysis_id: UUID
    upload_id: UUID
    status: AnalysisStatus
    message: str