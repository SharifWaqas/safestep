from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from backend.app.database.session import SessionFactory
from backend.app.services.auth_service import AuthService
from backend.app.services.password_service import PasswordService
from backend.app.services.jwt_service import JWTService
from backend.app.services.token_service import TokenService
from backend.app.repositories.session_repository import SessionRepository
from backend.app.repositories.user_repository import UserRepository
from backend.app.repositories.upload_repository import UploadRepository

from backend.app.services.upload_service import UploadService
from backend.app.services.storage_service import StorageService

from backend.app.core.config import settings
from pathlib import Path


async def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        await session.close()

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


