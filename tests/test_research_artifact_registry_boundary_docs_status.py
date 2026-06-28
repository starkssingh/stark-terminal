from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_75_DOCS = [
    "RESEARCH_ARTIFACT_REGISTRY_SYSTEM_BOUNDARY_HARDENING.md",
    "RESEARCH_ARTIFACT_FORBIDDEN_BEHAVIOR_REGISTRY.md",
    "RESEARCH_ARTIFACT_ENDPOINT_BOUNDARY_POLICY.md",
    "RESEARCH_ARTIFACT_MODULE_BOUNDARY_POLICY.md",
    "RESEARCH_ARTIFACT_CROSS_MODULE_INVARIANTS.md",
    "RESEARCH_ARTIFACT_BOUNDARY_NO_INGESTION_STORAGE_POLICY.md",
    "RESEARCH_ARTIFACT_BOUNDARY_NO_UPLOAD_DOWNLOAD_POLICY.md",
    "RESEARCH_ARTIFACT_BOUNDARY_NO_ACTIVE_UI_POLICY.md",
    "RESEARCH_ARTIFACT_BOUNDARY_NO_PAPER_PARSING_POLICY.md",
    "RESEARCH_ARTIFACT_BOUNDARY_NO_STRATEGY_GENERATION_POLICY.md",
    "RESEARCH_ARTIFACT_BOUNDARY_NO_BACKTESTING_POLICY.md",
    "RESEARCH_ARTIFACT_BOUNDARY_NO_EXECUTION_POLICY.md",
]


def _doc_text(name: str) -> str:
    return (ROOT / "docs" / name).read_text(encoding="utf-8")


def test_prompt_75_boundary_docs_exist() -> None:
    for doc in PROMPT_75_DOCS:
        assert (ROOT / "docs" / doc).exists(), doc


def test_prompt_75_boundary_docs_state_forbidden_scope() -> None:
    combined = "\n".join(_doc_text(doc) for doc in PROMPT_75_DOCS).lower()

    for phrase in [
        "boundary-hardening-only",
        "forbidden behavior registry",
        "endpoint boundary policy",
        "module boundary policy",
        "cross-module invariants",
        "no active ingestion/storage",
        "no file upload/download",
        "no file preview",
        "no active ui",
        "no frontend/desktop implementation",
        "no paper parsing",
        "no pdf/arxiv ingestion",
        "no llm paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendation generation",
        "no action generation",
        "no confidence scoring",
        "no decisionobject generation",
        "no readiness-to-trade",
        "no broker controls",
        "no execution apis",
        "future prompt and audit required",
        "mac mini m2",
        "windows-native",
    ]:
        assert phrase in combined


def test_prompt_75_status_docs_are_updated() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")

    assert "Current Prompt: 78" in north_star
    assert "Completed Prompts: 76 after completion" in north_star
    assert "Research Artifact Registry Planning Phase - System Boundary Hardening" in north_star
    assert "Prompt 75 - Research Artifact Registry System Boundary Hardening" in prompt_log
    assert "research_artifact_registry_boundary" in project_map
    assert "Research Artifact Registry System Boundary Hardening" in project_map
    assert "Prompt 76 - Research Artifact Registry API/Display Integration Readiness Audit" in next_phase

