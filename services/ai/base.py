"""
MarketSpy AI - Base AI Provider Interface
Defines the abstract contract for all AI LLM providers according to SOLID principles.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseAIProvider(ABC):
    """Abstract interface that every LLM provider must implement."""

    def __init__(self, model_name: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns the human-readable identifier of the provider (e.g. 'gemini', 'openai', 'claude')."""
        pass

    @abstractmethod
    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generates raw text response for arbitrary prompts."""
        pass

    @abstractmethod
    async def optimize_listing(
        self,
        product_name: str,
        marketplace: str,
        key_features: str,
        target_audience: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generates an optimized e-commerce listing:
        - title: High-CTR title
        - bullet_points: 5 benefit-driven bullet points
        - description: SEO-optimized product description
        - backend_keywords: Search terms for indexing
        """
        pass

    @abstractmethod
    async def analyze_product(
        self,
        niche_or_product: str,
        marketplace: str,
        budget_range: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyzes product viability and market opportunity:
        - demand_level: High / Medium / Low
        - target_audience: Customer demographic profile
        - pricing_sweet_spot: Suggested price range & margins
        - competition_rating: Low / Moderate / Fierce
        - differentiation_angles: 3 actionable USPs
        - opportunity_score: Float out of 10
        - strategic_verdict: Executive summary
        """
        pass

    @abstractmethod
    async def audit_competitor(
        self,
        competitor_data: str,
        marketplace: str,
        details: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Audits a competitor listing:
        - strengths: What they do well
        - weaknesses: Customer friction points and gaps
        - counter_strategy: How to beat them on price, bundle, or messaging
        - recommended_usp: Suggested unique value proposition
        """
        pass

    @abstractmethod
    async def ask_assistant(self, question: str) -> str:
        """General e-commerce assistant Q&A."""
        pass

    async def close(self) -> None:
        """Gracefully release any underlying HTTP sessions or client pools."""
        pass
