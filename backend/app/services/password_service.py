

class PasswordService:

    def hash_password(self, password: str) -> str:
        ...
    def verify_password(self, password: str, password_hash: str) -> bool:
        ...

