from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_SAMPLE_PROVIDER = ROOT / "packages/data_platform/stark_terminal_data_platform/providers/local_sample.py"
LOCAL_SAMPLE_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/local_sample_provider.py"
PYPROJECT = ROOT / "pyproject.toml"


def test_local_sample_provider_imports_no_network_or_scraping_libraries() -> None:
    text = LOCAL_SAMPLE_PROVIDER.read_text(encoding="utf-8").lower()
    route_text = LOCAL_SAMPLE_ROUTE.read_text(encoding="utf-8").lower()
    forbidden_imports = (
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import aiohttp",
        "from aiohttp",
        "import urllib",
        "from urllib",
        "import socket",
        "from socket",
        "import selenium",
        "from selenium",
        "import scrapy",
        "from scrapy",
    )

    for token in forbidden_imports:
        assert token not in text
        assert token not in route_text


def test_local_sample_provider_adds_no_provider_sdk_or_broker_dependencies() -> None:
    text = PYPROJECT.read_text(encoding="utf-8").lower()
    forbidden = (
        "kiteconnect",
        "upstox",
        "angel",
        "fyers",
        "nsepython",
        "yfinance",
        "broker",
        "scrapy",
        "selenium",
    )

    for token in forbidden:
        assert token not in text


def test_local_sample_provider_source_states_safety_boundaries() -> None:
    text = LOCAL_SAMPLE_PROVIDER.read_text(encoding="utf-8")

    assert "LOCAL_SAMPLE" in text
    assert "synthetic-local-test-only" in text
    assert "network calls are forbidden" in text
    assert "real data is forbidden" in text
    assert "options chains" in text
    assert "futures chains" in text
