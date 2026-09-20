from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.core.exception_handlers import register_exception_handlers
from backend.app.services.exceptions import (
    AnalysisNotFoundError,
    InvalidCredentialsError,
    UploadNotFoundError,
)


def create_test_app() -> FastAPI:
    app = FastAPI()

    register_exception_handlers(app)

    @app.get("/analysis-missing")
    async def analysis_missing():
        raise AnalysisNotFoundError()

    @app.get("/upload-missing")
    async def upload_missing():
        raise UploadNotFoundError()

    @app.get("/invalid-credentials")
    async def invalid_credentials():
        raise InvalidCredentialsError()

    return app


def test_analysis_not_found_returns_404():
    client = TestClient(create_test_app())

    response = client.get("/analysis-missing")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The requested resource was not found."
    }


def test_upload_not_found_returns_404():
    client = TestClient(create_test_app())

    response = client.get("/upload-missing")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "The requested resource was not found."
    }


def test_invalid_credentials_returns_specific_401():
    client = TestClient(create_test_app())

    response = client.get("/invalid-credentials")

    assert response.status_code == 401
    assert response.json() == {
        "detail": (
            "Invalid email or password. "
            "Please check your credentials and try again."
        )
    }