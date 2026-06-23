from pydantic import ValidationError
import pytest

from stark_terminal_analytics.numerical.contracts import create_synthetic_source_reference, create_vector_contract
from stark_terminal_analytics.returns.contracts import (
    ReturnCalculationRequest,
    ReturnMethod,
    ReturnSeriesResult,
    create_return_request,
    create_return_result,
)


def _price_vector():
    return create_vector_contract("prices", "Synthetic prices", [100.0, 105.0, 103.0])


def test_valid_return_calculation_request() -> None:
    request = create_return_request("returns_request", _price_vector(), ReturnMethod.SIMPLE)

    assert request.method == ReturnMethod.SIMPLE
    assert request.price_vector.descriptive_only is True
    assert request.allow_real_data is False
    assert request.created_at.tzinfo is not None


@pytest.mark.parametrize(
    "field",
    ["allow_real_data", "allow_trade_signal", "allow_recommendation", "allow_decision_object"],
)
def test_return_request_rejects_unsafe_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        ReturnCalculationRequest(request_id="request", price_vector=_price_vector(), method=ReturnMethod.SIMPLE, **{field: True})


def test_return_request_rejects_unknown_method() -> None:
    with pytest.raises(ValidationError):
        ReturnCalculationRequest(request_id="request", price_vector=_price_vector(), method=ReturnMethod.UNKNOWN)


def test_return_result_preserves_source_reference_and_counts() -> None:
    source = create_synthetic_source_reference()
    result = create_return_result(
        result_id="result",
        request_id="request",
        method=ReturnMethod.SIMPLE,
        values=[0.1, -0.02],
        source=source,
        input_count=3,
    )

    assert result.source == source
    assert result.output_count == 2
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


@pytest.mark.parametrize("field", ["trade_signal", "recommendation", "decision_object_generated"])
def test_return_result_rejects_unsafe_flags(field: str) -> None:
    kwargs = {
        "result_id": "result",
        "request_id": "request",
        "method": ReturnMethod.SIMPLE,
        "values": [0.01],
        "source": create_synthetic_source_reference(),
        "input_count": 2,
        "output_count": 1,
        "status": "ok",
        field: True,
    }
    with pytest.raises(ValidationError):
        ReturnSeriesResult(**kwargs)


def test_return_result_rejects_bad_output_count() -> None:
    with pytest.raises(ValidationError):
        ReturnSeriesResult(
            result_id="result",
            request_id="request",
            method=ReturnMethod.SIMPLE,
            values=[0.01],
            source=create_synthetic_source_reference(),
            input_count=2,
            output_count=2,
            status="ok",
        )
