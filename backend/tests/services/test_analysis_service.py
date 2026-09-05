from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from backend.app.ai.schemas import AIResponseSchema, RiskFactorResult
from backend.app.enums.analysis import AnalysisStatus
from backend.app.enums.audit_action import AuditAction
from backend.app.enums.audit_resource_type import AuditResourceType
from backend.app.enums.risk_factor import RiskFactor
from backend.app.enums.risk_level import RiskLevel
from backend.app.models.analysis import Analysis
from backend.app.services.analysis_service import AnalysisService
from backend.app.services.exceptions import (
    AnalysisAlreadyExistsError,
    AnalysisNotFoundError,
    UploadNotFoundError,
)


@pytest.fixture
def audit_log_service():
    service = Mock()
    service.log = AsyncMock()
    return service


@pytest.fixture
def service(audit_log_service):
    service = AnalysisService(
        session=AsyncMock(),
        upload_repository=AsyncMock(),
        analysis_repository=AsyncMock(),
        ai_result_repository=AsyncMock(),
        risk_score_repository=AsyncMock(),
        storage_service=AsyncMock(),
        prompt_builder=Mock(),
        ai_orchestrator=AsyncMock(),
        risk_scoring_service=Mock(),
        audit_log_service=audit_log_service,
    )

    return service


@pytest.fixture
def user():
    user = Mock()
    user.id = uuid4()

    return user


@pytest.fixture
def upload_id():
    return uuid4()


@pytest.fixture
def upload(upload_id, user):
    return SimpleNamespace(
        id=upload_id,
        user_id=user.id,
        storage_path="uploads/test-image.png",
        content_type="image/png",
    )


@pytest.fixture
def ai_result():
    return AIResponseSchema(
        summary="This message appears suspicious.",
        risk_level=RiskLevel.HIGH,
        description="The message contains suspicious characteristics.",
        solution="Do not interact with the sender.",
        reassurance="You are safe if you avoid interacting with the message.",
        risk_factors=[
            RiskFactorResult(
                risk_factor=RiskFactor.SUSPICIOUS_LINK,
                description="The message contains a suspicious link.",
            ),
            RiskFactorResult(
                risk_factor=RiskFactor.URGENCY_LANGUAGE,
                description="The message creates urgency.",
            ),
        ],
    )


@pytest.mark.asyncio
async def test_create_analysis_success(
    service,
    user,
    upload_id,
    upload,
    ai_result,
    audit_log_service,
):
    service._upload_repository.get_by_id_and_user.return_value = upload
    service._analysis_repository.get_by_upload_id.return_value = None

    service._storage_service.get_file.return_value = b"image-bytes"
    service._prompt_builder.build.return_value = "Analyze this image."
    service._ai_orchestrator.analyze_image.return_value = ai_result

    scored_factors = [
        SimpleNamespace(
            risk_factor=RiskFactor.SUSPICIOUS_LINK,
            score=0.25,
            explanation="The message contains a suspicious link.",
        ),
        SimpleNamespace(
            risk_factor=RiskFactor.URGENCY_LANGUAGE,
            score=0.15,
            explanation="The message creates urgency.",
        ),
    ]

    service._risk_scoring_service.score_factors.return_value = scored_factors
    service._risk_scoring_service.calculate_overall_score.return_value = 0.40
    service._risk_scoring_service.determine_risk_level.return_value = (
        RiskLevel.MEDIUM
    )

    response = await service.create_analysis(
        user=user,
        upload_id=upload_id,
    )

    assert response.analysis_id is not None
    assert response.upload_id == upload_id
    assert response.status == AnalysisStatus.COMPLETED
    assert response.message == "Analysis completed successfully."

    service._upload_repository.get_by_id_and_user.assert_awaited_once_with(
        upload_id,
        user.id,
    )

    service._analysis_repository.get_by_upload_id.assert_awaited_once_with(
        upload_id,
    )

    service._storage_service.get_file.assert_awaited_once_with(
        upload.storage_path,
    )

    service._prompt_builder.build.assert_called_once()

    service._ai_orchestrator.analyze_image.assert_awaited_once_with(
        image_bytes=b"image-bytes",
        mime_type=upload.content_type,
        prompt="Analyze this image.",
    )

    service._risk_scoring_service.score_factors.assert_called_once_with(
        ai_result.risk_factors
    )

    service._risk_scoring_service.calculate_overall_score.assert_called_once_with(
        scored_factors
    )

    service._risk_scoring_service.determine_risk_level.assert_called_once_with(
        0.40
    )

    assert audit_log_service.log.await_count == 3

    first_audit_call = audit_log_service.log.await_args_list[0]
    assert first_audit_call.kwargs == {
        "action": AuditAction.ANALYSIS_REQUESTED,
        "resource_type": AuditResourceType.ANALYSIS,
        "resource_id": response.analysis_id,
        "actor_user_id": user.id,
    }

    second_audit_call = audit_log_service.log.await_args_list[1]
    assert second_audit_call.kwargs == {
        "action": AuditAction.ANALYSIS_STARTED,
        "resource_type": AuditResourceType.ANALYSIS,
        "resource_id": response.analysis_id,
        "actor_user_id": user.id,
    }

    third_audit_call = audit_log_service.log.await_args_list[2]
    assert third_audit_call.kwargs == {
        "action": AuditAction.ANALYSIS_COMPLETED,
        "resource_type": AuditResourceType.ANALYSIS,
        "resource_id": response.analysis_id,
        "actor_user_id": user.id,
    }

    service._session.commit.assert_awaited()


