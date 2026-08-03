class TokenVerificationError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__(
            "An account with this email already exists."
        )

class SessionNotFoundError(Exception):
    pass

class SessionRevokedError(Exception):
    pass

class SessionExpiredError(Exception):
    pass



class InvalidFileTypeError(Exception):
    pass

class FileTooLargeError(Exception):
    pass


class InvalidTokenTypeError(Exception):
    pass


class UploadNotFoundError(Exception):
    pass


class AnalysisAlreadyExistsError(Exception):
    def __init__(self):
        super().__init__(
            "An analysis already exists for this upload."
            )
        
