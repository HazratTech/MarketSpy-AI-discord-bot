# MarketSpy AI • E-Commerce Seller Intelligence Discord Bot

MarketSpy AI is an AI-powered e-commerce assistant bot built for Discord, engineered specifically for sellers on **Amazon, eBay, Etsy, Shopify, and TikTok Shop**.

Built on a clean **modular architecture** (SOLID principles) and using Discord's modern **Components V2 (`discord.ui.LayoutView`)** layout system, MarketSpy AI delivers real-time profit calculations, AI listing optimization, deep product research, and competitive teardowns.

---

## 🚀 Core Features & Slash Commands

| Command | Description | Supported Platforms |
| :--- | :--- | :--- |
| **`/profit-calculator`** | Calculates net profit, net margins %, and ROI factoring in platform fee structures (referral fees, FBA fulfillment, transaction fees, payment processing, COGS, shipping, ad spend). Includes an interactive button for detailed fee breakdown. | Amazon FBA, Amazon FBM, eBay, Etsy, Shopify, TikTok Shop |
| **`/optimize-listing`** | Uses AI to generate high-converting product titles, 5 benefit-driven bullet points, SEO descriptions, and backend search keywords formatted specifically for the target marketplace. | Amazon, eBay, Etsy, Shopify, TikTok Shop |
| **`/product-research`** | Performs a deep market viability audit for any product or niche. Analyzes market demand, ideal customer persona, pricing sweet spots, competition levels, 3 differentiation angles, and calculates a 1-to-10 Opportunity Score. | Amazon, eBay, Etsy, Shopify, TikTok Shop |
| **`/competitor-audit`** | Audits a competitor's listing or description to uncover customer friction points, listing weaknesses, and creates an actionable counter-strategy with a recommended USP. | Amazon, eBay, Etsy, Shopify, TikTok Shop |
| **`/help`** | Displays the full seller command directory and checks live database and AI engine connectivity status. | All |

---

## 🏗️ Architecture & Technology Stack

* **Language**: Python 3.10+ (Tested up to Python 3.14)
* **Discord Framework**: `discord.py` (v2.7+) using native **Slash Commands (`app_commands`)** and **Discord Components V2 (`discord.ui.LayoutView`, `ui.Container`, `ui.TextDisplay`, `ui.Separator`)**.
* **Database**: **PostgreSQL** using high-performance asynchronous connection pooling (`asyncpg`). Schema ready for multi-server scaling. 100% compatible with local PostgreSQL or cloud **Supabase** (Free Tier).
* **Modular AI Engine**: Built with the **Provider Pattern**. Supports **Google Gemini** (`gemini-1.5-flash`), **OpenAI** (`gpt-4o-mini`, `gpt-4o`), and pre-scaffolded for **Anthropic Claude** (`claude-3-5-sonnet`).

---

## 📋 Quick Setup & Installation Guide

### 1. Clone & Setup Python Environment

```bash
# Navigate to the project directory
cd "MarketSpy AI"

# Create a virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux / macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

---

### 2. Configure Environment Variables (`.env`)

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open `.env` and fill in your credentials:

```ini
# Discord Bot Token
DISCORD_BOT_TOKEN=your_bot_token_here

# PostgreSQL / Supabase Database URL
DATABASE_URL=postgresql://postgres:password@localhost:5432/marketspy_ai

# Default AI Provider ("gemini" or "openai" or "claude")
DEFAULT_AI_PROVIDER=gemini

# Google Gemini API Key (Recommended free starter: https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# OpenAI API Key (Optional: https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Anthropic Claude API Key (Optional: https://console.anthropic.com/)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

---

### 3. Setting Up the Database (Supabase or Local PostgreSQL)

