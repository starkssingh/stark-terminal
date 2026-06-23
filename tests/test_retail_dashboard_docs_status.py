from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOCS = [
    ROOT / "docs/RETAIL_DASHBOARD_PLANNING.md",
    ROOT / "docs/RETAIL_DASHBOARD_GUARDRAILS.md",
    ROOT / "docs/RETAIL_DASHBOARD_SECTION_PLACEHOLDERS.md",
    ROOT / "docs/RETAIL_DASHBOARD_CARD_PLACEHOLDERS.md",
    ROOT / "docs/RETAIL_DASHBOARD_FORBIDDEN_INTERACTIONS.md",
    ROOT / "docs/RETAIL_DASHBOARD_NO_RECOMMENDATION_POLICY.md",
    ROOT / "docs/RETAIL_DASHBOARD_NO_EXECUTION_POLICY.md",
]


def test_retail_dashboard_docs_exist_and_state_boundaries() -> None:
    for path in DOCS:
        assert path.exists(), path

    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in DOCS)
    for phrase in [
        "Retail Dashboard",
        "planning and guardrails",
        "no active UI",
        "no recommendation cards",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in docs_text


def test_prompt_49_status_docs_are_updated() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 49 - Retail Dashboard Planning and Guardrails" in prompt_log
    assert "Historical verifier reference: Current Prompt: 49" in north_star
    assert "Completed Prompts: 50 after completion" in north_star
    assert "Retail Dashboard Planning and Guardrails" in project_map
