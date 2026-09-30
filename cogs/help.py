"""
MarketSpy AI - Help & Status Cog
Provides /help command using modern discord.ui.LayoutView.
"""

import logging
import discord
from discord import app_commands
from discord.ext import commands
from discord import ui

from ui.colors import COLOR_PRIMARY, BRAND_FOOTER
from database.db import db
from config import config

logger = logging.getLogger("MarketSpyAI.HelpCog")


class HelpCog(commands.Cog, name="Help & Info"):
    """Cog for help information and system status."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="View all available MarketSpy AI seller commands and system status.",
    )
    async def help_command(self, interaction: discord.Interaction):
        view = ui.LayoutView(timeout=180.0)

        header_text = (
            "# 🛒 MarketSpy AI • E-Commerce Suite\n"
            "AI-powered intelligence tools designed for Amazon, eBay, Etsy, Shopify, and TikTok Shop sellers."
        )

        tools_text = (
            "### 🛠️ Core Seller Tools\n"
            "• **/profit-calculator**\n"
            "  Calculate net profit, margins %, and ROI factoring in platform fee structures (Amazon FBA, eBay, Etsy, Shopify, TikTok Shop).\n\n"
            "• **/optimize-listing**\n"
            "  Generate high-converting titles, 5 benefit-driven bullet points, SEO descriptions, and backend search terms.\n\n"
            "• **/product-research**\n"
            "  Deep AI market audit analyzing niche demand, buyer persona, pricing sweet spots, competition level, and risk scores.\n\n"
            "• **/competitor-audit**\n"
            "  Audit competitor listings to expose customer friction points, listing weaknesses, and actionable counter-strategies."
        )

        db_status = "🟢 Connected (PostgreSQL / Supabase)" if db.is_connected else "🟡 Running Local / Offline"
        system_text = (
            "### ⚙️ Architecture & Status\n"
            f"• **Database:** {db_status}\n"
            f"• **Default AI Provider:** `{config.default_ai_provider.upper()}`\n"
            f"• **Extensibility:** Modular provider system (Gemini, OpenAI, Claude ready)"
        )

        footer_text = f"_{BRAND_FOOTER}_"

        container = ui.Container(
            ui.TextDisplay(header_text),
            ui.Separator(),
            ui.TextDisplay(tools_text),
            ui.Separator(),
            ui.TextDisplay(system_text),
            ui.Separator(),
            ui.TextDisplay(footer_text),
            accent_color=COLOR_PRIMARY,
        )

        view.add_item(container)
        await interaction.response.send_message(view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))
