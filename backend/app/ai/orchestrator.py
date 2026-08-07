from backend.app.ai.dto import AnalysisResultDTO
from backend.app.ai.openai_client import OpenAIClient
from backend.app.ai.parser import AIResponseParser
from backend.app.ai.storage import StorageProvider
from backend.app.models.analysis import Analysis
from backend.app.models.upload import Upload


class AIOrchestrator:
    def __init__(
        self,
        storage_provider: StorageProvider,
        openai_client: OpenAIClient,
        parser: AIResponseParser,
    ):
        self._storage_provider = storage_provider
        self._openai_client = openai_client
        self._parser = parser

    async def analyze(
        self,
        upload: Upload,
        analysis: Analysis,
    ) -> AnalysisResultDTO:
        file_path = await self._storage_provider.get_file_path(upload)

        raw_response = await self._openai_client.analyze_image(
            file_path=file_path,
        )

        result = self._parser.parse(raw_response)

        return result