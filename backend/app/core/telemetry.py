import asyncio
import time

import httpx

from backend.app.core.config import settings


_background_tasks: set[asyncio.Task] = set()


async def send_request_telemetry(
    *,
    route: str,
    method: str,
    status: int,
    duration_ms: float,
    request_id: str,
    ip: str | None = None,
    user_id: int | None = None,
    action: str = "request_completed",
) -> None:
    payload = {
        "timestamp": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ",
            time.gmtime(),
        ),
        "level": "ERROR" if status >= 500 else "INFO",
        "service": "safestep-api",
        "user_id": user_id,
        "action": action,
        "status": status,
        "ip": ip,
        "route": route,
        "method": method,
        "duration_ms": duration_ms,
        "request_id": request_id,
        "deployment": settings.DEPLOYMENT_ID,
    }

    try:
        async with httpx.AsyncClient(
            timeout=settings.LOG_ANALYTICS_TIMEOUT
        ) as client:
            response = await client.post(
                f"{settings.LOG_ANALYTICS_URL}/logs/structured",
                json=payload,
            )

            response.raise_for_status()

    except Exception as exc:
        # Telemetry failures must never break SafeStep.
        print(f"[telemetry] Failed to send log: {exc}")


def send_telemetry_in_background(**kwargs) -> None:
    task = asyncio.create_task(
        send_request_telemetry(**kwargs)
    )

    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)