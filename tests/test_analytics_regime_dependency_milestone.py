from __future__ import annotations

from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
HEAVY_DEPS = {
    "numpy",
    "scipy",
    "pandas",
    "numba",
    "jax",
    "cupy",
    "torch",
    "tensorflow",
    "xgboost",
    "lightgbm",
    "catboost",
    "quantlib",
    "statsmodels",
    "arch",
    "scikit-learn",
    "sklearn",
    "hmmlearn",
    "ruptures",
    "vectorbt",
    "backtrader",
}
FORBIDDEN_PROVIDER_DEPS = {
    "kiteconnect",
    "upstox",
    "nsepython",
    "nsepy",
    "yfinance",
    "beautifulsoup",
    "bs4",
    "selenium",
    "scrapy",
    "alpaca-trade-api",
    "ib_insync",
    "ccxt",
}


def _project_dependencies() -> set[str]:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = pyproject.get("project", {}).get("dependencies", [])
    return {
        dependency.split("[", 1)[0]
        .split(">", 1)[0]
        .split("=", 1)[0]
        .split("<", 1)[0]
        .split("!", 1)[0]
        .split("~", 1)[0]
        .strip()
        .lower()
        for dependency in dependencies
    }


def test_pyproject_has_no_heavy_analytics_or_regime_model_dependencies() -> None:
    dependencies = _project_dependencies()

    assert dependencies.isdisjoint(HEAVY_DEPS)
    assert dependencies.isdisjoint(FORBIDDEN_PROVIDER_DEPS)


def test_analytics_regime_modules_do_not_import_external_call_clients() -> None:
    forbidden_imports = (
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import aiohttp",
        "from aiohttp",
        "import urllib.request",
        "from urllib.request",
        "import socket",
    )
    root = ROOT / "packages/analytics/stark_terminal_analytics"

    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden_imports:
            assert phrase not in text, f"{phrase} found in {path}"


def test_dependency_audit_docs_keep_heavy_dependencies_gated() -> None:
    text = (ROOT / "docs/ANALYTICS_REGIME_DEPENDENCY_AUDIT.md").read_text(encoding="utf-8")

    for phrase in [
        "No heavy analytics/model dependencies",
        "provider SDKs",
        "scraping dependencies",
        "broker/trading dependencies",
        "future dependency gate",
    ]:
        assert phrase in text
