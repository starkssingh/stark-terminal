from pathlib import Path
import re

from stark_terminal_core.decision_desk.action_placeholders import default_retail_action_placeholder_contracts


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "packages/core/stark_terminal_core/decision_desk"
ROUTE = ROOT / "apps/api/stark_terminal_api/routes/decision_desk.py"


def _python_texts() -> list[tuple[Path, str]]:
    files = [*PACKAGE.glob("*.py"), ROUTE]
    return [(path, path.read_text(encoding="utf-8")) for path in files]


def test_decision_desk_modules_do_not_generate_recommendations_or_confidence() -> None:
    forbidden_patterns = [
        r"\bdef generate_recommendation\b",
        r"\bdef generate_action\b",
        r"\bdef score_confidence\b",
        r"\bclassify_regime\b",
        r"\bdetect_regime\b",
        r"DecisionObject\(",
        r"@router\.post",
    ]

    for path, text in _python_texts():
        for pattern in forbidden_patterns:
            assert re.search(pattern, text) is None, f"{pattern} found in {path}"


def test_action_terms_are_placeholders_not_generated_outputs() -> None:
    placeholders = default_retail_action_placeholder_contracts()

    assert placeholders
    assert all(placeholder.planning_only for placeholder in placeholders)
    assert all(not placeholder.generated_now for placeholder in placeholders)
    assert all(not placeholder.recommendation for placeholder in placeholders)
    assert all(not placeholder.trade_signal for placeholder in placeholders)
    assert all(not placeholder.decision_object_generated for placeholder in placeholders)
    assert all(not placeholder.execution_ready for placeholder in placeholders)


def test_decision_desk_route_has_no_posts_or_recommendation_paths() -> None:
    route_text = ROUTE.read_text(encoding="utf-8").lower()

    assert "@router.post" not in route_text
    assert "/recommend" not in route_text
    assert "/signal" not in route_text
    assert "/execute" not in route_text


def test_docs_explicitly_forbid_recommendations_decision_objects_and_execution() -> None:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "docs/RETAIL_DECISION_DESK_PLANNING.md",
            "docs/DECISION_DESK_ACTION_PLACEHOLDERS.md",
            "docs/DECISION_DESK_SAFETY_POLICY.md",
            "docs/DECISION_DESK_DISPLAY_BOUNDARY.md",
        ]
    )

    for phrase in [
        "no recommendations",
        "no action-state generation",
        "no confidence scoring",
        "no DecisionObject generation",
        "no execution APIs",
    ]:
        assert phrase in combined
