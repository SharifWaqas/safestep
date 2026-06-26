from enum import StrEnum, auto

class RiskLevel(StrEnum):
    """Represents the risk Level."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    VERY_HIGH = auto()