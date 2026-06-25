from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_strategy_research_workspace_modules_do_not_define_forbidden_active_functions():
    forbidden_function_names = [
        "ingest_paper",
        "parse_paper",
        "generate_strategy",
        "generate_strategy_code",
        "run_backtest",
        "optimize_strategy",
        "generate_recommendation",
        "score_confidence",
        "generate_decision_object",
        "generate_readiness_status",
        "create_order_button",
        "execute_trade",
    ]
    files = list((ROOT / "packages/core/stark_terminal_core/strategy_research_workspace").glob("*.py"))
    files.append(ROOT / "apps/api/stark_terminal_api/routes/strategy_research_workspace.py")

    for path in files:
        text = path.read_text(encoding="utf-8")
        assert "DecisionObject(" not in text
        assert "@router.post" not in text
        for name in forbidden_function_names:
            assert f"def {name}" not in text


def test_strategy_research_workspace_no_frontend_or_desktop_files_added():
    frontend_matches = list(ROOT.glob("**/*strategy*research*workspace*.tsx")) + list(
        ROOT.glob("**/*strategy*research*workspace*.jsx")
    )
    desktop_matches = [
        path
        for path in ROOT.glob("apps/desktop/**/*strategy*research*workspace*.py")
        if "test" not in path.name
    ]

    assert frontend_matches == []
    assert desktop_matches == []


def test_strategy_research_workspace_docs_explicitly_forbid_active_ui_and_execution():
    text = (ROOT / "docs/STRATEGY_RESEARCH_WORKSPACE_PLANNING.md").read_text(encoding="utf-8")
    text += (ROOT / "docs/STRATEGY_RESEARCH_NO_EXECUTION_POLICY.md").read_text(encoding="utf-8")

    assert "No active UI" in text
    assert "No frontend components" in text
    assert "No desktop components" in text
    assert "No execution APIs" in text
    assert "No broker controls" in text
