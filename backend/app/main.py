import time
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.auth import router as auth_router
from backend.app.api.upload import router as upload_router
from backend.app.api.analysis import router as analysis_router
from backend.app.core.config import settings
from backend.app.core.exception_handlers import register_exception_handlers
from backend.app.core.telemetry import send_telemetry_in_background


app = FastAPI()


cors_origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


register_exception_handlers(app)


@app.middleware("http")
async def telemetry_middleware(request, call_next):
    # CORS preflight requests do not represent actual application traffic.
    # Skip them so they do not pollute request analytics.
    if request.method == "OPTIONS":
        return await call_next(request)

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        # Use FastAPI's route template when available so dynamic paths
        # such as /analyses/<uuid> are grouped as /analyses/{upload_id}.
        route = getattr(
            request.scope.get("route"),
            "path",
            request.url.path,
        )

        response.headers["X-Request-ID"] = request_id

        send_telemetry_in_background(
            route=route,
            method=request.method,
            status=response.status_code,
            duration_ms=round(duration_ms, 2),
            request_id=request_id,
            ip=request.client.host if request.client else None,
            action="request_completed",
        )

        return response

    except Exception:
        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        # Route resolution may not have completed when an exception occurs,
        # so fall back to the raw request path.
        route = getattr(
            request.scope.get("route"),
            "path",
            request.url.path,
        )

        send_telemetry_in_background(
            route=route,
            method=request.method,
            status=500,
            duration_ms=round(duration_ms, 2),
            request_id=request_id,
            ip=request.client.host if request.client else None,
            action="request_failed",
        )

        raise

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(analysis_router)