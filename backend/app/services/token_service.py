from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repositories.session_repository import SessionRepository
from backend.app.services.jwt_service import JWTService


class TokenService:

    def __init__(self,db: AsyncSession, session_repository: SessionRepository, jwt_service: JWTService) -> None:
        self._db = db
        self._session_repository = session_repository
        self._jwt_service = jwt_service
    