"""
MarketSpy AI - Database Manager
Handles async connection pooling and execution for PostgreSQL / Supabase.
Includes graceful offline mode if database credentials are not yet configured.
"""

import os
import logging
from typing import Optional, List, Dict, Any
import asyncpg
from config import config

logger = logging.getLogger("MarketSpyAI.Database")


class DatabaseManager:
    """Manages PostgreSQL connection pooling and resilient query execution."""

    def __init__(self, dsn: Optional[str] = None):
        self.dsn = dsn or config.database_url
        self.pool: Optional[asyncpg.Pool] = None
        self.is_connected = False

    async def connect(self) -> bool:
        """Establishes connection pool and executes schema migrations."""
        if not self.dsn or "your_database" in self.dsn:
            logger.warning(
                "DATABASE_URL not configured. Running in offline/in-memory mode (commands will function, logs skipped)."
            )
            return False

        try:
            self.pool = await asyncpg.create_pool(
                dsn=self.dsn,
                min_size=1,
                max_size=10,
                command_timeout=60,
            )
            self.is_connected = True
            logger.info("Successfully connected to PostgreSQL database.")

            # Run schema initialization
            await self._initialize_schema()
            return True
        except Exception as e:
            logger.warning(
                "Could not connect to PostgreSQL database (%s). Running with database features degraded gracefully.",
                e,
            )
            self.is_connected = False
            return False

    async def _initialize_schema(self) -> None:
        """Reads schema.sql and runs DDL migrations if pool is active."""
        if not self.is_connected or not self.pool:
            return

        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        if not os.path.exists(schema_path):
            logger.warning("schema.sql not found at %s", schema_path)
            return

        try:
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()

            async with self.pool.acquire() as conn:
                await conn.execute(schema_sql)
            logger.info("PostgreSQL schema validated and up to date.")
        except Exception as e:
            logger.error("Failed to initialize PostgreSQL schema: %s", e)

    async def execute(self, query: str, *args) -> Optional[str]:
        """Executes an INSERT/UPDATE/DELETE query safely."""
        if not self.is_connected or not self.pool:
            return None
        try:
            async with self.pool.acquire() as conn:
                return await conn.execute(query, *args)
        except Exception as e:
            logger.error("Database execute error: %s (Query: %s)", e, query)
            return None

    async def fetchrow(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Fetches a single row as a dictionary."""
        if not self.is_connected or not self.pool:
            return None
        try:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(query, *args)
                return dict(row) if row else None
        except Exception as e:
            logger.error("Database fetchrow error: %s (Query: %s)", e, query)
            return None

    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        """Fetches multiple rows as dictionaries."""
        if not self.is_connected or not self.pool:
            return []
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query, *args)
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error("Database fetch error: %s (Query: %s)", e, query)
            return []

    async def close(self) -> None:
        """Gracefully closes the connection pool."""
        if self.pool:
            await self.pool.close()
            self.is_connected = False
            logger.info("PostgreSQL connection pool closed.")


# Global database instance
db = DatabaseManager()
