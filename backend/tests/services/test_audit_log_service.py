from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.app.enums.audit_action import AuditAction
from backend.app.enums.audit_resource_type import AuditResourceType
from backend.app.models.audit_log import AuditLog
from backend.app.services.audit_log_service import AuditLogService


@pytest.mark.asyncio
async def test_log_creates_and_saves_audit_log():
    audit_log_repository = MagicMock()
    audit_log_repository.save = AsyncMock()

    service = AuditLogService(
        audit_log_repository=audit_log_repository,
    )

    actor_user_id = uuid4()
    resource_id = uuid4()

    await service.log(
        action=AuditAction.LOGIN_SUCCEEDED,
        resource_type=AuditResourceType.USER,
        resource_id=resource_id,
        actor_user_id=actor_user_id,
        details="User logged in successfully.",
    )

    audit_log_repository.save.assert_awaited_once()

    saved_log = audit_log_repository.save.call_args.args[0]

    assert isinstance(saved_log, AuditLog)
    assert saved_log.actor_user_id == actor_user_id
    assert saved_log.action == AuditAction.LOGIN_SUCCEEDED
    assert saved_log.resource_type == AuditResourceType.USER
    assert saved_log.resource_id == resource_id
    assert saved_log.details == "User logged in successfully."


@pytest.mark.asyncio
async def test_log_allows_anonymous_actor():
    audit_log_repository = MagicMock()
    audit_log_repository.save = AsyncMock()

    service = AuditLogService(
        audit_log_repository=audit_log_repository,
    )

    resource_id = uuid4()

    await service.log(
        action=AuditAction.LOGIN_FAILED,
        resource_type=AuditResourceType.USER,
        resource_id=resource_id,
    )

    saved_log = audit_log_repository.save.call_args.args[0]

    assert saved_log.actor_user_id is None
    assert saved_log.action == AuditAction.LOGIN_FAILED
    assert saved_log.resource_type == AuditResourceType.USER
    assert saved_log.resource_id == resource_id


@pytest.mark.asyncio
async def test_log_returns_saved_audit_log():
    audit_log_repository = MagicMock()

    saved_log = MagicMock(spec=AuditLog)

    audit_log_repository.save = AsyncMock(
        return_value=saved_log
    )

    service = AuditLogService(
        audit_log_repository=audit_log_repository,
    )

    result = await service.log(
        action=AuditAction.UPLOAD_CREATED,
        resource_type=AuditResourceType.UPLOAD,
        resource_id=uuid4(),
    )

    assert result is saved_log