import base64

from openai import AsyncOpenAI

from backend.app.ai.schemas import AIResponseSchema

from backend.app.ai.providers.base import AIProvider

class OpenAIClient(AIProvider):
    def __init__(self, api_key: str, model: str):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def analyze_image(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> AIResponseSchema:
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        image_data_url = f"data:{mime_type};base64,{base64_image}"

        response = await self._client.responses.parse(
            model=self._model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        },
                        {
                            "type": "input_image",
                            "image_url": image_data_url,
                        },
                    ],
                }
            ],
            text_format=AIResponseSchema,
        )

        return response.output_parsed