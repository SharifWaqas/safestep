import base64

from openai import AsyncOpenAI

from backend.app.ai.parser import AIResponseParser
from backend.app.ai.providers.base import AIProvider, AIProviderError
from backend.app.ai.schemas import AIResponseSchema
import logging

class NVIDIAClient(AIProvider):

    def __init__(self, api_key: str, model: str):
        self._client = AsyncOpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
        )
        self._model = model

    async def analyze_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> AIResponseSchema:
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        image_data_url = f"data:{mime_type};base64,{base64_image}"

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_data_url,
                                },
                            },
                        ],
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "AIResponseSchema",
                        "schema": AIResponseSchema.model_json_schema(),
                    },
                },
            )

            content = response.choices[0].message.content

            return AIResponseParser.parse(content)

        except Exception as exc:
            raise AIProviderError(
                "NVIDIA failed to analyze the image."
            ) from exc

    async def close(self) -> None:
        await self._client.close()