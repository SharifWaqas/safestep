from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.app.models.session import Session
from backend.app.repositories.base_repository import BaseRepository


class SessionRepository(BaseRepository[Session]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Session)


    async def find_by_refresh_token_hash(
        self,
        refresh_token_hash: str,
    ) -> Session | None:
        query = (
            select(self._model)
            .options(selectinload(self._model.user))
            .where(self._model.refresh_token_hash == refresh_token_hash)
            .with_for_update()
        )
        result = await self._db_session.execute(query)
        return result.scalar_one_or_none()
