from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_91_research_knowledge_map_display_docs_and_status() -> None:
    phase_doc = _read("docs/phases/research_knowledge_map.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    combined = "\n".join([phase_doc, consolidation, north_star, prompt_log, next_phase])
    combined_lower = combined.lower()

    assert "prompt 91" in combined_lower
    assert "research knowledge map display contract skeleton" in combined_lower
    assert "display-contract-skeleton-only" in combined_lower
    assert "item display placeholder" in combined_lower
    assert "relationship display placeholder" in combined_lower
    assert "evidence display placeholder" in combined_lower
    assert "provenance display placeholder" in combined_lower
    assert "lifecycle display placeholder" in combined_lower
    assert "unavailable display response" in combined_lower
    assert "display safety helpers" in combined_lower
    assert "get-only read-only display metadata endpoints" in combined_lower
    assert "no post endpoints" in combined_lower
    assert "prompt 92" in combined_lower
    assert "safety boundary audit" in combined_lower
    assert "no active ui" in combined_lower
    assert "no frontend" in combined_lower
    assert "no desktop" in combined_lower
    assert "no active knowledge map" in combined_lower
    assert "no database" in combined_lower
    assert "no persistent writes" in combined_lower
    assert "no traversal" in combined_lower
    assert "no search" in combined_lower
    assert "no ranking" in combined_lower
    assert "no retrieval" in combined_lower
    assert "no embeddings" in combined_lower
    assert "no vector store" in combined_lower
    assert "no paper parsing" in combined_lower
    assert "no strategy generation" in combined_lower
    assert "no backtesting" in combined_lower
    assert "no recommendations" in combined_lower
    assert "no execution" in combined_lower
    assert "no micro-audit" in combined_lower


def test_prompt_91_added_no_micro_audit_sprawl() -> None:
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
