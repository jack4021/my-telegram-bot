from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from .handlers.commands import (
    start,
    commands_cmd,
    help_cmd,
    reset_cmd,
    status_cmd,
    ping_cmd,
    tokens_cmd,
    websearch_cmd,
    websearch_callback,
    mode_cmd,
    mode_callback,
)
from .handlers.models import models_cmd, models_callback
from .handlers.message import message

from .utils.auth import authorized_only
from .utils.logger import logger
from .utils.config import TOKEN


def run_bot():
    """
    Initialize and start the Telegram bot application.

    Sets up the bot with all command and message handlers, including authorization
    checks for protected endpoints. Configures handlers for user commands (start, help,
    reset, models, etc.), callback queries for model selection, mode switching, and
    web search results, and general message processing.

    Returns:
        None

    Raises:
        Typically raises telegram library exceptions if token is invalid or network
        issues occur during bot startup.

    Note:
        - The bot runs with concurrent_updates enabled for handling multiple
          simultaneous requests.
        - Authorization is enforced on most commands via the authorized_only decorator.
        - The bot blocks indefinitely during run_polling() until interrupted.
    """
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()
    app.add_handler(CommandHandler("start", authorized_only(start)))
    app.add_handler(CommandHandler("help", authorized_only(help_cmd)))
    app.add_handler(CommandHandler("reset", authorized_only(reset_cmd)))
    app.add_handler(CommandHandler("models", authorized_only(models_cmd)))
    app.add_handler(CommandHandler("commands", authorized_only(commands_cmd)))
    app.add_handler(CommandHandler("status", authorized_only(status_cmd)))
    app.add_handler(CommandHandler("ping", authorized_only(ping_cmd)))
    app.add_handler(CommandHandler("tokens", authorized_only(tokens_cmd)))
    app.add_handler(CommandHandler("websearch", authorized_only(websearch_cmd)))
    app.add_handler(
        CallbackQueryHandler(authorized_only(websearch_callback), pattern="^websearch_")
    )
    app.add_handler(
        CallbackQueryHandler(authorized_only(models_callback), pattern=r"^set_model:")
    )
    app.add_handler(CommandHandler("mode", authorized_only(mode_cmd)))
    app.add_handler(
        CallbackQueryHandler(authorized_only(mode_callback), pattern="^mode_")
    )
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, authorized_only(message))
    )

    logger.info("Bot is running...")
    app.run_polling()
