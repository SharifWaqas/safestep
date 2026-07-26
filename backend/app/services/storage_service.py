from fastapi import UploadFile
from pathlib import Path
import uuid
import aiofiles

from backend.app.schemas.upload import StorageResult

class StorageService:

    def __init__(self, upload_directory: Path):
        self._upload_directory = upload_directory
        self._upload_directory.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile)-> StorageResult:
        file_path = Path(file.filename)
        file_extension = file_path.suffix
        file_id = uuid.uuid4()
        stored_file_name = f"{file_id}{file_extension}"
        storage_path = self._upload_directory / stored_file_name
        file_data = await file.read()
        async with aiofiles.open(storage_path, "wb") as f:
            await f.write(file_data)

        return StorageResult(storage_path=str(storage_path),file_name=stored_file_name,file_size= len(file_data),content_type= file.content_type)

    def delete_file(self):
        ...

    def get_file(self):
        ...

    def exists(self):
        ...