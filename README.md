# My Telegram Bot

A Telegram bot that routes user messages to LLMs via the OpenRouter API. Built with Python 3.11+, using `python-telegram-bot` for the Telegram interface and `openrouter` for AI completions. All handlers are async. State is held in-memory (no database).

## Features

- **AI Conversations**: Send any message and receive AI-powered responses via OpenRouter
- **Multiple Models**: Choose from 17+ available AI models
- **Two Modes**: Switch between `assistant` and `roleplay` modes with different personalities
- **Conversation History**: Maintains context with up to 80 messages per user
- **Token Tracking**: View prompt, completion, and total token usage after each response
- **Web Search**: Toggle web search integration for real-time information
- **Authorized Users Only**: Only configured users can interact with the bot

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show how to use the bot |
| `/commands` | List all available commands |
| `/models` | Show available AI models (select via buttons) |
| `/mode` | Toggle between assistant and roleplay modes |
| `/ping` | Check bot responsiveness |
| `/reset` | Clear conversation history |
| `/status` | Show current model, mode, and history count |
| `/tokens` | Show last API token usage |
| `/websearch` | Toggle web search integration |

## Tech Stack

- Python 3.11+
- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram Bot API
- [openrouter](https://openrouter.ai/) - Unified API for LLMs
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management

## Setup

### Prerequisites

- Python 3.11 or higher
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))
- An OpenRouter API key (from [openrouter.ai](https://openrouter.ai/))

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd my-telegram-bot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate   # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_API_KEY` | Your Telegram bot token from @BotFather |
| `OPENROUTER_API_KEY` | Your OpenRouter API key |
| `MY_TELEGRAM_ID` | Your numeric Telegram user ID (to authorize yourself) |

## Running the Bot

```bash
python app.py
```

## Available AI Models

The bot supports the following models (configured in `bot/utils/config.py`):

- anthropic/claude-haiku-4.5
- deepseek/deepseek-v3.2
- ibm-granite/granite-4.0-h-micro
- minimax/minimax-m2.5
- mistralai/ministral-14b-2512
- mistralai/mistral-nemo
- mistralai/mistral-small-3.2-24b-instruct
- mistralai/mistral-small-24b-instruct-2501
- mistralai/mistral-small-creative
- moonshotai/kimi-k2.5
- nousresearch/hermes-4-70b
- openai/gpt-5-nano
- qwen/qwen3.5-397b-a17b
- x-ai/grok-4.1-fast
- xiaomi/mimo-v2-flash
- z-ai/glm-5

Default model: `x-ai/grok-4.1-fast`

## Project Structure

```
my-telegram-bot/
├── app.py                      # Entry point
├── bot/
│   ├── __init__.py             # Re-exports public symbols
│   ├── bot.py                  # Bot initialization & handler registration
│   ├── handlers/
│   │   ├── commands.py         # Command handlers
│   │   ├── message.py          # Text message handler (OpenRouter API)
│   │   └── models.py           # /model command & callbacks
│   └── utils/
│       ├── auth.py             # Authorization decorator
│       ├── config.py           # Configuration & constants
│       ├── logger.py           # Logging setup
│       └── state.py            # In-memory state management
├── assistant_prompt.md        # System prompt for assistant mode
├── roleplay_prompt.md         # System prompt for roleplay mode
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment file
├── Dockerfile                 # Docker container definition
└── railway.toml               # Railway deployment config
```

## Deployment

### Docker

```bash
docker build -t my-telegram-bot .
docker run -d --env-file .env my-telegram-bot
```

### Railway

The project includes `railway.toml` for one-click deployment on Railway:

1. `railway init`
2. `railway up`

## License

This project is licensed under the [MIT License](LICENSE).

## Linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
# Lint
ruff check .

# Lint and auto-fix
ruff check --fix .

# Format
ruff format .
```
