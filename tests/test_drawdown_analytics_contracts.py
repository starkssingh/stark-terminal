from pydantic import ValidationError
import pytest

from stark_terminal_analytics.drawdown.contracts import (
    DrawdownCalculationRequest,
    DrawdownResult,
    create_drawdown_request,
    create_drawdown_result,
)
from stark_terminal_analytics.numerical.contracts import create_synthetic_source_reference, create_vector_contract


def _value_vector():
    return create_vector_contract("values", "Synthetic values", [100.0, 110.0, 90.0])


def test_valid_drawdown_calculation_request() -> None:
    request = create_drawdown_request("drawdown_request", _value_vector())

    assert request.value_vector.descriptive_only is True
    assert request.require_positive_values is True
    assert request.allow_real_data is False
    assert request.created_at.tzinfo is not None


@pytest.mark.parametrize(
    "field",
    ["allow_real_data", "allow_trade_signal", "allow_recommendation", "allow_decision_object"],
)
def test_drawdown_request_rejects_unsafe_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        DrawdownCalculationRequest(request_id="request", value_vector=_value_vector(), **{field: True})


def test_drawdown_result_preserves_source_reference_and_counts() -> None:
    source = create_synthetic_source_reference()
    result = create_drawdown_result(
        result_id="result",
        request_id="request",
        drawdown_values=[0.0, -0.1],
        max_drawdown=-0.1,
        max_drawdown_index=1,
        longest_drawdown_duration=1,
        source=source,
        input_count=2,
    )

    assert result.source == source
    assert result.output_count == 2
    assert result.max_drawdown == -0.1
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


@pytest.mark.parametrize("field", ["trade_signal", "recommendation", "decision_object_generated"])
def test_drawdown_result_rejects_unsafe_flags(field: str) -> None:
    kwargs = {
        "result_id": "result",
        "request_id": "request",
        "drawdown_values": [0.0, -0.1],
        "max_drawdown": -0.1,
        "source": create_synthetic_source_reference(),
        "input_count": 2,
        "output_count": 2,
        "status": "ok",
        field: True,
    }
    with pytest.raises(ValidationError):
        DrawdownResult(**kwargs)


def test_drawdown_result_rejects_positive_drawdown_values() -> None:
    with pytest.raises(ValidationError):
        DrawdownResult(
            result_id="result",
            request_id="request",
            drawdown_values=[0.0, 0.1],
            max_drawdown=0.0,
            source=create_synthetic_source_reference(),
            input_count=2,
            output_count=2,
            status="ok",
        )
