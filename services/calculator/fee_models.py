"""
MarketSpy AI - Marketplace Fee Models
Implements realistic platform fee structures for major e-commerce platforms.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PlatformFeeBreakdown:
    platform_name: str
    referral_or_commission_fee: float
    fulfillment_or_fixed_fee: float
    payment_processing_fee: float
    total_platform_fees: float
    notes: str


class MarketplaceFeeCalculator:
    """Calculates platform-specific seller fees."""

    @staticmethod
    def calculate_amazon_fba(selling_price: float, fba_tier: str = "standard") -> PlatformFeeBreakdown:
        """
        Amazon FBA Fee calculation:
        - 15% referral fee (min $0.30)
        - FBA fulfillment fee based on standard size tiers
        - Est. 30-day storage fee (~$0.40)
        """
        referral_fee = max(selling_price * 0.15, 0.30)
        
        # FBA fulfillment fee estimate
        fulfillment_fees = {
            "small": 3.25,
            "standard": 4.75,
            "large": 6.50,
            "oversize": 10.50,
        }
        fba_fee = fulfillment_fees.get(fba_tier.lower(), 4.75)
        storage_fee = 0.40
        total_fulfillment = fba_fee + storage_fee

        total_fees = referral_fee + total_fulfillment
        return PlatformFeeBreakdown(
            platform_name="Amazon FBA",
            referral_or_commission_fee=round(referral_fee, 2),
            fulfillment_or_fixed_fee=round(total_fulfillment, 2),
            payment_processing_fee=0.0,  # Included in Amazon referral
            total_platform_fees=round(total_fees, 2),
            notes=f"15% referral (${referral_fee:.2f}) + FBA fulfillment & storage (${total_fulfillment:.2f})"
        )

    @staticmethod
    def calculate_amazon_fbm(selling_price: float) -> PlatformFeeBreakdown:
        """Amazon FBM: 15% referral fee (merchant ships)."""
        referral_fee = max(selling_price * 0.15, 0.30)
        return PlatformFeeBreakdown(
            platform_name="Amazon FBM",
            referral_or_commission_fee=round(referral_fee, 2),
            fulfillment_or_fixed_fee=0.0,
            payment_processing_fee=0.0,
            total_platform_fees=round(referral_fee, 2),
            notes=f"15% referral fee (Merchant fulfilled shipping)"
        )

    @staticmethod
    def calculate_ebay(selling_price: float) -> PlatformFeeBreakdown:
        """eBay: 13.25% Final Value Fee + $0.30 fixed per order."""
        variable_fee = selling_price * 0.1325
        fixed_fee = 0.30
        total_fees = variable_fee + fixed_fee
        return PlatformFeeBreakdown(
            platform_name="eBay",
            referral_or_commission_fee=round(variable_fee, 2),
            fulfillment_or_fixed_fee=round(fixed_fee, 2),
            payment_processing_fee=0.0,  # Managed payments included in final value fee
            total_platform_fees=round(total_fees, 2),
            notes="13.25% Final Value Fee + $0.30 order fee"
        )

    @staticmethod
    def calculate_etsy(selling_price: float) -> PlatformFeeBreakdown:
        """
        Etsy:
        - $0.20 listing fee
        - 6.5% transaction fee
        - 3.0% + $0.25 payment processing
        """
        transaction_fee = selling_price * 0.065
        payment_fee = (selling_price * 0.03) + 0.25
        listing_fee = 0.20
        total_fees = transaction_fee + payment_fee + listing_fee
        return PlatformFeeBreakdown(
            platform_name="Etsy",
            referral_or_commission_fee=round(transaction_fee, 2),
            fulfillment_or_fixed_fee=round(listing_fee, 2),
            payment_processing_fee=round(payment_fee, 2),
            total_platform_fees=round(total_fees, 2),
            notes="6.5% transaction + 3% + $0.25 payment processing + $0.20 listing"
        )

    @staticmethod
    def calculate_shopify(selling_price: float) -> PlatformFeeBreakdown:
        """Shopify (Standard Shopify Payments): 2.9% + $0.30."""
        payment_fee = (selling_price * 0.029) + 0.30
        return PlatformFeeBreakdown(
            platform_name="Shopify",
            referral_or_commission_fee=0.0,
            fulfillment_or_fixed_fee=0.30,
            payment_processing_fee=round(payment_fee, 2),
            total_platform_fees=round(payment_fee, 2),
            notes="Shopify Payments (2.9% + $0.30 per transaction)"
        )

    @staticmethod
    def calculate_tiktok_shop(selling_price: float) -> PlatformFeeBreakdown:
        """TikTok Shop: 6% commission + $0.30 transaction fee."""
        commission_fee = selling_price * 0.06
        fixed_fee = 0.30
        total_fees = commission_fee + fixed_fee
        return PlatformFeeBreakdown(
            platform_name="TikTok Shop",
            referral_or_commission_fee=round(commission_fee, 2),
            fulfillment_or_fixed_fee=round(fixed_fee, 2),
            payment_processing_fee=0.0,
            total_platform_fees=round(total_fees, 2),
            notes="6.0% commission + $0.30 referral fee"
        )
