from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.audit_log import AuditLog
from backend.app.repositories.base_repository import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(
            db_session=db_session,
            model=AuditLog,
        )

    async def list_by_actor(
        self,
        actor_user_id: UUID,
    ) -> list[AuditLog]:
        query = (
            select(AuditLog)
            .where(AuditLog.actor_user_id == actor_user_id)
            .order_by(AuditLog.created_at.desc())
        )

        result = await self._db_session.execute(query)

        return list(result.scalars().all())