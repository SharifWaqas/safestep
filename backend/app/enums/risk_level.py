from enum import StrEnum, auto

class RiskLevel(StrEnum):
    """Represents the risk level."""
    SAFE = "SAFE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"