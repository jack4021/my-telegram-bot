import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

TOKEN = os.environ["TELEGRAM_BOT_API_KEY"]
XAI_API_KEY = os.environ["XAI_API_KEY"]
API_KEY = os.environ["OPENROUTER_API_KEY"]


def _load_prompts() -> list[dict]:
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    with open(os.path.join(base_dir, "assistant_prompt.md")) as f:
        assistant = f.read()
    with open(os.path.join(base_dir, "roleplay_prompt.md")) as f:
        roleplay = f.read()
    return [{"default": {"system": {"assistant": assistant, "roleplay": roleplay}}}]


PROMPTS = _load_prompts()
DEFAULT_MODEL = "inception/mercury-2"
MAX_HISTORY_MESSAGES = 80

ALLOWED_USER_IDS: set[int] = {
    int(os.environ["MY_TELEGRAM_ID"]),
}

ALLOWED_MODELS = [
    "x-ai/grok-4.1-fast",
    "inception/mercury-2",
    "anthropic/claude-haiku-4.5",
    "openai/gpt-5-nano",
    "xiaomi/mimo-v2-flash",
    "deepseek/deepseek-v3.2",
    "mistralai/mistral-nemo",
    "nousresearch/hermes-4-70b",
]

IMAGE_MODEL = os.getenv("IMAGE_MODEL", "grok-imagine-image")
IMAGE_RESOLUTION = os.getenv("IMAGE_RESOLUTION", "1k")

IMAGE_MODELS = {
    "normal": "grok-imagine-image",
    "pro": "grok-imagine-image-pro",
}
IMAGE_QUALITIES = ["1k", "2k"]
