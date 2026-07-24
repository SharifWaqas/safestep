from pydantic import BaseModel
from uuid import UUID

class UploadResponse(BaseModel):
    upload_id: UUID
    message: str

class StorageResult(BaseModel):
    storage_path: str
    file_name: str
    file_size: int
    content_type: str


