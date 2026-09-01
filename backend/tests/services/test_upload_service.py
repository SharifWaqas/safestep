from datetime import UTC, datetime
from io import BytesIO
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest
from fastapi import UploadFile

from backend.app.models.upload import Upload
from backend.app.models.user import User
from backend.app.schemas.upload import StorageResult
from backend.app.services.exceptions import (
    FileTooLargeError,
    InvalidFileTypeError,
    UploadNotFoundError,
)
from backend.app.services.upload_service import UploadService


@pytest.fixture
def db_session():
    session = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.fixture
def upload_repository():
    repository = MagicMock()
    repository.save = AsyncMock()
    repository.get_by_id_and_user = AsyncMock()
    repository.delete = AsyncMock()
    repository.list_uploads = AsyncMock()
    return repository


@pytest.fixture
def storage_service():
    storage = MagicMock()
    storage.save_file = AsyncMock()
    storage.delete_file = AsyncMock()
    storage.get_file = AsyncMock()
    return storage


@pytest.fixture
def upload_service(
    db_session,
    upload_repository,
    storage_service,
):
    return UploadService(
        session=db_session,
        upload_repository=upload_repository,
        storage_service=storage_service,
    )


@pytest.fixture
def user():
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="John Doe",
    )
    user.id = uuid4()
    return user


def create_upload_file(
    filename="test.jpg",
    content_type="image/jpeg",
    content=b"test image data",
):
    file = UploadFile(
        filename=filename,
        file=BytesIO(content),
    )
    file.headers = {
        "content-type": content_type,
    }
    return file


@pytest.mark.asyncio
async def test_upload_file_creates_upload_and_commits(
    upload_service,
    db_session,
    upload_repository,
    storage_service,
    user,
):
    file = create_upload_file()

    storage_result = StorageResult(
        storage_path="uploads/test-id.jpg",
        file_name="test-id.jpg",
        file_size=15,
        content_type="image/jpeg",
    )

    storage_service.save_file.return_value = storage_result

    await upload_service.upload_file(
        user=user,
        file=file,
    )

    storage_service.save_file.assert_awaited_once_with(file)

    upload_repository.save.assert_awaited_once()

    saved_upload = upload_repository.save.await_args.args[0]

    assert isinstance(saved_upload, Upload)
    assert saved_upload.user_id == user.id
    assert saved_upload.storage_path == storage_result.storage_path
    assert saved_upload.file_name == storage_result.file_name
    assert saved_upload.file_size == storage_result.file_size
    assert saved_upload.content_type == storage_result.content_type

    db_session.commit.assert_awaited_once()
    db_session.refresh.assert_awaited_once_with(saved_upload)


@pytest.mark.asyncio
async def test_upload_file_returns_upload_response(
    upload_service,
    db_session,
    upload_repository,
    storage_service,
    user,
):
    file = create_upload_file()

    storage_service.save_file.return_value = StorageResult(
        storage_path="uploads/test-id.jpg",
        file_name="test-id.jpg",
        file_size=15,
        content_type="image/jpeg",
    )

    saved_upload_id = uuid4()

    async def refresh_upload(upload):
        upload.id = saved_upload_id

    db_session.refresh.side_effect = refresh_upload

    result = await upload_service.upload_file(
        user=user,
        file=file,
    )

    assert result.upload_id == saved_upload_id
    assert result.message == "File has been successfully uploaded."


@pytest.mark.asyncio
async def test_upload_file_rejects_invalid_content_type(
    upload_service,
):
    file = create_upload_file(
        filename="malicious.exe",
        content_type="application/octet-stream",
        content=b"malicious data",
    )

    with pytest.raises(InvalidFileTypeError):
        await upload_service.upload_file(
            user=MagicMock(),
            file=file,
        )


@pytest.mark.asyncio
async def test_upload_file_rejects_oversized_file(
    upload_service,
    monkeypatch,
):
    from backend.app.services import upload_service as upload_service_module

    monkeypatch.setattr(
        upload_service_module.settings,
        "MAX_UPLOAD_SIZE",
        5,
    )

    file = create_upload_file(
        filename="large.jpg",
        content_type="image/jpeg",
        content=b"this is larger than five bytes",
    )

    with pytest.raises(FileTooLargeError):
        await upload_service.upload_file(
            user=MagicMock(),
            file=file,
        )


@pytest.mark.asyncio
async def test_upload_file_rolls_back_and_deletes_storage_on_failure(
    upload_service,
    db_session,
    upload_repository,
    storage_service,
    user,
):
    file = create_upload_file()

    storage_result = StorageResult(
        storage_path="uploads/test-id.jpg",
        file_name="test-id.jpg",
        file_size=15,
        content_type="image/jpeg",
    )

    storage_service.save_file.return_value = storage_result

    upload_repository.save.side_effect = RuntimeError(
        "database failure"
    )

    with pytest.raises(RuntimeError, match="database failure"):
        await upload_service.upload_file(
            user=user,
            file=file,
        )

    db_session.rollback.assert_awaited_once()

    storage_service.delete_file.assert_awaited_once_with(
        storage_result.storage_path
    )

    db_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_upload_returns_upload_detail(
    upload_service,
    upload_repository,
    user,
):
    upload_id = uuid4()
    created_at = datetime.now(UTC)

    upload = MagicMock(spec=Upload)
    upload.id = upload_id
    upload.file_name = "test.jpg"
    upload.file_size = 1024
    upload.content_type = "image/jpeg"
    upload.created_at = created_at

    upload_repository.get_by_id_and_user.return_value = upload

    result = await upload_service.get_upload(
        user=user,
        upload_id=upload_id,
    )

    upload_repository.get_by_id_and_user.assert_awaited_once_with(
        upload_id,
        user.id,
    )

    assert result.upload_id == upload_id
    assert result.file_name == "test.jpg"
    assert result.file_size == 1024
    assert result.content_type == "image/jpeg"
    assert result.created_at == created_at


