import pytest
import datetime

from unittest.mock import AsyncMock, MagicMock

from backend.app.services.exceptions import (
    InvalidCredentialsError,
    SessionNotFoundError,
    SessionRevokedError,
    SessionExpiredError,
)

from backend.app.schemas.auth import LogoutResponse

from backend.app.enums.audit_action import AuditAction
from backend.app.enums.audit_resource_type import AuditResourceType


# ============================================================
# LOGIN
# ============================================================


@pytest.mark.asyncio
async def test_login_success(
    auth_service,
    user_repository,
    user,
    password_service,
    jwt_service,
    token_service,
    user_session,
    db_session,
    audit_log_service,
):
    # ARRANGE

    user_repository.find_by_email = AsyncMock(
        return_value=user
    )

    password_service.verify_password = MagicMock(
        return_value=True
    )

    jwt_service.create_access_token.return_value = (
        "fake_access_token"
    )

    jwt_service.create_refresh_token.return_value = (
        "fake_refresh_token"
    )

    jwt_service.access_token_expires_in = 3600

    token_service.create_session = AsyncMock(
        return_value=user_session
    )

    # ACT

    result = await auth_service.login(
        user.email,
        "correct_password",
    )

    # ASSERT

    assert result.access_token == "fake_access_token"
    assert result.refresh_token == "fake_refresh_token"
    assert result.token_type == "Bearer"
    assert result.expires_in == (
        jwt_service.access_token_expires_in
    )

    user_repository.find_by_email.assert_awaited_once_with(
        user.email
    )

    password_service.verify_password.assert_called_once_with(
        "correct_password",
        user.password_hash,
    )

    jwt_service.create_access_token.assert_called_once_with(
        str(user.id)
    )

    jwt_service.create_refresh_token.assert_called_once_with(
        str(user.id)
    )

    token_service.create_session.assert_awaited_once_with(
        user,
        "fake_refresh_token",
    )

    audit_log_service.log.assert_awaited_once_with(
        action=AuditAction.LOGIN_SUCCEEDED,
        resource_type=AuditResourceType.USER,
        resource_id=user.id,
        actor_user_id=user.id,
    )

    db_session.commit.assert_awaited_once()
    db_session.rollback.assert_not_awaited()


@pytest.mark.asyncio
async def test_login_invalid_password(
    user_repository,
    password_service,
    user,
    auth_service,
    jwt_service,
    token_service,
    db_session,
    audit_log_service,
):
    # ARRANGE

    user_repository.find_by_email = AsyncMock(
        return_value=user
    )

    password_service.verify_password = MagicMock(
        return_value=False
    )

    # ACT & ASSERT

    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            user.email,
            "wrong_password",
        )

    # ASSERT

    user_repository.find_by_email.assert_awaited_once_with(
        user.email
    )

    password_service.verify_password.assert_called_once_with(
        "wrong_password",
        user.password_hash,
    )

    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()

    token_service.create_session.assert_not_called()

    audit_log_service.log.assert_awaited_once_with(
        action=AuditAction.LOGIN_FAILED,
        resource_type=AuditResourceType.USER,
        resource_id=user.id,
        actor_user_id=user.id,
        details="Login failed due to invalid credentials.",
    )

    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_login_user_not_found(
    user_repository,
    user,
    auth_service,
    password_service,
    jwt_service,
    token_service,
    db_session,
    audit_log_service,
):
    # ARRANGE

    user_repository.find_by_email = AsyncMock(
        return_value=None
    )

    # ACT & ASSERT

    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            user.email,
            "password",
        )

    # ASSERT

    user_repository.find_by_email.assert_awaited_once_with(
        user.email
    )

    password_service.verify_password.assert_not_called()

    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()

    token_service.create_session.assert_not_called()

    audit_log_service.log.assert_awaited_once_with(
        action=AuditAction.LOGIN_FAILED,
        resource_type=AuditResourceType.USER,
        resource_id=user.id,
        actor_user_id=None,
        details="Login failed for unknown user.",
    )

    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()
# ============================================================
# REFRESH
# ============================================================