@pytest.mark.asyncio
async def test_create_analysis_upload_not_found(
    service,
    user,
    upload_id,
    audit_log_service,
):
    service._upload_repository.get_by_id_and_user.return_value = None

    with pytest.raises(UploadNotFoundError):
        await service.create_analysis(
            user=user,
            upload_id=upload_id,
        )

    service._upload_repository.get_by_id_and_user.assert_awaited_once_with(
        upload_id,
        user.id,
    )

    service._analysis_repository.get_by_upload_id.assert_not_awaited()
    audit_log_service.log.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_analysis_already_exists(
    service,
    user,
    upload_id,
    upload,
    audit_log_service,
):
    existing_analysis = Mock(spec=Analysis)

    service._upload_repository.get_by_id_and_user.return_value = upload
    service._analysis_repository.get_by_upload_id.return_value = (
        existing_analysis
    )

    with pytest.raises(AnalysisAlreadyExistsError):
        await service.create_analysis(
            user=user,
            upload_id=upload_id,
        )

    service._upload_repository.get_by_id_and_user.assert_awaited_once_with(
        upload_id,
        user.id,
    )

    service._analysis_repository.get_by_upload_id.assert_awaited_once_with(
        upload_id,
    )

    service._analysis_repository.save.assert_not_awaited()
    audit_log_service.log.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_analysis_creates_pending_analysis(
    service,
    user,
    upload_id,
    upload,
    ai_result,
):
    service._upload_repository.get_by_id_and_user.return_value = upload
    service._analysis_repository.get_by_upload_id.return_value = None

    service._storage_service.get_file.return_value = b"image-bytes"
    service._prompt_builder.build.return_value = "Analyze this image."
    service._ai_orchestrator.analyze_image.return_value = ai_result

    service._risk_scoring_service.score_factors.return_value = []
    service._risk_scoring_service.calculate_overall_score.return_value = 0
    service._risk_scoring_service.determine_risk_level.return_value = (
        RiskLevel.SAFE
    )

    saved_analysis = None

    async def capture_analysis(analysis):
        nonlocal saved_analysis

        saved_analysis = {
            "upload_id": analysis.upload_id,
            "status": analysis.status,
            "started_at": analysis.started_at,
            "completed_at": analysis.completed_at,
        }

    service._analysis_repository.save.side_effect = capture_analysis

    await service.create_analysis(
        user=user,
        upload_id=upload_id,
    )

    assert saved_analysis is not None
    assert saved_analysis["upload_id"] == upload_id
    assert saved_analysis["status"] == AnalysisStatus.PENDING
    assert saved_analysis["started_at"] is not None


