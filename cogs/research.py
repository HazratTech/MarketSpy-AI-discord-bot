"""
MarketSpy AI - Product Research Cog
Slash command /product-research to analyze niche potential, competition, and margins.
Uses modern discord.ui.LayoutView.
"""

import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from services.ai.factory import AIFactory
from ui.layouts import create_research_layout, create_error_layout
from database.repository import Repository

logger = logging.getLogger("MarketSpyAI.ResearchCog")


class ResearchCog(commands.Cog, name="Product Research"):
    """Cog for analyzing product niches, competition, and market viability."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="product-research",
        description="Deep AI analysis of niche demand, competition, pricing sweet spots, and risk scores.",
    )
    @app_commands.describe(
        niche_or_product="Product idea or niche keyword (e.g. 'Ceramic Self-Heating Coffee Mug')",
        marketplace="Target marketplace for market context",
        budget_range="Estimated initial budget or test capital (e.g. '$1,000 - $3,000')",
        ai_provider="Choose AI engine (Default: server setting / Gemini)",
    )
    @app_commands.choices(
        marketplace=[
            app_commands.Choice(name="Amazon", value="Amazon"),
            app_commands.Choice(name="eBay", value="eBay"),
            app_commands.Choice(name="Etsy", value="Etsy"),
            app_commands.Choice(name="Shopify", value="Shopify"),
            app_commands.Choice(name="TikTok Shop", value="TikTok Shop"),
        ],
        ai_provider=[
            app_commands.Choice(name="Google Gemini (Gemini 3.8 Flash - Fast)", value="gemini"),
            app_commands.Choice(name="OpenAI (GPT-5 Flagship - Deep Reasoning)", value="openai"),
            app_commands.Choice(name="Anthropic Claude (Claude 3.5 Sonnet)", value="claude"),
        ],
    )
    async def product_research(
        self,
        interaction: discord.Interaction,
        niche_or_product: str,
        marketplace: app_commands.Choice[str],
        budget_range: Optional[str] = None,
        ai_provider: Optional[app_commands.Choice[str]] = None,
    ):
        # 1. Defer interaction to prevent Discord timeout
        await interaction.response.defer(thinking=True)

        try:
            # 2. Resolve AI provider
            provider_key = ai_provider.value if ai_provider else None
            provider = AIFactory.get_provider(provider_key)

            # 3. Call AI product research
            research_data = await provider.analyze_product(
                niche_or_product=niche_or_product,
                marketplace=marketplace.value,
                budget_range=budget_range,
            )

            # 4. Log to PostgreSQL
            guild_id = interaction.guild_id if interaction.guild else None
            await Repository.record_query_log(
                user_id=interaction.user.id,
                username=interaction.user.name,
                guild_id=guild_id,
                command="product-research",
                marketplace=marketplace.value,
                provider=provider.provider_name,
                status="success",
                query_input=f"Niche/Product: {niche_or_product} | Budget: {budget_range or 'N/A'}",
                query_result=research_data,
            )

            # 5. Send rich response LayoutView
            layout_view = create_research_layout(
                niche_or_product=niche_or_product,
                marketplace=marketplace.value,
                data=research_data,
                provider=provider.provider_name,
            )
            await interaction.followup.send(view=layout_view)

        except Exception as e:
            logger.error("Error executing /product-research: %s", e)
            error_layout = create_error_layout(
                f"Failed to analyze product with AI: {e}\n\n"
                f"_Tip: Ensure your GEMINI_API_KEY or OPENAI_API_KEY is properly set in .env._"
            )
            await interaction.followup.send(view=error_layout)


async def setup(bot: commands.Bot):
    await bot.add_cog(ResearchCog(bot))