#### Option A: Supabase (Recommended Free Cloud Database - 2 Minutes)
1. Go to [https://supabase.com](https://supabase.com) and create a free account.
2. Click **New Project**, choose a project name (e.g. `marketspy-ai`), and set a strong database password.
3. Once created, go to **Project Settings** > **Database** > **Connection string** > **URI**.
4. Copy the URI (it looks like `postgresql://postgres:[YOUR-PASSWORD]@db.[REF].supabase.co:5432/postgres`) and paste it into `DATABASE_URL` in your `.env` file.
5. In your Supabase dashboard, click **SQL Editor**, open the provided `database/schema.sql` file, paste the contents, and click **Run**. All tables and indexes are created automatically!

#### Option B: Local PostgreSQL
If you have PostgreSQL installed locally on your machine or VPS:
```bash
# Create the database
createdb marketspy_ai

# Run schema migrations
psql -d marketspy_ai -f database/schema.sql
```

*(Note: If you run the bot without a database configured, the bot will automatically run in graceful offline mode so your slash commands still function).*

---

### 4. Setting Up the Discord Bot & Invite Link

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** and name it **MarketSpy AI**.
3. Under the **Bot** tab:
   - Click **Reset Token** to copy your **Bot Token** into `.env`.
   - Scroll down to **Privileged Gateway Intents** and enable **Server Members Intent** and **Message Content Intent**.
4. Under **Installation** / **OAuth2 URL Generator**:
   - Select scopes: `bot`, `applications.commands`.
   - Under Bot Permissions, select:
     - `Send Messages`
     - `Embed Links`
     - `Attach Files`
     - `Use External Emojis`
     - `Read Message History`
5. Copy the generated invite link and paste it into your browser to invite MarketSpy AI to your Discord server.

---

### 5. Starting the Bot

With your virtual environment activated and `.env` configured, simply run:

```bash
python bot.py
```

You will see:
```text
[INFO] MarketSpy AI is ONLINE and ready!
[INFO] Logged in as: MarketSpy AI#0000
[INFO] Synchronized 5 global application slash commands.
```

Your Discord server will now have all slash commands active!

---

## 🧩 Extending AI Providers (Adding Claude, Mistral, Ollama)

Because MarketSpy AI is built following the **Open/Closed Principle (SOLID)**, adding or changing AI models requires **zero changes to Discord commands**:

1. Create a new provider file in `services/ai/providers/my_new_provider.py` inheriting from `BaseAIProvider`.
2. Implement the 5 abstract methods (`generate_text`, `optimize_listing`, `analyze_product`, `audit_competitor`, `ask_assistant`).
3. Register the key in `services/ai/factory.py`.
4. Put your API key in `.env`.

*Note: Anthropic Claude is already pre-coded in `services/ai/providers/claude_provider.py`. Simply enter `ANTHROPIC_API_KEY` in `.env` and set `DEFAULT_AI_PROVIDER=claude` to use Claude 3.5 Sonnet.*

---

## 📁 Project Directory Structure

```
MarketSpy AI/
├── bot.py                        # Main bot startup & lifecycle management
├── config.py                     # Centralized, validated configuration
├── requirements.txt              # Pinned Python dependencies
├── .env.example                  # Environment configuration template
├── README.md                     # Full setup & operational manual
├── cogs/                         # Discord Slash Command extensions
│   ├── calculator.py             # /profit-calculator command
│   ├── listing.py                # /optimize-listing command
│   ├── research.py               # /product-research command
│   ├── competitor.py             # /competitor-audit command
│   └── help.py                   # /help command and system diagnostics
├── database/                     # PostgreSQL / Supabase persistence
│   ├── db.py                     # asyncpg connection pool & resilient executor
│   ├── repository.py             # Domain repositories (users, guilds, queries)
│   └── schema.sql                # SQL schema DDL for PostgreSQL / Supabase
├── services/                     # Business logic & AI abstractions
│   ├── calculator/               # E-commerce unit economics & platform fee models
│   │   ├── fee_models.py         # Amazon, eBay, Etsy, Shopify, TikTok fee math
│   │   └── profit_engine.py      # Net profit, margin %, ROI calculation engine
│   └── ai/                       # Modular AI LLM subsystem
│       ├── base.py               # BaseAIProvider abstract interface
│       ├── factory.py            # Dynamic AIFactory for runtime model switching
│       ├── prompts.py            # High-conversion e-commerce prompts
│       ├── utils.py              # Safe JSON parsing & cleaning
│       └── providers/            # Concrete AI provider implementations
│           ├── gemini_provider.py
│           ├── openai_provider.py
│           └── claude_provider.py
└── ui/                           # Discord Components V2 UI Layer
    ├── colors.py                 # Hex brand palette tokens
    └── layouts.py                # discord.ui.LayoutView builders (NO embeds)
```

---

## ⚖️ License & Ownership
Full source code and commercial rights belong to the client. Built with care for e-commerce entrepreneurs.

# MarketSpy-AI-discord-bot
Bot by [RelayWorks](https://relayworks.dev/)
