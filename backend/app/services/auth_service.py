from backend.app.services.exceptions import InvalidCredentialsError
from backend.app.services.jwt_service import JWTService
from backend.app.services.password_service import PasswordService
from backend.app.services.token_service import TokenService
from backend.app.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession



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
    

    async def login(self, email: str, password: str):
        try:
            user = await self._user_repository.find_by_email(email)
            if user is None:
                raise InvalidCredentialsError
            verified_password = self._password_service.verify_password(password, user.password_hash)
            if not verified_password:
                raise InvalidCredentialsError
            access_token = self._jwt_service.create_access_token(str(user.id))
            refresh_token = self._jwt_service.create_refresh_token(str(user.id))            
            await self._token_service.create_session(user, refresh_token)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise 
