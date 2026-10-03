"""
MarketSpy AI - Configuration Module
Loads, validates, and provides centralized access to application settings.
"""

import os
import logging
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("MarketSpyAI.Config")


@dataclass(frozen=True)
class BotConfig:
    # Discord
    discord_token: str = os.getenv("DISCORD_BOT_TOKEN", "").strip("'\"")
    bot_prefix: str = os.getenv("BOT_PREFIX", "!").strip("'\"")

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:password@localhost:5432/marketspy_ai"
    ).strip("'\"")

    # AI Defaults
    default_ai_provider: str = os.getenv("DEFAULT_AI_PROVIDER", "gemini").strip("'\"").lower()

    # Google Gemini
    gemini_api_key: Optional[str] = (
        os.getenv("GEMINI_API_KEY").strip("'\"") if os.getenv("GEMINI_API_KEY") else None
    )
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip("'\"")

    # OpenAI Flagship
    openai_api_key: Optional[str] = (
        os.getenv("OPENAI_API_KEY").strip("'\"") if os.getenv("OPENAI_API_KEY") else None
    )
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5").strip("'\"")

    # Claude / Anthropic Flagship
    anthropic_api_key: Optional[str] = (
        os.getenv("ANTHROPIC_API_KEY").strip("'\"") if os.getenv("ANTHROPIC_API_KEY") else None
    )
    claude_model: str = os.getenv("CLAUDE_MODEL", "sonnet-5.5").strip("'\"")

    # General Defaults
    default_currency: str = os.getenv("DEFAULT_CURRENCY", "USD").strip("'\"")

    def validate(self) -> None:
        """Validates critical settings and logs warnings for missing optional keys."""
        if not self.discord_token or self.discord_token == "your_discord_bot_token_here":
            logger.warning(
                "DISCORD_BOT_TOKEN is not set or using placeholder! Bot will not be able to log in to Discord."
            )

        # Check AI keys
        available_ai = []
        if self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here":
            available_ai.append("Google Gemini")
        if self.openai_api_key and self.openai_api_key != "your_openai_api_key_here":
            available_ai.append("OpenAI")
        if self.anthropic_api_key and self.anthropic_api_key != "your_anthropic_api_key_here":
            available_ai.append("Anthropic Claude")

        if available_ai:
            logger.info("Configured AI Providers available: %s", ", ".join(available_ai))
        else:
            logger.warning(
                "No AI API keys configured! Please set GEMINI_API_KEY or OPENAI_API_KEY in .env."
            )


config = BotConfig()
config.validate()