@pytest.mark.asyncio
async def test_get_upload_raises_when_upload_not_found(
    upload_service,
    upload_repository,
    user,
):
    upload_id = uuid4()

    upload_repository.get_by_id_and_user.return_value = None

    with pytest.raises(UploadNotFoundError):
        await upload_service.get_upload(
            user=user,
            upload_id=upload_id,
        )

    upload_repository.get_by_id_and_user.assert_awaited_once_with(
        upload_id,
        user.id,
    )


@pytest.mark.asyncio
async def test_delete_upload_deletes_upload_and_storage(
    upload_service,
    db_session,
    upload_repository,
    storage_service,
    user,
):
    upload_id = uuid4()

    upload = MagicMock(spec=Upload)
    upload.id = upload_id
    upload.storage_path = "uploads/test-id.jpg"

    upload_repository.get_by_id_and_user.return_value = upload

    result = await upload_service.delete_upload(
        user=user,
        upload_id=upload_id,
    )

    upload_repository.get_by_id_and_user.assert_awaited_once_with(
        upload_id,
        user.id,
    )

    upload_repository.delete.assert_awaited_once_with(upload)

    db_session.commit.assert_awaited_once()

    storage_service.delete_file.assert_awaited_once_with(
        upload.storage_path
    )

    assert result.upload_id == upload_id
    assert result.message == "Upload deleted successfully."


@pytest.mark.asyncio
async def test_delete_upload_raises_when_upload_not_found(
    upload_service,
    upload_repository,
    db_session,
    user,
):
    upload_id = uuid4()

    upload_repository.get_by_id_and_user.return_value = None

    with pytest.raises(UploadNotFoundError):
        await upload_service.delete_upload(
            user=user,
            upload_id=upload_id,
        )

    upload_repository.delete.assert_not_awaited()
    db_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_list_uploads_returns_upload_summaries(
    upload_service,
    upload_repository,
    user,
):
    upload_1 = MagicMock(spec=Upload)
    upload_1.id = uuid4()
    upload_1.file_name = "first.jpg"
    upload_1.file_size = 100
    upload_1.content_type = "image/jpeg"
    upload_1.created_at = datetime.now(UTC)

    upload_2 = MagicMock(spec=Upload)
    upload_2.id = uuid4()
    upload_2.file_name = "second.png"
    upload_2.file_size = 200
    upload_2.content_type = "image/png"
    upload_2.created_at = datetime.now(UTC)

    upload_repository.list_uploads.return_value = [
        upload_1,
        upload_2,
    ]

    result = await upload_service.list_uploads(user)

    upload_repository.list_uploads.assert_awaited_once_with(
        user.id
    )

    assert len(result) == 2

    assert result[0].upload_id == upload_1.id
    assert result[0].file_name == upload_1.file_name
    assert result[0].file_size == upload_1.file_size
    assert result[0].content_type == upload_1.content_type
    assert result[0].created_at == upload_1.created_at

    assert result[1].upload_id == upload_2.id
    assert result[1].file_name == upload_2.file_name
    assert result[1].file_size == upload_2.file_size
    assert result[1].content_type == upload_2.content_type
    assert result[1].created_at == upload_2.created_at


@pytest.mark.asyncio
async def test_list_uploads_returns_empty_list_when_no_uploads(
    upload_service,
    upload_repository,
    user,
):
    upload_repository.list_uploads.return_value = []

    result = await upload_service.list_uploads(user)

    upload_repository.list_uploads.assert_awaited_once_with(
        user.id
    )

    assert result == []

@pytest.mark.asyncio
async def test_upload_file_creates_upload_and_commits(
    upload_service,
    db_session,
    upload_repository,
    storage_service,
    user,
):
    file = create_upload_file()

    storage_result = StorageResult(
        storage_path="uploads/test-id.jpg",
        file_name="test-id.jpg",
        file_size=15,
        content_type="image/jpeg",
    )

    storage_service.save_file.return_value = storage_result

    async def refresh_upload(upload):
        upload.id = uuid4()

    db_session.refresh.side_effect = refresh_upload

    await upload_service.upload_file(
        user=user,
        file=file,
    )

    upload_repository.save.assert_awaited_once()

    saved_upload = upload_repository.save.await_args.args[0]

    assert saved_upload.user_id == user.id
    assert saved_upload.storage_path == storage_result.storage_path
    assert saved_upload.file_name == storage_result.file_name
    assert saved_upload.file_size == storage_result.file_size
    assert saved_upload.content_type == storage_result.content_type

    db_session.commit.assert_awaited_once()
    db_session.refresh.assert_awaited_once_with(saved_upload)


