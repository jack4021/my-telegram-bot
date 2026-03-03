# AGENTS.md

## Project Overview

Python 3.11+ Telegram bot that routes user messages to LLMs via the OpenRouter API.
Uses `python-telegram-bot` for the Telegram interface and `openrouter` for AI completions.
All handlers are async. State is held in-memory (no database).

## Repository Structure

```
app.py                # Entry point: calls run_bot()
bot/
  __init__.py           # Re-exports all public symbols via __all__
  bot.py                # Bot initialization, handler registration, run_polling()
  handlers/
    commands.py         # Command handlers (/start, /help, /reset, /status, /websearch, /mode, /ping, /tokens, /commands, etc.)
    message.py          # Text message handler (OpenRouter API call)
    models.py           # /model, /models commands and callbacks
  utils/
    auth.py             # authorized_only decorator
    config.py           # Environment variables, constants, allowed models list
    logger.py           # Logging setup
    state.py            # In-memory dicts for conversations, models, locks, plugins
.env.example           # Example environment variables file
assistant_prompt.md    # System prompt for assistant mode
roleplay_prompt.md     # System prompt for roleplay mode
requirements.txt       # Dependencies: openrouter, python-telegram-bot
Dockerfile             # Docker container definition
railway.toml           # Railway deployment configuration
```

## Environment Variables (Required)

| Variable               | Description                        |
|------------------------|------------------------------------|
| `TELEGRAM_BOT_API_KEY` | Telegram Bot API token             |
| `OPENROUTER_API_KEY`   | OpenRouter API key                 |
| `MY_TELEGRAM_ID`       | Numeric Telegram user ID (owner)   |

These are read via `os.environ[]` in `bot/utils/config.py` and will raise
`KeyError` at import time if missing. Never commit `.env` files or secrets.

## Build / Run / Lint / Test Commands

### Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the bot

```bash
python app.py
```

### Linting (Ruff)

Ruff is used for linting and formatting. No config file exists; defaults apply.

```bash
# Lint
ruff check .

# Lint and auto-fix
ruff check --fix .

# Format
ruff format .

# Check a single file
ruff check bot/handlers/commands.py
```

### Testing

No test suite exists yet. If tests are added, use `pytest`:

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_commands.py

# Run a single test function
pytest tests/test_commands.py::test_reset_clears_history

