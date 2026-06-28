from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ROUTES_ROOT = ROOT / "apps/api/stark_terminal_api/routes"


def test_consolidated_no_execution_doc_contains_hard_boundary() -> None:
    text = (ROOT / "docs/audits/no_execution.md").read_text(encoding="utf-8").lower()

    required = [
        "execution apis remain forbidden",
        "no broker controls",
        "no order placement",
        "no real-money routing",
        "no hidden trade interpretation",
        "no readiness-to-trade",
        "no approvals or overrides as an execution bypass",
        "no market-data-to-trade path",
        "no signal-to-trade path",
    ]

    for phrase in required:
        assert phrase in text


def test_api_routes_do_not_define_execution_like_write_routes() -> None:
    forbidden_route_fragments = [
        '@router.post("/execution',
        '@router.post("/execute',
        '@router.post("/orders',
        '@router.post("/broker',
        '@router.post("/approval',
        '@router.post("/override',
        '@router.put("/execution',
        '@router.delete("/execution',
    ]
    forbidden_functions = [
        "def execute_trade",
        "def place_order",
        "def route_order",
        "def submit_order",
        "def approve_trade",
        "def override_trade",
    ]

    bad: list[str] = []
    for path in ROUTES_ROOT.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for phrase in [*forbidden_route_fragments, *forbidden_functions]:
            if phrase in text:
                bad.append(f"{path.relative_to(ROOT)}:{phrase}")

    assert bad == []
