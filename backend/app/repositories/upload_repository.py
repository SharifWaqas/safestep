from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID

from backend.app.models.upload import Upload
from backend.app.repositories.base_repository import BaseRepository


class UploadRepository(BaseRepository[Upload]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Upload)

    async def get_by_id_and_user(self, upload_id: UUID, user_id: UUID) -> Upload | None:
        query = select(self._model).where(self._model.id == upload_id, self._model.user_id == user_id)
        result = await self._db_session.execute(query)
        return result.scalar_one_or_none()

    async def list_uploads(self, user_id: UUID)-> list[Upload]:
        query = select(self._model).where(self._model.user_id == user_id).order_by(self._model.created_at.desc())
        result = await self._db_session.execute(query)
        return list(result.scalars()) 
        
