from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_strategy_research_workspace_phase_doc_exists_and_summarizes_phase() -> None:
    text = (ROOT / "docs/phases/strategy_research_workspace.md").read_text(encoding="utf-8")

    required = [
        "Strategy Research Workspace",
        "planning",
        "API contract skeleton",
        "display contract skeleton",
        "safety audit",
        "milestone audit",
        "system boundary hardening",
        "API/display integration readiness",
    ]

    for phrase in required:
        assert phrase in text


def test_strategy_research_workspace_phase_preserves_research_safety_boundaries() -> None:
    text = (ROOT / "docs/phases/strategy_research_workspace.md").read_text(encoding="utf-8").lower()

    required = [
        "no active ui",
        "no paper ingestion",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no broker controls",
        "no execution apis",
    ]

    for phrase in required:
        assert phrase in text
