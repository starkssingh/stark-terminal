from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_pyproject_has_no_provider_sdk_scraping_or_broker_dependencies() -> None:
    text = _read("pyproject.toml").lower()
    forbidden = [
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

    for dependency in forbidden:
        assert dependency not in text


def test_provider_docs_confirm_no_sdks_or_scraping_dependencies() -> None:
    text = "\n".join(
        _read(path)
        for path in [
            "docs/PROVIDER_ADAPTER_MILESTONE_AUDIT.md",
            "docs/PROVIDER_NO_EXTERNAL_CALLS_AUDIT.md",
            "docs/TECH_STACK.md",
            "docs/SAFETY_AUDIT.md",
        ]
    )

    for phrase in [
        "no provider SDKs",
        "no scraping",
        "no broker/trading dependencies",
        "no credentials",
        "no real market ingestion",
    ]:
        assert phrase in text
