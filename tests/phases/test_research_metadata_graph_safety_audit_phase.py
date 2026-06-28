from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_87_research_metadata_graph_safety_audit_docs_and_status() -> None:
    safety_doc = ROOT / "docs/RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md"
    phase_doc = ROOT / "docs/phases/research_metadata_graph.md"
    readiness_doc = ROOT / "docs/RESEARCH_METADATA_GRAPH_READINESS_PLAN.md"
    consolidation_doc = ROOT / "docs/testing/CONSOLIDATION_MAP.md"

    assert safety_doc.exists()
    assert phase_doc.exists()
    assert readiness_doc.exists()
    assert consolidation_doc.exists()

    combined = "\n".join(
        [
            safety_doc.read_text(encoding="utf-8"),
            phase_doc.read_text(encoding="utf-8"),
            readiness_doc.read_text(encoding="utf-8"),
            consolidation_doc.read_text(encoding="utf-8"),
            _read("docs/NORTH_STAR.md"),
            _read("docs/NEXT_PHASE_PLAN.md"),
            _read("docs/PROMPT_LOG.md"),
        ]
    ).lower()

    for phrase in [
        "prompt 87",
        "research metadata graph safety boundary audit",
        "prompts 84-86",
        "planning safety verdict",
        "api safety verdict",
        "display safety verdict",
        "no active ui",
        "no frontend",
        "no desktop",
        "no active graph database",
        "no persistent graph writes",
        "no graph tables",
        "no graph migrations",
        "no graph traversal",
        "no graph query",
        "no graph search",
        "no graph ranking",
        "no graph retrieval",
        "no embeddings",
        "no vector store",
        "no active ingestion",
        "no upload/download/preview",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendations",
        "no execution",
        "grouped documentation/testing policy",
        "no micro-audit sprawl",
        "prompt 88",
        "research metadata graph milestone audit",
    ]:
        assert phrase in combined


def test_prompt_87_added_no_research_metadata_graph_micro_audit_sprawl() -> None:
    allowed_docs = {
        "RESEARCH_METADATA_GRAPH_API_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_DISPLAY_CONTRACT_SKELETON.md",
        "RESEARCH_METADATA_GRAPH_PLANNING_AND_GUARDRAILS.md",
        "RESEARCH_METADATA_GRAPH_READINESS_PLAN.md",
        "RESEARCH_METADATA_GRAPH_SAFETY_BOUNDARY_AUDIT.md",
    }
    unexpected_docs = [
        path.name
        for path in (ROOT / "docs").glob("RESEARCH_METADATA_GRAPH_*.md")
        if path.name not in allowed_docs
    ]

    allowed_tests = {
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
    unexpected_tests = [
        path.name
        for path in (ROOT / "tests").rglob("*research_metadata_graph*.py")
        if path.name not in allowed_tests
    ]

    assert unexpected_docs == []
    assert unexpected_tests == []
