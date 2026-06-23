from pydantic import ValidationError
import pytest

from stark_terminal_analytics.numerical.contracts import create_synthetic_source_reference, create_vector_contract
from stark_terminal_analytics.rolling.contracts import (
    RollingMetric,
    RollingWindowAlignment,
    RollingWindowRequest,
    RollingWindowResult,
    create_rolling_request,
    create_rolling_result,
)


def _vector():
    return create_vector_contract("values", "Values", [1.0, 2.0, 3.0, 4.0])


def test_valid_rolling_window_request() -> None:
    request = create_rolling_request("rolling", _vector(), 2, RollingMetric.MEAN)

    assert request.window == 2
    assert request.metric == RollingMetric.MEAN
    assert request.alignment == RollingWindowAlignment.RIGHT
    assert request.allow_trade_signal is False


def test_rolling_window_request_rejects_invalid_window_alignment_or_metric() -> None:
    with pytest.raises(ValidationError):
        RollingWindowRequest(request_id="rolling", vector=_vector(), window=0, metric=RollingMetric.MEAN)
    with pytest.raises(ValidationError):
        RollingWindowRequest(request_id="rolling", vector=_vector(), window=2, metric=RollingMetric.UNKNOWN)
    with pytest.raises(ValidationError):
        RollingWindowRequest(
            request_id="rolling",
            vector=_vector(),
            window=2,
            metric=RollingMetric.MEAN,
            alignment=RollingWindowAlignment.LEFT,
        )


@pytest.mark.parametrize(
    "field",
    ["allow_real_data", "allow_trade_signal", "allow_recommendation", "allow_decision_object"],
)
def test_rolling_window_request_rejects_unsafe_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        RollingWindowRequest(request_id="rolling", vector=_vector(), window=2, metric=RollingMetric.MEAN, **{field: True})


def test_rolling_window_result_counts_and_source() -> None:
    source = create_synthetic_source_reference()
    result = create_rolling_result(
        result_id="result",
        request_id="rolling",
        metric=RollingMetric.MEAN,
        window=2,
        values=[1.5, 2.5],
        source=source,
        input_count=3,
    )

    assert result.source == source
    assert result.output_count == 2
    assert result.descriptive_only is True


@pytest.mark.parametrize("field", ["trade_signal", "recommendation", "decision_object_generated"])
def test_rolling_window_result_rejects_unsafe_flags(field: str) -> None:
    kwargs = {
        "result_id": "result",
        "request_id": "rolling",
        "metric": RollingMetric.MEAN,
        "window": 2,
        "values": [1.5],
        "source": create_synthetic_source_reference(),
        "input_count": 2,
        "output_count": 1,
        "status": "ok",
        field: True,
    }
    with pytest.raises(ValidationError):
        RollingWindowResult(**kwargs)
