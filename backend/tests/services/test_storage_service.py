from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.app.services.storage_service import StorageService


@pytest.fixture
def upload_directory(tmp_path):
    return tmp_path / "uploads"


@pytest.fixture
def storage_service(upload_directory):
    return StorageService(upload_directory)


@pytest.mark.asyncio
async def test_save_file_saves_file_and_returns_storage_result(
    storage_service,
    upload_directory,
):
    file = MagicMock()
    file.filename = "test_image.jpg"
    file.content_type = "image/jpeg"
    file.read = AsyncMock(return_value=b"test image data")

    result = await storage_service.save_file(file)

    assert result.storage_path == str(upload_directory / result.file_name)
    assert result.file_name.endswith(".jpg")
    assert result.file_size == len(b"test image data")
    assert result.content_type == "image/jpeg"

    stored_file = Path(result.storage_path)

    assert stored_file.exists()
    assert stored_file.read_bytes() == b"test image data"


@pytest.mark.asyncio
async def test_save_file_reads_uploaded_file(
    storage_service,
):
    file = MagicMock()
    file.filename = "document.pdf"
    file.content_type = "application/pdf"
    file.read = AsyncMock(return_value=b"pdf data")

    await storage_service.save_file(file)

    file.read.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_file_preserves_file_extension(
    storage_service,
):
    file = MagicMock()
    file.filename = "photo.png"
    file.content_type = "image/png"
    file.read = AsyncMock(return_value=b"png data")

    result = await storage_service.save_file(file)

    assert result.file_name.endswith(".png")


@pytest.mark.asyncio
async def test_get_file_returns_file_contents(
    storage_service,
    tmp_path,
):
    file_path = tmp_path / "test_file.txt"
    expected_data = b"hello SafeStep"

    file_path.write_bytes(expected_data)

    result = await storage_service.get_file(str(file_path))

    assert result == expected_data


@pytest.mark.asyncio
async def test_delete_file_deletes_existing_file(
    storage_service,
    tmp_path,
):
    file_path = tmp_path / "test_file.txt"
    file_path.write_bytes(b"delete me")

    assert file_path.exists()

    await storage_service.delete_file(str(file_path))

    assert not file_path.exists()


@pytest.mark.asyncio
async def test_delete_file_does_nothing_when_file_does_not_exist(
    storage_service,
    tmp_path,
):
    file_path = tmp_path / "does_not_exist.txt"

    assert not file_path.exists()

    await storage_service.delete_file(str(file_path))

    assert not file_path.exists()

