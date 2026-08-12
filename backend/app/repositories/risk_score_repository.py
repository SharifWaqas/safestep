from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.risk_score import RiskScore
from backend.app.repositories.base_repository import BaseRepository


class RiskScoreRepository(BaseRepository[RiskScore]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session,model=RiskScore)