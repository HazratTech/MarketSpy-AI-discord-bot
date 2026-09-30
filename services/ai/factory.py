"""
MarketSpy AI - AI Provider Factory
Resolves and returns the configured AI provider dynamically (SOLID Open/Closed Principle).
"""

import logging
from typing import Dict, Optional
from services.ai.base import BaseAIProvider
from services.ai.providers.gemini_provider import GeminiProvider
from services.ai.providers.openai_provider import OpenAIProvider
from services.ai.providers.claude_provider import ClaudeProvider
from config import config

logger = logging.getLogger("MarketSpyAI.AIFactory")


class AIFactory:
    """Factory to instantiate and cache AI providers."""

    _providers: Dict[str, BaseAIProvider] = {}

    @classmethod
    def get_provider(cls, provider_name: Optional[str] = None) -> BaseAIProvider:
        """
        Returns the requested provider (gemini, openai, claude).
        Falls back to default_ai_provider or first available configured provider.
        """
        name = (provider_name or config.default_ai_provider).lower().strip()

        # Cache check
        if name in cls._providers:
            return cls._providers[name]

        # Instantiation
        if name == "gemini":
            provider = GeminiProvider()
        elif name == "openai":
            provider = OpenAIProvider()
        elif name == "claude":
            provider = ClaudeProvider()
        else:
            logger.warning("Unknown AI provider '%s'. Falling back to Gemini.", name)
            provider = GeminiProvider()

        # If selected provider is not configured, find an alternative
        if not getattr(provider, "is_configured", True):
            if config.gemini_api_key and config.gemini_api_key != "your_gemini_api_key_here":
                provider = GeminiProvider()
            elif config.openai_api_key and config.openai_api_key != "your_openai_api_key_here":
                provider = OpenAIProvider()
            elif config.anthropic_api_key and config.anthropic_api_key != "your_anthropic_api_key_here":
                provider = ClaudeProvider()

        cls._providers[name] = provider
        return provider

    @classmethod
    async def close_all(cls) -> None:
        """Gracefully closes all instantiated providers."""
        for provider in cls._providers.values():
            try:
                await provider.close()
            except Exception as e:
                logger.error("Error closing provider %s: %s", provider.provider_name, e)
        cls._providers.clear()
