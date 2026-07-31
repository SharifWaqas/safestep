from fastapi import APIRouter, Depends
from fastapi import UploadFile


from backend.app.schemas.upload import UploadResponse
from backend.app.services.upload_service import UploadService
from backend.app.api.dependencies import get_upload_service
from backend.app.models.user import User


router = APIRouter(prefix="/uploads")

@router.post(...)
async def upload_file(
    file: UploadFile,
    user: User = Depends(get_current_user),
    upload_service: UploadService = Depends(get_upload_service),
):
    return await upload_service.upload_file(user, file)