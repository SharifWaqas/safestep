from fastapi import APIRouter, Depends
from uuid import UUID

from backend.app.api.dependencies import get_analysis_service, get_current_user
from backend.app.models.user import User
from backend.app.services.analysis_service import AnalysisService


router = APIRouter(prefix="/analyses",tags=["Analysis"])

@router.post("/{upload_id}")
async def create_analysis(upload_id: UUID, user: User = Depends(get_current_user), analysis_service: AnalysisService = Depends(get_analysis_service)):
    return await analysis_service.create_analysis(user, upload_id)
