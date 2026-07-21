from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models.user import User
from backend.app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=User)


    async def create(self, user: User) -> User:
        self._db_session.add(user)
        return user


    async def find_by_email(self, email: str) -> User | None:
        query = select(self._model).where(self._model.email == email)
        result = await self._db_session.execute(query)
        return result.scalar_one_or_none()


        
