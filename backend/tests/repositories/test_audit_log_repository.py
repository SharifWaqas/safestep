from datetime import datetime, UTC, timedelta
from uuid import uuid4

import pytest
from unittest.mock import AsyncMock, MagicMock

from backend.app.models.audit_log import AuditLog
from backend.app.repositories.audit_log_repository import AuditLogRepository


@pytest.mark.asyncio
async def test_list_by_actor_returns_actor_logs():
    actor_user_id = uuid4()

    older_log = MagicMock(spec=AuditLog)
    older_log.actor_user_id = actor_user_id
    older_log.created_at = datetime.now(UTC) - timedelta(minutes=10)

    newer_log = MagicMock(spec=AuditLog)
    newer_log.actor_user_id = actor_user_id
    newer_log.created_at = datetime.now(UTC)

    db_session = AsyncMock()

    result = MagicMock()
    result.scalars.return_value.all.return_value = [
        newer_log,
        older_log,
    ]

    db_session.execute.return_value = result

    repository = AuditLogRepository(db_session)

    actual_logs = await repository.list_by_actor(actor_user_id)

    assert actual_logs == [
        newer_log,
        older_log,
    ]

    db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_by_actor_returns_empty_list_when_no_logs():
    actor_user_id = uuid4()

    db_session = AsyncMock()

    result = MagicMock()
    result.scalars.return_value.all.return_value = []

    db_session.execute.return_value = result

    repository = AuditLogRepository(db_session)

    actual_logs = await repository.list_by_actor(actor_user_id)

    assert actual_logs == []

    db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_by_actor_only_queries_requested_actor():
    actor_user_id = uuid4()

    db_session = AsyncMock()

    result = MagicMock()
    result.scalars.return_value.all.return_value = []

    db_session.execute.return_value = result

    repository = AuditLogRepository(db_session)

    await repository.list_by_actor(actor_user_id)

    query = db_session.execute.call_args.args[0]

    compiled_query = str(query)

    assert "audit_logs.actor_user_id" in compiled_query
    assert "audit_logs.created_at" in compiled_query