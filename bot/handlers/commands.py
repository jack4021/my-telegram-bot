from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils.state import (
    get_history,
    get_model,
    conversations,
    last_usage,
    set_web_search,
    is_web_search_enabled,
)
from bot.utils.config import MAX_HISTORY_MESSAGES

import time


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hey! I'm alive. Send me a message to chat.",
    )


# noinspection PyUnusedLocal
async def commands_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_text = (
        "*Available commands:*\n\n"
        "/commands - List all available commands\n"
        "/help - Show how to use the bot\n"
        "/models - Show available AI models (with buttons)\n"
        "/mode - Toggle between assistant, roleplay, and image modes\n"
        "/ping - Check responsiveness\n"
        "/reset - Clear conversation history\n"
        "/start - Start the bot\n"
        "/status - Bot status (model & history)\n"
        "/tokens - Last API token usage\n"
        "/websearch - Toggle web search integration"
    )
    await update.message.reply_text(commands_text, parse_mode="Markdown")


# noinspection PyUnusedLocal
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Just send me any message and I'll respond via AI.")


# noinspection PyUnusedLocal
async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conversations.pop(update.effective_user.id, None)
    await update.message.reply_text("Conversation cleared!")


# noinspection PyUnusedLocal
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    history = get_history(user_id)
    msg_count = len(history)
    model = get_model(user_id)
    mode = context.user_data.get("mode", "assistant")
    text = f"""*Bot Status:*
• Current model: `{model}`
• Mode: `{mode.capitalize()}`
• History: {msg_count} messages
• Max history: {MAX_HISTORY_MESSAGES} messages
• Web Search: {is_web_search_enabled(user_id)}"""
    await update.message.reply_text(text, parse_mode="Markdown")


# noinspection PyUnusedLocal
async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    latency = (time.time() - start_time) * 1000
    await msg.edit_text(
        f"🏓 Pong! *(~{latency:.0f}ms round-trip)*", parse_mode="Markdown"
    )


# noinspection PyUnusedLocal
async def tokens_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    usage = last_usage.get(user_id)
    if not usage:
        await update.message.reply_text("❌ No recent API usage. Send a message first!")
        return
    text = f"""*Last Response Tokens:*
• Prompt: `{usage.get("prompt_tokens", 0):,}`
• Completion: `{usage.get("completion_tokens", 0):,}`
• Total: `{usage.get("total_tokens", 0):,}`"""
    await update.message.reply_text(text, parse_mode="Markdown")


# noinspection PyUnusedLocal
async def websearch_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show web search toggle with inline buttons."""
    user_id = update.effective_user.id
    enabled = is_web_search_enabled(user_id)

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ ON" if enabled else "ON", callback_data="websearch_on"
            ),
            InlineKeyboardButton(
                "OFF ✅" if not enabled else "OFF", callback_data="websearch_off"
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    status_text = "enabled" if enabled else "disabled"
    await update.message.reply_text(
        f"🌐 Web Search is currently *{status_text}*.",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


# noinspection PyUnusedLocal
async def websearch_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses for web search toggle."""
    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    if query.data == "websearch_on":
        set_web_search(user_id, True)
        enabled = True
    else:
        set_web_search(user_id, False)
        enabled = False

    # Update buttons to reflect new state
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ ON" if enabled else "ON", callback_data="websearch_on"
            ),
            InlineKeyboardButton(
                "OFF ✅" if not enabled else "OFF", callback_data="websearch_off"
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    status_text = "enabled" if enabled else "disabled"
    await query.edit_message_text(
        f"🌐 Web Search is currently *{status_text}*.",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


# noinspection PyUnusedLocal
async def mode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show mode selection with inline buttons."""
    current_mode = context.user_data.get("mode", "assistant")

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ ASSISTANT" if current_mode == "assistant" else "ASSISTANT",
                callback_data="mode_assistant",
            ),
            InlineKeyboardButton(
                "ROLEPLAY ✅" if current_mode == "roleplay" else "ROLEPLAY",
                callback_data="mode_roleplay",
            ),
        ],
        [
            InlineKeyboardButton(
                "🖼️ IMAGE ✅" if current_mode == "image" else "🖼️ IMAGE",
                callback_data="mode_image",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🎭 Current mode: *{current_mode.capitalize()}*",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


# noinspection PyUnusedLocal
async def mode_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses for mode selection."""
    query = update.callback_query

    await query.answer()

    if query.data == "mode_assistant":
        context.user_data["mode"] = "assistant"
        current_mode = "assistant"
    elif query.data == "mode_roleplay":
        context.user_data["mode"] = "roleplay"
        current_mode = "roleplay"
    else:
        context.user_data["mode"] = "image"
        current_mode = "image"

    # Update buttons to reflect new state
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ ASSISTANT" if current_mode == "assistant" else "ASSISTANT",
                callback_data="mode_assistant",
            ),
            InlineKeyboardButton(
                "ROLEPLAY ✅" if current_mode == "roleplay" else "ROLEPLAY",
                callback_data="mode_roleplay",
            ),
        ],
        [
            InlineKeyboardButton(
                "🖼️ IMAGE ✅" if current_mode == "image" else "🖼️ IMAGE",
                callback_data="mode_image",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"🎭 Current mode: *{current_mode.capitalize()}*",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )
