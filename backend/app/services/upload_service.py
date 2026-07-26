from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repositories.upload_repository import UploadRepository
from backend.app.services.storage_service import StorageService


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
