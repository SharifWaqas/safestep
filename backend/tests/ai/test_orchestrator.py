from unittest.mock import AsyncMock, Mock

import pytest

from backend.app.ai.orchestrator import AIOrchestrator
from backend.app.ai.schemas import AIResponseSchema
from backend.app.enums.risk_level import RiskLevel

from decimal import Decimal
from backend.app.enums.risk_factor import RiskFactor
from backend.app.ai.schemas import RiskFactorResult


@pytest.mark.asyncio
async def test_analyze():
    storage_provider = Mock()
    storage_provider.get_image_data = AsyncMock(
        return_value=b"fake-image-bytes"
    )

    openai_client = Mock()
    openai_client.analyze_image = AsyncMock()

    prompt_builder = Mock()
    prompt_builder.build.return_value = "Test prompt"

    expected_result = AIResponseSchema(
        summary="This message appears to be a scam.",
        risk_level=RiskLevel.HIGH,
        description="Test analysis.",
        solution="Do not interact with the message.",
        reassurance="You are safe.",
        risk_factors=[RiskFactorResult(risk_factor=RiskFactor.UNREALISTIC_PRICE,value=Decimal("0.85"),description="The item is being offered at an unusually low price.")]
    )

    openai_client.analyze_image.return_value = expected_result

    orchestrator = AIOrchestrator(
        storage_provider=storage_provider,
        openai_client=openai_client,
        prompt_builder=prompt_builder,
    )

    upload = Mock()
    upload.storage_path = "test/path/image.png"
    upload.mime_type = "image/png"

    result = await orchestrator.analyze(upload)

    assert result == expected_result

    storage_provider.get_image_data.assert_awaited_once_with(
        "test/path/image.png"
    )

    prompt_builder.build.assert_called_once_with()

    openai_client.analyze_image.assert_awaited_once_with(
        image_bytes=b"fake-image-bytes",
        mime_type="image/png",
        prompt="Test prompt",
    )