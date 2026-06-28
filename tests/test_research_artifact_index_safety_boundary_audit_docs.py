from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT_80_ACTIVE_DOCS = [
    "docs/RESEARCH_ARTIFACT_INDEX_SAFETY_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_INDEX_MILESTONE_READINESS.md",
    "docs/phases/research_artifact_index.md",
    "docs/audits/research_artifact_boundaries.md",
    "docs/audits/safety_boundaries.md",
    "docs/testing/CONSOLIDATION_MAP.md",
]


def test_prompt_80_safety_boundary_audit_docs_exist() -> None:
    for relative in PROMPT_80_ACTIVE_DOCS:
        assert (ROOT / relative).exists(), relative


def test_prompt_80_safety_boundary_audit_docs_cover_forbidden_scope() -> None:
    combined = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in PROMPT_80_ACTIVE_DOCS)

    for phrase in [
        "Prompts 77-79 audited",
        "Research Artifact Index Planning and Guardrails",
        "Research Artifact Index API Contract Skeleton",
        "Research Artifact Index Display Contract Skeleton",
        "No active UI",
        "No frontend implementation",
        "No desktop implementation",
        "No indexing engine",
        "No search engine",
        "No ranking engine",
        "No retrieval",
        "No embeddings",
        "No vector store",
        "No active artifact index ingestion",
        "No persistent artifact index storage",
        "No file upload endpoints",
        "No file download endpoints",
        "No file preview endpoints",
        "No paper parsing",
        "No PDF parsing",
        "No arXiv ingestion",
        "No LLM paper analysis",
        "No strategy generation",
        "No strategy code generation",
        "No backtesting",
        "No optimization",
        "No recommendations",
        "No action generation",
        "No confidence scoring",
        "No active DecisionObjects",
        "No broker controls",
        "No readiness-to-trade",
        "No execution APIs",
        "Prompt 81",
        "Archive Pass 1",
    ]:
        assert phrase in combined


def test_prompt_80_micro_audit_details_preserved_after_deletion() -> None:
    archive_map = (ROOT / "docs/testing/CONSOLIDATION_MAP.md").read_text(encoding="utf-8")
    deleted_report = (ROOT / "docs/reports/DELETED_FILES_REPORT.md").read_text(encoding="utf-8")
    tests_report = (ROOT / "docs/reports/TESTS_CONSOLIDATED_REPORT.md").read_text(encoding="utf-8")

    assert "docs/RESEARCH_ARTIFACT_INDEX_NO_ACTIVE_UI_AUDIT.md" in archive_map
    assert "tests/test_research_artifact_index_no_active_ui_audit.py" in archive_map
    assert "RESEARCH_ARTIFACT_INDEX_NO_ACTIVE_UI_AUDIT.md" in deleted_report
    assert "test_research_artifact_index_no_active_ui_audit.py.archived" in tests_report


def test_prompt_80_active_decision_architecture_preserved() -> None:
    active_decision = (ROOT / "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md").read_text(encoding="utf-8")
    assert "Decision candidate is not a trade" in active_decision
    assert "execution APIs remain forbidden" in active_decision
    assert "No direct signal-to-trade path is allowed" in active_decision
