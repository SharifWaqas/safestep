import uuid
from decimal import Decimal

from sqlalchemy import Text, Enum as SQLEnum, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base
from backend.app.enums.risk_factor import RiskFactor


class RiskScore(Base):

    __tablename__ = "risk_scores"
    
    analysis_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("analyses.id"), nullable=False)

    analysis: Mapped["Analysis"] = relationship("Analysis", back_populates="risk_scores")

    risk_factor: Mapped[RiskFactor] = mapped_column(SQLEnum(RiskFactor, name= "risk_factor"), nullable=False)
    
    score: Mapped[Decimal] = mapped_column(nullable=False, type_=DECIMAL(5,2))
    
    explanation: Mapped[str] = mapped_column(nullable=False, type_=Text)
