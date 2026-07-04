class JWTService:

    def generate_access_token(self, user_id: str) -> str:
        ...

    def verify_access_token(self, token: str) -> dict:
        ...