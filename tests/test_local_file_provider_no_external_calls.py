from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_local_file_provider_modules_do_not_import_network_clients() -> None:
    for path in [
        "packages/data_platform/stark_terminal_data_platform/providers/local_file.py",
        "apps/api/stark_terminal_api/routes/local_file_provider.py",
    ]:
        text = _read(path)
        forbidden_imports = [
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
        for forbidden in forbidden_imports:
            assert forbidden not in text


def test_no_provider_sdk_scraping_or_broker_dependencies_added() -> None:
    pyproject = _read("pyproject.toml").lower()

    for forbidden in [
        "kiteconnect",
        "nsepython",
        "yfinance",
        "beautifulsoup",
        "selenium",
        "alpaca",
        "ib_insync",
        "broker",
    ]:
        assert forbidden not in pyproject


def test_local_file_provider_has_no_persistence_or_event_publishing_calls() -> None:
    text = _read("packages/data_platform/stark_terminal_data_platform/providers/local_file.py")

    for forbidden in [
        "Session(",
        "create_engine",
        "KafkaProducer",
        "Redis",
        "publish(",
        "produce(",
        "insert(",
    ]:
        assert forbidden not in text
