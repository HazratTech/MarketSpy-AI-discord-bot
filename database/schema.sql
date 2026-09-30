-- =======================================================
-- MarketSpy AI - PostgreSQL Database Schema
-- Scalable, multi-server ready schema for e-commerce bot
-- =======================================================

-- 1. Guilds / Servers Table
CREATE TABLE IF NOT EXISTS guilds (
    guild_id BIGINT PRIMARY KEY,
    guild_name VARCHAR(255) NOT NULL,
    preferred_ai VARCHAR(50) DEFAULT 'gemini',
    currency VARCHAR(10) DEFAULT 'USD',
    plan_tier VARCHAR(50) DEFAULT 'free',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    total_queries INT DEFAULT 0,
    daily_queries INT DEFAULT 0,
    last_query_date DATE DEFAULT CURRENT_DATE,
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Queries / Audit Log Table
CREATE TABLE IF NOT EXISTS queries_log (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    guild_id BIGINT,
    command VARCHAR(100) NOT NULL,
    marketplace VARCHAR(50),
    provider VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'success',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for high-performance query analytics
CREATE INDEX IF NOT EXISTS idx_queries_user ON queries_log(user_id);
CREATE INDEX IF NOT EXISTS idx_queries_guild ON queries_log(guild_id);
CREATE INDEX IF NOT EXISTS idx_queries_created ON queries_log(created_at);
CREATE INDEX IF NOT EXISTS idx_queries_command ON queries_log(command);

-- 4. Global Settings Table
CREATE TABLE IF NOT EXISTS settings (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tracked Products Table (Foundation for future Phase 2/3 price alert features)
CREATE TABLE IF NOT EXISTS tracked_products (
    id BIGSERIAL PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    marketplace VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    product_url TEXT NOT NULL,
    target_price NUMERIC(10, 2),
    current_price NUMERIC(10, 2),
    alert_triggered BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
