from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_analytics_foundation_modules_do_not_expose_action_states() -> None:
    foundation_root = ROOT / "packages/analytics/stark_terminal_analytics/foundation"
    forbidden_terms = ["strong buy", "buy bias", "sell bias", "strong sell", "watchlist", "avoid trade"]

    for path in foundation_root.glob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for term in forbidden_terms:
            assert term not in text, f"{term} leaked into {path}"


def test_analytics_foundation_routes_do_not_imply_recommendations_or_signals() -> None:
    route = _read("apps/api/stark_terminal_api/routes/analytics_foundation.py").lower()

    assert "@router.get(\"/analytics-foundation/health\")" in route
    assert "@router.get(\"/analytics-foundation/contracts\")" in route
    assert "recommendation" not in "/analytics-foundation/health"
    assert "signal" not in "/analytics-foundation/contracts"
    assert "compute_" not in route
    assert "calculate_" not in route


def test_analytics_foundation_does_not_import_heavy_or_external_libraries() -> None:
    foundation_root = ROOT / "packages/analytics/stark_terminal_analytics/foundation"
    forbidden_imports = [
        "import numpy",
        "import scipy",
        "import pandas",
        "import numba",
        "import jax",
        "import torch",
        "import tensorflow",
        "import statsmodels",
        "import requests",
        "import httpx",
        "import aiohttp",
    ]

    for path in foundation_root.glob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for forbidden in forbidden_imports:
            assert forbidden not in text, f"{forbidden} found in {path}"


def test_docs_explicitly_state_no_signals_recommendations_or_calculations() -> None:
    docs = "\n".join(
        _read(path).lower()
        for path in [
            "docs/QUANT_ANALYTICS_FOUNDATION_PLAN.md",
            "docs/TIME_SERIES_ANALYTICS_BOUNDARY.md",
            "docs/ANALYTICS_SAFETY_POLICY.md",
            "docs/ANALYTICS_DEPENDENCY_STAGING.md",
            "docs/ANALYTICS_ROADMAP.md",
        ]
    )

    assert "no analytics calculations" in docs
    assert "no trading signals" in docs
    assert "no recommendations" in docs
    assert "no execution apis" in docs
    assert "descriptive/research-only" in docs
