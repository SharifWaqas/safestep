import base64
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from backend.app.ai.openai_client import OpenAIClient
from backend.app.ai.schemas import AIResponseSchema
from backend.app.enums.risk_level import RiskLevel

@pytest.mark.asyncio
async def test_analyze_image():
    image_path = Path("backend/tests/fixtures/test_screenshot.png")
    image_bytes = image_path.read_bytes()

    client = OpenAIClient(
        api_key="test-api-key",
        model="test-model",
    )

    expected_result = AIResponseSchema(
        summary="This message appears to be a scam.",
        risk_level=RiskLevel.HIGH,
        description="Test analysis.",
        solution="Do not interact with the message.",
        reassurance="You are safe.",
    )
    client._client.responses.parse = AsyncMock(
        return_value=type(
            "MockResponse",
            (),
            {"output_parsed": expected_result},
        )()
    )

    result = await client.analyze_image(
        image_bytes=image_bytes,
        mime_type="image/png",
        prompt="Test prompt",
    )

    assert result == expected_result

    client._client.responses.parse.assert_awaited_once()

    call_kwargs = client._client.responses.parse.call_args.kwargs

    assert call_kwargs["model"] == "test-model"
    assert call_kwargs["text_format"] is AIResponseSchema

    image_url = call_kwargs["input"][0]["content"][1]["image_url"]

    expected_base64 = base64.b64encode(image_bytes).decode("utf-8")

    assert image_url == f"data:image/png;base64,{expected_base64}"