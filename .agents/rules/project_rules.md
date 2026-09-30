# MarketSpy AI - Agent Rules & Workflow Constraints

## CRITICAL UI REQUIREMENT (STRICT)
- **NEVER USE EMBEDS (`discord.Embed`)**: Always use **`discord.ui.LayoutView`** (Discord Components V2) with `discord.ui.Container`, `discord.ui.Section`, `discord.ui.TextDisplay`, `discord.ui.Separator`, `discord.ui.ActionRow`, and `discord.ui.Button`.
- Do not use `discord.Embed`. All visual layouts must be built using `LayoutView` and `Container` with `accent_color`.

## CRITICAL BEHAVIORAL RULE (STRICT)
- **NEVER INITIALIZE GIT (`.git`)**: Never create, initialize, or re-add a git repository (`git init` or `.git`) unless the user explicitly tells you to do so.
- **NEVER START CODING AUTOMATICALLY**: When in conversation with the user, ALWAYS ask for explicit confirmation before writing any code, modifying files, or installing packages. Never start coding or making edits without the user explicitly telling you to do so.
- **PLAN FIRST**: Always present the plan, discuss requirements, and wait for the user's explicit command.

## RECOMMENDED ENGINEERING RULES (SOLID & CLEAN ARCHITECTURE)
1. **Single Responsibility Principle (SRP)**: Each module, cog, and service class must have one responsibility. Database queries stay in the database layer, AI formatting stays in the AI provider layer, and Discord views stay in the UI layer.
2. **Open/Closed Principle (OCP)**: The AI engine must be open for extension (adding Claude, Groq, Ollama, OpenRouter) but closed for modification. Never modify existing cogs when adding a new LLM provider.
3. **Liskov Substitution Principle (LSP)**: Any AI provider implementing `BaseAIProvider` must be completely interchangeable without breaking any command.
4. **Interface Segregation Principle (ISP)**: Keep interfaces focused. Commands should only interact with methods relevant to their task.
5. **Dependency Inversion Principle (DIP)**: Cogs and high-level modules must depend on abstractions (`BaseAIProvider`, `DatabaseManager`), not concrete SDK implementations.
6. **Async Safety**: All I/O operations (Discord API, PostgreSQL queries, AI API requests) must be non-blocking using `asyncio` and `aiohttp`.
7. **Graceful Error Handling**: Every Discord command must handle API timeouts, invalid inputs, and rate limits gracefully, displaying user-friendly LayoutViews instead of crashing.

---

## LOCKED-IN PROJECT SCOPE ($125 / $150 ORDER)
Do NOT deviate from this scope or accept additions without formal order upgrade:

1. **MarketSpy AI Branding & Architecture**:
   - Modern `discord.py` (v2.x) bot with slash commands (`/`).
   - Modern Discord Components V2 UI using `discord.ui.LayoutView` (NO embeds).
   - Modular Cog-based architecture.

2. **Modular AI Engine**:
   - Abstract `BaseAIProvider` interface.
   - Concrete implementations for **OpenAI** (`gpt-4o`, `gpt-4o-mini`) and **Google Gemini** (`gemini-1.5-flash`).
   - Claude (`claude-3-5-sonnet`) ready scaffold so client can plug it in later without rebuilding.
   - Provider factory dynamically loaded from `.env`.

3. **Core E-Commerce Seller Tools (Slash Commands)**:
   - `/profit-calculator`: Net profit, margin %, and ROI calculator with preset fee structures for Amazon FBA, Amazon FBM, eBay, Etsy, Shopify, and TikTok Shop.
   - `/optimize-listing`: AI listing optimizer generating CTR titles, 5 benefit-driven bullet points, SEO description, and search keywords for any marketplace.
   - `/product-research`: Deep AI analysis of niche potential, target customer persona, pricing sweet spot, competition, and risk score.
   - `/competitor-audit`: Competitive analysis assistant identifying competitor listing weaknesses, friction points, and differentiation strategy.

4. **PostgreSQL Database Foundation**:
   - Asynchronous PostgreSQL integration (`asyncpg`).
   - Schema (`schema.sql`) with tables: `guilds`, `users`, `queries_log`, `settings`.
   - Compatible with local PostgreSQL or cloud Supabase connection string.

5. **Client Delivery Package**:
   - Complete source code.
   - `README.md` with step-by-step setup and deployment guide.
   - `.env.example` with clear comments for all keys.
   - `schema.sql` for 1-click database setup.
