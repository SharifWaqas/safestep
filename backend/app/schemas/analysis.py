from pydantic import BaseModel
from uuid import UUID


from backend.app.enums.analysis import AnalysisStatus


class CreateAnalysisResponse(BaseModel):
    analysis_id : UUID
    upload_id : UUID
    status :  AnalysisStatus
    message : str