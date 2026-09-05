import asyncio
from io import BytesIO
from pathlib import Path
import uuid

import boto3
from fastapi import UploadFile

from backend.app.schemas.upload import StorageResult


class StorageService:

    def __init__(
        self,
        account_id: str,
        access_key_id: str,
        secret_access_key: str,
        bucket_name: str,
    ) -> None:
        self._bucket_name = bucket_name

        self._client = boto3.client(
            "s3",
            endpoint_url=(
                f"https://{account_id}.r2.cloudflarestorage.com"
            ),
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name="auto",
        )

    async def save_file(
        self,
        file: UploadFile,
    ) -> StorageResult:

        file_path = Path(file.filename or "")
        file_extension = file_path.suffix

        file_id = uuid.uuid4()
        stored_file_name = f"{file_id}{file_extension}"

        storage_path = stored_file_name

        file_data = await file.read()

        await asyncio.to_thread(
            self._client.put_object,
            Bucket=self._bucket_name,
            Key=storage_path,
            Body=BytesIO(file_data),
            ContentType=file.content_type or "application/octet-stream",
        )

        return StorageResult(
            storage_path=storage_path,
            file_name=stored_file_name,
            file_size=len(file_data),
            content_type=file.content_type,
        )

    async def get_file(
        self,
        storage_path: str,
    ) -> bytes:

        response = await asyncio.to_thread(
            self._client.get_object,
            Bucket=self._bucket_name,
            Key=storage_path,
        )

        return await asyncio.to_thread(
            response["Body"].read,
        )

    async def delete_file(
        self,
        storage_path: str,
    ) -> None:

        await asyncio.to_thread(
            self._client.delete_object,
            Bucket=self._bucket_name,
            Key=storage_path,
        )