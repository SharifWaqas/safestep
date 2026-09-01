from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from backend.app.models.session import Session
from backend.app.models.user import User
from backend.app.services.token_service import TokenService


@pytest.fixture
def session_repository():
    repository = MagicMock()
    repository.save = AsyncMock()
    repository.find_by_refresh_token_hash = AsyncMock()
    return repository


@pytest.fixture
def jwt_service():
    return MagicMock()


@pytest.fixture
def token_service(session_repository, jwt_service):
    return TokenService(
        session_repository=session_repository,
        jwt_service=jwt_service,
    )


@pytest.fixture
def user():
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="John Doe",
    )
    user.id = uuid4()
    return user


@pytest.mark.asyncio
async def test_create_session_saves_session(
    token_service,
    session_repository,
    jwt_service,
    user,
):
    refresh_token = "refresh-token"

    expiration = datetime.now(UTC) + timedelta(days=30)

    jwt_service.verify_token.return_value = {
        "exp": expiration.timestamp(),
    }

    await token_service.create_session(
        user=user,
        refresh_token=refresh_token,
    )

    session_repository.save.assert_awaited_once()

    saved_session = session_repository.save.await_args.args[0]

    assert isinstance(saved_session, Session)
    assert saved_session.user_id == user.id
    assert saved_session.expires_at == datetime.fromtimestamp(
        expiration.timestamp(),
        UTC,
    )
    assert saved_session.refresh_token_hash == (
        token_service._hash_refresh_token(refresh_token)
    )


@pytest.mark.asyncio
async def test_create_session_uses_jwt_expiration(
    token_service,
    session_repository,
    jwt_service,
    user,
):
    refresh_token = "refresh-token"
    expiration_timestamp = datetime.now(UTC).timestamp() + 3600

    jwt_service.verify_token.return_value = {
        "exp": expiration_timestamp,
    }

    await token_service.create_session(
        user=user,
        refresh_token=refresh_token,
    )

    saved_session = session_repository.save.await_args.args[0]

    assert saved_session.expires_at == datetime.fromtimestamp(
        expiration_timestamp,
        UTC,
    )


@pytest.mark.asyncio
async def test_get_session_by_refresh_token_returns_session(
    token_service,
    session_repository,
):
    refresh_token = "refresh-token"

    expected_session = MagicMock(spec=Session)

    session_repository.find_by_refresh_token_hash.return_value = (
        expected_session
    )

    result = await token_service.get_session_by_refresh_token(
        refresh_token
    )

    expected_hash = token_service._hash_refresh_token(refresh_token)

    session_repository.find_by_refresh_token_hash.assert_awaited_once_with(
        expected_hash
    )

    assert result is expected_session


@pytest.mark.asyncio
async def test_get_session_by_refresh_token_returns_none(
    token_service,
    session_repository,
):
    refresh_token = "refresh-token"

    session_repository.find_by_refresh_token_hash.return_value = None

    result = await token_service.get_session_by_refresh_token(
        refresh_token
    )

    expected_hash = token_service._hash_refresh_token(refresh_token)

    session_repository.find_by_refresh_token_hash.assert_awaited_once_with(
        expected_hash
    )

    assert result is None


@pytest.mark.asyncio
async def test_revoke_session_sets_revoked_at(
    token_service,
):
    session = MagicMock(spec=Session)
    session.revoked_at = None

    before = datetime.now(UTC)

    await token_service.revoke_session(session)

    after = datetime.now(UTC)

    assert session.revoked_at is not None
    assert before <= session.revoked_at <= after


@pytest.mark.asyncio
async def test_revoke_session_does_nothing_when_already_revoked(
    token_service,
):
    existing_revoked_at = datetime.now(UTC) - timedelta(hours=1)

    session = MagicMock(spec=Session)
    session.revoked_at = existing_revoked_at

    await token_service.revoke_session(session)

    assert session.revoked_at == existing_revoked_at


def test_rotate_refresh_token_updates_hash(
    token_service,
):
    session = MagicMock(spec=Session)
    session.refresh_token_hash = "old-hash"

    new_refresh_token = "new-refresh-token"

    token_service.rotate_refresh_token(
        session,
        new_refresh_token,
    )

    expected_hash = token_service._hash_refresh_token(
        new_refresh_token
    )

    assert session.refresh_token_hash == expected_hash