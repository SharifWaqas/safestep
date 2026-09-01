from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from backend.app.models.user import User
from backend.app.repositories.base_repository import BaseRepository


@pytest.mark.asyncio
async def test_get_by_id_returns_entity():
    entity_id = uuid4()

    expected_entity = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="John Doe",
    )
    expected_entity.id = entity_id

    db_session = MagicMock()
    db_session.execute = AsyncMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = expected_entity
    db_session.execute.return_value = result

    repository = BaseRepository(
        db_session=db_session,
        model=User,
    )

    actual_entity = await repository.get_by_id(entity_id)

    assert actual_entity is expected_entity
    db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_adds_and_returns_entity():
    entity = MagicMock()
    db_session = MagicMock()

    repository = BaseRepository(
        db_session=db_session,
        model=User,
    )

    result = await repository.save(entity)

    assert result is entity
    db_session.add.assert_called_once_with(entity)


@pytest.mark.asyncio
async def test_delete_deletes_entity():
    entity = MagicMock()
    db_session = MagicMock()
    db_session.delete = AsyncMock()

    repository = BaseRepository(
        db_session=db_session,
        model=User,
    )

    result = await repository.delete(entity)

    assert result is None
    db_session.delete.assert_awaited_once_with(entity)