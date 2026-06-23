from __future__ import annotations

import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_safety.overrides import (
    DecisionOverrideProhibition,
    default_decision_override_prohibitions,
    evaluate_decision_override_prohibitions,
)


def test_valid_override_prohibition_blocks_outputs() -> None:
    prohibition = DecisionOverrideProhibition(
        prohibition_id="override-1",
        name="Override Prohibition",
        description="No override is allowed.",
    )

    assert prohibition.overrides_allowed is False
    assert prohibition.emergency_bypass_allowed is False
    assert prohibition.bypass_requires_future_prompt is True
    assert prohibition.blocks_recommendations is True
    assert prohibition.blocks_decision_object_generation is True
    assert prohibition.blocks_execution is True


def test_override_prohibition_rejects_bypass_or_unblocked_outputs() -> None:
    for field, value in [
        ("overrides_allowed", True),
        ("emergency_bypass_allowed", True),
        ("bypass_requires_future_prompt", False),
        ("blocks_recommendations", False),
        ("blocks_decision_object_generation", False),
        ("blocks_execution", False),
    ]:
        with pytest.raises(ValidationError):
            DecisionOverrideProhibition(
                prohibition_id="override-1",
                name="Override Prohibition",
                description="Unsafe override contract.",
                **{field: value},
            )


def test_default_override_prohibitions_exist_and_evaluate_cleanly() -> None:
    prohibitions = default_decision_override_prohibitions()

    assert prohibitions
    assert evaluate_decision_override_prohibitions(prohibitions) == []