@pytest.mark.asyncio
async def test_refresh_success(
    db_session,
    auth_service,
    jwt_service,
    token_service,
    user_session,
    audit_log_service,
):
    # ARRANGE

    jwt_service.access_token_expires_in = 1

    refresh_token = "dummy_refresh_token"

    jwt_service.verify_token = MagicMock(
        return_value={"type": "refresh"}
    )

    token_service.get_session_by_refresh_token = AsyncMock(
        return_value=user_session
    )

    jwt_service.create_access_token = MagicMock(
        return_value="new_access_token"
    )

    jwt_service.create_refresh_token = MagicMock(
        return_value="new_refresh_token"
    )

    token_service.rotate_refresh_token = MagicMock()

    # ACT

    result = await auth_service.refresh(
        refresh_token
    )

    # ASSERT

    assert result.access_token == "new_access_token"
    assert result.refresh_token == "new_refresh_token"
    assert result.token_type == "Bearer"
    assert result.expires_in == (
        jwt_service.access_token_expires_in
    )

    jwt_service.verify_token.assert_called_once_with(
        refresh_token
    )

    token_service.get_session_by_refresh_token.assert_awaited_once_with(
        refresh_token
    )

    jwt_service.create_access_token.assert_called_once_with(
        str(user_session.user.id)
    )

    jwt_service.create_refresh_token.assert_called_once_with(
        str(user_session.user.id)
    )

    token_service.rotate_refresh_token.assert_called_once_with(
        user_session,
        "new_refresh_token",
    )

    db_session.commit.assert_awaited_once()

    audit_log_service.log.assert_awaited_once_with(
        action=AuditAction.SESSION_REFRESHED,
        resource_type=AuditResourceType.SESSION,
        resource_id=user_session.id,
        actor_user_id=user_session.user.id,
    )


@pytest.mark.asyncio
async def test_refresh_invalid_token_type(
    jwt_service,
    auth_service,
    token_service,
    db_session,
    audit_log_service,
):
    # ARRANGE

    jwt_service.access_token_expires_in = 1

    refresh_token = "dummy_refresh_token"

    jwt_service.verify_token = MagicMock(
        return_value={"type": "access"}
    )

    # ACT & ASSERT

    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(refresh_token)

    # ASSERT

    token_service.get_session_by_refresh_token.assert_not_called()

    jwt_service.verify_token.assert_called_once_with(
        refresh_token
    )

    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()

    token_service.rotate_refresh_token.assert_not_called()

    audit_log_service.log.assert_not_awaited()

    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_refresh_session_not_found(
    jwt_service,
    token_service,
    auth_service,
    db_session,
    audit_log_service,
):
    # ARRANGE

    jwt_service.access_token_expires_in = 1

    refresh_token = "dummy_refresh_token"

    jwt_service.verify_token = MagicMock(
        return_value={"type": "refresh"}
    )

    token_service.get_session_by_refresh_token = AsyncMock(
        return_value=None
    )

    # ACT & ASSERT

    with pytest.raises(SessionNotFoundError):
        await auth_service.refresh(refresh_token)

    # ASSERT

    token_service.get_session_by_refresh_token.assert_awaited_once_with(
        refresh_token
    )

    jwt_service.verify_token.assert_called_once_with(
        refresh_token
    )

    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()

    token_service.rotate_refresh_token.assert_not_called()

    audit_log_service.log.assert_not_awaited()

    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_refresh_session_revoked(
    jwt_service,
    token_service,
    auth_service,
    user_session,
    db_session,
    audit_log_service,
):
    # ARRANGE

    jwt_service.access_token_expires_in = 1

    refresh_token = "dummy_refresh_token"

    jwt_service.verify_token = MagicMock(
        return_value={"type": "refresh"}
    )

    token_service.get_session_by_refresh_token = AsyncMock(
        return_value=user_session
    )

    user_session.revoked_at = datetime.datetime.now()

    # ACT & ASSERT

    with pytest.raises(SessionRevokedError):
        await auth_service.refresh(refresh_token)

    # ASSERT

    token_service.get_session_by_refresh_token.assert_awaited_once_with(
        refresh_token
    )

    jwt_service.verify_token.assert_called_once_with(
        refresh_token
    )

    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()

    token_service.rotate_refresh_token.assert_not_called()

    audit_log_service.log.assert_not_awaited()

    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_refresh_session_expired(
    jwt_service,
    token_service,
    auth_service,
    user_session,
    db_session,
    audit_log_service,
):
    # ARRANGE

    jwt_service.access_token_expires_in = 1

    refresh_token = "dummy_refresh_token"

    jwt_service.verify_token = MagicMock(
        return_value={"type": "refresh"}
    )

    token_service.get_session_by_refresh_token = AsyncMock(
        return_value=user_session
    )

    user_session.expires_at = (
        datetime.datetime.now(datetime.UTC)
        - datetime.timedelta(minutes=30)
    )

    # ACT & ASSERT

    with pytest.raises(SessionExpiredError):
        await auth_service.refresh(refresh_token)

    # ASSERT

    token_service.get_session_by_refresh_token.assert_awaited_once_with(
        refresh_token
    )

    jwt_service.verify_token.assert_called_once_with(
        refresh_token
    )

    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()

    token_service.rotate_refresh_token.assert_not_called()

    audit_log_service.log.assert_not_awaited()

    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_refresh_user_not_found(
    jwt_service,
    token_service,
    auth_service,
    user_session,
    db_session,
    audit_log_service,
):
    # ARRANGE

    jwt_service.access_token_expires_in = 1

    refresh_token = "dummy_refresh_token"

    jwt_service.verify_token = MagicMock(
        return_value={"type": "refresh"}
    )

    token_service.get_session_by_refresh_token = AsyncMock(
        return_value=user_session
    )

    user_session.expires_at = (
        datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(minutes=30)
    )

    user_session.user = None

    # ACT & ASSERT

    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(refresh_token)

    # ASSERT

    token_service.get_session_by_refresh_token.assert_awaited_once_with(
        refresh_token
    )

    jwt_service.verify_token.assert_called_once_with(
        refresh_token
    )

    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()

    token_service.rotate_refresh_token.assert_not_called()

    audit_log_service.log.assert_not_awaited()

    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()


