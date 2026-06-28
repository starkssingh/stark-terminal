from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_product_surface_reorientation_doc_and_next_prompt_are_recorded() -> None:
    phase_doc = _read("docs/phases/product_surface_reorientation.md")
    policy = _read("docs/testing/TEST_POLICY.md").lower()
    consolidation = _read("docs/testing/CONSOLIDATION_MAP.md")
    north_star = _read("docs/NORTH_STAR.md")
    prompt_log = _read("docs/PROMPT_LOG.md")
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")

    assert "Retail Decision Console / Decision Desk productization" in phase_doc
    assert "Prompt 95 - Retail Decision Console Productization Plan and UI Shell Boundary" in phase_doc
    assert "Prompt 94 does not implement product capability" in phase_doc
    assert "phase-based docs/tests only" in policy
    assert "behavior tests are preferred when real product behavior is added" in policy
    assert "Prompt 94 follows the phase-based docs/tests policy" in consolidation
    assert "Current Prompt: 94" in north_star
    assert "Current Milestone: Product Surface Reorientation" in north_star
    assert "Next Focus: Retail Decision Console / Decision Desk productization" in north_star
    assert "Prompt 94 - Product Surface Reorientation and Development Plan" in prompt_log
    assert "Prompt 95 - Retail Decision Console Productization Plan and UI Shell Boundary" in next_phase


def test_prompt_94_added_no_micro_audit_doc_sprawl() -> None:
    top_level_docs = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").glob("PRODUCT_SURFACE*.md")
    ]
    allowed_tests = {
        "test_product_surface_reorientation_phase.py",
        "test_product_surface_reorientation_boundaries.py",
    }
    unexpected_tests = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*product_surface_reorientation*.py")
        if path.name not in allowed_tests
    ]

    assert (ROOT / "docs/phases/product_surface_reorientation.md").exists()
    assert top_level_docs == []
    assert unexpected_tests == []
