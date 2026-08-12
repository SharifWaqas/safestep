import asyncio
import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

from backend.app.ai.schemas import AIResponseSchema

async def main():
    image_path = Path("backend/tests/fixtures/test_screenshot.png")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    image_data_url = f"data:image/png;base64,{base64_image}"

    client = AsyncOpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ["NVIDIA_API_KEY"],
        timeout=60.0,
    )
    response = await client.chat.completions.create(
        model="meta/llama-3.2-90b-vision-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
    Analyze this image as a digital safety assistant.

    Determine the overall risk level, explain what the content is
    asking the user to do, identify suspicious characteristics,
    provide safe practical guidance, and provide reassurance.

    Do not assume the content is legitimate or malicious.
    Base your assessment only on evidence visible in the image.

    Return the result according to the provided JSON schema.
    """,
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

    result = AIResponseSchema.model_validate_json(
        response.choices[0].message.content
    )

    print(result)
    print(type(result))

if __name__ == "__main__":
    asyncio.run(main())