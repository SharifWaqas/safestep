import jwt
from datetime import datetime, timedelta, timezone
from backend.app.core.config import settings
from backend.app.services.exceptions import TokenVerificationError


class JWTService:

    def __init__(self):
        self._jwt_secret = settings.JWT_SECRET
        self._jwt_algorithm = settings.JWT_ALGORITHM
        self._access_token_expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_token_expires_days = settings.REFRESH_TOKEN_EXPIRE_DAYS

    def create_access_token(self, user_id: str) -> str:
        current_time = datetime.now(timezone.utc)
        expiration_time = current_time + timedelta(minutes=self._access_token_expires_minutes)
        return jwt.encode(
            payload={
                "sub": user_id, 
                "type": "access",
                "iat": current_time,
                "exp": expiration_time,
                    },
            key=self._jwt_secret,
            algorithm=self._jwt_algorithm,
        )

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, 
                key=self._jwt_secret, 
               algorithms=[self._jwt_algorithm,],
                )
        except jwt.InvalidTokenError as e:
            raise TokenVerificationError() from e  

  
    def create_refresh_token(self, user_id: str) -> str:
        current_time = datetime.now(timezone.utc)
        expiration_time = current_time + timedelta(days=self._refresh_token_expires_days)
        return jwt.encode(
            payload={"sub": user_id, 
                    "type": "refresh",
                    "iat": current_time,
                    "exp": expiration_time,
                    },
            key=self._jwt_secret,
            algorithm=self._jwt_algorithm,
        )

    @property
    def access_token_expires_in(self) -> int:
        return self._access_token_expires_minutes * 60