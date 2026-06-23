from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
REGIME_ROOTS = [
    ROOT / "packages/analytics/stark_terminal_analytics/regime",
    ROOT / "packages/analytics/stark_terminal_analytics/regime_features",
]


def _python_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for root in REGIME_ROOTS for path in root.glob("*.py"))


def test_regime_packages_remain_planning_and_contracts_only() -> None:
    text = _python_text()

    assert "RegimeLabelContract" in text
    assert "RegimeFeatureCandidate" in text
    assert "RegimeFeatureEvidenceMapping" in text
    assert "RegimeFeatureProvenanceRequirement" in text
    assert "FeatureValue(" not in text
    assert "FeatureSnapshot(" not in text


def test_no_regime_feature_values_or_label_assignment_functions_exist() -> None:
    text = _python_text()
    forbidden_patterns = [
        r"\bdef compute_feature\b",
        r"\bdef calculate_feature\b",
        r"\bdef assign_regime\b",
        r"\bdef classify_regime\b",
        r"\bdef detect_regime\b",
        r"\bdef fit_",
        r"\bdef predict_",
        r"\badfuller\b",
        r"\bkpss\b",
        r"\bhurst\b",
    ]

    for pattern in forbidden_patterns:
        assert re.search(pattern, text, flags=re.IGNORECASE) is None, pattern


def test_no_feature_registry_write_or_classifier_input_behavior_exists() -> None:
    text = _python_text()

    for phrase in [
        "write_feature_value",
        "register_feature_value",
        "feature_serving",
        "classifier_input",
        "model_input_vector",
    ]:
        assert phrase not in text.lower()

    assert "DecisionObject(" not in text
