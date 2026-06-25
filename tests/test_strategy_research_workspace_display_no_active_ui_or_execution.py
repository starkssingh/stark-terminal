from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISPLAY_PACKAGE = ROOT / "packages/core/stark_terminal_core/strategy_research_workspace_display"
DISPLAY_ROUTE = ROOT / "apps/api/stark_terminal_api/routes/strategy_research_workspace_display.py"


FORBIDDEN_FUNCTIONS = [
    "def ingest_paper",
    "def parse_paper",
    "def generate_strategy",
    "def generate_strategy_code",
    "def run_backtest",
    "def optimize_strategy",
    "def generate_recommendation",
    "def score_confidence",
    "def generate_decision_object",
    "def generate_readiness_status",
    "def create_order_button",
    "def render_active_workspace",
    "def execute_trade",
]


def test_strategy_research_workspace_display_modules_do_not_generate_decision_objects_or_execution():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in DISPLAY_PACKAGE.glob("*.py"))

    assert "DecisionObject(" not in combined
    assert "@router.post" not in DISPLAY_ROUTE.read_text(encoding="utf-8")
    for forbidden in FORBIDDEN_FUNCTIONS:
        assert forbidden not in combined


def test_strategy_research_workspace_display_route_paths_do_not_imply_active_recommendations():
    route_text = DISPLAY_ROUTE.read_text(encoding="utf-8")

    forbidden_path_terms = [
        "generate-strategy",
        "run-backtest",
        "recommendation-card",
        "buy",
        "sell",
        "hold",
        "watch",
        "avoid",
        "broker",
        "order",
        "execute",
    ]
    for term in forbidden_path_terms:
        assert f'"/strategy-research-workspace-display/{term}' not in route_text


def test_strategy_research_workspace_display_has_no_frontend_or_desktop_files():
    forbidden_files = [
        path
        for path in ROOT.rglob("*strategy*research*workspace*display*")
        if (
            "node_modules" not in path.parts
            and ".git" not in path.parts
            and (
                any(part in {"frontend", "web", "ui"} for part in path.parts)
                or "apps/desktop" in path.as_posix()
            )
        )
    ]

    assert forbidden_files == []


def test_strategy_research_workspace_display_docs_explicitly_state_no_active_ui_and_execution():
    docs_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "docs").glob("STRATEGY_RESEARCH_WORKSPACE_DISPLAY_*.md")
    )

    for phrase in [
        "no active UI",
        "no frontend components",
        "no desktop components",
        "no paper parsing",
        "no strategy generation",
        "no backtesting",
        "no recommendation generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no broker controls",
        "no execution APIs",
    ]:
        assert phrase in docs_text

