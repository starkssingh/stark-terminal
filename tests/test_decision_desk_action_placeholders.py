import pytest
from pydantic import ValidationError

from stark_terminal_core.decision_desk.action_placeholders import (
    RetailActionPlaceholder,
    RetailActionPlaceholderContract,
    default_retail_action_placeholder_contracts,
)


def test_valid_action_placeholder_contract_is_inactive() -> None:
    contract = RetailActionPlaceholderContract(
        placeholder_id="placeholder-watch",
        action=RetailActionPlaceholder.WATCH,
        display_name="Watch",
        description="Planning placeholder only.",
    )

    assert contract.planning_only is True
    assert contract.generated_now is False
    assert contract.recommendation is False
    assert contract.trade_signal is False
    assert contract.decision_object_generated is False
    assert contract.execution_ready is False


@pytest.mark.parametrize(
    "override",
    [
        {"action": RetailActionPlaceholder.UNKNOWN},
        {"planning_only": False},
        {"generated_now": True},
        {"recommendation": True},
        {"trade_signal": True},
        {"decision_object_generated": True},
        {"execution_ready": True},
    ],
)
def test_action_placeholder_rejects_active_or_unsafe_state(override: dict[str, object]) -> None:
    kwargs = {
        "placeholder_id": "placeholder-test",
        "action": RetailActionPlaceholder.WATCH,
        "display_name": "Watch",
        "description": "Planning placeholder only.",
        **override,
    }

    with pytest.raises(ValidationError):
        RetailActionPlaceholderContract(**kwargs)


def test_default_placeholders_exist_but_are_not_generated_outputs() -> None:
    placeholders = default_retail_action_placeholder_contracts()
    actions = {placeholder.action for placeholder in placeholders}

    assert {
        RetailActionPlaceholder.BUY_BIAS,
        RetailActionPlaceholder.SELL_BIAS,
        RetailActionPlaceholder.HOLD,
        RetailActionPlaceholder.WATCH,
        RetailActionPlaceholder.AVOID,
        RetailActionPlaceholder.REDUCE,
    }.issubset(actions)
    assert all(placeholder.planning_only for placeholder in placeholders)
    assert all(not placeholder.generated_now for placeholder in placeholders)
    assert all(not placeholder.recommendation for placeholder in placeholders)
