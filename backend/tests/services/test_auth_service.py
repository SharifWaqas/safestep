import pytest

from backend.app.services.auth_service import AuthService
from backend.app.services.jwt_service import JWTService
from backend.app.services.password_service import PasswordService
from backend.app.services.token_service import TokenService
from backend.app.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


def test_login_success():
    auth_service = AuthService(AsyncSession, UserRepository, PasswordService, JWTService, TokenService)
    result = auth_service.login("shaarif.1031@gmail.com", "ThiSisSaMplePassWoRds" )
    
    


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