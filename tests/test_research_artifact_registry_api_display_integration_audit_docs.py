from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROMPT_76_DOCS = [
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_CROSS_ENDPOINT_CONSISTENCY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_API_DISPLAY_BOUNDARY_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_BOUNDARY_INTEGRATION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_ACTIVE_INGESTION_STORAGE_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_UPLOAD_DOWNLOAD_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_ACTIVE_UI_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_PAPER_PARSING_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_STRATEGY_BACKTEST_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_RECOMMENDATION_EXECUTION_AUDIT.md",
    "docs/RESEARCH_ARTIFACT_INDEX_READINESS_PLAN.md",
]


def test_prompt_76_docs_exist() -> None:
    for doc in PROMPT_76_DOCS:
        assert (ROOT / doc).exists(), doc


def test_prompt_76_docs_contain_required_safety_language() -> None:
    text = "\n".join((ROOT / doc).read_text(encoding="utf-8") for doc in PROMPT_76_DOCS)
    for phrase in [
        "Prompts 70-75",
        "no active ingestion/storage",
        "no upload/download",
        "no active UI",
        "no frontend implementation",
        "no desktop implementation",
        "no paper parsing",
        "no PDF parsing",
        "no arXiv ingestion",
        "no LLM paper analysis",
        "no strategy generation",
        "no strategy code generation",
        "no backtesting",
        "no optimization",
        "no recommendation",
        "no action generation",
        "no confidence scoring",
        "no DecisionObject",
        "no broker controls",
        "no readiness-to-trade",
        "no execution APIs",
        "Research Artifact Index Planning and Guardrails only",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in text


def test_prompt_76_status_docs_are_updated() -> None:
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    next_phase = (ROOT / "docs/NEXT_PHASE_PLAN.md").read_text(encoding="utf-8")

    assert "Current Prompt: 78" in north_star
    assert "Completed Prompts: 79 after completion" in north_star
    assert "Research Artifact Registry Planning Phase - API/Display Integration Readiness Audit completed" in north_star
    assert "Prompt 76 - Research Artifact Registry API/Display Integration Readiness Audit" in prompt_log
    assert "Research Artifact Registry API/Display Integration Readiness Audit" in project_map
    assert "Prompt 77 - Research Artifact Index Planning and Guardrails" in next_phase
