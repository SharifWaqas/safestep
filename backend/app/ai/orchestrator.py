import time

from backend.app.ai.providers.base import AIProvider, AIProviderError
from backend.app.ai.schemas import AIResponseSchema
from backend.app.core.telemetry import send_telemetry_in_background


class AIOrchestrator:
    def __init__(
        self,
        primary_provider: AIProvider,
        fallback_provider: AIProvider,
    ):
        self._primary_provider = primary_provider
        self._fallback_provider = fallback_provider

    async def analyze_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
        *,
        analysis_id: str | None = None,
        user_id: int | None = None,
        request_id: str = "unknown",
    ) -> AIResponseSchema:

        primary_start = time.perf_counter()

        try:
            result = await self._primary_provider.analyze_image(
                image_bytes=image_bytes,
                mime_type=mime_type,
                prompt=prompt,
            )

            primary_duration_ms = (
                time.perf_counter() - primary_start
            ) * 1000

            send_telemetry_in_background(
                route="/analyses/{upload_id}",
                method="POST",
                status=200,
                duration_ms=round(primary_duration_ms, 2),
                request_id=request_id,
                action="ai_openai_completed",
            )

            return result

        except AIProviderError:
            primary_duration_ms = (
                time.perf_counter() - primary_start
            ) * 1000

            send_telemetry_in_background(
                route="/analyses/{upload_id}",
                method="POST",
                status=200,
                duration_ms=round(primary_duration_ms, 2),
                request_id=request_id,
                action="ai_openai_failed",
            )

            fallback_start = time.perf_counter()

            try:
                result = await self._fallback_provider.analyze_image(
                    image_bytes=image_bytes,
                    mime_type=mime_type,
                    prompt=prompt,
                )

                fallback_duration_ms = (
                    time.perf_counter() - fallback_start
                ) * 1000

                send_telemetry_in_background(
                    route="/analyses/{upload_id}",
                    method="POST",
                    status=200,
                    duration_ms=round(fallback_duration_ms, 2),
                    request_id=request_id,
                    action="ai_nvidia_completed",
                )

                return result

            except AIProviderError:
                fallback_duration_ms = (
                    time.perf_counter() - fallback_start
                ) * 1000

                send_telemetry_in_background(
                    route="/analyses/{upload_id}",
                    method="POST",
                    status=200,
                    duration_ms=round(fallback_duration_ms, 2),
                    request_id=request_id,
                    action="ai_nvidia_failed",
                )

                raise