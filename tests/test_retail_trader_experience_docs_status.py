from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/RETAIL_TRADER_EXPERIENCE_PLANNING.md",
    "docs/RETAIL_TRADER_EXPERIENCE_GUARDRAILS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_PERSONA_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_JOURNEY_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_SECTION_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_CARD_PLACEHOLDERS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_FORBIDDEN_INTERACTIONS.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_RECOMMENDATION_POLICY.md",
    "docs/RETAIL_TRADER_EXPERIENCE_NO_EXECUTION_POLICY.md",
]


def test_retail_trader_experience_prompt_56_docs_exist_and_state_boundaries() -> None:
    combined = ""
    for relative_path in REQUIRED_DOCS:
        path = ROOT / relative_path
        assert path.exists(), relative_path
        combined += path.read_text(encoding="utf-8") + "\n"

    required_phrases = [
        "Retail Trader Experience",
        "planning and guardrails",
        "no active UI",
        "no frontend components",
        "no desktop components",
        "no recommendation cards",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no suitability profiling",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]
    for phrase in required_phrases:
        assert phrase in combined


def test_retail_trader_experience_status_docs_are_updated() -> None:
    assert "Prompt 56" in (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    assert "Current Prompt: 60" in (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    assert "Retail Trader Experience Planning and Guardrails" in (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
