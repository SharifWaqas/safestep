from fastapi import APIRouter, Depends, UploadFile, File
from uuid import UUID

from backend.app.schemas.upload import UploadResponse
from backend.app.services.upload_service import UploadService, UploadDetailResponse, DeleteUploadResponse
from backend.app.api.dependencies import get_upload_service, get_current_user
from backend.app.models.user import User


router = APIRouter(prefix="/uploads",tags=["Upload"])

@router.post("")
async def upload_file(file: UploadFile = File() ,user: User = Depends(get_current_user),upload_service: UploadService = Depends(get_upload_service))-> UploadResponse:
    return await upload_service.upload_file(user, file)

@router.get("/{upload_id}")
async def get_upload(upload_id: UUID ,user: User = Depends(get_current_user), upload_service: UploadService = Depends(get_upload_service))-> UploadDetailResponse:
    return await upload_service.get_upload(user, upload_id)

@router.delete("/{upload_id}")
async def delete_upload(upload_id: UUID ,user: User = Depends(get_current_user), upload_service: UploadService = Depends(get_upload_service))-> DeleteUploadResponse:
    return await upload_service.delete_upload(user, upload_id)