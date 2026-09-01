from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.audit_log import AuditLog
from backend.app.repositories.base_repository import BaseRepository


class AuditLogRepository(BaseRepository[AuditLog]):

    def __init__(self, db_session: AsyncSession):
        super().__init__(
            db_session=db_session,
            model=AuditLog,
        )