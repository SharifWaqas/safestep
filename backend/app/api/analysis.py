from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from backend.app.api.dependencies import (
    get_analysis_service,
    get_current_user,
)

from backend.app.models.user import User

from backend.app.schemas.analysis import (
    AnalysisResponse,
    CreateAnalysisResponse,
)

from backend.app.services.analysis_service import AnalysisService


router = APIRouter(
    prefix="/analyses",
    tags=["Analysis"],
)


@router.post(
    "/{upload_id}",
    response_model=CreateAnalysisResponse,
)
async def create_analysis(
    upload_id: UUID,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    analysis_service: Annotated[
        AnalysisService,
        Depends(get_analysis_service),
    ],
):
    return await analysis_service.create_analysis(
        user,
        upload_id,
    )


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse,
)
async def get_analysis(
    analysis_id: UUID,
    user: Annotated[
        User,
        Depends(get_current_user),
    ],
    analysis_service: Annotated[
        AnalysisService,
        Depends(get_analysis_service),
    ],
):
    return await analysis_service.get_analysis(
        user=user,
        analysis_id=analysis_id,
    )