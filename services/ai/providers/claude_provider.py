"""
MarketSpy AI - Anthropic Claude Provider
Implements BaseAIProvider using Anthropic AsyncAnthropic client.
Pre-scaffolded to enable Claude models with zero bot modifications.
"""

import logging
from typing import Dict, Any, Optional
from anthropic import AsyncAnthropic
from services.ai.base import BaseAIProvider
from services.ai.utils import clean_and_parse_json
from services.ai.prompts import (
    SYSTEM_PROMPT_BASE,
    LISTING_OPTIMIZER_PROMPT,
    PRODUCT_RESEARCH_PROMPT,
    COMPETITOR_AUDIT_PROMPT,
    GENERAL_ASSISTANT_SYSTEM,
)
from config import config

logger = logging.getLogger("MarketSpyAI.Claude")


class ClaudeProvider(BaseAIProvider):
    """Anthropic Claude API implementation."""

    def __init__(self, model_name: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(
            model_name=model_name or config.claude_model,
            api_key=api_key or config.anthropic_api_key,
        )
        if self.api_key and self.api_key != "your_anthropic_api_key_here":
            self.client = AsyncAnthropic(api_key=self.api_key)
            self.is_configured = True
        else:
            self.client = None
            self.is_configured = False
            logger.info("ClaudeProvider: ANTHROPIC_API_KEY is not set (ready for plug-in).")

    @property
    def provider_name(self) -> str:
        return "claude"

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.is_configured or not self.client:
            raise RuntimeError(
                "Claude API key is not configured. Please set ANTHROPIC_API_KEY in .env to use Claude."
            )

        response = await self.client.messages.create(
            model=self.model_name,
            max_tokens=2048,
            system=system_prompt or SYSTEM_PROMPT_BASE,
            messages=[{"role": "user", "content": prompt}],
        )
        # Anthropic message content is a list of blocks
        text_blocks = [b.text for b in response.content if hasattr(b, "text")]
        return "\n".join(text_blocks)

    async def optimize_listing(
        self,
        product_name: str,
        marketplace: str,
        key_features: str,
        target_audience: Optional[str] = None,
    ) -> Dict[str, Any]:
        prompt = LISTING_OPTIMIZER_PROMPT.format(
            marketplace=marketplace,
            product_name=product_name,
            key_features=key_features,
            target_audience=target_audience or "General e-commerce shoppers",
        )
        raw_text = await self.generate_text(prompt)
        return clean_and_parse_json(raw_text)

    async def analyze_product(
        self,
        niche_or_product: str,
        marketplace: str,
        budget_range: Optional[str] = None,
    ) -> Dict[str, Any]:
        prompt = PRODUCT_RESEARCH_PROMPT.format(
            marketplace=marketplace,
            niche_or_product=niche_or_product,
            budget_range=budget_range or "Not specified ($500 - $3,000 initial test)",
        )
        raw_text = await self.generate_text(prompt)
        return clean_and_parse_json(raw_text)

    async def audit_competitor(
        self,
        competitor_data: str,
        marketplace: str,
        details: Optional[str] = None,
    ) -> Dict[str, Any]:
        prompt = COMPETITOR_AUDIT_PROMPT.format(
            marketplace=marketplace,
            competitor_data=competitor_data,
            details=details or "Standard competitor listing audit",
        )
        raw_text = await self.generate_text(prompt)
        return clean_and_parse_json(raw_text)

    async def ask_assistant(self, question: str) -> str:
        return await self.generate_text(question, system_prompt=GENERAL_ASSISTANT_SYSTEM)

    async def close(self) -> None:
        if self.client:
            await self.client.close()
            self.client = None
