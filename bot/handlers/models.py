from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.utils.config import ALLOWED_MODELS
from bot.utils.state import user_models


# noinspection PyUnusedLocal
async def models_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(model, callback_data=f"set_model:{model}")]
        for model in ALLOWED_MODELS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "*Available models:*\nTap one to select it.",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


# noinspection PyUnusedLocal
async def models_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    model_name = query.data.removeprefix("set_model:")
    if model_name in ALLOWED_MODELS:
        user_models[update.effective_user.id] = model_name
        await query.edit_message_text(
            f"✅ Model set to: `{model_name}`", parse_mode="Markdown"
        )
    else:
        await query.edit_message_text("❌ Model not allowed.")
