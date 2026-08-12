from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from backend.app.repositories.upload_repository import UploadRepository
from backend.app.repositories.analysis_repository import AnalysisRepository
from backend.app.repositories.ai_result_repository import AIResultRepository
from backend.app.repositories.risk_score_repository import RiskScoreRepository

from backend.app.models.user import User
from backend.app.models.analysis import Analysis
from backend.app.models.risk_score import RiskScore
from backend.app.models.ai_result import AIResult

from backend.app.enums.analysis import AnalysisStatus

from backend.app.services.exceptions import UploadNotFoundError, AnalysisAlreadyExistsError

from backend.app.schemas.analysis import CreateAnalysisResponse

from backend.app.ai.orchestrator import AIOrchestrator


class AnalysisService:

    def __init__(
            self, 
            session: AsyncSession,
            upload_repository: UploadRepository,
            analysis_repository: AnalysisRepository,
            ai_orchestrator: AIOrchestrator,
            ai_result_repository: AIResultRepository,
            risk_score_repository: RiskScoreRepository
    ) -> None:
        self._session = session
        self._upload_repository = upload_repository
        self._analysis_repository = analysis_repository
        self._ai_orchestrator = ai_orchestrator
        self._ai_result_repository = ai_result_repository
        self._risk_score_repository = risk_score_repository


    async def create_analysis(self,user: User,upload_id: UUID) -> CreateAnalysisResponse:
        try:
            upload = await self._upload_repository.get_by_id_and_user(upload_id,user.id)

            if upload is None:
                raise UploadNotFoundError()

            analysis = await self._analysis_repository.get_by_upload_id(upload_id)

            if analysis is not None:
                raise AnalysisAlreadyExistsError()

            user_analysis = Analysis(upload_id=upload.id)

            await self._analysis_repository.save(user_analysis)
            await self._session.commit()

            try:
                result = await self._ai_orchestrator.analyze(upload)

                ai_result = AIResult(
                    analysis_id=user_analysis.id,
                    summary=result.summary,
                    explanation=result.description,
                    guidance=result.solution,
                    reassurance=result.reassurance,
                    risk_level=result.risk_level,
                )

                await self._ai_result_repository.save(ai_result)

                for risk_factor in result.risk_factors:
                    risk_score = RiskScore(
                        analysis_id=user_analysis.id,
                        risk_factor=risk_factor.risk_factor,
                        score=risk_factor.value,
                        explanation=risk_factor.description,
                    )
                    await self._risk_score_repository.save(risk_score)


                user_analysis.status = AnalysisStatus.COMPLETED

                await self._session.commit()

            except Exception:
                user_analysis.status = AnalysisStatus.FAILED

                await self._session.commit()

                raise

            return CreateAnalysisResponse(
                analysis_id=user_analysis.id,
                upload_id=user_analysis.upload_id,
                status=user_analysis.status,
                message="Analysis created successfully.",
            )

        except Exception:
            await self._session.rollback()
            raise