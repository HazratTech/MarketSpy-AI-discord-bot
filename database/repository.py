"""
MarketSpy AI - Database Repository
Encapsulates all domain-specific PostgreSQL queries for guilds, users, and audit logs.
"""

import logging
from typing import Optional, Dict, Any, List
from database.db import db

logger = logging.getLogger("MarketSpyAI.Repository")


class Repository:
    """Provides strongly-typed asynchronous repository methods."""

    @staticmethod
    async def get_or_create_guild(
        guild_id: int, guild_name: str, preferred_ai: str = "gemini", currency: str = "USD"
    ) -> Dict[str, Any]:
        """Retrieves an existing guild or inserts a new one with default settings."""
        if not db.is_connected:
            return {
                "guild_id": guild_id,
                "guild_name": guild_name,
                "preferred_ai": preferred_ai,
                "currency": currency,
                "plan_tier": "free",
            }

        select_query = "SELECT * FROM guilds WHERE guild_id = $1"
        row = await db.fetchrow(select_query, guild_id)
        if row:
            return row

        insert_query = """
        INSERT INTO guilds (guild_id, guild_name, preferred_ai, currency, plan_tier)
        VALUES ($1, $2, $3, $4, 'free')
        ON CONFLICT (guild_id) DO UPDATE 
        SET guild_name = EXCLUDED.guild_name, updated_at = CURRENT_TIMESTAMP
        RETURNING *;
        """
        row = await db.fetchrow(insert_query, guild_id, guild_name, preferred_ai, currency)
        return row or {
            "guild_id": guild_id,
            "guild_name": guild_name,
            "preferred_ai": preferred_ai,
            "currency": currency,
            "plan_tier": "free",
        }

    @staticmethod
    async def update_guild_ai_preference(guild_id: int, provider: str) -> bool:
        """Updates the default AI provider for a specific server."""
        if not db.is_connected:
            return True
        query = """
        UPDATE guilds 
        SET preferred_ai = $2, updated_at = CURRENT_TIMESTAMP 
        WHERE guild_id = $1;
        """
        res = await db.execute(query, guild_id, provider.lower())
        return res is not None

    @staticmethod
    async def record_query_log(
        user_id: int,
        username: str,
        guild_id: Optional[int],
        command: str,
        marketplace: Optional[str],
        provider: str,
        status: str = "success",
    ) -> None:
        """Records command usage and updates user stats."""
        if not db.is_connected:
            return

        try:
            # 1. Update or create user record
            user_upsert = """
            INSERT INTO users (user_id, username, total_queries, daily_queries, last_query_date, last_seen)
            VALUES ($1, $2, 1, 1, CURRENT_DATE, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id) DO UPDATE SET
                username = EXCLUDED.username,
                total_queries = users.total_queries + 1,
                daily_queries = CASE 
                    WHEN users.last_query_date = CURRENT_DATE THEN users.daily_queries + 1 
                    ELSE 1 
                END,
                last_query_date = CURRENT_DATE,
                last_seen = CURRENT_TIMESTAMP;
            """
            await db.execute(user_upsert, user_id, username)

            # 2. Insert query audit record
            log_query = """
            INSERT INTO queries_log (user_id, guild_id, command, marketplace, provider, status)
            VALUES ($1, $2, $3, $4, $5, $6);
            """
            await db.execute(log_query, user_id, guild_id, command, marketplace, provider, status)
        except Exception as e:
            logger.error("Failed to log query for user %s: %s", user_id, e)

    @staticmethod
    async def get_stats(guild_id: Optional[int] = None) -> Dict[str, Any]:
        """Returns analytics summary for bot status command."""
        if not db.is_connected:
            return {
                "total_users": "N/A (Offline DB)",
                "total_queries": "N/A (Offline DB)",
                "active_guilds": "N/A (Offline DB)",
            }

        users_count = await db.fetchrow("SELECT COUNT(*) as count FROM users")
        queries_count = await db.fetchrow("SELECT COUNT(*) as count FROM queries_log")
        guilds_count = await db.fetchrow("SELECT COUNT(*) as count FROM guilds WHERE is_active = TRUE")

        return {
            "total_users": users_count["count"] if users_count else 0,
            "total_queries": queries_count["count"] if queries_count else 0,
            "active_guilds": guilds_count["count"] if guilds_count else 0,
        }
