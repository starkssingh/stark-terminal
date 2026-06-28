from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_89_research_knowledge_map_docs_and_status() -> None:
    phase_doc = _read("docs/phases/research_knowledge_map.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Prompt 89" in phase_doc
    assert "planning and guardrails" in phase_doc.lower()
    assert "no active knowledge map" in phase_doc.lower()
    assert "no graph or database implementation" in phase_doc.lower()
    assert "no traversal engine" in phase_doc.lower()
    assert "no search engine" in phase_doc.lower()
    assert "no retrieval engine" in phase_doc.lower()
    assert "no embeddings or vector store" in phase_doc.lower()
    assert "no strategy generation" in phase_doc.lower()
    assert "no backtesting" in phase_doc.lower()
    assert "no recommendations" in phase_doc.lower()
    assert "no broker controls" in phase_doc.lower()
    assert "no execution apis" in phase_doc.lower()

    assert "Prompt 89 follows the phase-based docs/tests policy" in consolidation
    assert "No prompt-level micro-audit docs" in consolidation
    assert "Current Prompt: 93" in north_star
    assert "Research Knowledge Map Status: planning/guardrails, API contract skeleton" in north_star
    assert "safety boundary audit complete" in north_star
    assert "Prompt 89 - Research Knowledge Map Planning and Guardrails" in prompt_log
    assert "Prompt 90 - Research Knowledge Map API Contract Skeleton" in next_phase


def test_prompt_89_added_no_micro_audit_sprawl() -> None:
    forbidden_docs = [
        path
        for path in (ROOT / "docs").glob("RESEARCH_KNOWLEDGE_MAP*.md")
        if path.name != "phases/research_knowledge_map.md"
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

    assert [path.relative_to(ROOT).as_posix() for path in forbidden_docs] == []
    assert unexpected_tests == []
