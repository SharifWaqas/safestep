class TokenVerificationError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class SessionNotFoundError(Exception):
    pass

class SessionRevokedError(Exception):
    pass

class SessionExpiredError(Exception):
    pass