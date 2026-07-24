from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from backend.app.services.exceptions import InvalidCredentialsError, TokenVerificationError, SessionNotFoundError, SessionRevokedError, SessionExpiredError, EmailAlreadyExistsError

def handle_authentication_error(_request: Request , _exception: Exception)-> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": "Authentication failed."})


def handle_conflict_error(_request: Request, exception: Exception)-> JSONResponse:
    return JSONResponse(status_code=409,content={"detail": str(exception)})


def register_exception_handlers(app: FastAPI) -> None:
    authentication_exceptions = (InvalidCredentialsError, TokenVerificationError, SessionNotFoundError, SessionRevokedError, SessionExpiredError)
    conflict_exceptions = (EmailAlreadyExistsError,)
    for exception_type in authentication_exceptions:
        app.add_exception_handler(exception_type, handle_authentication_error)

    for exception_type in conflict_exceptions:
        app.add_exception_handler(exception_type,handle_conflict_error)