from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.services.exceptions import (
    AnalysisAlreadyExistsError,
    AnalysisNotFoundError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    SessionExpiredError,
    SessionNotFoundError,
    SessionRevokedError,
    TokenVerificationError,
    UploadNotFoundError,
)


def handle_invalid_credentials_error(
    _request: Request,
    _exception: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "detail": "Invalid email or password. Please check your credentials and try again."
        },
    )


def handle_authentication_error(
    _request: Request,
    _exception: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "Authentication failed."},
    )


def handle_conflict_error(
    _request: Request,
    exception: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exception)},
    )


def handle_not_found_error(
    _request: Request,
    exception: Exception,
) -> JSONResponse:
    message = (
        str(exception).strip()
        or "The requested resource was not found."
    )

    return JSONResponse(
        status_code=404,
        content={"detail": message},
    )


def register_exception_handlers(app: FastAPI) -> None:
    authentication_exceptions = (
        TokenVerificationError,
        SessionNotFoundError,
        SessionRevokedError,
        SessionExpiredError,
    )

    conflict_exceptions = (
        EmailAlreadyExistsError,
        AnalysisAlreadyExistsError,
    )

    not_found_exceptions = (
        UploadNotFoundError,
        AnalysisNotFoundError,
    )

    app.add_exception_handler(
        InvalidCredentialsError,
        handle_invalid_credentials_error,
    )

    for exception_type in authentication_exceptions:
        app.add_exception_handler(
            exception_type,
            handle_authentication_error,
        )

    for exception_type in conflict_exceptions:
        app.add_exception_handler(
            exception_type,
            handle_conflict_error,
        )

    for exception_type in not_found_exceptions:
        app.add_exception_handler(
            exception_type,
            handle_not_found_error,
        )