from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/core/stark_terminal_core/retail_dashboard"
ROUTE = ROOT / "apps/api/stark_terminal_api/routes/retail_dashboard.py"


def test_retail_dashboard_modules_do_not_define_forbidden_generators() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in [*PACKAGE.glob("*.py"), ROUTE])

    forbidden_names = [
        "def generate_dashboard_recommendation",
        "def build_active_dashboard",
        "def create_order_button",
        "def generate_decision_object",
        "def generate_recommendation",
        "def score_confidence",
        "def generate_readiness_status",
        "DecisionObject(",
    ]
    for name in forbidden_names:
        assert name not in text


def test_retail_dashboard_routes_do_not_imply_active_recommendations_or_execution() -> None:
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = getattr(route, "methods", set())
        if path.startswith("/retail-dashboard"):
            lowered = path.lower()
            assert "recommendation" not in lowered
            assert "broker" not in lowered
            assert "execution" not in lowered
            assert "order" not in lowered
            assert "readiness-to-trade" not in lowered
            assert "POST" not in methods


def test_retail_dashboard_prompt_49_adds_no_frontend_ui_files() -> None:
    ui_candidates = [
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard",
        ROOT / "apps/web/retail_dashboard",
    ]
    for path in ui_candidates:
        assert not path.exists()


def test_retail_dashboard_docs_state_no_active_ui_or_broker_controls() -> None:
    docs = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/RETAIL_DASHBOARD_PLANNING.md",
            "docs/RETAIL_DASHBOARD_GUARDRAILS.md",
            "docs/RETAIL_DASHBOARD_NO_EXECUTION_POLICY.md",
        ]
    )
    for phrase in [
        "no active UI",
        "no recommendation cards",
        "no broker controls",
        "no execution APIs",
        "no action states",
    ]:
        assert phrase in docs
