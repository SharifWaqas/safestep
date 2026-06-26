from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.app.database.base import Base
from backend.app.database.mixins import SoftDeleteMixin
from sqlalchemy import Text, ForeignKey, Integer
import uuid


class Upload(Base, SoftDeleteMixin):
    __tablename__ = "uploads"

    user: Mapped["User"] = relationship("User", back_populates="uploads") 

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"),nullable=False)
    storage_path: Mapped[str] = mapped_column(nullable=False, type_=Text)
    file_name: Mapped[str] = mapped_column(nullable=False, type_=Text)
    file_size: Mapped[int] = mapped_column(nullable=False, type_=Integer)