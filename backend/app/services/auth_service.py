from backend.app.services.exceptions import InvalidCredentialsError
from backend.app.services.jwt_service import JWTService
from backend.app.services.password_service import PasswordService
from backend.app.services.token_service import TokenService
from backend.app.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.auth import LoginResponse, RefreshResponse

import datetime

class AuthService:
    
    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository,
        password_service: PasswordService,
        jwt_service: JWTService,
        token_service: TokenService,
    ) -> None:
        self._session = session
        self._user_repository = user_repository
        self._password_service = password_service
        self._jwt_service = jwt_service
        self._token_service = token_service
    

    async def login(self, email: str, password: str) -> LoginResponse:
        try:
            user = await self._user_repository.find_by_email(email)
            if user is None:
                raise InvalidCredentialsError
            if not self._password_service.verify_password(password, user.password_hash):
                raise InvalidCredentialsError
            user_access_token = self._jwt_service.create_access_token(str(user.id))
            user_refresh_token = self._jwt_service.create_refresh_token(str(user.id))            
            await self._token_service.create_session(user, user_refresh_token)
            await self._session.commit()
            return LoginResponse(
                access_token=user_access_token,
                refresh_token=user_refresh_token,
                token_type="Bearer",
                expires_in=self._jwt_service.access_token_expires_in,)       
        except Exception:
            await self._session.rollback()
            raise 
    

    async def refresh(self, refresh_token : str) -> RefreshResponse:
        try:
            claims = self._jwt_service.verify_token(refresh_token)    
            if claims["type"] != "refresh":
                raise InvalidCredentialsError
            session = await self._token_service.get_session_by_refresh_token(refresh_token)

            if session is None:
                raise InvalidCredentialsError

            if session.revoked_at is not None:
                raise InvalidCredentialsError

            if session.expires_at < datetime.datetime.now(datetime.UTC):
                raise InvalidCredentialsError
            
            user = session.user

            if user is None:
                raise InvalidCredentialsError
            
            new_access_token = self._jwt_service.create_access_token(str(user.id))
            new_refresh_token = self._jwt_service.create_refresh_token(str(user.id))
            self._token_service.rotate_refresh_token(session, new_refresh_token)
            await self._session.commit()
            return RefreshResponse(
                access_token = new_access_token,
                refresh_token = new_refresh_token,
                token_type= "Bearer",
                expires_in = self._jwt_service.access_token_expires_in ,
            )
        except Exception:
            await self._session.rollback()
            raise