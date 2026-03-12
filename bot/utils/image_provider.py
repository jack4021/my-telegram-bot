from bot.utils.logger import logger
from bot.utils.config import XAI_API_KEY, IMAGE_MODEL, IMAGE_MODELS

import xai_sdk


class ImageProvider:
    """Placeholder image generation provider."""

    async def send(
            self,
            prompt: str,
            num_of_images: int = 1,
            model_key: str = "normal",
            resolution: str = "1k",
    ) -> list[str]:
        model = IMAGE_MODELS.get(model_key, IMAGE_MODEL)
        client = xai_sdk.Client(api_key=XAI_API_KEY)
        responses = client.image.sample_batch(
            prompt=prompt,
            model=model,
            n=num_of_images,
            image_format="url",
            resolution=resolution,
        )
        urls = [response.url for _, response in enumerate(responses)]
        logger.info(
            "Generated %d image(s) with '%s' model, '%s' resolution, and prompt: %s -> %s",
            num_of_images,
            model,
            resolution,
            prompt,
            ", ".join(urls),
        )
        return urls


def get_image_provider() -> ImageProvider:
    """Return an instance of the image provider."""
    return ImageProvider()
