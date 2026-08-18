from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.analysis import Analysis
from backend.app.models.upload import Upload
from backend.app.repositories.base_repository import BaseRepository


class AnalysisRepository(BaseRepository[Analysis]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(
            db_session=db_session,
            model=Analysis,
        )

    async def get_by_upload_id(
        self,
        upload_id: UUID,
    ) -> Analysis | None:

        query = select(self._model).where(
            self._model.upload_id == upload_id
        )

        result = await self._db_session.execute(query)

        return result.scalar_one_or_none()

    async def get_by_id_and_user(
        self,
        analysis_id: UUID,
        user_id: UUID,
    ) -> Analysis | None:

        query = (
            select(self._model)
            .options(
                selectinload(self._model.ai_result),
                selectinload(self._model.risk_scores),
            )
            .join(
                Upload,
                self._model.upload_id == Upload.id,
            )
            .where(
                self._model.id == analysis_id,
                Upload.user_id == user_id,
            )
        )

        result = await self._db_session.execute(query)

        return result.scalar_one_or_none()