from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_provider_guardrail_modules_do_not_import_network_or_scraping_clients() -> None:
    files = [
        ROOT / "packages/data_platform/stark_terminal_data_platform/providers/guardrails.py",
        ROOT / "packages/data_platform/stark_terminal_data_platform/providers/approval.py",
        ROOT / "packages/data_platform/stark_terminal_data_platform/providers/readiness.py",
        ROOT / "apps/api/stark_terminal_api/routes/provider_guardrails.py",
    ]
    forbidden_imports = [
        "import requests",
        "import httpx",
        "import aiohttp",
        "import urllib.request",
        "from urllib",
        "import socket",
        "selenium",
        "beautifulsoup",
        "bs4",
    ]

    for path in files:
        text = path.read_text(encoding="utf-8").lower()
        assert all(term not in text for term in forbidden_imports)


def test_no_provider_sdk_scraping_or_broker_dependencies_added() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    dependencies_section = pyproject.split("dependencies = [", 1)[1].split("]", 1)[0]
    forbidden_dependencies = [
        "kiteconnect",
        "zerodha",
        "upstox",
        "nsetools",
        "beautifulsoup4",
        "scrapy",
        "selenium",
        "playwright",
        "broker",
        "trading",
    ]

    assert all(dependency not in dependencies_section for dependency in forbidden_dependencies)
