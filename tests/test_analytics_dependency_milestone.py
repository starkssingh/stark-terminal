from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
ANALYTICS_ROOT = ROOT / "packages/analytics/stark_terminal_analytics"


FORBIDDEN_DEPENDENCIES = [
    "numpy",
    "scipy",
    "numba",
    "jax",
    "cupy",
    "torch",
    "tensorflow",
    "statsmodels",
    "arch",
    "ta-lib",
    "vectorbt",
    "backtrader",
    "quantlib",
    "xgboost",
    "lightgbm",
    "catboost",
    "scikit-learn",
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
]

FORBIDDEN_IMPORTS = [
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_pyproject_has_no_new_heavy_provider_scraping_or_broker_dependencies() -> None:
    data = tomllib.loads(_read("pyproject.toml"))
    dependencies = data.get("project", {}).get("dependencies", [])
    dependency_names = {
        dependency.split("[", 1)[0].split(">", 1)[0].split("=", 1)[0].split("<", 1)[0].strip().lower()
        for dependency in dependencies
    }

    for dependency in FORBIDDEN_DEPENDENCIES:
        assert dependency not in dependency_names


def test_analytics_modules_do_not_import_external_call_clients() -> None:
    for path in ANALYTICS_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_IMPORTS:
            assert forbidden not in text, f"{path} imports {forbidden}"


def test_dependency_audit_docs_state_heavy_dependencies_remain_gated() -> None:
    text = "\n".join(
        [
            _read("docs/ANALYTICS_DEPENDENCY_AUDIT.md"),
            _read("docs/TECH_STACK.md"),
            _read("docs/ANALYTICS_STACK.md"),
        ]
    )

    for phrase in [
        "no heavy analytics dependencies",
        "no provider SDKs",
        "no scraping dependencies",
        "no broker/trading dependencies",
        "future dependency gate",
    ]:
        assert phrase in text
