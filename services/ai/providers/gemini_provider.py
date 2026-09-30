"""
MarketSpy AI - Google Gemini Provider
Implements BaseAIProvider using Google Gemini API.
"""

import logging
import warnings
from typing import Dict, Any, Optional

# Suppress legacy package notice for clean terminal logs
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
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

logger = logging.getLogger("MarketSpyAI.Gemini")


class GeminiProvider(BaseAIProvider):
    """Google Gemini AI implementation."""

    def __init__(self, model_name: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(
            model_name=model_name or config.gemini_model,
            api_key=api_key or config.gemini_api_key,
        )
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            genai.configure(api_key=self.api_key)
            self._model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=SYSTEM_PROMPT_BASE,
            )
            self.is_configured = True
        else:
            self._model = None
            self.is_configured = False
            logger.warning("GeminiProvider: GEMINI_API_KEY is not set.")

    @property
    def provider_name(self) -> str:
        return "gemini"

    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.is_configured or not self._model:
            raise RuntimeError("Gemini API key is not configured. Please set GEMINI_API_KEY in .env.")

        models_to_try = [self.model_name, "gemini-3.8-flash", "gemini-flash-latest"]
        last_error = None

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_prompt or SYSTEM_PROMPT_BASE,
                )
                response = await model.generate_content_async(prompt)
                return response.text or ""
            except Exception as e:
                last_error = e
                logger.warning("Gemini model '%s' failed (%s). Attempting fallback...", model_name, e)

        raise last_error or RuntimeError("Failed to generate content with Gemini.")

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
