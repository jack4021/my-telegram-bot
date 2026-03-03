import functools

from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.logger import logger
from bot.utils.config import ALLOWED_USER_IDS


# Decorator to restrict access to allowed users
def authorized_only(handler):
    @functools.wraps(handler)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if ALLOWED_USER_IDS and user_id not in ALLOWED_USER_IDS:
            logger.error("User %d is not allowed to use the bot.", user_id)
            if update.message:
                await update.message.reply_text("Sorry, this bot is private.")
            elif update.callback_query:
                await update.callback_query.answer(
                    "Sorry, this bot is private.", show_alert=True
                )
            return None
        return await handler(update, context)

    return wrapper
