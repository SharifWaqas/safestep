from app.ai.dto import AnalysisResultDTO
from app.ai.orchestrator import AIOrchestrator
from app.models.analysis import Analysis
from app.models.upload import Upload


class AIService:

    def __init__(self, orchestrator: AIOrchestrator):
        self._orchestrator = orchestrator

    async def analyze(
        self,
        upload: Upload,
        analysis: Analysis,
    ) -> AnalysisResultDTO:
        """
        Analyze an uploaded image and return the structured AI result.
        """

        return await self._orchestrator.analyze(
            upload=upload,
            analysis=analysis,
        )