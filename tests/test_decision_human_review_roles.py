from __future__ import annotations

import pytest

from stark_terminal_core.decision_human_review.roles import (
    DecisionReviewerRolePlaceholder,
    default_decision_reviewer_role_placeholders,
)
from stark_terminal_core.decision_human_review.workflow import DecisionReviewerRoleKind


def _role_kwargs() -> dict[str, object]:
    return {
        "role_id": "role-test",
        "role_kind": DecisionReviewerRoleKind.HUMAN_OPERATOR,
        "display_name": "Role Test",
        "description": "Role placeholder test",
    }


def test_valid_decision_reviewer_role_placeholder() -> None:
    role = DecisionReviewerRolePlaceholder(**_role_kwargs())

    assert role.authenticated is False
    assert role.active_user_bound is False
    assert role.can_approve is False
    assert role.can_override is False
    assert role.can_generate_recommendations is False
    assert role.can_generate_decision_objects is False
    assert role.can_execute is False


def test_unknown_decision_reviewer_role_kind_rejected() -> None:
    kwargs = _role_kwargs()
    kwargs["role_kind"] = DecisionReviewerRoleKind.UNKNOWN

    with pytest.raises(ValueError):
        DecisionReviewerRolePlaceholder(**kwargs)


@pytest.mark.parametrize(
    "flag",
    [
        "authenticated",
        "active_user_bound",
        "can_approve",
        "can_override",
        "can_generate_recommendations",
        "can_generate_decision_objects",
        "can_execute",
    ],
)
def test_decision_reviewer_role_rejects_capability_flags(flag: str) -> None:
    kwargs = _role_kwargs()
    kwargs[flag] = True

    with pytest.raises(ValueError):
        DecisionReviewerRolePlaceholder(**kwargs)


def test_default_decision_reviewer_role_placeholders_validate() -> None:
    roles = default_decision_reviewer_role_placeholders()

    assert roles
    assert all(role.authenticated is False for role in roles)
    assert all(role.can_approve is False for role in roles)
    assert all(role.can_execute is False for role in roles)
