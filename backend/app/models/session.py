from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.app.database.base import Base
from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import INET
import uuid
from datetime import datetime

class Session(Base):

    __tablename__ = "sessions"

    user: Mapped["User"] = relationship("User", back_populates="sessions")
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),nullable=False
    )

    refresh_token_hash: Mapped[str] = mapped_column(
        nullable=False, type_=Text
    )

    ip_address: Mapped[str | None] = mapped_column(
        nullable=True, type_= INET
    )

    device_info: Mapped[str | None] = mapped_column(
        nullable=True, type_= String(64)
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )