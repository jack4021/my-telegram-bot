import asyncio
from .config import DEFAULT_MODEL, IMAGE_MODEL

conversations: dict[int, list[dict]] = {}
last_usage: dict[int, dict] = {}
user_models: dict[int, str] = {}
_user_locks: dict[int, asyncio.Lock] = {}
plugin_settings = {}
image_models: dict[int, str] = {}
image_qualities: dict[int, str] = {}


def get_lock(user_id: int) -> asyncio.Lock:
    if user_id not in _user_locks:
        _user_locks[user_id] = asyncio.Lock()
    return _user_locks[user_id]


def get_model(user_id: int) -> str:
    return user_models.get(user_id, DEFAULT_MODEL)


def get_history(user_id: int) -> list[dict]:
    if user_id not in conversations:
        conversations[user_id] = []
    return conversations[user_id]


def get_plugins(user_id: int) -> list[dict]:
    """Returns plugins with web plugin if enabled, empty dict otherwise."""
    if plugin_settings.get(user_id, False):
        return [{"id": "web"}]
    return []


def set_web_search(user_id: int, enabled: bool):
    """Enable or disable web search for a user."""
    plugin_settings[user_id] = enabled


def is_web_search_enabled(user_id: int) -> bool:
    """Check if web search is enabled for a user."""
    return plugin_settings.get(user_id, False)


def get_image_model(user_id: int) -> str:
    return image_models.get(user_id, IMAGE_MODEL)


def get_image_quality(user_id: int) -> str:
    return image_qualities.get(user_id, "1k")


def set_image_model(user_id: int, model: str):
    image_models[user_id] = model


def set_image_quality(user_id: int, quality: str):
    image_qualities[user_id] = quality
