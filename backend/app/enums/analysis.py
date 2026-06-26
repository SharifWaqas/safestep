from enum import StrEnum, auto

class AnalysisStatus(StrEnum):
    """Represents the lifecycle state of an analysis."""
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()