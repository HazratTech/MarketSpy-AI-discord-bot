"""
MarketSpy AI - Main Bot Application Entry Point
Discord e-commerce intelligence bot for Amazon, eBay, Etsy, Shopify, and TikTok Shop.
"""

import sys
import asyncio
import logging
import discord
from discord.ext import commands

from config import config, logger
from database.db import db
from database.repository import Repository

# Extension Cogs to load
EXTENSIONS = [
    "cogs.calculator",
    "cogs.listing",
    "cogs.research",
    "cogs.competitor",
    "cogs.help",
]


class MarketSpyBot(commands.Bot):
    """Custom bot class with async lifecycle and database initialization."""

    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix=config.bot_prefix,
            intents=intents,
            help_command=None,  # We use our custom /help slash command
        )

    async def setup_hook(self):
        """Asynchronous initialization before bot connects to Discord."""
        logger.info("Initializing MarketSpy AI services...")

        # 1. Initialize PostgreSQL Connection Pool
        await db.connect()

        # 2. Load Cogs
        for ext in EXTENSIONS:
            try:
                await self.load_extension(ext)
                logger.info("Loaded extension: %s", ext)
            except Exception as e:
                logger.error("Failed to load extension %s: %s", ext, e)

        # 3. Synchronize application slash commands with Discord
        try:
            synced = await self.tree.sync()
            logger.info("Synchronized %d global application slash commands.", len(synced))
        except Exception as e:
            logger.error("Failed to sync slash commands: %s", e)

    async def on_ready(self):
        """Triggered when bot connects to Discord."""
        logger.info("==================================================")
        logger.info("MarketSpy AI is ONLINE and ready!")
        logger.info("Logged in as: %s (ID: %s)", self.user.name, self.user.id)
        logger.info("Connected to %d servers / guilds", len(self.guilds))
        logger.info("==================================================")

        # Set rich activity
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="E-Commerce Marketplaces | /help",
        )
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_guild_join(self, guild: discord.Guild):
        """Triggered when the bot is added to a new Discord server."""
        logger.info("Joined new guild: %s (ID: %s)", guild.name, guild.id)
        await Repository.get_or_create_guild(
            guild_id=guild.id,
            guild_name=guild.name,
            preferred_ai=config.default_ai_provider,
            currency=config.default_currency,
        )

    async def close(self):
        """Gracefully closes bot, AI sessions, and database connections."""
        logger.info("Shutting down MarketSpy AI...")
        from services.ai.factory import AIFactory
        await AIFactory.close_all()
        await db.close()
        await super().close()


def main():
    """Entry point execution."""
    if not config.discord_token or config.discord_token == "your_discord_bot_token_here":
        logger.error(
            "DISCORD_BOT_TOKEN is not set in .env! Please set your bot token before starting."
        )
        sys.exit(1)

    bot = MarketSpyBot()
    bot.run(config.discord_token)


if __name__ == "__main__":
    main()
