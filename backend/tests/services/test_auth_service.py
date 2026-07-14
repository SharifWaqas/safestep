import pytest

from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_login_success(auth_service, user_repository, user, password_service, jwt_service, token_service, user_session, db_session):

    """ARRANGE"""
    user_repository.find_by_email = AsyncMock(return_value=user)
    password_service.verify_password.return_value = True
    jwt_service.create_access_token.return_value = "fake_access_token"
    jwt_service.create_refresh_token.return_value = "fake_refresh_token"
    jwt_service.access_token_expires_in = 3600
    token_service.create_session = AsyncMock(return_value=user_session)

    """ACT"""
    result = await auth_service.login(user.email,"correct_password" )

    """ASSERT"""
    assert result.access_token == "fake_access_token"
    assert result.refresh_token == "fake_refresh_token"
    assert result.token_type == "Bearer"
    assert result.expires_in == jwt_service.access_token_expires_in
    user_repository.find_by_email.assert_awaited_once_with(user.email)
    db_session.commit.assert_awaited_once()
    db_session.rollback.assert_not_awaited()
    password_service.verify_password.assert_called_once_with("correct_password",user.password_hash)
    jwt_service.create_access_token.assert_called_once_with(str(user.id))
    jwt_service.create_refresh_token.assert_called_once_with(str(user.id))
    token_service.create_session.assert_awaited_once_with(user,"fake_refresh_token")    


def test_login_invalid_password():
    ...


def test_login_user_not_found():
    ...


def test_refresh_success():
    ...


def test_refresh_session_revoked():
    ...


def test_logout_success():
    ...