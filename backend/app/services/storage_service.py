from fastapi import UploadFile
from pathlib import Path

from backend.app.schemas.upload import StorageResult

class StorageService:

    def __init__(self, upload_directory: Path):
        self._upload_directory = upload_directory
        self._upload_directory.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile)-> StorageResult:
        ...

    def delete_file(self):
        ...

    def get_file(self):
        ...

    def exists(self):
        ...