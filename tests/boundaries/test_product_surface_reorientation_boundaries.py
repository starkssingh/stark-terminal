from pathlib import Path

from stark_terminal_core.config.settings import get_settings


ROOT = Path(__file__).resolve().parents[2]

ACTIVE_DECISION_DOCS = [
    "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    "docs/AUDIT_LOG_JOURNAL_TARGET.md",
    "docs/phases/active_decision_architecture.md",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_product_surface_reorientation_adds_no_runtime_capability() -> None:
    phase_doc = _read("docs/phases/product_surface_reorientation.md").lower()
    combined = "\n".join(
        [
            phase_doc,
            _read("docs/NORTH_STAR.md").lower(),
            _read("docs/SAFETY_AUDIT.md").lower(),
        ]
    )

    assert not (ROOT / "apps/api/stark_terminal_api/routes/product_surface_reorientation.py").exists()
    assert not (ROOT / "packages/core/stark_terminal_core/product_surface_reorientation").exists()
    assert "adds no product runtime capability" in combined
    assert "no product runtime capability" in combined
    assert "no active recommendations" in combined
    assert "no active decisionobject generation" in combined
    assert "no confidence scoring" in combined
    assert "no broker controls" in combined
    assert "execution apis remain forbidden" in combined
    assert get_settings().execution_apis_enabled is False


def test_execution_boundary_and_active_decision_docs_are_preserved() -> None:
    combined = "\n".join(
        [
            _read("docs/NORTH_STAR.md"),
            _read("docs/audits/no_execution.md"),
            *[_read(path) for path in ACTIVE_DECISION_DOCS],
        ]
    ).lower()

    assert "decision candidate is not a trade" in combined
    assert "execution apis remain forbidden" in combined
    assert "execution apis: forbidden" in combined

    for path in ACTIVE_DECISION_DOCS:
        assert (ROOT / path).exists()
