import pytest
import datetime

from backend.app.services.exceptions import InvalidCredentialsError
from unittest.mock import AsyncMock, MagicMock

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

@pytest.mark.asyncio
async def test_login_invalid_password(user_repository, password_service, user, auth_service, jwt_service, token_service, db_session):
    
    user_repository.find_by_email = AsyncMock(return_value=user)
    password_service.verify_password = MagicMock(return_value=False)
    
    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(user.email, "wrong_password")


    user_repository.find_by_email.assert_awaited_once_with(user.email)
    password_service.verify_password.assert_called_once_with("wrong_password",user.password_hash)
    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()
    token_service.create_session.assert_not_called()
    db_session.commit.assert_not_called()
    db_session.rollback.assert_awaited_once()





@pytest.mark.asyncio
async def test_login_user_not_found(user_repository, user, auth_service, password_service, jwt_service, token_service, db_session):
    
    # Arrange
    user_repository.find_by_email = AsyncMock(return_value=None)

    # Act & Assert
    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(user.email, "password")  

    # Interaction Assertions
    user_repository.find_by_email.assert_awaited_once_with(user.email)
    password_service.verify_password.assert_not_called()
    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()
    token_service.create_session.assert_not_called()
    db_session.commit.assert_not_called()
    db_session.rollback.assert_awaited_once()

 

    

@pytest.mark.asyncio
async def test_refresh_success(db_session, auth_service, jwt_service, token_service, user_session):

    # Arrange

    jwt_service.access_token_expires_in = 1
    refresh_token = "dummy_refresh_token"
    jwt_service.verify_token = MagicMock(return_value = {"type": "refresh"})
    token_service.get_session_by_refresh_token = AsyncMock(return_value = user_session)
    jwt_service.create_access_token = MagicMock(return_value = "new_access_token")
    jwt_service.create_refresh_token = MagicMock(return_value = "new_refresh_token")
    token_service.rotate_refresh_token = MagicMock()    
    
    # Act

    result = await auth_service.refresh(refresh_token)
    # Assert

    assert result.access_token == "new_access_token"
    assert result.refresh_token == "new_refresh_token"
    assert result.token_type == "Bearer"
    assert result.expires_in == jwt_service.access_token_expires_in

    jwt_service.verify_token.assert_called_once_with(refresh_token)
    token_service.get_session_by_refresh_token.assert_awaited_once_with(refresh_token)
    jwt_service.create_access_token.assert_called_once_with(str(user_session.user.id))
    jwt_service.create_refresh_token.assert_called_once_with(str(user_session.user.id))
    token_service.rotate_refresh_token.assert_called_once_with(user_session, "new_refresh_token")
    db_session.commit.assert_awaited_once()



@pytest.mark.asyncio
async def test_refresh_invalid_token_type(jwt_service, auth_service, token_service, db_session):

    # Arrange

    jwt_service.access_token_expires_in = 1
    refresh_token = "dummy_refresh_token"
    jwt_service.verify_token = MagicMock(return_value = {"type": "access"})


    # Act and Assert
    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(refresh_token)


    # Assert

    token_service.get_session_by_refresh_token.assert_not_called()
    jwt_service.verify_token.assert_called_once_with(refresh_token)
    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()
    token_service.rotate_refresh_token.assert_not_called()
    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()



@pytest.mark.asyncio
async def test_refresh_session_not_found(jwt_service, token_service, auth_service, db_session):

    # Arrange

    jwt_service.access_token_expires_in = 1
    refresh_token = "dummy_refresh_token"
    jwt_service.verify_token = MagicMock(return_value = {"type": "refresh"})
    token_service.get_session_by_refresh_token = AsyncMock(return_value = None)

    # Act and Assert

    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(refresh_token)

    # Assert
    
    token_service.get_session_by_refresh_token.assert_awaited_once_with(refresh_token)
    jwt_service.verify_token.assert_called_once_with(refresh_token)
    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()
    token_service.rotate_refresh_token.assert_not_called()
    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()



    

@pytest.mark.asyncio
async def test_refresh_session_revoked(jwt_service, token_service, auth_service, user_session, db_session):
    
    # Arrange

    jwt_service.access_token_expires_in = 1
    refresh_token = "dummy_refresh_token"
    jwt_service.verify_token = MagicMock(return_value = {"type": "refresh"})
    token_service.get_session_by_refresh_token = AsyncMock(return_value = user_session)
    user_session.revoked_at = datetime.datetime.now()

    # Act

    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(refresh_token)
    
    # Assert
    token_service.get_session_by_refresh_token.assert_awaited_once_with(refresh_token)
    jwt_service.verify_token.assert_called_once_with(refresh_token)
    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()
    token_service.rotate_refresh_token.assert_not_called()
    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_refresh_session_expired(jwt_service, token_service, auth_service, user_session, db_session):
    
    # Arrange

    jwt_service.access_token_expires_in = 1
    refresh_token = "dummy_refresh_token"
    jwt_service.verify_token = MagicMock(return_value = {"type": "refresh"})
    token_service.get_session_by_refresh_token = AsyncMock(return_value = user_session)
    user_session.expires_at = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=30)

    # Act

    with pytest.raises(InvalidCredentialsError):
        await auth_service.refresh(refresh_token)
    
    # Assert
    token_service.get_session_by_refresh_token.assert_awaited_once_with(refresh_token)
    jwt_service.verify_token.assert_called_once_with(refresh_token)
    jwt_service.create_access_token.assert_not_called()
    jwt_service.create_refresh_token.assert_not_called()
    token_service.rotate_refresh_token.assert_not_called()
    db_session.commit.assert_not_awaited()
    db_session.rollback.assert_awaited_once()


def test_logout_success():
    ...