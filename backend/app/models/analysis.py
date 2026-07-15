from datetime import datetime
import uuid

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base
from backend.app.database.mixins import SoftDeleteMixin
from backend.app.enums.analysis import AnalysisStatus


class Analysis(Base, SoftDeleteMixin):
    __tablename__ = "analyses"

    ai_result: Mapped["AIResult"] = relationship("AIResult", back_populates="analysis", uselist=False)
    upload: Mapped["Upload"] = relationship("Upload",back_populates="analyses")
    risk_scores: Mapped[list["RiskScore"]] = relationship("RiskScore",back_populates="analysis",)

    upload_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("uploads.id"),nullable=False)

    status: Mapped[AnalysisStatus] = mapped_column(
        SQLEnum(AnalysisStatus,name="analysis_status"),nullable=False,default=AnalysisStatus.PENDING,server_default=AnalysisStatus.PENDING.value)

    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)

    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)