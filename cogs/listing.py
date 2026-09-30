"""
MarketSpy AI - Listing Optimizer Cog
Slash command /optimize-listing using modern discord.ui.LayoutView.
"""

import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from services.ai.factory import AIFactory
from ui.layouts import create_listing_layout, create_error_layout
from database.repository import Repository

logger = logging.getLogger("MarketSpyAI.ListingCog")


class ListingCog(commands.Cog, name="Listing Optimizer"):
    """Cog for generating optimized e-commerce product listings."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="optimize-listing",
        description="Generate high-converting titles, bullet points, and SEO descriptions for any marketplace.",
    )
    @app_commands.describe(
        product_name="Product title or core keyword (e.g. 'Magnetic Wireless Power Bank')",
        marketplace="Target e-commerce platform for formatting & SEO rules",
        key_features="Core product features, materials, and benefits separated by commas",
        target_audience="Target buyer persona (e.g. 'Travelers, iPhone users')",
        ai_provider="Choose AI engine to generate the listing (Default: server setting / Gemini)",
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
            app_commands.Choice(name="Google Gemini (Fast & Creative)", value="gemini"),
            app_commands.Choice(name="OpenAI (GPT-4o)", value="openai"),
            app_commands.Choice(name="Anthropic Claude (High Detail)", value="claude"),
        ],
    )
    async def optimize_listing(
        self,
        interaction: discord.Interaction,
        product_name: str,
        marketplace: app_commands.Choice[str],
        key_features: str,
        target_audience: Optional[str] = None,
        ai_provider: Optional[app_commands.Choice[str]] = None,
    ):
        # 1. Defer interaction to prevent Discord timeout
        await interaction.response.defer(thinking=True)

        try:
            # 2. Resolve AI provider
            provider_key = ai_provider.value if ai_provider else None
            provider = AIFactory.get_provider(provider_key)

            # 3. Call AI optimization
            listing_data = await provider.optimize_listing(
                product_name=product_name,
                marketplace=marketplace.value,
                key_features=key_features,
                target_audience=target_audience,
            )

            # 4. Log to PostgreSQL
            guild_id = interaction.guild_id if interaction.guild else None
            await Repository.record_query_log(
                user_id=interaction.user.id,
                username=interaction.user.name,
                guild_id=guild_id,
                command="optimize-listing",
                marketplace=marketplace.value,
                provider=provider.provider_name,
                status="success",
            )

            # 5. Send rich response LayoutView
            layout_view = create_listing_layout(
                product_name=product_name,
                marketplace=marketplace.value,
                data=listing_data,
                provider=provider.provider_name,
            )
            await interaction.followup.send(view=layout_view)

        except Exception as e:
            logger.error("Error executing /optimize-listing: %s", e)
            error_layout = create_error_layout(
                f"Failed to generate listing with AI: {e}\n\n"
                f"_Tip: Ensure your GEMINI_API_KEY or OPENAI_API_KEY is properly set in .env._"
            )
            await interaction.followup.send(view=error_layout)


async def setup(bot: commands.Bot):
    await bot.add_cog(ListingCog(bot))
