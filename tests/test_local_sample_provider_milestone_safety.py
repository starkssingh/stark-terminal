from __future__ import annotations

from pathlib import Path

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import MarketDataRequestKind
from stark_terminal_core.domain.market_data_contracts import create_market_data_request
from stark_terminal_data_platform.providers.local_sample import (
    LOCAL_SAMPLE_SOURCE_REFERENCE,
    LocalSampleProviderAdapter,
)


ROOT = Path(__file__).resolve().parents[1]


def test_local_sample_provider_remains_synthetic_local_only() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())
    health = provider.health_check()
    assert health.synthetic_only is True
    assert health.real_data_allowed is False
    assert health.network_allowed is False
    assert health.credentials_required is False
    assert health.status == "HEALTHY"


def test_local_sample_provider_unsupported_capabilities_remain_unsupported() -> None:
    provider = LocalSampleProviderAdapter(settings=Settings())
    request = create_market_data_request(MarketDataRequestKind.LATEST_BAR, provider=provider.provider_id)
    response = provider.get_latest_bar(request)
    assert response.errors
    assert response.source_data_reference == LOCAL_SAMPLE_SOURCE_REFERENCE
    assert "real latest bars" in response.errors[0]


def test_local_sample_provider_source_has_no_network_or_scraping_imports() -> None:
    text = (ROOT / "packages/data_platform/stark_terminal_data_platform/providers/local_sample.py").read_text(
        encoding="utf-8"
    )
    forbidden_imports = [
        "import requests",
        "from requests",
        "import httpx",
        "from httpx",
        "import aiohttp",
        "from aiohttp",
        "import socket",
        "from socket",
        "urllib.request",
    ]
    for forbidden in forbidden_imports:
        assert forbidden not in text


def test_local_sample_provider_docs_keep_no_real_data_boundary() -> None:
    text = "\n".join(
        [
            (ROOT / "docs/LOCAL_SAMPLE_PROVIDER_ADAPTER.md").read_text(encoding="utf-8"),
            (ROOT / "docs/LOCAL_SAMPLE_PROVIDER_POLICY.md").read_text(encoding="utf-8"),
            (ROOT / "docs/LOCAL_SAMPLE_PROVIDER_AUDIT.md").read_text(encoding="utf-8"),
        ]
    )
    for phrase in [
        "synthetic",
        "local-only",
        "no external calls",
        "no scraping",
        "no credentials",
        "no real market data",
        "no execution APIs",
    ]:
        assert phrase in text