# Run with verbose output
pytest -v
```

## Code Style Guidelines

### Python Version

Target Python 3.11+. Use modern built-in generic types for annotations:
`list[dict]`, `dict[int, str]`, `set[int]` -- not `typing.List`, `typing.Dict`, etc.

### Naming Conventions

- **Functions and variables**: `snake_case` -- e.g., `get_history`, `user_id`
- **Constants**: `UPPER_SNAKE_CASE` -- e.g., `MAX_HISTORY_MESSAGES`, `ALLOWED_MODELS`
- **Modules**: `snake_case` -- e.g., `commands.py`, `state.py`
- **Handler functions**: named after the command they handle, suffixed with `_cmd`
  for commands or `_callback` for inline button callbacks --
  e.g., `status_cmd`, `models_callback`
- **No classes**: this codebase uses plain functions and module-level state, not OOP

### Imports

- Use absolute imports for `bot.*` modules:
  `from bot.utils.config import TOKEN` (not `from .utils.config import TOKEN`)
  Exception: within the `bot/` package itself, relative imports (`from .utils...`)
  are used in `bot/__init__.py` and `bot/bot.py`.
- Wildcard imports (`from bot.utils.config import *`) are used in some handler
  files. This is the existing pattern; follow it for consistency in those files.
- Standard library imports come first, then third-party, then local -- but there
  are no isort or import-ordering tools enforced.

### Async Patterns

- All Telegram handler functions are `async def`.
- Use `async with get_lock(user_id)` to serialize per-user processing.
- Use `await` for all Telegram API calls and OpenRouter async calls.

### Type Hints

- Handler function signatures follow the `python-telegram-bot` convention:
  ```python
  async def handler_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
  ```
- Add type hints to utility function signatures and return types.
- Module-level state dicts are annotated at declaration:
  ```python
  conversations: dict[int, list[dict]] = {}
  ```

### Error Handling

- Wrap external API calls (OpenRouter) in `try/except Exception as e`.
- Log errors with `logger.error(...)` including the exception.
- Send a user-friendly message on failure; never expose tracebacks to users.
- On API failure, roll back state (e.g., `history.pop()` to remove the
  unanswered user message).

### Logging

- Use the shared logger from `bot.utils.logger`:
  ```python
  from bot.utils.logger import logger
  ```
- Use `logger.info` for operational events, `logger.debug` for detailed traces,
  `logger.error` for failures.
- Use `%s` style formatting (not f-strings) in logger calls for lazy evaluation:
  ```python
  logger.error("API error: %s", e)        # correct
  logger.error(f"API error: {e}")          # avoid
  ```

### Telegram Message Formatting

- Use `parse_mode="Markdown"` for formatted replies.
- Wrap model names and code in backticks in user-facing messages.
- Long messages (>4096 chars) must be chunked before sending.
- Provide a plain-text fallback if Markdown parsing fails:
  ```python
  try:
      await update.message.reply_text(chunk, parse_mode="Markdown")
  except Exception:
      await update.message.reply_text(chunk)
  ```

### Authorization

- All command and message handlers must be wrapped with `authorized_only()`:
  ```python
  app.add_handler(CommandHandler("help", authorized_only(help_cmd)))
  ```
- The decorator checks `update.effective_user.id` against `ALLOWED_USER_IDS`.

### Adding a New Command

1. Create the handler function in `bot/handlers/commands.py` (or a new handler file).
2. Follow the signature: `async def mycommand_cmd(update, context)`.
3. Register it in `bot/bot.py` with `authorized_only`:
   ```python
   app.add_handler(CommandHandler("mycommand", authorized_only(mycommand_cmd)))
   ```
4. Add the import to `bot/__init__.py` and include it in `__all__`.
5. Add a line to the `/commands` help text in `commands_cmd`.

### Docstrings

- Use docstrings on non-trivial functions. Google style is preferred.
- Simple command handlers that are self-explanatory may omit docstrings.
- `# noinspection PyUnusedLocal` is used above handlers where `context` is
  unused; keep this pattern for PyCharm compatibility.

### Configuration

- All configuration lives in `bot/utils/config.py`.
- Key constants:
  - `TOKEN` - Telegram bot API key
  - `API_KEY` - OpenRouter API key
  - `DEFAULT_MODEL` - Default AI model (x-ai/grok-4.1-fast)
  - `MAX_HISTORY_MESSAGES` - Max conversation history per user (80)
  - `PROMPTS` - System prompts loaded from assistant_prompt.md and roleplay_prompt.md
  - `ALLOWED_MODELS` - List of permitted AI models
  - `ALLOWED_USER_IDS` - Set of authorized user IDs
- To add a new model, append it to `ALLOWED_MODELS`.
- To add a new allowed user, add their numeric ID to `ALLOWED_USER_IDS`
  (or set up another env var).

### State Management

- All runtime state is in `bot/utils/state.py` as module-level dicts.
- State is keyed by `user_id: int`.
- State is not persisted -- it resets on bot restart.
- Key state variables:
  - `conversations` - Per-user message history
  - `user_models` - Per-user selected model
  - `last_usage` - Per-user API token usage tracking
  - `_user_locks` - Per-user async locks for serializing requests
  - `plugin_settings` - Per-user plugin enabled states (e.g., web search)
- Helper functions: `get_lock()`, `get_model()`, `get_history()`, `set_web_search()`, `is_web_search_enabled()`

### Git Conventions

- Branch: `master`
- Keep commits focused. Existing messages are terse ("Update"); prefer
  slightly more descriptive messages for new work.
- Never commit `.env`, credentials, or API keys.
