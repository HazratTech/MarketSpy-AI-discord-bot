"""
MarketSpy AI - Competitor Audit Cog
Slash command /competitor-audit to perform strategic listing teardowns and identify weaknesses.
Uses modern discord.ui.LayoutView.
"""

import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from services.ai.factory import AIFactory
from ui.layouts import create_competitor_layout, create_error_layout
from database.repository import Repository

logger = logging.getLogger("MarketSpyAI.CompetitorCog")


class CompetitorCog(commands.Cog, name="Competitor Audit"):
    """Cog for competitive analysis and listing teardowns."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="competitor-audit",
        description="Audit competitor listings to expose customer complaints, gaps, and winning counter-strategies.",
    )
    @app_commands.describe(
        competitor_data="Competitor product title, listing description, or key features",
        marketplace="E-commerce marketplace where competitor is selling",
        details="Additional context (e.g. competitor pricing, 1-star review themes, flaws)",
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
            app_commands.Choice(name="Google Gemini (Fast & Sharp)", value="gemini"),
            app_commands.Choice(name="OpenAI (GPT-4o)", value="openai"),
            app_commands.Choice(name="Anthropic Claude (Deep Teardown)", value="claude"),
        ],
    )
    async def competitor_audit(
        self,
        interaction: discord.Interaction,
        competitor_data: str,
        marketplace: app_commands.Choice[str],
        details: Optional[str] = None,
        ai_provider: Optional[app_commands.Choice[str]] = None,
    ):
        # 1. Defer interaction to prevent Discord timeout
        await interaction.response.defer(thinking=True)

        try:
            # 2. Resolve AI provider
            provider_key = ai_provider.value if ai_provider else None
            provider = AIFactory.get_provider(provider_key)

            # 3. Call AI competitor teardown
            audit_data = await provider.audit_competitor(
                competitor_data=competitor_data,
                marketplace=marketplace.value,
                details=details,
            )

            # 4. Log to PostgreSQL
            guild_id = interaction.guild_id if interaction.guild else None
            await Repository.record_query_log(
                user_id=interaction.user.id,
                username=interaction.user.name,
                guild_id=guild_id,
                command="competitor-audit",
                marketplace=marketplace.value,
                provider=provider.provider_name,
                status="success",
            )

            # 5. Send rich response LayoutView
            layout_view = create_competitor_layout(
                marketplace=marketplace.value,
                data=audit_data,
                provider=provider.provider_name,
            )
            await interaction.followup.send(view=layout_view)

        except Exception as e:
            logger.error("Error executing /competitor-audit: %s", e)
            error_layout = create_error_layout(
                f"Failed to audit competitor with AI: {e}\n\n"
                f"_Tip: Ensure your GEMINI_API_KEY or OPENAI_API_KEY is properly set in .env._"
            )
            await interaction.followup.send(view=error_layout)


async def setup(bot: commands.Bot):
    await bot.add_cog(CompetitorCog(bot))
