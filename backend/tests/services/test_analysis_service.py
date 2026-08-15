from uuid import UUID

from fastapi import APIRouter, Depends, status

from backend.app.api.dependencies import (
    get_analysis_service,
    get_current_user,
)
from backend.app.models.user import User
from backend.app.schemas.analysis import CreateAnalysisResponse
from backend.app.services.analysis_service import AnalysisService


router = APIRouter(
    prefix="/analyses",
    tags=["Analysis"],
)


@router.post(
    "/{upload_id}",
    response_model=CreateAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_analysis(
    upload_id: UUID,
    user: User = Depends(get_current_user),
    analysis_service: AnalysisService = Depends(get_analysis_service),
) -> CreateAnalysisResponse:
    return await analysis_service.create_analysis(
        user=user,
        upload_id=upload_id,
    )