from abc import ABC, abstractmethod
from backend.app.ai.schemas import AIResponseSchema


class AIProvider(ABC):

    @abstractmethod
    async def analyze_image(self, image_bytes: bytes,mime_type: str,prompt: str) ->AIResponseSchema:
        pass