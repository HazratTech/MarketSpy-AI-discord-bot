"""
MarketSpy AI - AI Utilities & JSON Parser
Robust parser to extract JSON from LLM outputs even if surrounded by markdown or conversational text.
Includes automatic sanitation for trailing commas.
"""

import json
import re
import logging
from typing import Dict, Any

logger = logging.getLogger("MarketSpyAI.AIUtils")


def sanitize_json_str(s: str) -> str:
    """Removes trailing commas before closing brackets/braces."""
    return re.sub(r",\s*([}\]])", r"\1", s)


def clean_and_parse_json(raw_text: str) -> Dict[str, Any]:
    """Extracts and parses JSON object from LLM response safely."""
    text = raw_text.strip()

    # 1. Direct parse attempt
    try:
        return json.loads(sanitize_json_str(text))
    except json.JSONDecodeError:
        pass

    # 2. Extract content within ```json ... ``` or ``` ... ```
    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if code_block_match:
        try:
            cleaned = sanitize_json_str(code_block_match.group(1).strip())
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

    # 3. Find outermost curly braces { ... }
    brace_match = re.search(r"(\{[\s\S]*\})", text)
    if brace_match:
        try:
            cleaned = sanitize_json_str(brace_match.group(1).strip())
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

    # 4. Fallback: wrap raw text so the user's generated AI copy is never lost
    logger.warning("Could not parse LLM output as strict JSON. Preserving raw content.")
    return {"raw_content": text}
