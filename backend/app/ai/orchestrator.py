from backend.app.ai.providers.base import AIProvider, AIProviderError
from backend.app.ai.schemas import AIResponseSchema


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
    ) -> AIResponseSchema:

        try:
            return await self._primary_provider.analyze_image(
                image_bytes=image_bytes,
                mime_type=mime_type,
                prompt=prompt,
            )

        except AIProviderError:
            return await self._fallback_provider.analyze_image(
                image_bytes=image_bytes,
                mime_type=mime_type,
                prompt=prompt,
            )