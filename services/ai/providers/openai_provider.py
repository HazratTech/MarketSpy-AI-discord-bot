"""
MarketSpy AI - OpenAI Provider
Implements BaseAIProvider using OpenAI AsyncClient (gpt-4o / gpt-4o-mini).
"""

import logging
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
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

logger = logging.getLogger("MarketSpyAI.OpenAI")


class OpenAIProvider(BaseAIProvider):
    """OpenAI API implementation."""

    def __init__(self, model_name: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(
            model_name=model_name or config.openai_model,
            api_key=api_key or config.openai_api_key,
        )
        if self.api_key and self.api_key != "your_openai_api_key_here":
            self.client = AsyncOpenAI(api_key=self.api_key)
            self.is_configured = True
        else:
            self.client = None
            self.is_configured = False
            logger.warning("OpenAIProvider: OPENAI_API_KEY is not set.")

    @property
    def provider_name(self) -> str:
        return "openai"

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.is_configured or not self.client:
            raise RuntimeError("OpenAI API key is not configured. Please set OPENAI_API_KEY in .env.")

        messages = [
            {"role": "system", "content": system_prompt or SYSTEM_PROMPT_BASE},
            {"role": "user", "content": prompt},
        ]
        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content or ""

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
