from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOTS = [
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
    ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
]
ROUTE_FILES = [
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_api.py",
    ROOT / "apps/api/stark_terminal_api/routes/research_artifact_registry_display.py",
]


def test_phase_has_no_backtest_optimization_or_performance_paths() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for root in SOURCE_ROOTS
        for path in root.glob("*.py")
    )
    for phrase in [
        "def run_backtest",
        "def optimize_strategy",
        "def parameter_search",
        "def walk_forward",
        "def artifact_to_backtest",
        "performance_claim",
    ]:
        assert phrase not in source

    route_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in ROUTE_FILES)
    assert "/backtest" not in route_text


def test_phase_no_backtesting_doc_states_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_PHASE_NO_BACKTESTING_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no backtesting engine",
        "no optimization",
        "no parameter search",
        "no walk-forward analysis",
        "no performance claims",
        "no backtest result endpoints",
        "no artifact-to-backtest path",
    ]:
        assert phrase in text
