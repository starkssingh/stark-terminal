from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_volatility_drawdown_docs_exist_and_contain_required_boundaries() -> None:
    required_docs = [
        "docs/VOLATILITY_ANALYTICS_V0.md",
        "docs/DRAWDOWN_ANALYTICS_V0.md",
        "docs/VOLATILITY_DRAWDOWN_VALIDATION_POLICY.md",
        "docs/VOLATILITY_DRAWDOWN_SAFETY_BOUNDARY.md",
    ]
    combined = "\n".join(_read(path) for path in required_docs)

    for path in required_docs:
        assert (ROOT / path).exists()

    required_phrases = [
        "Volatility Analytics",
        "Drawdown Analytics",
        "sample standard deviation",
        "population standard deviation",
        "annualized volatility",
        "drawdown series",
        "max drawdown",
        "drawdown duration",
        "descriptive-only",
        "no correlation",
        "no backtesting",
        "no regimes",
        "no signals",
        "no recommendations",
        "no DecisionObject",
        "no execution APIs",
        "Mac mini M2",
        "Windows-native",
    ]
    lowered = combined.lower()
    for phrase in required_phrases:
        assert phrase.lower() in lowered


def test_volatility_drawdown_status_docs_reflect_prompt_29() -> None:
    assert "Current Prompt: 36" in _read("docs/NORTH_STAR.md")
    assert "Prompt 29 - Volatility and Drawdown Analytics v0" in _read("docs/PROMPT_LOG.md")
    assert "Volatility and Drawdown Analytics v0" in _read("PROJECT_MAP.md")


def test_next_phase_recommends_prompt_30() -> None:
    next_phase = _read("docs/NEXT_PHASE_PLAN.md")
    roadmap = _read("docs/ANALYTICS_ROADMAP.md")

    assert "Prompt 34 - Regime Feature Preparation Contracts" in next_phase
    assert "Prompt 34 - Regime Feature Preparation Contracts" in roadmap
