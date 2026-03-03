import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

TOKEN = os.environ["TELEGRAM_BOT_API_KEY"]
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
DEFAULT_MODEL = "x-ai/grok-4.1-fast"
MAX_HISTORY_MESSAGES = 80

ALLOWED_USER_IDS: set[int] = {
    int(os.environ["MY_TELEGRAM_ID"]),
}

ALLOWED_MODELS = [
    "anthropic/claude-haiku-4.5",
    "deepseek/deepseek-v3.2",
    "ibm-granite/granite-4.0-h-micro",
    "minimax/minimax-m2.5",
    "mistralai/ministral-14b-2512",
    "mistralai/mistral-nemo",
    "mistralai/mistral-small-3.2-24b-instruct",
    "mistralai/mistral-small-24b-instruct-2501",
    "mistralai/mistral-small-creative",
    "moonshotai/kimi-k2.5",
    "nousresearch/hermes-4-70b",
    "openai/gpt-5-nano",
    "qwen/qwen3.5-397b-a17b",
    "x-ai/grok-4.1-fast",
    "xiaomi/mimo-v2-flash",
    "z-ai/glm-5",
    # ---------------------------------------------
    # "alibaba/tongyi-deepresearch-30b-a3b",
    # "gryphe/mythomax-l2-13b",
    # "meta-llama/llama-3.3-70b-instruct",
    # "meta-llama/llama-4-maverick",
    # "meta-llama/llama-4-scout",
    # "nousresearch/hermes-4-405b",
    # "nvidia/nemotron-nano-9b-v2",
    # "nvidia/nemotron-nano-12b-v2-vl",
    # "nvidia/nemotron-3-nano-30b-a3b",
    # "qwen/qwen3.5-plus-02-15",
    # "sao10k/l3-lunaris-8b",
]
