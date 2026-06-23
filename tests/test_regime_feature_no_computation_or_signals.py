from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/analytics/stark_terminal_analytics/regime_features"
ROUTE = ROOT / "apps/api/stark_terminal_api/routes/regime_features.py"


def _python_texts() -> list[tuple[Path, str]]:
    files = [*PACKAGE.glob("*.py"), ROUTE]
    return [(path, path.read_text(encoding="utf-8")) for path in files]


def test_regime_features_modules_do_not_compute_feature_values() -> None:
    forbidden_patterns = [
        r"\bdef compute_feature\b",
        r"\bdef calculate_feature\b",
        r"\bclassify_regime\b",
        r"\bdetect_regime\b",
        r"FeatureValue",
        r"FeatureSnapshot",
    ]

    for path, text in _python_texts():
        for pattern in forbidden_patterns:
            assert re.search(pattern, text) is None, f"{pattern} found in {path}"


def test_regime_features_modules_do_not_expose_trading_action_fields() -> None:
    action_terms = ("buy", "sell", "hold", "watch", "avoid")

    for path, text in _python_texts():
        lowered = text.lower()
        for term in action_terms:
            assert re.search(rf"\b{term}\b", lowered) is None, f"{term} found in {path}"


def test_regime_features_route_has_no_posts_or_recommendation_paths() -> None:
    route_text = ROUTE.read_text(encoding="utf-8").lower()

    assert "@router.post" not in route_text
    assert "recommendation" not in {"/regime-features/recommendation", "/regime-features/signal"}
    assert "/recommend" not in route_text
    assert "/signal" not in route_text


def test_docs_explicitly_forbid_computation_classification_signals_and_execution() -> None:
    docs = [
        ROOT / "docs/REGIME_FEATURE_PREPARATION_CONTRACTS.md",
        ROOT / "docs/REGIME_FEATURE_SAFETY_POLICY.md",
        ROOT / "docs/REGIME_FEATURE_DEPENDENCY_STAGING.md",
    ]
    combined = "\n".join(doc.read_text(encoding="utf-8") for doc in docs)

    for phrase in [
        "no feature computation",
        "no regime classification",
        "no signals",
        "no recommendations",
        "no DecisionObject generation",
        "no execution APIs",
    ]:
        assert phrase in combined
