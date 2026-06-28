from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_74_DOCS = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PLANNING_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_DISPLAY_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_SAFETY_MILESTONE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_ACTIVE_INGESTION_STORAGE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_UPLOAD_DOWNLOAD_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_ACTIVE_UI_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_PAPER_PARSING_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_STRATEGY_GENERATION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_BACKTESTING_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_NEXT_PHASE_PLAN.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_74_milestone_audit_docs_exist() -> None:
    for doc in PROMPT_74_DOCS:
        assert (ROOT / doc).exists(), doc


def test_prompt_74_docs_capture_prompt_70_to_73_scope_and_verdicts() -> None:
    combined = "\n".join(_read(doc) for doc in PROMPT_74_DOCS).lower()

    for phrase in [
        "prompts 70-73",
        "research artifact registry planning and guardrails",
        "research artifact registry api contract skeleton",
        "research artifact registry display contract skeleton",
        "research artifact registry safety boundary audit",
        "verification summary",
        "planning verdict",
        "api verdict",
        "display verdict",
        "safety boundary verdict",
        "no-active-ingestion/storage verdict",
        "no-upload/download verdict",
        "no-active-ui verdict",
        "no-paper-parsing verdict",
        "no-strategy-generation verdict",
        "no-backtesting verdict",
        "no-recommendation verdict",
        "no-execution verdict",
        "next-phase readiness verdict",
    ]:
        assert phrase in combined


def test_prompt_74_docs_state_all_forbidden_surfaces() -> None:
    combined = "\n".join(_read(doc) for doc in PROMPT_74_DOCS).lower()

    for phrase in [
        "no ingestion/storage",
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


def test_prompt_74_next_phase_doc_recommends_prompt_75() -> None:
    text = _read("docs/RESEARCH_ARTIFACT_REGISTRY_NEXT_PHASE_PLAN.md")
    assert "Prompt 75 - Research Artifact Registry System Boundary Hardening" in text
    assert "Prompt 76 - Research Artifact Registry API/Display Integration Readiness Audit" in text
    assert "Prompt 77 - Research Artifact Index Planning and Guardrails" in text
