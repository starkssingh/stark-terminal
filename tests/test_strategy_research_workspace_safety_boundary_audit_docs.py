from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_66_ACTIVE_DOCS = [
    "docs/STRATEGY_RESEARCH_WORKSPACE_SAFETY_BOUNDARY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_API_BOUNDARY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/STRATEGY_RESEARCH_WORKSPACE_MILESTONE_READINESS.md",
    "docs/phases/strategy_research_workspace.md",
    "docs/audits/safety_boundaries.md",
    "docs/testing/CONSOLIDATION_MAP.md",
]


def _read_doc(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_strategy_research_workspace_safety_boundary_audit_docs_exist() -> None:
    for doc in PROMPT_66_ACTIVE_DOCS:
        assert (ROOT / doc).exists(), doc


def test_strategy_research_workspace_safety_boundary_docs_capture_prompt_63_to_65_scope() -> None:
    combined = "\n".join(_read_doc(doc) for doc in PROMPT_66_ACTIVE_DOCS).lower()

    for phrase in [
        "prompts 63-65",
        "strategy research workspace planning and guardrails",
        "strategy research workspace api contract skeleton",
        "strategy research workspace display contract skeleton",
        "verification summary",
        "planning boundary verdict",
        "api boundary verdict",
        "display boundary verdict",
        "no-active-ui verdict",
        "no-paper-ingestion/parsing verdict",
        "no-strategy-generation verdict",
        "no-backtesting verdict",
        "no-recommendation verdict",
        "no-broker-control verdict",
        "no-execution verdict",
        "milestone-readiness verdict",
    ]:
        assert phrase in combined


def test_strategy_research_workspace_safety_boundary_docs_state_all_forbidden_surfaces() -> None:
    combined = "\n".join(_read_doc(doc) for doc in PROMPT_66_ACTIVE_DOCS).lower()

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
        "decisionobject generation",
        "no broker controls",
        "no readiness-to-trade",
        "no execution apis",
    ]:
        assert phrase in combined


def test_strategy_research_workspace_micro_audit_details_preserved_after_deletion() -> None:
    archive_map = _read_doc("docs/testing/CONSOLIDATION_MAP.md")
    deleted_report = _read_doc("docs/reports/DELETED_FILES_REPORT.md")
    tests_report = _read_doc("docs/reports/TESTS_CONSOLIDATED_REPORT.md")

    assert "docs/STRATEGY_RESEARCH_WORKSPACE_NO_ACTIVE_UI_AUDIT.md" in archive_map
    assert "tests/test_strategy_research_workspace_no_active_ui_audit.py" in archive_map
    assert "STRATEGY_RESEARCH_WORKSPACE_NO_ACTIVE_UI_AUDIT.md" in deleted_report
    assert "test_strategy_research_workspace_no_active_ui_audit.py.archived" in tests_report


def test_strategy_research_workspace_milestone_readiness_points_to_prompt_68_only() -> None:
    readiness = _read_doc("docs/STRATEGY_RESEARCH_WORKSPACE_MILESTONE_READINESS.md")

    assert "Prompt 67 completes Strategy Research Workspace Milestone Audit" in readiness
    assert "Prompt 69 - Strategy Research Workspace API/Display Integration Readiness Audit" in readiness
    assert "active research workspace UI is still not allowed" in readiness
    assert "paper ingestion and paper parsing are still not allowed" in readiness
    assert "strategy generation and strategy code generation are still not allowed" in readiness
    assert "backtesting, optimization" in readiness
    assert "Broker controls" in readiness or "broker controls" in readiness
