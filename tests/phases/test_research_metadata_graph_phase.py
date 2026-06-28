from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_84_research_metadata_graph_docs_and_status() -> None:
    planning_doc = _read("docs/RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md")
    phase_doc = _read("docs/phases/research_metadata_graph.md")
    readiness_plan = _read("docs/RESEARCH_METADATA_GRAPH_READINESS_PLAN.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    combined = "\n".join(
        [planning_doc, phase_doc, readiness_plan, consolidation, north_star, prompt_log, next_phase]
    )
    combined_lower = combined.lower()

    assert "prompt 84" in combined_lower
    assert "research metadata graph planning and guardrails" in combined_lower
    assert "planning and guardrails only" in combined_lower
    assert "prompt 85" in combined_lower
    assert "api contract skeleton" in combined_lower
    assert "graph node placeholder" in combined_lower
    assert "graph edge placeholder" in combined_lower
    assert "provenance" in combined_lower
    assert "lifecycle" in combined_lower
    assert "dependency" in combined_lower
    assert "no active graph database" in combined_lower
    assert "no persistent graph writes" in combined_lower
    assert "no graph traversal" in combined_lower
    assert "no graph search" in combined_lower
    assert "no graph ranking" in combined_lower
    assert "no graph retrieval" in combined_lower
    assert "no embeddings" in combined_lower
    assert "no vector store" in combined_lower
    assert "no active ingestion" in combined_lower
    assert "upload/download/preview" in combined_lower
    assert "no paper parsing" in combined_lower
    assert "no strategy generation" in combined_lower
    assert "no backtesting" in combined_lower
    assert "no recommendations" in combined_lower
    assert "no execution" in combined_lower
    assert "grouped docs/tests policy" in combined_lower
    assert "no micro-audit sprawl" in combined_lower


def test_prompt_84_does_not_add_micro_audit_sprawl() -> None:
    allowed_docs = {
        "RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md",
        "RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
        "RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md",
    }
    prompt_84_docs = [
        path
        for path in (ROOT / "docs").glob("RESEARCH_METADATA_GRAPH_*.md")
        if path.name not in allowed_docs
    ]
    prompt_84_tests = [
        path
        for path in (ROOT / "tests").rglob("*research_metadata_graph*.py")
        if path.name
        not in {
            "test_research_metadata_graph_phase.py",
            "test_research_metadata_graph_boundaries.py",
            "test_api_research_metadata_graph.py",
            "test_research_metadata_graph_api_phase.py",
            "test_research_metadata_graph_api_boundaries.py",
            "test_api_research_metadata_graph_contract.py",
            "test_research_metadata_graph_display_phase.py",
            "test_research_metadata_graph_display_boundaries.py",
            "test_api_research_metadata_graph_display.py",
            "test_research_metadata_graph_safety_audit_phase.py",
            "test_research_metadata_graph_safety_boundaries.py",
            "test_api_research_metadata_graph_safety_surface.py",
            "test_research_metadata_graph_phase_closure.py",
        }
    ]

    assert prompt_84_docs == []
    assert prompt_84_tests == []
