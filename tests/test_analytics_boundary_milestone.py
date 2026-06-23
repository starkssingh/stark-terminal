from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANALYTICS_ROOT = ROOT / "packages/analytics/stark_terminal_analytics"


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_analytics_foundation_remains_planning_contracts_guardrails() -> None:
    foundation_contracts = _read("packages/analytics/stark_terminal_analytics/foundation/contracts.py")
    foundation_safety = _read("packages/analytics/stark_terminal_analytics/foundation/safety.py")

    assert "AnalyticsModulePlan" in foundation_contracts
    assert "AnalyticsSafetyPolicy" in foundation_safety
    assert "allow_trade_signals: bool = False" in foundation_safety
    assert "allow_recommendations: bool = False" in foundation_safety
    assert "allow_execution: bool = False" in foundation_safety


def test_implemented_analytics_modules_are_descriptive_only() -> None:
    module_files = [
        "packages/analytics/stark_terminal_analytics/numerical/contracts.py",
        "packages/analytics/stark_terminal_analytics/returns/contracts.py",
        "packages/analytics/stark_terminal_analytics/rolling/contracts.py",
        "packages/analytics/stark_terminal_analytics/volatility/contracts.py",
        "packages/analytics/stark_terminal_analytics/drawdown/contracts.py",
        "packages/analytics/stark_terminal_analytics/correlation/contracts.py",
        "packages/analytics/stark_terminal_analytics/beta/contracts.py",
        "packages/analytics/stark_terminal_analytics/diagnostics/contracts.py",
    ]

    for path in module_files:
        text = _read(path)
        assert "descriptive_only: bool = True" in text
        assert "trade_signal" in text
        assert "recommendation" in text
        assert "decision_object" in text.lower()


def test_future_analytics_modules_and_regime_classifiers_remain_unimplemented() -> None:
    missing_dirs = [
        "packages/analytics/stark_terminal_analytics/backtesting",
        "packages/analytics/stark_terminal_analytics/indicators",
        "packages/analytics/stark_terminal_analytics/features",
    ]

    for path in missing_dirs:
        assert not (ROOT / path).exists()

    regime_root = ROOT / "packages/analytics/stark_terminal_analytics/regime"
    assert regime_root.exists()
    for path in regime_root.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "def classify_regime" not in text
        assert "def detect_regime" not in text
        assert "DecisionObject(" not in text


def test_analytics_boundary_docs_match_current_scope() -> None:
    text = _read("docs/ANALYTICS_BOUNDARY_AUDIT.md")

    for allowed in [
        "simple returns",
        "rolling count",
        "sample standard deviation",
        "annualized volatility",
        "drawdown series",
        "Pearson correlation",
        "beta = covariance",
    ]:
        assert allowed in text

    for forbidden in [
        "run backtests",
        "run regimes",
        "compute indicators",
        "compute factors or features",
        "run ML models",
    ]:
        assert forbidden in text
