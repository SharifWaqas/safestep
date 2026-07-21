from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from backend.app.database.session import SessionFactory
from backend.app.services.auth_service import AuthService
from backend.app.services.password_service import PasswordService
from backend.app.services.jwt_service import JWTService
from backend.app.services.token_service import TokenService
from backend.app.repositories.session_repository import SessionRepository
from backend.app.repositories.user_repository import UserRepository

async def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        await session.close()


async def get_auth_service(session: AsyncSession = Depends(get_db),) -> AuthService :

    password_service = PasswordService()
    jwt_service = JWTService()
    session_repository = SessionRepository(session)
    token_service = TokenService(session_repository, jwt_service)
    user_repository = UserRepository(session)

    return (AuthService(session, user_repository, password_service, jwt_service, token_service))
