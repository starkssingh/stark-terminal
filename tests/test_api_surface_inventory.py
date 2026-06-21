from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_ENDPOINTS = {
    "/health",
    "/config",
    "/database/health",
    "/timeseries/health",
    "/research-lake/health",
    "/cache/health",
    "/streams/health",
    "/event-backbone/health",
    "/data-quality/health",
    "/workers/health",
    "/instruments/health",
    "/providers/health",
    "/warehouse/health",
    "/features/health",
    "/warehouse/contracts",
    "/features/contracts",
    "/event-backbone/topics",
    "/data-quality/contracts",
    "/instruments/sample",
}

FORBIDDEN_ROUTE_TERMS = (
    "execution",
    "execute",
    "order",
    "broker",
    "live-trading",
    "live_trading",
    "real-money",
    "real_money",
)


def _app_route_paths() -> set[str]:
    route_paths: set[str] = set()
    for route in app.routes:
        if hasattr(route, "path"):
            route_paths.add(route.path)
        original_router = getattr(route, "original_router", None)
        if original_router is not None:
            route_paths.update(
                nested.path for nested in original_router.routes if hasattr(nested, "path")
            )
    return route_paths


def test_api_surface_inventory_lists_expected_endpoints() -> None:
    inventory = (ROOT / "docs/API_SURFACE_INVENTORY.md").read_text(encoding="utf-8")

    for endpoint in EXPECTED_ENDPOINTS:
        assert endpoint in inventory


def test_fastapi_routes_match_inventory_broadly() -> None:
    route_paths = _app_route_paths()

    assert EXPECTED_ENDPOINTS.issubset(route_paths)


def test_no_route_path_contains_forbidden_execution_terms() -> None:
    route_paths = {path.lower() for path in _app_route_paths()}

    for route_path in route_paths:
        assert not any(term in route_path for term in FORBIDDEN_ROUTE_TERMS)
