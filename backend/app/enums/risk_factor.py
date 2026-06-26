from enum import StrEnum, auto

class RiskFactor(StrEnum):
    """Represents the predefined risk factors that contribute to an analysis's overall risk assessment."""
    URGENCY_LANGUAGE = auto()
    THREAT_LANGUAGE = auto()
    CREDENTIAL_REQUEST = auto()
    FINANCIAL_REQUEST = auto()
    SUSPICIOUS_LINK = auto()
    SUSPICIOUS_DOMAIN = auto()
    BRAND_IMPERSONATION = auto()
    UNKNOWN_SENDER = auto()
    LOGIN_FORM = auto()
    PAYMENT_REQUEST = auto()
    REWARD_LANGUAGE = auto()