from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_67_DOCS = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PLANNING_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_SAFETY_MILESTONE_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_ACTIVE_UI_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_PAPER_PARSING_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_STRATEGY_GENERATION_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_BACKTESTING_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_NEXT_PHASE_PLAN.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_strategy_research_workspace_milestone_audit_docs_exist() -> None:
    for doc in PROMPT_67_DOCS:
        assert (ROOT / doc).exists(), doc


def test_strategy_research_workspace_milestone_audit_docs_capture_scope() -> None:
    combined = "\n".join(_read(doc) for doc in PROMPT_67_DOCS).lower()

    for phrase in [
        "prompts 63-66",
        "strategy research workspace planning and guardrails",
        "strategy research workspace api contract skeleton",
        "strategy research workspace display contract skeleton",
        "strategy research workspace safety boundary audit",
        "planning verdict",
        "api verdict",
        "display verdict",
        "safety boundary verdict",
        "next-phase readiness verdict",
    ]:
        assert phrase in combined


def test_strategy_research_workspace_milestone_docs_state_forbidden_surfaces() -> None:
    combined = "\n".join(_read(doc) for doc in PROMPT_67_DOCS).lower()

    for phrase in [
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no paper ingestion",
        "no paper parsing",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendation",
        "no action generation",
        "no confidence scoring",
        "decisionobject",
        "no broker controls",
        "no readiness-to-trade",
        "no execution apis",
    ]:
        assert phrase in combined
