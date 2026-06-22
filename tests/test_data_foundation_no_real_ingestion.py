from pathlib import Path

from stark_terminal_core.config.settings import Settings


ROOT = Path(__file__).resolve().parents[1]

PROMPT_14_TO_16_CODE_ROOTS = [
    ROOT / "packages/data_platform/stark_terminal_data_platform/fixtures",
    ROOT / "packages/data_platform/stark_terminal_data_platform/repositories",
    ROOT / "packages/data_platform/stark_terminal_data_platform/services",
    ROOT / "apps/api/stark_terminal_api/routes",
]

FORBIDDEN_FILENAME_TERMS = {
    "scrape",
    "scraper",
    "real_ingestion",
    "live_provider",
    "live_data",
    "execution",
    "broker",
    "order",
}

FORBIDDEN_EXTERNAL_CALL_SNIPPETS = {
    "requests.",
    "httpx.",
    "aiohttp",
    "urllib.request",
    "socket.create_connection",
    "selenium",
    "playwright",
}


def test_no_route_file_names_imply_real_ingestion_or_execution() -> None:
    bad = []
    for route in (ROOT / "apps/api/stark_terminal_api/routes").glob("*.py"):
        lowered = route.name.lower()
        if any(term in lowered for term in FORBIDDEN_FILENAME_TERMS):
            bad.append(route.name)

    assert bad == []


def test_prompt_14_to_16_code_has_no_external_call_dependencies() -> None:
    bad = []
    for root in PROMPT_14_TO_16_CODE_ROOTS:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            if any(snippet in text for snippet in FORBIDDEN_EXTERNAL_CALL_SNIPPETS):
                bad.append(str(path.relative_to(ROOT)))

    assert bad == []


def test_provider_network_and_external_market_calls_remain_disabled_by_default() -> None:
    settings = Settings()

    assert settings.allow_external_market_data_calls is False
    assert settings.allow_provider_network_calls is False
    assert settings.execution_apis_enabled is False
    assert settings.broker_integrations_enabled is False
    assert settings.live_trading_enabled is False


def test_fixture_docs_and_api_route_clearly_mark_synthetic() -> None:
    docs_and_routes = "\n".join(
        [
            (ROOT / "docs/SYNTHETIC_MARKET_DATA_FIXTURES.md").read_text(encoding="utf-8"),
            (ROOT / "docs/SAMPLE_DATA_POLICY.md").read_text(encoding="utf-8"),
            (ROOT / "apps/api/stark_terminal_api/routes/fixtures.py").read_text(encoding="utf-8"),
        ]
    )

    for phrase in [
        "synthetic",
        "local-only",
        "test/dev",
        "real_market_data",
        "False",
        "no external calls",
    ]:
        assert phrase in docs_and_routes
