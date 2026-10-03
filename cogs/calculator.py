"""
MarketSpy AI - Profit Calculator Cog
Slash command /profit-calculator using modern discord.ui.LayoutView.
"""

import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from services.calculator import ProfitEngine
from ui.layouts import create_profit_layout, create_error_layout
from database.repository import Repository

logger = logging.getLogger("MarketSpyAI.CalculatorCog")


class CalculatorCog(commands.Cog, name="Profit Calculator"):
    """Cog for unit economics and marketplace profit calculations."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="profit-calculator",
        description="Calculate net profit, margins %, and ROI factoring in platform seller fees.",
    )
    @app_commands.describe(
        marketplace="E-commerce platform preset for fee calculations",
        selling_price="Final retail selling price to customer",
        cogs="Cost of Goods Sold (Unit manufacturing / sourcing cost)",
        shipping_cost="Cost to ship unit to customer or warehouse",
        ad_spend="Estimated advertising or PPC cost per unit",
        fba_tier="Amazon FBA size tier (only used if Amazon FBA is selected)",
    )
    @app_commands.choices(
        marketplace=[
            app_commands.Choice(name="Amazon FBA (Fulfillment by Amazon)", value="amazon_fba"),
            app_commands.Choice(name="Amazon FBM (Merchant Fulfilled)", value="amazon_fbm"),
            app_commands.Choice(name="eBay (Final Value Fee 13.25% + $0.30)", value="ebay"),
            app_commands.Choice(name="Etsy (6.5% + 3% + $0.45)", value="etsy"),
            app_commands.Choice(name="Shopify (Shopify Payments 2.9% + $0.30)", value="shopify"),
            app_commands.Choice(name="TikTok Shop (6.0% commission + $0.30)", value="tiktok"),
        ],
        fba_tier=[
            app_commands.Choice(name="Standard Size (~$4.75 FBA Fee)", value="standard"),
            app_commands.Choice(name="Small Standard (~$3.25 FBA Fee)", value="small"),
            app_commands.Choice(name="Large Standard (~$6.50 FBA Fee)", value="large"),
            app_commands.Choice(name="Oversize (~$10.50 FBA Fee)", value="oversize"),
        ],
    )
    async def profit_calculator(
        self,
        interaction: discord.Interaction,
        marketplace: app_commands.Choice[str],
        selling_price: float,
        cogs: float,
        shipping_cost: float = 0.0,
        ad_spend: float = 0.0,
        fba_tier: Optional[app_commands.Choice[str]] = None,
    ):
        # 1. Defer interaction immediately to guarantee 3-second Discord acknowledgment
        await interaction.response.defer()

        try:
            # 2. Validation
            if selling_price <= 0:
                error_layout = create_error_layout("Selling price must be greater than $0.00.")
                await interaction.followup.send(view=error_layout, ephemeral=True)
                return

            if cogs < 0 or shipping_cost < 0 or ad_spend < 0:
                error_layout = create_error_layout("Costs cannot be negative numbers.")
                await interaction.followup.send(view=error_layout, ephemeral=True)
                return

            # 3. Calculation
            tier_val = fba_tier.value if fba_tier else "standard"
            res = ProfitEngine.calculate(
                marketplace=marketplace.value,
                selling_price=selling_price,
                cogs=cogs,
                shipping_cost=shipping_cost,
                ad_spend=ad_spend,
                fba_tier=tier_val,
                currency="USD",
            )

            # 4. Log query to PostgreSQL
            guild_id = interaction.guild_id if interaction.guild else None
            calc_input = (
                f"Selling: ${selling_price:.2f}, COGS: ${cogs:.2f}, "
                f"Shipping: ${shipping_cost:.2f}, Ad Spend: ${ad_spend:.2f}"
            )
            if fba_tier:
                calc_input += f", FBA Tier: {tier_val}"
            await Repository.record_query_log(
                user_id=interaction.user.id,
                username=interaction.user.name,
                guild_id=guild_id,
                command="profit-calculator",
                marketplace=marketplace.value,
                provider="math_engine",
                status="success",
                query_input=calc_input,
                query_result={
                    "net_profit": res.net_profit,
                    "net_margin_pct": res.net_margin_pct,
                    "roi_pct": res.roi_pct,
                    "total_costs": res.total_costs,
                },
            )

            # 5. Display result with LayoutView via followup
            layout_view = create_profit_layout(res)
            await interaction.followup.send(view=layout_view)

        except Exception as e:
            logger.error("Error executing /profit-calculator: %s", e)
            error_layout = create_error_layout(f"Failed to calculate profit: {e}")
            if interaction.response.is_done():
                await interaction.followup.send(view=error_layout)
            else:
                await interaction.response.send_message(view=error_layout, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CalculatorCog(bot))
