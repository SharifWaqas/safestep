import base64

from openai import AsyncOpenAI

from app.ai.schemas import AIResponseSchema


class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def analyze_image(
        self,
        file_path: str,
        mime_type: str,
        prompt: str,
    ):
        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()

        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        image_data_url = (
            f"data:{mime_type};base64,{base64_image}"
        )

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

        return response