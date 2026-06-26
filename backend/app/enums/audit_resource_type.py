from enum import StrEnum, auto

class AuditResourceType(StrEnum):
    USER = auto()
    SESSION = auto()
    UPLOAD = auto()
    ANALYSIS = auto()
    AI_RESULT = auto()