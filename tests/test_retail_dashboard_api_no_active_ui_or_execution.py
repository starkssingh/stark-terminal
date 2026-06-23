from __future__ import annotations

from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/core/stark_terminal_core/retail_dashboard_api"
ROUTE = ROOT / "apps/api/stark_terminal_api/routes/retail_dashboard_api.py"


def test_retail_dashboard_api_modules_do_not_define_forbidden_generators() -> None:
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


def test_retail_dashboard_api_routes_do_not_imply_active_recommendations_or_execution() -> None:
    paths = app.openapi()["paths"]
    for path, operations in paths.items():
        if path.startswith("/retail-dashboard-api"):
            lowered = path.lower()
            assert "recommendation" not in lowered
            assert "broker" not in lowered
            assert "execution" not in lowered
            assert "order" not in lowered
            assert "readiness-to-trade" not in lowered
            assert "post" not in operations


def test_retail_dashboard_api_prompt_50_adds_no_frontend_ui_files() -> None:
    ui_candidates = [
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard_api.py",
        ROOT / "apps/desktop/stark_terminal_desktop/retail_dashboard_api",
        ROOT / "apps/web/retail_dashboard_api",
        ROOT / "apps/web/retail-dashboard-api",
    ]
    for path in ui_candidates:
        assert not path.exists()


def test_retail_dashboard_api_docs_state_no_active_ui_or_broker_controls() -> None:
    docs = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/RETAIL_DASHBOARD_API_CONTRACT_SKELETON.md",
            "docs/RETAIL_DASHBOARD_API_SAFETY_BOUNDARY.md",
            "docs/RETAIL_DASHBOARD_API_NO_EXECUTION_POLICY.md",
        ]
    )
    for phrase in [
        "no active UI",
        "no recommendation cards",
        "no broker controls",
        "no execution APIs",
        "no action generation",
    ]:
        assert phrase in docs
