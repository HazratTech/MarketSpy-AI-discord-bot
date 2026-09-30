"""
MarketSpy AI - Profit Calculation Engine
Combines platform fee breakdown with unit economics (COGS, shipping, ad spend).
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from services.calculator.fee_models import MarketplaceFeeCalculator, PlatformFeeBreakdown


@dataclass
class ProfitCalculationResult:
    marketplace: str
    selling_price: float
    cogs: float
    shipping_cost: float
    ad_spend: float
    total_costs: float
    platform_fees: PlatformFeeBreakdown
    net_profit: float
    net_margin_pct: float
    roi_pct: float
    health_status: str  # "EXCELLENT", "HEALTHY", "MODERATE", "UNPROFITABLE"
    health_emoji: str
    currency: str = "USD"


class ProfitEngine:
    """Calculates comprehensive unit economics and margin metrics."""

    @classmethod
    def calculate(
        cls,
        marketplace: str,
        selling_price: float,
        cogs: float,
        shipping_cost: float = 0.0,
        ad_spend: float = 0.0,
        fba_tier: str = "standard",
        currency: str = "USD",
    ) -> ProfitCalculationResult:
        marketplace_key = marketplace.lower().strip()

        # 1. Fetch platform fee breakdown
        if "fba" in marketplace_key:
            fees = MarketplaceFeeCalculator.calculate_amazon_fba(selling_price, fba_tier)
        elif "amazon" in marketplace_key:
            fees = MarketplaceFeeCalculator.calculate_amazon_fbm(selling_price)
        elif "ebay" in marketplace_key:
            fees = MarketplaceFeeCalculator.calculate_ebay(selling_price)
        elif "etsy" in marketplace_key:
            fees = MarketplaceFeeCalculator.calculate_etsy(selling_price)
        elif "shopify" in marketplace_key:
            fees = MarketplaceFeeCalculator.calculate_shopify(selling_price)
        elif "tiktok" in marketplace_key:
            fees = MarketplaceFeeCalculator.calculate_tiktok_shop(selling_price)
        else:
            # Default to standard marketplace 15% model
            fees = MarketplaceFeeCalculator.calculate_amazon_fbm(selling_price)

        # 2. Total Costs = Platform Fees + COGS + Shipping + Ad Spend
        total_costs = fees.total_platform_fees + cogs + shipping_cost + ad_spend
        net_profit = round(selling_price - total_costs, 2)

        # 3. Margins & ROI
        net_margin_pct = round((net_profit / selling_price) * 100, 2) if selling_price > 0 else 0.0
        investment_basis = cogs + shipping_cost + ad_spend
        roi_pct = round((net_profit / investment_basis) * 100, 2) if investment_basis > 0 else 0.0

        # 4. Determine Health Status
        if net_profit <= 0:
            health_status = "UNPROFITABLE / LOSS"
            health_emoji = "🔴"
        elif net_margin_pct < 15:
            health_status = "TIGHT MARGIN (High Risk)"
            health_emoji = "🟡"
        elif net_margin_pct < 30:
            health_status = "HEALTHY (Standard E-Com)"
            health_emoji = "🟢"
        else:
            health_status = "EXCELLENT (High Profit)"
            health_emoji = "🚀"

        return ProfitCalculationResult(
            marketplace=fees.platform_name,
            selling_price=round(selling_price, 2),
            cogs=round(cogs, 2),
            shipping_cost=round(shipping_cost, 2),
            ad_spend=round(ad_spend, 2),
            total_costs=round(total_costs, 2),
            platform_fees=fees,
            net_profit=net_profit,
            net_margin_pct=net_margin_pct,
            roi_pct=roi_pct,
            health_status=health_status,
            health_emoji=health_emoji,
            currency=currency,
        )
