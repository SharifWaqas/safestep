from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from backend.app.ai.orchestrator import AIOrchestrator
from backend.app.ai.providers.base import AIProviderError
from backend.app.ai.schemas import AIResponseSchema, RiskFactorResult
from backend.app.enums.risk_factor import RiskFactor
from backend.app.enums.risk_level import RiskLevel


def create_response() -> AIResponseSchema:
    return AIResponseSchema(
        summary="This message appears to be a scam.",
        risk_level=RiskLevel.HIGH,
        description="Test analysis.",
        solution="Do not interact with the message.",
        reassurance="You are safe.",
        risk_factors=[
            RiskFactorResult(
                risk_factor=RiskFactor.UNREALISTIC_PRICE,
                value=Decimal("0.85"),
                description=(
                    "The item is being offered at an unusually "
                    "low price."
                ),
            )
        ],
    )


@pytest.mark.asyncio
async def test_primary_provider_success():
    primary_provider = AsyncMock()
    fallback_provider = AsyncMock()

    expected_result = create_response()

    primary_provider.analyze_image.return_value = expected_result

    orchestrator = AIOrchestrator(
        primary_provider=primary_provider,
        fallback_provider=fallback_provider,
    )

    result = await orchestrator.analyze_image(
        image_bytes=b"fake-image-bytes",
        mime_type="image/png",
        prompt="Test prompt",
    )

    assert result == expected_result

    primary_provider.analyze_image.assert_awaited_once_with(
        image_bytes=b"fake-image-bytes",
        mime_type="image/png",
        prompt="Test prompt",
    )

    fallback_provider.analyze_image.assert_not_awaited()


@pytest.mark.asyncio
async def test_primary_provider_failure_uses_fallback():
    primary_provider = AsyncMock()
    fallback_provider = AsyncMock()

    expected_result = create_response()

    primary_provider.analyze_image.side_effect = AIProviderError(
        "Primary provider failed"
    )

    fallback_provider.analyze_image.return_value = expected_result

    orchestrator = AIOrchestrator(
        primary_provider=primary_provider,
        fallback_provider=fallback_provider,
    )

    result = await orchestrator.analyze_image(
        image_bytes=b"fake-image-bytes",
        mime_type="image/png",
        prompt="Test prompt",
    )

    assert result == expected_result

    primary_provider.analyze_image.assert_awaited_once_with(
        image_bytes=b"fake-image-bytes",
        mime_type="image/png",
        prompt="Test prompt",
    )

    fallback_provider.analyze_image.assert_awaited_once_with(
        image_bytes=b"fake-image-bytes",
        mime_type="image/png",
        prompt="Test prompt",
    )


@pytest.mark.asyncio
async def test_fallback_failure_propagates_error():
    primary_provider = AsyncMock()
    fallback_provider = AsyncMock()

    primary_provider.analyze_image.side_effect = AIProviderError(
        "Primary provider failed"
    )

    fallback_error = AIProviderError(
        "Fallback provider failed"
    )

    fallback_provider.analyze_image.side_effect = fallback_error

    orchestrator = AIOrchestrator(
        primary_provider=primary_provider,
        fallback_provider=fallback_provider,
    )

    with pytest.raises(AIProviderError, match="Fallback provider failed"):
        await orchestrator.analyze_image(
            image_bytes=b"fake-image-bytes",
            mime_type="image/png",
            prompt="Test prompt",
        )

    primary_provider.analyze_image.assert_awaited_once()

    fallback_provider.analyze_image.assert_awaited_once()