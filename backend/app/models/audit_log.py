import uuid

from backend.app.database.base import Base
from backend.app.enums.audit_action import AuditAction
from backend.app.enums.audit_resource_type import AuditResourceType

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum as SQLEnum, String, Text

class AuditLog(Base):

    __tablename__ = "audit_logs"


    actor_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=True)
    actor: Mapped["User"] = relationship("User", back_populates="audit_logs")
    action: Mapped[AuditAction] = mapped_column(SQLEnum(AuditAction, name="audit_action"),nullable=False)
    resource_type: Mapped[AuditResourceType] = mapped_column(SQLEnum(AuditResourceType, name="audit_resource_type")nullable=False)
    resource_id: Mapped[uuid.UUID] = mapped_column(nullable=False)
    details: Mapped[str | None] = mapped_column(nullable=True, type_=Text)
