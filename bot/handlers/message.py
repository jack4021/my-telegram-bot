from openrouter import OpenRouter
from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.config import API_KEY, PROMPTS, MAX_HISTORY_MESSAGES
from bot.utils.state import (
    get_lock,
    get_history,
    get_plugins,
    get_model,
    last_usage,
    get_image_model,
    get_image_quality,
)
from bot.utils.logger import logger
from bot.utils.image_provider import get_image_provider


def load_prompts():
    return PROMPTS


def safe_nested_get(obj, *keys, default=None):
    """
    Safely get nested value from dict/list, returning default if any step fails.

    Args:
        obj: Starting object (dict, list, etc.)
        *keys: Sequence of keys/indices to traverse
        default: Value to return on failure (default: None)

    Returns:
        Nested value or default.
    """
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, (list, tuple)) and isinstance(key, int):
            try:
                current = current[key]
            except (IndexError, TypeError):
                return default
        else:
            return default
        if current is None:
            return default
    return current


# noinspection PyUnusedLocal
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not update.message or not update.message.text:
        return

    current_mode = context.user_data.get("mode", "assistant")
    logger.debug("Current mode: %s", current_mode)

    if current_mode == "image":
        await handle_image_mode(update, context)
        return

    async with get_lock(user_id):
        logger.debug("Received message from user %d: %s", user_id, update.message.text)
        history = get_history(user_id)
        history.append({"role": "user", "content": update.message.text})

        # trim to keep context window in check
        if len(history) > MAX_HISTORY_MESSAGES:
            history[:] = history[-MAX_HISTORY_MESSAGES:]

        try:
            plugins = get_plugins(user_id)
            logger.debug("plugins: %s", plugins)

            prompts = load_prompts()
            system_prompt = safe_nested_get(
                prompts[0], "default", "system", current_mode
            )
            logger.debug("Using system prompt: %s", system_prompt)

            with OpenRouter(api_key=API_KEY) as client:
                completion = await client.chat.send_async(
                    model=get_model(user_id),
                    messages=[{"role": "system", "content": system_prompt}] + history,
                    plugins=plugins,
                )
                assistant_content = completion.choices[0].message.content

            if not assistant_content:
                await update.message.reply_text(
                    "⚠️ The model returned an empty response."
                )
                history.pop()  # remove the user message we just appended
                return

            if completion.usage:
                last_usage[user_id] = {
                    "prompt_tokens": completion.usage.prompt_tokens,
                    "completion_tokens": completion.usage.completion_tokens,
                    "total_tokens": completion.usage.total_tokens,
                }

        except Exception as e:
            logger.error("OpenRouter API error: %s", e)
            history.pop()
            await update.message.reply_text(
                "⚠️ Something went wrong. Try again in a moment."
            )
            return

        history.append({"role": "assistant", "content": assistant_content})

    for i in range(0, len(assistant_content), 4096):
        chunk = assistant_content[i : i + 4096]
        try:
            await update.message.reply_text(chunk, parse_mode="Markdown")
        except Exception:
            await update.message.reply_text(chunk)


async def handle_image_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image generation mode."""
    user_id = update.effective_user.id
    prompt = update.message.text
    model_key = get_image_model(user_id)
    quality = get_image_quality(user_id)

    msg = await update.message.reply_text("🎨 Generating image...")

    try:
        image_provider = get_image_provider()
        image_urls = await image_provider.send(
            prompt, model_key=model_key, resolution=quality
        )
    except Exception as e:
        logger.error("Image generation error: %s", e)
        await msg.edit_text("⚠️ Image generation failed. Try again in a moment.")
        return

    for url in image_urls:
        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=url,
            )
        except Exception as e:
            logger.error("Failed to send image: %s", e)
            await msg.edit_text(f"⚠️ Failed to send image. View it here: {url}")
            return

    await msg.delete()
