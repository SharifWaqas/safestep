from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from backend.app.models.analysis import Analysis
from backend.app.repositories.analysis_repository import AnalysisRepository


@pytest.mark.asyncio
async def test_get_by_upload_id_returns_analysis():
    upload_id = uuid4()

    expected_analysis = Analysis(
        upload_id=upload_id,
    )

    db_session = MagicMock()
    db_session.execute = AsyncMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = expected_analysis
    db_session.execute.return_value = result

    repository = AnalysisRepository(db_session)

    actual_analysis = await repository.get_by_upload_id(upload_id)

    assert actual_analysis is expected_analysis
    db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_upload_id_returns_none_when_analysis_does_not_exist():
    upload_id = uuid4()

    db_session = MagicMock()
    db_session.execute = AsyncMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    db_session.execute.return_value = result

    repository = AnalysisRepository(db_session)

    actual_analysis = await repository.get_by_upload_id(upload_id)

    assert actual_analysis is None
    db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_id_and_user_returns_analysis():
    analysis_id = uuid4()
    user_id = uuid4()
    upload_id = uuid4()

    expected_analysis = Analysis(
        upload_id=upload_id,
    )
    expected_analysis.id = analysis_id

    db_session = MagicMock()
    db_session.execute = AsyncMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = expected_analysis
    db_session.execute.return_value = result

    repository = AnalysisRepository(db_session)

    actual_analysis = await repository.get_by_id_and_user(
        analysis_id=analysis_id,
        user_id=user_id,
    )

    assert actual_analysis is expected_analysis
    db_session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_by_id_and_user_returns_none_when_analysis_does_not_exist():
    analysis_id = uuid4()
    user_id = uuid4()

    db_session = MagicMock()
    db_session.execute = AsyncMock()

    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    db_session.execute.return_value = result

    repository = AnalysisRepository(db_session)

    actual_analysis = await repository.get_by_id_and_user(
        analysis_id=analysis_id,
        user_id=user_id,
    )

    assert actual_analysis is None
    db_session.execute.assert_awaited_once()