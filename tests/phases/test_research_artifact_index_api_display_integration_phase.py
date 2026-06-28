from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_83_integration_readiness_docs_and_status() -> None:
    audit_doc = _read("docs/RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md")
    graph_plan = _read("docs/RESEARCH_METADATA_GRAPH_READINESS_PLAN.md")
    phase_doc = _read("docs/phases/research_artifact_index.md")
    artifact_audit = _read("docs/audits/research_artifact_boundaries.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    combined = "\n".join(
        [audit_doc, graph_plan, phase_doc, artifact_audit, consolidation, north_star, prompt_log, next_phase]
    )
    combined_lower = combined.lower()

    assert "prompt 83" in combined_lower
    assert "api/display integration readiness" in combined_lower
    assert "research metadata graph planning and guardrails" in combined_lower
    assert "prompt 83" in combined_lower
    assert "prompts 77-82" in combined_lower
    assert "cross-endpoint consistency" in combined_lower
    assert "cross-module invariant" in combined_lower
    assert "no active ui" in combined_lower
    assert "no frontend" in combined_lower
    assert "no desktop" in combined_lower
    assert "no indexing" in combined_lower
    assert "no search" in combined_lower
    assert "no ranking" in combined_lower
    assert "no retrieval" in combined_lower
    assert "no embeddings" in combined_lower
    assert "no vector store" in combined_lower
    assert "no ingestion" in combined_lower
    assert "no storage" in combined_lower
    assert "upload/download/preview" in combined_lower
    assert "no paper parsing" in combined_lower
    assert "pdf parsing" in combined_lower
    assert "arxiv ingestion" in combined_lower
    assert "llm paper analysis" in combined_lower
    assert "no strategy generation" in combined_lower
    assert "strategy code generation" in combined_lower
    assert "no backtesting" in combined_lower
    assert "optimization" in combined_lower
    assert "no recommendations" in combined_lower
    assert "action generation" in combined_lower
    assert "confidence scoring" in combined_lower
    assert "active decisionobjects" in combined_lower
    assert "no broker controls" in combined_lower
    assert "readiness-to-trade" in combined_lower
    assert "execution apis" in combined_lower
    assert "grouped docs/tests policy" in combined_lower
    assert "no micro-audit sprawl" in combined_lower


def test_prompt_83_does_not_add_micro_audit_sprawl() -> None:
    prompt_83_docs = [
        path
        for path in (ROOT / "docs").glob("RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_*.md")
        if path.name != "RESEARCH_ARTIFACT_INDEX_API_DISPLAY_INTEGRATION_READINESS_AUDIT.md"
    ]
    prompt_83_tests = [
        path
        for path in (ROOT / "tests").rglob("*research_artifact_index_api_display_integration*.py")
        if path.name
        not in {
            "test_research_artifact_index_api_display_integration_phase.py",
            "test_research_artifact_index_api_display_integration_boundaries.py",
        }
    ]

    assert prompt_83_docs == []
    assert prompt_83_tests == []
