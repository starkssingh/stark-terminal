from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_73_ACTIVE_DOCS = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_SAFETY_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_MILESTONE_READINESS.md",
    "docs/phases/research_artifact_registry.md",
    "docs/audits/research_artifact_boundaries.md",
    "docs/audits/safety_boundaries.md",
    "docs/testing/CONSOLIDATION_MAP.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_73_safety_boundary_audit_docs_exist() -> None:
    for doc in PROMPT_73_ACTIVE_DOCS:
        assert (ROOT / doc).exists(), doc


def test_prompt_73_docs_capture_prompt_70_to_72_scope_and_verdicts() -> None:
    combined = "\n".join(_read(doc) for doc in PROMPT_73_ACTIVE_DOCS).lower()

    for phrase in [
        "prompts 70-72",
        "research artifact registry planning and guardrails",
        "research artifact registry api contract skeleton",
        "research artifact registry display contract skeleton",
        "verification summary",
        "planning safety verdict",
        "api safety verdict",
        "display safety verdict",
        "no-active-ingestion verdict",
        "no-persistent-storage verdict",
        "no-upload/download verdict",
        "no-active-ui verdict",
        "no-paper-parsing verdict",
        "no-strategy-generation verdict",
        "no-backtesting verdict",
        "no-recommendation verdict",
        "no-execution verdict",
        "milestone readiness verdict",
    ]:
        assert phrase in combined


def test_prompt_73_docs_state_all_forbidden_surfaces() -> None:
    combined = "\n".join(_read(doc) for doc in PROMPT_73_ACTIVE_DOCS).lower()

    for phrase in [
        "no active artifact ingestion",
        "no active artifact storage",
        "no persistent artifact storage",
        "no upload/download",
        "no active ui",
        "no frontend implementation",
        "no desktop implementation",
        "no paper parsing",
        "no pdf parsing",
        "no arxiv ingestion",
        "no llm paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendations",
        "no action generation",
        "no confidence scoring",
        "decisionobject generation",
        "no broker controls",
        "no readiness-to-trade",
        "no execution apis",
    ]:
        assert phrase in combined


def test_prompt_73_micro_audit_details_preserved_after_deletion() -> None:
    archive_map = _read("docs/testing/CONSOLIDATION_MAP.md")
    deleted_report = _read("docs/reports/DELETED_FILES_REPORT.md")
    tests_report = _read("docs/reports/TESTS_CONSOLIDATED_REPORT.md")

    assert "docs/RESEARCH_ARTIFACT_REGISTRY_NO_ACTIVE_UI_AUDIT.md" in archive_map
    assert "tests/test_research_artifact_registry_no_active_ui_audit.py" in archive_map
    assert "RESEARCH_ARTIFACT_REGISTRY_NO_ACTIVE_UI_AUDIT.md" in deleted_report
    assert "test_research_artifact_registry_no_active_ui_audit.py.archived" in tests_report