@pytest.mark.asyncio
async def test_create_analysis_uses_ai_risk_factors_for_scoring(
    service,
    user,
    upload_id,
    upload,
    ai_result,
):
    service._upload_repository.get_by_id_and_user.return_value = upload
    service._analysis_repository.get_by_upload_id.return_value = None

    service._storage_service.get_file.return_value = b"image-bytes"
    service._prompt_builder.build.return_value = "Analyze this image."
    service._ai_orchestrator.analyze_image.return_value = ai_result

    scored_factors = [
        SimpleNamespace(
            risk_factor=RiskFactor.SUSPICIOUS_LINK,
            score=0.25,
            explanation="Suspicious link.",
        ),
    ]

    service._risk_scoring_service.score_factors.return_value = scored_factors
    service._risk_scoring_service.calculate_overall_score.return_value = 0.25
    service._risk_scoring_service.determine_risk_level.return_value = (
        RiskLevel.LOW
    )

    await service.create_analysis(
        user=user,
        upload_id=upload_id,
    )

    service._risk_scoring_service.score_factors.assert_called_once_with(
        ai_result.risk_factors
    )

    service._risk_scoring_service.calculate_overall_score.assert_called_once_with(
        scored_factors
    )

    service._risk_scoring_service.determine_risk_level.assert_called_once_with(
        0.25
    )


@pytest.mark.asyncio
async def test_create_analysis_saves_each_risk_factor(
    service,
    user,
    upload_id,
    upload,
    ai_result,
):
    service._upload_repository.get_by_id_and_user.return_value = upload
    service._analysis_repository.get_by_upload_id.return_value = None

    service._storage_service.get_file.return_value = b"image-bytes"
    service._prompt_builder.build.return_value = "Analyze this image."
    service._ai_orchestrator.analyze_image.return_value = ai_result

    scored_factors = [
        SimpleNamespace(
            risk_factor=RiskFactor.SUSPICIOUS_LINK,
            score=0.25,
            explanation="Suspicious link.",
        ),
        SimpleNamespace(
            risk_factor=RiskFactor.URGENCY_LANGUAGE,
            score=0.15,
            explanation="Urgency.",
        ),
    ]

    service._risk_scoring_service.score_factors.return_value = scored_factors
    service._risk_scoring_service.calculate_overall_score.return_value = 0.40
    service._risk_scoring_service.determine_risk_level.return_value = (
        RiskLevel.MEDIUM
    )

    await service.create_analysis(
        user=user,
        upload_id=upload_id,
    )

    assert service._risk_score_repository.save.await_count == 2

    saved_risk_scores = [
        call.args[0]
        for call in service._risk_score_repository.save.await_args_list
    ]

    assert saved_risk_scores[0].risk_factor == RiskFactor.SUSPICIOUS_LINK
    assert saved_risk_scores[0].score == 0.25
    assert saved_risk_scores[0].explanation == "Suspicious link."

    assert saved_risk_scores[1].risk_factor == RiskFactor.URGENCY_LANGUAGE
    assert saved_risk_scores[1].score == 0.15
    assert saved_risk_scores[1].explanation == "Urgency."


@pytest.mark.asyncio
async def test_create_analysis_ai_failure_rolls_back(
    service,
    user,
    upload_id,
    upload,
    audit_log_service,
):
    service._upload_repository.get_by_id_and_user.return_value = upload
    service._analysis_repository.get_by_upload_id.return_value = None

    service._storage_service.get_file.return_value = b"image-bytes"
    service._prompt_builder.build.return_value = "Analyze this image."

    service._ai_orchestrator.analyze_image.side_effect = RuntimeError(
        "AI provider failed"
    )

    with pytest.raises(RuntimeError, match="AI provider failed"):
        await service.create_analysis(
            user=user,
            upload_id=upload_id,
        )

    service._session.rollback.assert_awaited_once()

    analysis_id = (
        service._analysis_repository.save.await_args.args[0].id
    )

    audit_actions = [
        call.kwargs["action"]
        for call in audit_log_service.log.await_args_list
    ]

    assert AuditAction.ANALYSIS_REQUESTED in audit_actions
    assert AuditAction.ANALYSIS_STARTED in audit_actions
    assert AuditAction.ANALYSIS_FAILED in audit_actions

    for call in audit_log_service.log.await_args_list:
        if call.kwargs["action"] == AuditAction.ANALYSIS_FAILED:
            assert call.kwargs["resource_type"] == AuditResourceType.ANALYSIS
            assert call.kwargs["resource_id"] == analysis_id
            assert call.kwargs["actor_user_id"] == user.id


