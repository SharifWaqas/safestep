from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.app.database.base import Base
from backend.app.database.mixins import SoftDeleteMixin
from sqlalchemy import String, Text, Boolean

class User(Base, SoftDeleteMixin ):
    __tablename__ = "users"

    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="user")
    uploads: Mapped[list["Upload"]] = relationship("Upload", back_populates="user")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog",back_populates="actor",)

    email: Mapped[str] = mapped_column(unique=True, nullable=False, type_=String(255))
    password_hash: Mapped[str] = mapped_column(nullable=False, type_= Text)
    Full_name: Mapped[str] = mapped_column(nullable=False, type_= String(50))
    is_verified: Mapped[bool] = mapped_column(default=False,nullable=False, type_= Boolean)
    is_active: Mapped[bool] = mapped_column(default=True,nullable=False,  type_= Boolean)