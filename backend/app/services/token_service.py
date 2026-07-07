from app.services.jwt_service import JWTService


class TokenService:
    """
    Manages the lifecycle of authenticated user sessions.

    Responsibilities:
    - Create authenticated sessions
    - Revoke sessions
    - Validate active sessions
    """

    def __init__(self, jwt_service: JWTService) -> None:
        self._jwt_service = jwt_service