from abc import ABC, abstractmethod

from backend.app.ai.schemas import AIResponseSchema


class AIProviderError(Exception):
    """Raised when an AI provider cannot complete an analysis."""

class AIProvider(ABC):

    @abstractmethod
    async def analyze_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> AIResponseSchema:
        pass