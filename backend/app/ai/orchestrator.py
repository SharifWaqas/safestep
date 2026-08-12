from backend.app.ai.providers.openai_client import OpenAIClient
from backend.app.ai.prompts import PromptBuilder
from backend.app.ai.storage import StorageProvider
from backend.app.models.upload import Upload


class AIOrchestrator:
    def __init__(
        self,
        storage_provider: StorageProvider,
        openai_client: OpenAIClient,
        prompt_builder: PromptBuilder,
    ):
        self._storage_provider = storage_provider
        self._openai_client = openai_client
        self._prompt_builder = prompt_builder

    async def analyze(self, upload: Upload):
        image_bytes = await self._storage_provider.get_image_data(
            upload.storage_path
        )

        prompt = self._prompt_builder.build()

        result = await self._openai_client.analyze_image(
            image_bytes=image_bytes,
            mime_type=upload.mime_type,
            prompt=prompt,
        )

        return result