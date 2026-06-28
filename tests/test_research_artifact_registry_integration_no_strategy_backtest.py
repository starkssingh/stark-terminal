from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_no_strategy_backtest_docs_state_integration_boundary() -> None:
    text = (ROOT / "docs/RESEARCH_ARTIFACT_REGISTRY_INTEGRATION_NO_STRATEGY_BACKTEST_AUDIT.md").read_text(
        encoding="utf-8"
    ).lower()
    for phrase in [
        "no strategy generation",
        "no strategy code generation",
        "no signal",
        "factor",
        "alpha generation",
        "no backtesting engine",
        "no optimization",
        "no parameter search",
        "no walk-forward analysis",
        "no performance claims",
        "no backtest result endpoints",
    ]:
        assert phrase in text


def test_no_strategy_backtest_functions_exist() -> None:
    forbidden_defs = [
        "generate_strategy",
        "generate_strategy_code",
        "generate_signal",
        "generate_factor",
        "generate_alpha",
        "run_backtest",
        "optimize_strategy",
        "parameter_search",
        "walk_forward",
    ]
    pattern = re.compile(r"^\s*def\s+(" + "|".join(forbidden_defs) + r")\s*\(", re.MULTILINE)
    for root in [
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_api",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_display",
        ROOT / "packages/core/stark_terminal_core/research_artifact_registry_boundary",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]:
        candidates = root.glob("research_artifact_registry*.py") if root.name == "routes" else root.rglob("*.py")
        for path in candidates:
            assert pattern.search(path.read_text(encoding="utf-8")) is None, str(path.relative_to(ROOT))

