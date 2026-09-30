"""
MarketSpy AI - Modern UI LayoutViews
Constructs Discord Components V2 LayoutViews with Containers, TextDisplays, Separators, and ActionRows.
Strictly adheres to:
1. Never use embeds; always use discord.ui.LayoutView.
2. Enforce character budgets to prevent Discord 4000-character payload limits.
3. Optimize memory by setting timeout=None on non-interactive views.
"""

from typing import Dict, Any, List, Optional
import discord
from discord import ui
from ui.colors import (
    COLOR_PRIMARY,
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_INFO,
    BRAND_FOOTER,
)
from services.calculator.profit_engine import ProfitCalculationResult


def safe_truncate(text: Optional[str], max_chars: int) -> str:
    """Trims text to max_chars safely without breaking."""
    if not text:
        return ""
    text = str(text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def create_profit_layout(res: ProfitCalculationResult) -> ui.LayoutView:
    """Builds a modern LayoutView for unit economics and profit analysis."""
    if res.net_profit <= 0:
        accent = COLOR_DANGER
    elif res.net_margin_pct < 15:
        accent = COLOR_WARNING
    else:
        accent = COLOR_SUCCESS

    curr = "$" if res.currency == "USD" else res.currency + " "

    # 180s timeout only because it has an interactive button
    view = ui.LayoutView(timeout=180.0)

    header_text = (
        f"# 📊 {res.marketplace} Profit & Margin Breakdown\n"
        f"Unit economics analysis for **{curr}{res.selling_price:.2f}** retail price."
    )

    summary_text = (
        f"### 💵 Financial Summary\n"
        f"• **Net Profit:** `{curr}{res.net_profit:.2f}`\n"
        f"• **Net Margin:** `{res.net_margin_pct:.1f}%`\n"
        f"• **Return on Investment (ROI):** `{res.roi_pct:.1f}%`\n"
        f"• **Profitability Health:** {res.health_emoji} **{res.health_status}**"
    )

    deductions_text = (
        f"### 🏷️ Cost & Fee Breakdown\n"
        f"• **Total Platform Fees:** `{curr}{res.platform_fees.total_platform_fees:.2f}`\n"
        f"• **COGS + Sourcing:** `{curr}{res.cogs:.2f}`\n"
        f"• **Shipping to Customer:** `{curr}{res.shipping_cost:.2f}`\n"
        f"• **Ad Spend / PPC:** `{curr}{res.ad_spend:.2f}`\n"
        f"• **Total Unit Costs:** `{curr}{res.total_costs:.2f}`"
    )

    btn = ui.Button(
        label="Platform Fee Breakdown",
        style=discord.ButtonStyle.secondary,
        emoji="🔍",
    )

    async def on_fee_click(interaction: discord.Interaction):
        fees = res.platform_fees
        detail_msg = (
            f"**{fees.platform_name} Fee Breakdown:**\n"
            f"• **Referral / Commission:** {curr}{fees.referral_or_commission_fee:.2f}\n"
            f"• **Fulfillment / Fixed Fee:** {curr}{fees.fulfillment_or_fixed_fee:.2f}\n"
            f"• **Payment Processing:** {curr}{fees.payment_processing_fee:.2f}\n"
            f"• **Total Platform Deductions:** {curr}{fees.total_platform_fees:.2f}\n\n"
            f"📌 **Formula Rule:** {fees.notes}"
        )
        await interaction.response.send_message(detail_msg, ephemeral=True)

    btn.callback = on_fee_click
    action_row = ui.ActionRow(btn)
    footer_text = f"_{BRAND_FOOTER}_"

    container = ui.Container(
        ui.TextDisplay(header_text),
        ui.Separator(),
        ui.TextDisplay(summary_text),
        ui.Separator(),
        ui.TextDisplay(deductions_text),
        action_row,
        ui.Separator(),
        ui.TextDisplay(footer_text),
        accent_color=accent,
    )

    view.add_item(container)
    return view


def create_listing_layout(
    product_name: str, marketplace: str, data: Dict[str, Any], provider: str
) -> ui.LayoutView:
    """Builds a modern LayoutView for the AI-optimized listing components (timeout=None for zero memory overhead)."""
    view = ui.LayoutView(timeout=None)

    header_text = (
        f"# ✨ Optimized Listing • {marketplace.upper()}\n"
        f"AI-generated conversion copy for: **{safe_truncate(product_name, 100)}**"
    )

    # Check if raw fallback
    if "raw_content" in data:
        raw_display = safe_truncate(data["raw_content"], 3200)
        container = ui.Container(
            ui.TextDisplay(header_text),
            ui.Separator(),
            ui.TextDisplay(f"### 📝 Generated Listing\n{raw_display}"),
            ui.Separator(),
            ui.TextDisplay(f"_{BRAND_FOOTER} • Generated via {provider.upper()}_"),
            accent_color=COLOR_PRIMARY,
        )
        view.add_item(container)
        return view

    title = safe_truncate(data.get("title", product_name), 300)
    bullets = data.get("bullet_points", [])
    if isinstance(bullets, list) and bullets:
        bullet_text = "\n\n".join(f"{b}" for b in bullets[:5])
    else:
        bullet_text = "No bullet points generated."
    bullet_text = safe_truncate(bullet_text, 1100)

    desc = safe_truncate(data.get("description", "No description generated."), 1000)
    keywords = safe_truncate(data.get("backend_keywords", "No keywords generated."), 400)

    title_text = f"### 📌 High-CTR Title\n```\n{title}\n```"
    bullets_section = f"### 🎯 5 Strategic Bullet Points\n{bullet_text}"
    desc_section = f"### 📝 SEO Product Description\n{desc}"
    keywords_section = f"### 🔍 Backend Search Terms / SEO Tags\n`{keywords}`"
    footer_text = f"_{BRAND_FOOTER} • Generated via {provider.upper()}_"

    container = ui.Container(
        ui.TextDisplay(header_text),
        ui.Separator(),
        ui.TextDisplay(title_text),
        ui.Separator(),
        ui.TextDisplay(bullets_section),
        ui.Separator(),
        ui.TextDisplay(desc_section),
        ui.Separator(),
        ui.TextDisplay(keywords_section),
        ui.Separator(),
        ui.TextDisplay(footer_text),
        accent_color=COLOR_PRIMARY,
    )

    view.add_item(container)
    return view


def create_research_layout(
    niche_or_product: str, marketplace: str, data: Dict[str, Any], provider: str
) -> ui.LayoutView:
    """Builds a modern LayoutView for product research and market viability audit."""
    view = ui.LayoutView(timeout=None)

    header_text = (
        f"# 🔍 Product Viability Audit • {safe_truncate(niche_or_product, 100)}\n"
        f"Market analysis for **{marketplace.upper()}**"
    )

    if "raw_content" in data:
        raw_display = safe_truncate(data["raw_content"], 3200)
        container = ui.Container(
            ui.TextDisplay(header_text),
            ui.Separator(),
            ui.TextDisplay(f"### 📊 Market Analysis\n{raw_display}"),
            ui.Separator(),
            ui.TextDisplay(f"_{BRAND_FOOTER} • Analyzed via {provider.upper()}_"),
            accent_color=COLOR_INFO,
        )
        view.add_item(container)
        return view

    score = data.get("opportunity_score", 7.5)
    try:
        score_val = float(score)
    except (ValueError, TypeError):
        score_val = 7.0

    score_bar = "🟢" if score_val >= 8.0 else ("🟡" if score_val >= 6.0 else "🔴")

    score_text = (
        f"### ⭐ Opportunity Score: {score_bar} `{score_val:.1f} / 10`\n"
        f"• **Market Demand:** {safe_truncate(str(data.get('demand_level', 'Medium')), 250)}\n"
        f"• **Competition Rating:** {safe_truncate(str(data.get('competition_rating', 'Moderate')), 250)}\n"
        f"• **Pricing Sweet Spot:** {safe_truncate(str(data.get('pricing_sweet_spot', 'Standard retail')), 250)}"
    )

    audience_text = (
        f"### 👥 Target Buyer Persona\n"
        f"{safe_truncate(str(data.get('target_audience', 'General e-commerce buyers')), 700)}"
    )

    angles = data.get("differentiation_angles", [])
    if isinstance(angles, list) and angles:
        angles_str = "\n".join(f"• {a}" for a in angles[:3])
    else:
        angles_str = "• Focus on superior customer support and premium packaging."
    angles_text = f"### 💡 3 Angles to Beat Competitors\n{safe_truncate(angles_str, 800)}"

    verdict_text = (
        f"### 🎯 Strategic Verdict\n"
        f"_{safe_truncate(str(data.get('strategic_verdict', 'Solid niche with proper differentiation.')), 600)}_"
    )

    footer_text = f"_{BRAND_FOOTER} • Analyzed via {provider.upper()}_"

    container = ui.Container(
        ui.TextDisplay(header_text),
        ui.Separator(),
        ui.TextDisplay(score_text),
        ui.Separator(),
        ui.TextDisplay(audience_text),
        ui.Separator(),
        ui.TextDisplay(angles_text),
        ui.Separator(),
        ui.TextDisplay(verdict_text),
        ui.Separator(),
        ui.TextDisplay(footer_text),
        accent_color=COLOR_INFO,
    )

    view.add_item(container)
    return view


def create_competitor_layout(
    marketplace: str, data: Dict[str, Any], provider: str
) -> ui.LayoutView:
    """Builds a modern LayoutView for competitor listing teardown."""
    view = ui.LayoutView(timeout=None)

    header_text = (
        f"# ⚔️ Competitor Listing Teardown • {marketplace.upper()}\n"
        f"Strategic audit of competitor weaknesses, customer complaints, and counter-tactics."
    )

    if "raw_content" in data:
        raw_display = safe_truncate(data["raw_content"], 3200)
        container = ui.Container(
            ui.TextDisplay(header_text),
            ui.Separator(),
            ui.TextDisplay(f"### ⚔️ Competitor Audit\n{raw_display}"),
            ui.Separator(),
            ui.TextDisplay(f"_{BRAND_FOOTER} • Audited via {provider.upper()}_"),
            accent_color=COLOR_WARNING,
        )
        view.add_item(container)
        return view

    strengths = data.get("strengths", [])
    if isinstance(strengths, list) and strengths:
        strengths_str = "\n".join(f"• {s}" for s in strengths[:3])
    else:
        strengths_str = "• Established market presence."
    strengths_text = f"### 🛡️ Competitor Strengths\n{safe_truncate(strengths_str, 700)}"

    weaknesses = data.get("weaknesses", [])
    if isinstance(weaknesses, list) and weaknesses:
        weaknesses_str = "\n".join(f"• {w}" for w in weaknesses[:4])
    else:
        weaknesses_str = "• Generic copy and lack of customer reassurance."
    weaknesses_text = f"### ⚠️ Critical Vulnerabilities & Customer Friction\n{safe_truncate(weaknesses_str, 800)}"

    counter_strategy = data.get(
        "counter_strategy", "Bundle complementary accessories and offer faster dispatch."
    )
    strategy_text = f"### 🎯 Counter-Strategy (How to Win)\n{safe_truncate(counter_strategy, 800)}"

    usp = data.get(
        "recommended_usp", "Highlight superior quality materials and responsive warranty."
    )
    usp_text = f"### 🏆 Recommended USP\n**{safe_truncate(usp, 350)}**"

    footer_text = f"_{BRAND_FOOTER} • Audited via {provider.upper()}_"

    container = ui.Container(
        ui.TextDisplay(header_text),
        ui.Separator(),
        ui.TextDisplay(strengths_text),
        ui.Separator(),
        ui.TextDisplay(weaknesses_text),
        ui.Separator(),
        ui.TextDisplay(strategy_text),
        ui.Separator(),
        ui.TextDisplay(usp_text),
        ui.Separator(),
        ui.TextDisplay(footer_text),
        accent_color=COLOR_WARNING,
    )

    view.add_item(container)
    return view


def create_error_layout(error_message: str) -> ui.LayoutView:
    """Builds a modern LayoutView for error reporting."""
    view = ui.LayoutView(timeout=None)

    container = ui.Container(
        ui.TextDisplay("# ❌ Execution Error"),
        ui.Separator(),
        ui.TextDisplay(f"**Error Details:**\n{safe_truncate(error_message, 1200)}"),
        ui.Separator(),
        ui.TextDisplay(f"_{BRAND_FOOTER}_"),
        accent_color=COLOR_DANGER,
    )

    view.add_item(container)
    return view
