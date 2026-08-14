from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.ai.orchestrator import AIOrchestrator
from backend.app.ai.prompts import PromptBuilder

from backend.app.enums.analysis import AnalysisStatus

from backend.app.models.analysis import Analysis
from backend.app.models.ai_result import AIResult
from backend.app.models.risk_score import RiskScore
from backend.app.models.user import User

from backend.app.repositories.ai_result_repository import AIResultRepository
from backend.app.repositories.analysis_repository import AnalysisRepository
from backend.app.repositories.risk_score_repository import RiskScoreRepository
from backend.app.repositories.upload_repository import UploadRepository

from backend.app.schemas.analysis import CreateAnalysisResponse

from backend.app.services.exceptions import (
    AnalysisAlreadyExistsError,
    UploadNotFoundError,
)
from backend.app.services.storage_service import StorageService


class AnalysisService:

    def __init__(
        self,
        session: AsyncSession,
        upload_repository: UploadRepository,
        analysis_repository: AnalysisRepository,
        storage_service: StorageService,
        prompt_builder: PromptBuilder,
        ai_orchestrator: AIOrchestrator,
        ai_result_repository: AIResultRepository,
        risk_score_repository: RiskScoreRepository,
    ) -> None:
        self._session = session
        self._upload_repository = upload_repository
        self._analysis_repository = analysis_repository
        self._storage_service = storage_service
        self._prompt_builder = prompt_builder
        self._ai_orchestrator = ai_orchestrator
        self._ai_result_repository = ai_result_repository
        self._risk_score_repository = risk_score_repository

    async def create_analysis(
        self,
        user: User,
        upload_id: UUID,
    ) -> CreateAnalysisResponse:

        upload = await self._upload_repository.get_by_id_and_user(
            upload_id,
            user.id,
        )

        if upload is None:
            raise UploadNotFoundError()

        existing_analysis = await self._analysis_repository.get_by_upload_id(
            upload_id
        )

        if existing_analysis is not None:
            raise AnalysisAlreadyExistsError()

        analysis = Analysis(
            upload_id=upload.id,
            status=AnalysisStatus.PENDING,
            started_at=datetime.now(timezone.utc),
        )

        try:
            await self._analysis_repository.save(analysis)
            await self._session.commit()
            await self._session.refresh(analysis)

            image_bytes = await self._storage_service.get_file(
                upload.storage_path
            )

            prompt = self._prompt_builder.build()

            result = await self._ai_orchestrator.analyze_image(
                image_bytes=image_bytes,
                mime_type=upload.content_type,
                prompt=prompt,
            )

            ai_result = AIResult(
                analysis_id=analysis.id,
                summary=result.summary,
                explanation=result.description,
                guidance=result.solution,
                reassurance=result.reassurance,
                risk_level=result.risk_level,
            )

            await self._ai_result_repository.save(ai_result)

            for risk_factor in result.risk_factors:
                risk_score = RiskScore(
                    analysis_id=analysis.id,
                    risk_factor=risk_factor.risk_factor,
                    score=risk_factor.value,
                    explanation=risk_factor.description,
                )

                await self._risk_score_repository.save(risk_score)

            analysis.status = AnalysisStatus.COMPLETED
            analysis.completed_at = datetime.now(timezone.utc)

            await self._session.commit()

            return CreateAnalysisResponse(
                analysis_id=analysis.id,
                upload_id=analysis.upload_id,
                status=analysis.status,
                message="Analysis completed successfully.",
            )

        except Exception:
            await self._session.rollback()

            analysis.status = AnalysisStatus.FAILED
            analysis.completed_at = datetime.now(timezone.utc)

            await self._session.commit()

            raise