import hashlib

from datetime import UTC, datetime

from backend.app.models.session import Session
from backend.app.repositories.session_repository import SessionRepository
from backend.app.services.jwt_service import JWTService
from backend.app.models.user import User


class TokenService:

    def __init__(self, session_repository: SessionRepository, jwt_service: JWTService) -> None:
        self._session_repository = session_repository
        self._jwt_service = jwt_service
    
    def _hash_refresh_token(self, refresh_token: str) -> str:
        return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


    async def create_session(self, user: User, refresh_token: str) -> None:
        payload = self._jwt_service.verify_token(refresh_token)

        expires_at = datetime.fromtimestamp(payload["exp"], UTC)        
        
        refresh_token_hash = self._hash_refresh_token(refresh_token)
        
        session = Session(
            user_id=user.id,
            refresh_token_hash=refresh_token_hash,
            expires_at=expires_at
            )
            
        await self._session_repository.save(session)

    
    async def get_session_by_refresh_token(self,refresh_token: str) -> Session | None :
        refresh_token_hash = self._hash_refresh_token(refresh_token)
        result = await self._session_repository.find_by_refresh_token_hash(
            refresh_token_hash
        )
        return result


    async def revoke_session(self, session: Session) -> None:
        if session.revoked_at is not None:
            return

        session.revoked_at = datetime.now(UTC)

        await self._session_repository.save(session)
