from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prompt_82_system_boundary_docs_and_policy_status() -> None:
    system_doc = _read("docs/RESEARCH_ARTIFACT_INDEX_SYSTEM_BOUNDARY_HARDENING.md")
    phase_doc = _read("docs/phases/research_artifact_index.md")
    artifact_audit = _read("docs/audits/research_artifact_boundaries.md")
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    combined = "\n".join(
        [system_doc, phase_doc, artifact_audit, consolidation, north_star, prompt_log, next_phase]
    ).lower()

    assert "prompt 82" in combined
    assert "system boundary hardening" in combined
    assert "research_artifact_index_boundary" in system_doc
    assert "forbidden behavior registry" in combined
    assert "endpoint polic" in combined
    assert "module polic" in combined
    assert "invariant" in combined
    assert "no active ui" in combined
    assert "no frontend" in combined
    assert "no desktop" in combined
    assert "no indexing" in combined
    assert "no search" in combined
    assert "no ranking" in combined
    assert "no retrieval" in combined
    assert "no embeddings" in combined
    assert "no vector store" in combined
    assert "no active ingestion" in combined
    assert "no persistent storage" in combined
    assert "no file upload/download/preview" in combined
    assert "no paper parsing" in combined
    assert "no strategy generation" in combined
    assert "no backtesting" in combined
    assert "no recommendations" in combined
    assert "no execution" in combined
    assert "grouped documentation/testing policy" in combined
    assert "prompt 83" in combined


def test_prompt_82_does_not_add_micro_audit_sprawl() -> None:
    prompt_82_docs = [
        path
        for path in (ROOT / "docs").glob("RESEARCH_ARTIFACT_INDEX_SYSTEM_BOUNDARY_*.md")
        if path.name != "RESEARCH_ARTIFACT_INDEX_SYSTEM_BOUNDARY_HARDENING.md"
    ]
    prompt_82_tests = [
        path
        for path in (ROOT / "tests").rglob("*research_artifact_index_system_boundary*.py")
        if path.name
        not in {
            "test_research_artifact_index_system_boundary_phase.py",
            "test_research_artifact_index_system_boundaries.py",
        }
    ]

    assert not prompt_82_docs
    assert prompt_82_tests == []