@pytest.mark.asyncio
async def test_create_analysis_storage_failure_rolls_back(
    service,
    user,
    upload_id,
    upload,
    audit_log_service,
):
    service._upload_repository.get_by_id_and_user.return_value = upload
    service._analysis_repository.get_by_upload_id.return_value = None

    service._storage_service.get_file.side_effect = RuntimeError(
        "File could not be read"
    )

    with pytest.raises(RuntimeError, match="File could not be read"):
        await service.create_analysis(
            user=user,
            upload_id=upload_id,
        )

    service._session.rollback.assert_awaited_once()

    audit_actions = [
        call.kwargs["action"]
        for call in audit_log_service.log.await_args_list
    ]

    assert AuditAction.ANALYSIS_REQUESTED in audit_actions
    assert AuditAction.ANALYSIS_STARTED in audit_actions
    assert AuditAction.ANALYSIS_FAILED in audit_actions


@pytest.mark.asyncio
async def test_create_analysis_marks_analysis_failed_on_error(
    service,
    user,
    upload_id,
    upload,
    audit_log_service,
):
    service._upload_repository.get_by_id_and_user.return_value = upload
    service._analysis_repository.get_by_upload_id.return_value = None

    service._storage_service.get_file.side_effect = RuntimeError(
        "Storage failure"
    )

    with pytest.raises(RuntimeError):
        await service.create_analysis(
            user=user,
            upload_id=upload_id,
        )

    saved_analysis = (
        service._analysis_repository.save.call_args.args[0]
    )

    assert saved_analysis.status == AnalysisStatus.FAILED
    assert saved_analysis.completed_at is not None

    failed_audit_calls = [
        call
        for call in audit_log_service.log.await_args_list
        if call.kwargs["action"] == AuditAction.ANALYSIS_FAILED
    ]

    assert len(failed_audit_calls) == 1
    assert failed_audit_calls[0].kwargs["resource_type"] == (
        AuditResourceType.ANALYSIS
    )
    assert failed_audit_calls[0].kwargs["resource_id"] == saved_analysis.id
    assert failed_audit_calls[0].kwargs["actor_user_id"] == user.id


@pytest.mark.asyncio
async def test_get_analysis_returns_analysis_for_owner(
    service,
    user,
    audit_log_service,
):
    analysis_id = uuid4()

    analysis = Mock(spec=Analysis)
    analysis.id = analysis_id
    analysis.upload = Mock()
    analysis.upload.user_id = user.id

    service._analysis_repository.get_by_id.return_value = analysis

    result = await service.get_analysis(
        user=user,
        analysis_id=analysis_id,
    )

    assert result is analysis

    service._analysis_repository.get_by_id.assert_awaited_once_with(
        analysis_id
    )

    audit_log_service.log.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_analysis_raises_when_analysis_not_found(
    service,
    user,
    audit_log_service,
):
    analysis_id = uuid4()

    service._analysis_repository.get_by_id.return_value = None

    with pytest.raises(AnalysisNotFoundError):
        await service.get_analysis(
            user=user,
            analysis_id=analysis_id,
        )

    service._analysis_repository.get_by_id.assert_awaited_once_with(
        analysis_id
    )

    audit_log_service.log.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_analysis_denies_access_to_other_users_analysis(
    service,
    user,
    audit_log_service,
):
    analysis_id = uuid4()
    other_user_id = uuid4()

    analysis = Mock(spec=Analysis)
    analysis.id = analysis_id
    analysis.upload = Mock()
    analysis.upload.user_id = other_user_id

    service._analysis_repository.get_by_id.return_value = analysis

    with pytest.raises(AnalysisNotFoundError):
        await service.get_analysis(
            user=user,
            analysis_id=analysis_id,
        )

    service._analysis_repository.get_by_id.assert_awaited_once_with(
        analysis_id
    )

    audit_log_service.log.assert_awaited_once_with(
        action=AuditAction.ACCESS_DENIED,
        resource_type=AuditResourceType.ANALYSIS,
        resource_id=analysis_id,
        actor_user_id=user.id,
    )