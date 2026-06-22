from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_provider_readiness_modules_do_not_import_network_clients() -> None:
    files = [
        "packages/data_platform/stark_terminal_data_platform/providers/candidates.py",
        "packages/data_platform/stark_terminal_data_platform/providers/selection.py",
        "apps/api/stark_terminal_api/routes/provider_readiness.py",
    ]
    forbidden = ["import requests", "import httpx", "import aiohttp", "from requests", "from httpx", "socket."]

    for path in files:
        text = (ROOT / path).read_text(encoding="utf-8")
        for phrase in forbidden:
            assert phrase not in text


def test_no_provider_sdk_scraping_or_broker_dependencies_added() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    forbidden_dependencies = [
        "nsepy",
        "yfinance",
        "kiteconnect",
        "beautifulsoup",
        "selenium",
        "scrapy",
        "alpaca",
        "ib_insync",
    ]

    for dependency in forbidden_dependencies:
        assert dependency not in pyproject