# ============================================================
# LOGOUT
# ============================================================


@pytest.mark.asyncio
async def test_logout_success(
    auth_service,
    jwt_service,
    token_service,
    db_session,
    user_session,
    audit_log_service,
):
    # ARRANGE

    refresh_token = "refresh-token"

    jwt_service.verify_token = MagicMock(
        return_value={
            "sub": str(user_session.user_id),
            "type": "refresh",
        }
    )

    token_service.get_session_by_refresh_token = AsyncMock(
        return_value=user_session
    )

    token_service.revoke_session = AsyncMock()

    db_session.commit = AsyncMock()
    db_session.rollback = AsyncMock()

    # ACT

    response = await auth_service.logout(
        refresh_token
    )

    # ASSERT

    jwt_service.verify_token.assert_called_once_with(
        refresh_token
    )

    token_service.get_session_by_refresh_token.assert_awaited_once_with(
        refresh_token
    )

    token_service.revoke_session.assert_awaited_once_with(
        user_session
    )

    audit_log_service.log.assert_awaited_once_with(
        action=AuditAction.LOGOUT,
        resource_type=AuditResourceType.SESSION,
        resource_id=user_session.id,
        actor_user_id=user_session.user.id,
    )

    db_session.commit.assert_awaited_once()
    db_session.rollback.assert_not_awaited()

    assert isinstance(response, LogoutResponse)

    assert response.message == (
        "You have been successfully logged out"
    )


@pytest.mark.asyncio
async def test_logout_invalid_token_type(
    user_session,
    jwt_service,
    auth_service,
    token_service,
    db_session,
    audit_log_service,
):
    # ARRANGE

    token = "access-token"

    jwt_service.verify_token = MagicMock(
        return_value={
            "sub": str(user_session.user_id),
            "type": "access",
        }
    )

    # ACT & ASSERT

    with pytest.raises(InvalidCredentialsError):
        await auth_service.logout(token)

    # ASSERT

    jwt_service.verify_token.assert_called_once_with(
        token
    )

    token_service.get_session_by_refresh_token.assert_not_called()

    token_service.revoke_session.assert_not_called()

    audit_log_service.log.assert_not_awaited()

    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_logout_session_not_found(
    jwt_service,
    token_service,
    user_session,
    auth_service,
    db_session,
    audit_log_service,
):
    # ARRANGE

    refresh_token = "refresh-token"

    jwt_service.verify_token = MagicMock(
        return_value={
            "sub": str(user_session.user_id),
            "type": "refresh",
        }
    )

    token_service.get_session_by_refresh_token = AsyncMock(
        return_value=None
    )

    # ACT & ASSERT

    with pytest.raises(SessionNotFoundError):
        await auth_service.logout(refresh_token)

    # ASSERT

    jwt_service.verify_token.assert_called_once_with(
        refresh_token
    )

    token_service.get_session_by_refresh_token.assert_awaited_once_with(
        refresh_token
    )

    token_service.revoke_session.assert_not_called()

    audit_log_service.log.assert_not_awaited()

    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()