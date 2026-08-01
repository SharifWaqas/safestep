from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from uuid import UUID

from backend.app.core.config import settings

from backend.app.services.exceptions import InvalidFileTypeError, FileTooLargeError, UploadNotFoundError
from backend.app.services.storage_service import StorageService

from backend.app.schemas.upload import UploadResponse, UploadDetailResponse

from backend.app.models.user import User
from backend.app.models.upload import Upload

from backend.app.repositories.upload_repository import UploadRepository



class UploadService:

    def __init__(
            self, 
            session: AsyncSession,
            upload_repository: UploadRepository,
            storage_service: StorageService
    ) -> None:
        self._session = session
        self._upload_repository = upload_repository
        self._storage_service = storage_service


    async def upload_file(self, user: User, file: UploadFile) -> UploadResponse:
        self._validate_upload(file)
        storage_result = await self._storage_service.save_file(file)
        try:
            upload_object = Upload(
                user_id= user.id, 
                storage_path= storage_result.storage_path, 
                file_name= storage_result.file_name, 
                file_size= storage_result.file_size, 
                content_type= storage_result.content_type
                )
            await self._upload_repository.save(upload_object)
            await self._session.commit()
            await self._session.refresh(upload_object)

            return UploadResponse(
                upload_id= upload_object.id,
                message= "File has been successfully uploaded."
            )
        except Exception:
            await self._session.rollback()
            await self._storage_service.delete_file(storage_result.storage_path)
            raise



    def _validate_upload(self, file: UploadFile):
        allowed_content_types = {
            "image/png",
            "image/jpeg",
            "image/jpg"
        }
        content_type = file.content_type
        file.file.seek(0, 2)      
        size = file.file.tell()   
        file.file.seek(0)         

        if content_type not in allowed_content_types:
            raise InvalidFileTypeError

        if size > settings.MAX_UPLOAD_SIZE :
            raise FileTooLargeError        

    async def get_upload(self, user: User, upload_id: UUID) -> UploadDetailResponse:
        upload = await self._upload_repository.get_by_id_and_user(upload_id, user.id)

        if upload is None:
            raise UploadNotFoundError()

        return UploadDetailResponse(
            file_name = upload.file_name,
            file_size = upload.file_size,
            content_type = upload.content_type,
            upload_id = upload.id,
            created_at = upload.created_at 
        )