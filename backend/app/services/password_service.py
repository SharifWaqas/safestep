
from pwdlib import PasswordHash

class PasswordService:

    def __init__(self):
        self._password_hasher = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self._password_hasher.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return self._password_hasher.verify(password, password_hash)

