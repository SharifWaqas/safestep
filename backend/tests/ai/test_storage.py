from pathlib import Path

import pytest

from backend.app.ai.local_storage import LocalStorageProvider


@pytest.mark.asyncio
async def test_get_image_data():
    image_path = Path("backend/tests/fixtures/test_screenshot.png")
    storage = LocalStorageProvider()

    image_bytes = await storage.get_image_data(str(image_path))

    assert isinstance(image_bytes, bytes)
    assert len(image_bytes) > 0