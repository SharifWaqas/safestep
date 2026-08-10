from abc import ABC, abstractmethod


class StorageProvider(ABC):

    @abstractmethod
    async def get_image_data(self, storage_path: str) -> bytes:
        pass