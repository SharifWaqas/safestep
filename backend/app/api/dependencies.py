from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


from backend.app.database.session import SessionFactory

from backend.app.services.auth_service import AuthService
from backend.app.services.password_service import PasswordService
from backend.app.services.jwt_service import JWTService
from backend.app.services.token_service import TokenService

from backend.app.repositories.session_repository import SessionRepository
from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.upload_repository import UploadRepository
from backend.app.repositories.user_repository import UserRepository

from backend.app.models.user import User

from backend.app.services.upload_service import UploadService
from backend.app.services.storage_service import StorageService

from backend.app.core.config import settings
from pathlib import Path

from backend.app.services.exceptions import InvalidTokenTypeError, InvalidCredentialsError

async def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        await session.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_upload_directory():
    return Path(settings.UPLOAD_DIRECTORY)


async def get_auth_service(session: AsyncSession = Depends(get_db)) -> AuthService :

    password_service = PasswordService()
    jwt_service = JWTService()
    session_repository = SessionRepository(session)
    token_service = TokenService(session_repository, jwt_service)
    user_repository = UserRepository(session)

    return (AuthService(session, user_repository, password_service, jwt_service, token_service))

async def get_upload_service(session: AsyncSession = Depends(get_db), upload_directory: Path = Depends(get_upload_directory)) -> UploadService:
    upload_repository = UploadRepository(session)
    storage_service = StorageService(upload_directory)

    return UploadService(session, upload_repository, storage_service)


async def get_current_user(token: str = Depends(oauth2_scheme), db_session: AsyncSession = Depends(get_db)) -> User:
    jwt_service = JWTService()

    payload = jwt_service.verify_token(token)

    if payload["type"] != "access":
        raise InvalidTokenTypeError()
    user_id = payload["sub"]
    user_repository = UserRepository(db_session)
    user = await user_repository.get_by_id(user_id)
    if user is None:
        raise InvalidCredentialsError()
    return user
    

