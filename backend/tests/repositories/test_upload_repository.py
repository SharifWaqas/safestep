from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from backend.app.models.upload import Upload
from backend.app.repositories.upload_repository import UploadRepository


@pytest.mark.asyncio
async def test_get_by_id_and_user_returns_upload():
    upload_id = uuid4()
    user_id = uuid4()

    expected_upload = Upload(
        user_id=user_id,
        storage_path="uploads/test.png",
        file_name="test.png",
        file_size=1024,
        content_type="image/png",
    )
    expected_upload.id = upload_id

    db_session = MagicMock()
    db_session.execute = AsyncMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = expected_upload
    db_session.execute.return_value = result

    repository = UploadRepository(db_session)

    actual_upload = await repository.get_by_id_and_user(
        upload_id=upload_id,
        user_id=user_id,
    )

    assert actual_upload is expected_upload
    db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_id_and_user_returns_none_when_upload_does_not_exist():
    upload_id = uuid4()
    user_id = uuid4()

    db_session = MagicMock()
    db_session.execute = AsyncMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    db_session.execute.return_value = result

    repository = UploadRepository(db_session)

    actual_upload = await repository.get_by_id_and_user(
        upload_id=upload_id,
        user_id=user_id,
    )

    assert actual_upload is None
    db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_uploads_returns_user_uploads():
    user_id = uuid4()

    older_upload = Upload(
        user_id=user_id,
        storage_path="uploads/older.png",
        file_name="older.png",
        file_size=1024,
        content_type="image/png",
    )

    newer_upload = Upload(
        user_id=user_id,
        storage_path="uploads/newer.png",
        file_name="newer.png",
        file_size=2048,
        content_type="image/png",
    )

    older_upload.created_at = datetime(
        2026, 1, 1, tzinfo=timezone.utc
    )
    newer_upload.created_at = datetime(
        2026, 1, 2, tzinfo=timezone.utc
    )

    db_session = MagicMock()
    db_session.execute = AsyncMock()

    result = MagicMock()
    result.scalars.return_value = [
        newer_upload,
        older_upload,
    ]

    db_session.execute.return_value = result

    repository = UploadRepository(db_session)

    actual_uploads = await repository.list_uploads(user_id)

    assert actual_uploads == [
        newer_upload,
        older_upload,
    ]
    db_session.execute.assert_awaited_once()