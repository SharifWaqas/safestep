from typing import TypeVar, Generic, Type
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


T = TypeVar("T")


class BaseRepository(Generic[T]):


    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self._db_session = db_session
        self._model = model
    

    async def get_by_id(self, entity_id: UUID) -> T | None:
        query = select(self._model).where(self._model.id == entity_id)
        result = await self._db_session.execute(query)
        return result.scalar_one_or_none()