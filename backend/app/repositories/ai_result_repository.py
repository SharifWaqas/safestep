from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.ai_result import AIResult
from backend.app.repositories.base_repository import BaseRepository


class AIResultRepository(BaseRepository[AIResult]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session,model=AIResult)