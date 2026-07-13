import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timedelta, UTC

from backend.app.models.session import Session
from backend.app.models.user import User
from backend.app.services.auth_service import AuthService

@pytest.fixture
def db_session():
    return AsyncMock()

@pytest.fixture
def user_repository():
    return MagicMock()

@pytest.fixture
def token_service():
    return MagicMock()

@pytest.fixture
def password_service():
    return MagicMock()

@pytest.fixture
def jwt_service():
    return MagicMock()

@pytest.fixture
def user():
    return User(
        email="test@example.com",
        password_hash="hashed_password",
        first_name="John",
        last_name="Doe",
        is_verified=True,
        is_active=True,
    )

@pytest.fixture
def user_session(user):
    return Session(
        user=user,
        refresh_token_hash="hashed_refresh_token",
        ip_address="127.0.0.1",
        device_info="pytest",
        expires_at=datetime.now(UTC) + timedelta(days=30),
        revoked_at=None,
    )

@pytest.fixture
def auth_service(
    db_session,
    user_repository,
    password_service,
    jwt_service,
    token_service,
):
    return AuthService(
        session=db_session,
        user_repository=user_repository,
        password_service=password_service,
        jwt_service=jwt_service,
        token_service=token_service,
    )