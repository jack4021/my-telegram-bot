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


ALLOWED_MODELS = [
    "x-ai/grok-4.1-fast",
    "x-ai/grok-4.20-beta",
    "anthropic/claude-haiku-4.5",
    "inception/mercury-2",
    "deepseek/deepseek-v3.2",
    "nousresearch/hermes-4-70b",
]

PROMPTS = _load_prompts()
DEFAULT_MODEL = ALLOWED_MODELS[0]
MAX_HISTORY_MESSAGES = 80

ALLOWED_USER_IDS: set[int] = {
    int(os.environ["MY_TELEGRAM_ID"]),
}

IMAGE_MODEL = os.getenv("IMAGE_MODEL", "pro")
IMAGE_RESOLUTION = os.getenv("IMAGE_RESOLUTION", "1k")

IMAGE_MODELS = {
    "normal": "grok-imagine-image",
    "pro": "grok-imagine-image-pro",
}
IMAGE_QUALITIES = ["1k", "2k"]
