from pathlib import Path

from fastapi.testclient import TestClient

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]

PROVIDER_MODULES = [
    "packages/data_platform/stark_terminal_data_platform/providers/guardrails.py",
    "packages/data_platform/stark_terminal_data_platform/providers/approval.py",
    "packages/data_platform/stark_terminal_data_platform/providers/readiness.py",
    "packages/data_platform/stark_terminal_data_platform/providers/candidates.py",
    "packages/data_platform/stark_terminal_data_platform/providers/selection.py",
    "packages/data_platform/stark_terminal_data_platform/providers/local_sample.py",
    "packages/data_platform/stark_terminal_data_platform/providers/local_file.py",
    "apps/api/stark_terminal_api/routes/provider_guardrails.py",
    "apps/api/stark_terminal_api/routes/provider_readiness.py",
    "apps/api/stark_terminal_api/routes/local_sample_provider.py",
    "apps/api/stark_terminal_api/routes/local_file_provider.py",
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


def test_provider_modules_do_not_import_external_call_clients() -> None:
    for path in PROVIDER_MODULES:
        text = _read(path)
        for forbidden in FORBIDDEN_IMPORTS:
            assert forbidden not in text, f"{path} imports {forbidden}"


def test_provider_endpoints_do_not_call_out_or_claim_live_data() -> None:
    client = TestClient(app)
    endpoints = [
        "/provider-guardrails/health",
        "/provider-guardrails/contracts",
        "/provider-readiness/health",
        "/provider-readiness/contracts",
        "/local-sample-provider/health",
        "/local-sample-provider/contracts",
        "/local-file-provider/health",
        "/local-file-provider/contracts",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint
        text = str(response.json()).lower()
        assert "external_calls': true" not in text
        assert "network_calls': true" not in text
        assert "live market data" not in text
        assert "real_market_data': true" not in text
