import asyncio

import aiofiles

from backend.app.ai.providers.nvidia_client import NVIDIAClient
from backend.app.core.config import settings


async def main():
    client = NVIDIAClient(
        api_key=settings.NVIDIA_API_KEY,
        model=settings.NVIDIA_MODEL,
    )

    async with aiofiles.open("backend/tests/fixtures/test_screenshot.png","rb",) as image_file:
        image_bytes = await image_file.read()

    prompt = """
    Analyze this image as a digital safety assistant.

    Determine:
    - overall risk level
    - what the content is asking the user to do
    - suspicious characteristics
    - safe practical guidance
    - reassurance

    Return the result according to the required JSON schema.
    """

    result = await client.analyze_image(
        image_bytes=image_bytes,
        mime_type="image/png",
        prompt=prompt,
    )

    print(result)
    print()
    print("Risk level:", result.risk_level)
    print("Summary:", result.summary)


if __name__ == "__main__":
    asyncio.run(main())