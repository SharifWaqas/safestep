from backend.app.services.exceptions import InvalidCredentialsError, EmailAlreadyExistsError
from backend.app.services.jwt_service import JWTService
from backend.app.services.password_service import PasswordService
from backend.app.services.token_service import TokenService
from backend.app.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.auth import LoginResponse, RefreshResponse, LogoutResponse, RegisterRequest, RegisterResponse
from backend.app.models.user import User

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

    async def _issue_tokens(self, user : User)-> tuple[str, str]:
        access_token = self._jwt_service.create_access_token(str(user.id))
        refresh_token = self._jwt_service.create_refresh_token(str(user.id))            
        await self._token_service.create_session(user, refresh_token)

        return access_token, refresh_token 

    async def register(self, request: RegisterRequest) -> RegisterResponse:
        try:
            email = request.email
            user = await self._user_repository.find_by_email(email)
            if user is not None:
                raise EmailAlreadyExistsError()

            password = request.password
            hashed_password = self._password_service.hash_password(password)
            new_user = User(email=email, password_hash=hashed_password,full_name=request.full_name, is_verified=False, is_active=True)
            await self._user_repository.create(new_user)
            await self._session.flush()
            access_token, refresh_token = await self._issue_tokens(new_user)
            await self._session.commit()
            return RegisterResponse(access_token=access_token,refresh_token=refresh_token,token_type="Bearer",expires_in=self._jwt_service.access_token_expires_in,)
        except Exception:
            await self._session.rollback()
            raise

            
    async def login(self, email: str, password: str) -> LoginResponse:
        try:
            user = await self._user_repository.find_by_email(email)
            if user is None:
                raise InvalidCredentialsError
            if not self._password_service.verify_password(password, user.password_hash):
                raise InvalidCredentialsError
            access_token, refresh_token = await self._issue_tokens(user)
            return LoginResponse(
                access_token=access_token,
                refresh_token=refresh_token,
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
    
    async def logout(self, refresh_token: str) -> LogoutResponse:
        try:
            claims = self._jwt_service.verify_token(refresh_token)

            if claims["type"] != "refresh":
                raise InvalidCredentialsError
            
            session = await self._token_service.get_session_by_refresh_token(refresh_token)
            
            if session is None:
                raise InvalidCredentialsError
    
            self._token_service.revoke_session(session)
            await self._session.commit()
            return LogoutResponse(
                message="You have been successfully logged out"
            )
        except Exception:
            await self._session.rollback()
            raise
