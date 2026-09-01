from unittest.mock import AsyncMock, MagicMock

import pytest

from backend.app.models.user import User
from backend.app.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_adds_and_returns_user():
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="John Doe",
    )

    db_session = MagicMock()

    repository = UserRepository(db_session)

    result = await repository.create(user)

    assert result is user
    db_session.add.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_find_by_email_returns_user():
    expected_user = User(
        email="test@example.com",
        password_hash="hashed_password",
        full_name="John Doe",
    )

    db_session = MagicMock()
    db_session.execute = AsyncMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = expected_user
    db_session.execute.return_value = result

    repository = UserRepository(db_session)

    actual_user = await repository.find_by_email("test@example.com")

    assert actual_user is expected_user
    db_session.execute.assert_awaited_once()