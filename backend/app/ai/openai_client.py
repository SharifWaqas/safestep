from openai import AsyncOpenAI


class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def analyze_image(
        self,
        file_path: str,
        prompt: str,
    ):
        with open(file_path, "rb") as image_file:
            response = await self._client.responses.create(
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
                                "image_url": image_file,
                            },
                        ],
                    }
                ],
            )

        return response