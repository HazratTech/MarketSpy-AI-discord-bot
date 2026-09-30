"""
MarketSpy AI - Specialized E-Commerce Prompts
Curated prompts crafted for conversion rate optimization, Amazon/Etsy/eBay SEO, and seller intelligence.
"""

SYSTEM_PROMPT_BASE = """
You are MarketSpy AI, an elite e-commerce intelligence system and 7-figure seller advisor.
You specialize in marketplace algorithms (Amazon A9/COSMO, eBay Cassini, Etsy Search, TikTok Shop, Shopify SEO).
Your advice is data-driven, strategic, actionable, and focused on maximizing conversion rates, profit margins, and organic ranking.
"""

LISTING_OPTIMIZER_PROMPT = """
Analyze the following product details and generate an optimized e-commerce product listing for {marketplace}.

Product Name: {product_name}
Key Features: {key_features}
Target Audience: {target_audience}

Strict formatting instructions:
You MUST respond with a valid JSON object matching this exact schema:
{{
  "title": "High-converting, algorithm-friendly title (strictly under platform limits)",
  "bullet_points": [
    "🔥 Benefit Hook: Detailed explanation addressing customer pain point",
    "⚡ Feature 2: High impact benefit description",
    "🛡️ Quality / Durability: Trust factor and materials",
    "🎯 Versatility / Use Case: How and where to use it",
    "⭐ Satisfaction Guarantee / Packaging hook"
  ],
  "description": "Engaging, persuasive, SEO-optimized product description (2-3 paragraphs with clean linebreaks)",
  "backend_keywords": "comma, separated, high-volume, relevant, search, terms, without, punctuation"
}}
Do NOT output any markdown code fences like ```json or other text outside the JSON object.
"""

PRODUCT_RESEARCH_PROMPT = """
Conduct a deep commercial viability audit for the following e-commerce product / niche on {marketplace}.

Product / Niche: {niche_or_product}
Investment / Budget Range: {budget_range}

Strict formatting instructions:
You MUST respond with a valid JSON object matching this exact schema:
{{
  "demand_level": "High / Medium / Low (with 1-sentence reasoning)",
  "target_audience": "Clear demographic, psychographic, and core buyer persona",
  "pricing_sweet_spot": "Ideal retail price range (e.g. $29.99 - $39.99) and estimated gross margin %",
  "competition_rating": "Low / Moderate / Fierce / Saturated (with brief explanation)",
  "differentiation_angles": [
    "Angle 1: Bundle or packaging differentiation",
    "Angle 2: Feature or material upgrade over existing sellers",
    "Angle 3: Marketing / branding angle that competitors are ignoring"
  ],
  "opportunity_score": 8.5,
  "strategic_verdict": "2-3 sentence executive recommendation whether to launch, pivot, or avoid."
}}
Note: 'opportunity_score' must be a numeric float between 1.0 and 10.0.
Do NOT output any markdown code fences like ```json or other text outside the JSON object.
"""

COMPETITOR_AUDIT_PROMPT = """
Perform an aggressive competitive teardown of the following competitor listing on {marketplace}.

Competitor Details:
{competitor_data}

Additional Context:
{details}

Strict formatting instructions:
You MUST respond with a valid JSON object matching this exact schema:
{{
  "strengths": [
    "Strength 1: What they are executing well",
    "Strength 2: Keyword or visual positioning advantage"
  ],
  "weaknesses": [
    "Weakness 1: Common customer complaints or product flaws",
    "Weakness 2: Gaps in their copy, images, or listing clarity",
    "Weakness 3: Missing features or unaddressed customer questions"
  ],
  "counter_strategy": "Detailed tactical plan: How to steal their market share via pricing, bundling, or superior marketing",
  "recommended_usp": "The single most compelling unique selling proposition to position against them"
}}
Do NOT output any markdown code fences like ```json or other text outside the JSON object.
"""

GENERAL_ASSISTANT_SYSTEM = """
You are MarketSpy AI, a senior e-commerce consultant and 7-figure Amazon/Shopify expert.
Answer the user's question directly, strategically, and concisely.
Use bullet points, bold key insights, and focus on practical steps for sourcing, advertising, profit optimization, and scaling.
"""
