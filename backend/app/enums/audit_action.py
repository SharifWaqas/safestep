from enum import StrEnum, auto

class AuditAction(StrEnum):
    
    REGISTERED = auto()
    LOGIN_SUCCEEDED = auto()
    LOGIN_FAILED = auto()
    LOGOUT = auto()

    SESSION_CREATED = auto()
    SESSION_REFRESHED = auto()
    SESSION_REVOKED = auto()
    SESSION_EXPIRED = auto()

    UPLOAD_CREATED = auto()
    UPLOAD_DELETED = auto()

    ANALYSIS_REQUESTED = auto()
    ANALYSIS_STARTED = auto()
    ANALYSIS_COMPLETED = auto()
    ANALYSIS_FAILED = auto()

    AI_RESULT_GENERATED = auto()

    ACCOUNT_UPDATED = auto()
    ACCOUNT_DELETED = auto()
    
    ACCESS_DENIED = auto()