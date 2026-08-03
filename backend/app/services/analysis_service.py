from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.app.repositories.upload_repository import UploadRepository
from backend.app.repositories.analysis_repository import AnalysisRepository

from backend.app.models.user import User
from backend.app.models.analysis import Analysis

from backend.app.services.exceptions import UploadNotFoundError, AnalysisAlreadyExistsError


from backend.app.schemas.analysis import CreateAnalysisResponse

class AnalysisService:

    def __init__(
            self, 
            session: AsyncSession,
            upload_repository: UploadRepository,
            analysis_repository: AnalysisRepository,
    ) -> None:
        self._session = session
        self._upload_repository = upload_repository
        self._analysis_repository = analysis_repository


    async def create_analysis(self, user: User, upload_id: UUID,) -> CreateAnalysisResponse :
        try:
            upload = await self._upload_repository.get_by_id_and_user(upload_id, user.id)

            if upload is None:
                raise UploadNotFoundError()

            analysis = await self._analysis_repository.get_by_upload_id(upload_id)

            if analysis is not None:
                raise AnalysisAlreadyExistsError()

            user_analysis = Analysis(upload_id=upload.id)
            await self._analysis_repository.save(user_analysis)
            await self._session.commit()
            return (CreateAnalysisResponse(
                analysis_id=user_analysis.id,
                upload_id=user_analysis.upload_id,
                status=user_analysis.status,
                message= "Analysis created successfully."
            ))
        except Exception:
            await self._session.rollback()
            raise
