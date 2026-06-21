from sqlalchemy.orm import mapped_column, Mapped
from database.base import Base
from sqlalchemy import String, Text

class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, nullable=False, type_=String(255))
    password_hash: Mapped[str] = mapped_column(nullable=False, type_= Text)
    first_name: Mapped[str] = mapped_column(nullable=False, type_= String(50))
    last_name: Mapped[str] = mapped_column(nullable=True, type_=String(50))
    