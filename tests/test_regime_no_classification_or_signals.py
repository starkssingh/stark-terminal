from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_regime_modules_do_not_expose_action_terms_as_words() -> None:
    regime_root = ROOT / "packages/analytics/stark_terminal_analytics/regime"
    forbidden_terms = {"buy", "sell", "hold", "watch", "avoid"}

    for path in regime_root.glob("*.py"):
        text = _read(path).lower()
        for term in forbidden_terms:
            assert re.search(rf"\b{term}\b", text) is None, f"{term} found in {path}"


def test_regime_modules_do_not_classify_or_generate_decision_objects() -> None:
    regime_root = ROOT / "packages/analytics/stark_terminal_analytics/regime"

    for path in regime_root.glob("*.py"):
        text = _read(path)
        lowered = text.lower()
        assert "DecisionObject(" not in text
        assert "def classify_regime" not in lowered
        assert "def detect_regime" not in lowered
        if path.name != "dependencies.py":
            assert "hmmlearn" not in lowered
            assert "ruptures" not in lowered
        assert "adfuller" not in lowered
        assert "kpss" not in lowered
        assert "def generate_signal" not in lowered
        assert "def recommend" not in lowered


def test_regime_route_does_not_imply_signal_recommendation_or_data_input_paths() -> None:
    text = _read(ROOT / "apps/api/stark_terminal_api/routes/regime_analytics.py").lower()

    assert "/signals" not in text
    assert "/recommendations" not in text
    assert "/decisions" not in text
    assert "/classify" not in text
    assert "@router.post" not in text


def test_regime_docs_explicitly_forbid_classification_and_execution() -> None:
    docs = [
        ROOT / "docs/REGIME_ANALYTICS_PLANNING.md",
        ROOT / "docs/REGIME_LABEL_CONTRACTS.md",
        ROOT / "docs/REGIME_ANALYTICS_SAFETY_POLICY.md",
        ROOT / "docs/REGIME_DEPENDENCY_STAGING.md",
    ]
    combined = "\n".join(_read(path) for path in docs)

    assert "no classification" in combined
    assert "no regime classification" in combined
    assert "no signals" in combined
    assert "no recommendations" in combined
    assert "no DecisionObject generation" in combined
    assert "no execution APIs" in combined
