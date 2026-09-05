from io import BytesIO
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from backend.app.services.storage_service import StorageService


@pytest.fixture
def r2_client():
    return MagicMock()


@pytest.fixture
def storage_service(r2_client):
    with patch(
        "backend.app.services.storage_service.boto3.client",
        return_value=r2_client,
    ):
        service = StorageService(
            account_id="test-account-id",
            access_key_id="test-access-key",
            secret_access_key="test-secret-key",
            bucket_name="safestep-uploads",
        )

    return service


@pytest.mark.asyncio
async def test_save_file_uploads_file_to_r2(
    storage_service,
    r2_client,
):
    file = MagicMock()
    file.filename = "test_image.jpg"
    file.content_type = "image/jpeg"
    file.read = AsyncMock(return_value=b"test image data")

    result = await storage_service.save_file(file)

    file.read.assert_awaited_once()

    r2_client.put_object.assert_called_once()

    call_kwargs = r2_client.put_object.call_args.kwargs

    assert call_kwargs["Bucket"] == "safestep-uploads"
    assert call_kwargs["Key"] == result.storage_path
    assert call_kwargs["ContentType"] == "image/jpeg"

    body = call_kwargs["Body"]

    assert isinstance(body, BytesIO)
    assert body.read() == b"test image data"

    assert result.file_name.endswith(".jpg")
    assert result.file_size == len(b"test image data")
    assert result.content_type == "image/jpeg"
    assert result.storage_path == result.file_name


@pytest.mark.asyncio
async def test_save_file_preserves_file_extension(
    storage_service,
    r2_client,
):
    file = MagicMock()
    file.filename = "photo.png"
    file.content_type = "image/png"
    file.read = AsyncMock(return_value=b"png data")

    result = await storage_service.save_file(file)

    assert result.file_name.endswith(".png")

    r2_client.put_object.assert_called_once()


@pytest.mark.asyncio
async def test_get_file_returns_file_contents(
    storage_service,
    r2_client,
):
    body = MagicMock()
    body.read = MagicMock(return_value=b"hello SafeStep")

    r2_client.get_object.return_value = {
        "Body": body,
    }

    result = await storage_service.get_file(
        "test-file.jpg"
    )

    r2_client.get_object.assert_called_once_with(
        Bucket="safestep-uploads",
        Key="test-file.jpg",
    )

    body.read.assert_called_once()

    assert result == b"hello SafeStep"


@pytest.mark.asyncio
async def test_delete_file_deletes_object_from_r2(
    storage_service,
    r2_client,
):
    await storage_service.delete_file(
        "test-file.jpg"
    )

    r2_client.delete_object.assert_called_once_with(
        Bucket="safestep-uploads",
        Key="test-file.jpg",
    )