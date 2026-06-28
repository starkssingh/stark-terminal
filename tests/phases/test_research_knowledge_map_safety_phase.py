from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_92_research_knowledge_map_safety_docs_and_status() -> None:
    phase_doc = _read("docs/phases/research_knowledge_map.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    combined = "\n".join([phase_doc, consolidation, north_star, prompt_log, next_phase])
    combined_lower = combined.lower()

    assert "prompt 92" in combined_lower
    assert "research knowledge map safety boundary audit" in combined_lower
    assert "planning safety verdict" in combined_lower
    assert "api safety verdict" in combined_lower
    assert "display safety verdict" in combined_lower
    assert "no active ui/frontend/desktop verdict" in combined_lower
    assert "no database/tables/migrations verdict" in combined_lower
    assert "no persistent writes verdict" in combined_lower
    assert "no traversal/query/search/ranking/retrieval verdict" in combined_lower
    assert "no embeddings/vector-store verdict" in combined_lower
    assert "no ingestion/storage/upload/download/preview verdict" in combined_lower
    assert "no paper parsing verdict" in combined_lower
    assert "no strategy-generation verdict" in combined_lower
    assert "no backtesting verdict" in combined_lower
    assert "no recommendation/no-execution verdict" in combined_lower
    assert "grouped documentation/testing policy compliance verdict" in combined_lower
    assert "readiness for phase closure" in combined_lower
    assert "prompt 93" in combined_lower
    assert "research knowledge map phase closure" in combined_lower
    assert "no micro-audit" in combined_lower
    assert "current prompt: 92" in combined_lower
    assert "completed prompts: 93 after completion" in combined_lower


def test_prompt_92_added_no_micro_audit_sprawl() -> None:
    forbidden_docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("RESEARCH_KNOWLEDGE_MAP*.md")
    ]
    allowed_tests = {
        "test_research_knowledge_map_phase.py",
        "test_research_knowledge_map_boundaries.py",
        "test_api_research_knowledge_map.py",
        "test_research_knowledge_map_api_phase.py",
        "test_research_knowledge_map_api_boundaries.py",
        "test_api_research_knowledge_map_contract.py",
        "test_research_knowledge_map_display_phase.py",
        "test_research_knowledge_map_display_boundaries.py",
        "test_api_research_knowledge_map_display.py",
        "test_research_knowledge_map_safety_phase.py",
        "test_research_knowledge_map_safety_boundaries.py",
        "test_api_research_knowledge_map_safety_surface.py",
        "test_research_knowledge_map_phase_closure.py",
    }
    unexpected_tests = [
        path.name
        for path in (ROOT / "tests").rglob("*research_knowledge_map*.py")
        if path.name not in allowed_tests
    ]

    assert forbidden_docs == []
    assert unexpected_tests == []
