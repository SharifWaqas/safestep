from uuid import UUID

from backend.app.enums.audit_action import AuditAction
from backend.app.enums.audit_resource_type import AuditResourceType
from backend.app.models.audit_log import AuditLog
from backend.app.repositories.audit_log_repository import AuditLogRepository


class AuditLogService:

    def __init__(
        self,
        audit_log_repository: AuditLogRepository,
    ) -> None:
        self._audit_log_repository = audit_log_repository

    async def log(
        self,
        action: AuditAction,
        resource_type: AuditResourceType,
        resource_id: UUID,
        actor_user_id: UUID | None = None,
        details: str | None = None,
    ) -> AuditLog:
        audit_log = AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
        )

        return await self._audit_log_repository.save(audit_log)