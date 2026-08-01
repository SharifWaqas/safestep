from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UploadResponse(BaseModel):
    upload_id: UUID
    message: str

class StorageResult(BaseModel):
    storage_path: str
    file_name: str
    file_size: int
    content_type: str

class UploadDetailResponse(BaseModel):
    file_name: str
    file_size: int
    content_type: str
    upload_id: UUID
    created_at: datetime




