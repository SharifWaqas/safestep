import aiofiles

from backend.app.ai.storage import StorageProvider


class LocalStorageProvider(StorageProvider):

    async def get_image_data(self, storage_path: str) -> bytes:
        async with aiofiles.open(storage_path, "rb") as image_file:
            return await image_file.read()