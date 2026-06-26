from sqlalchemy.orm import mapped_column, Mapped, relationship
from backend.app.database.base import Base
from sqlalchemy import Text, String, ForeignKey, Enum as SQLEnum, DECIMAL, INTEGER
import uuid
from backend.app.enums.risk_level import RiskLevel
from decimal import Decimal

class AIResult(Base):

    __tablename__ = "ai_results"

    analysis: Mapped["Analysis"] = relationship("Analysis", back_populates="ai_result")

    analysis_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("analyses.id"), nullable=False, unique=True)
    summary: Mapped[str] = mapped_column(nullable=False, type_=Text)
    explanation: Mapped[str] = mapped_column(nullable=False, type_=Text)
    guidance: Mapped[str] = mapped_column(nullable = False, type_=Text)
    reassurance: Mapped[str] = mapped_column(nullable=False, type_=Text)
    risk_level: Mapped[RiskLevel] = mapped_column(SQLEnum(RiskLevel,name="risk_level"),nullable=False)
    confidence: Mapped[Decimal] = mapped_column(nullable=False, type_=DECIMAL(4,3))
    model_name: Mapped[str] = mapped_column(nullable=True, type_=String(64))
    prompt_tokens: Mapped[int] = mapped_column(nullable=True, type_= INTEGER)
    completion_tokens: Mapped[int] = mapped_column(nullable=True, type_=INTEGER)
