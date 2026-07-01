from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models.session import Session
from backend.app.repositories.base_repository import BaseRepository


class SessionRepository(BaseRepository[Session]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Session)


    async def find_by_refresh_token_hash(self, refresh_token_hash : str) -> Session | None:
        query = select(self._model).where(self._model.refresh_token_hash == refresh_token_hash)
        result = await self._db_session.execute(query)
        return result.scalar_one_or_none()