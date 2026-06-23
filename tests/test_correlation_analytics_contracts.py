from pydantic import ValidationError
import pytest

from stark_terminal_analytics.correlation.contracts import (
    CorrelationCalculationRequest,
    CorrelationMethod,
    CorrelationResult,
    create_correlation_request,
    create_correlation_result,
)
from stark_terminal_analytics.numerical.contracts import create_vector_contract


def _vectors():
    return (
        create_vector_contract("x", "X", [1.0, 2.0, 3.0]),
        create_vector_contract("y", "Y", [2.0, 4.0, 6.0]),
    )


def test_valid_correlation_request() -> None:
    x_vector, y_vector = _vectors()

    request = create_correlation_request("corr", x_vector, y_vector)

    assert request.request_id == "corr"
    assert request.method == CorrelationMethod.PEARSON
    assert request.min_observations == 2
    assert request.x_vector.source == x_vector.source
    assert request.y_vector.source == y_vector.source


@pytest.mark.parametrize(
    "field",
    ["allow_real_data", "allow_trade_signal", "allow_recommendation", "allow_decision_object"],
)
def test_correlation_request_rejects_unsafe_flags(field: str) -> None:
    x_vector, y_vector = _vectors()

    with pytest.raises(ValidationError):
        CorrelationCalculationRequest(request_id="corr", x_vector=x_vector, y_vector=y_vector, **{field: True})


def test_correlation_request_rejects_unequal_lengths() -> None:
    x_vector = create_vector_contract("x", "X", [1.0, 2.0, 3.0])
    y_vector = create_vector_contract("y", "Y", [1.0, 2.0])

    with pytest.raises(ValidationError):
        CorrelationCalculationRequest(request_id="corr", x_vector=x_vector, y_vector=y_vector)


def test_correlation_request_rejects_low_min_observations() -> None:
    x_vector, y_vector = _vectors()

    with pytest.raises(ValidationError):
        CorrelationCalculationRequest(request_id="corr", x_vector=x_vector, y_vector=y_vector, min_observations=1)


def test_correlation_result_preserves_sources_and_range() -> None:
    x_vector, y_vector = _vectors()

    result = create_correlation_result(
        result_id="corr_result",
        request_id="corr",
        method=CorrelationMethod.PEARSON,
        correlation=1.0,
        covariance=2.0,
        x_source=x_vector.source,
        y_source=y_vector.source,
        observation_count=3,
    )

    assert result.x_source == x_vector.source
    assert result.y_source == y_vector.source
    assert result.correlation == 1.0
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


@pytest.mark.parametrize(
    "field",
    ["trade_signal", "recommendation", "decision_object_generated"],
)
def test_correlation_result_rejects_unsafe_flags(field: str) -> None:
    x_vector, y_vector = _vectors()

    with pytest.raises(ValidationError):
        CorrelationResult(
            result_id="corr_result",
            request_id="corr",
            method=CorrelationMethod.PEARSON,
            correlation=0.5,
            covariance=1.0,
            x_source=x_vector.source,
            y_source=y_vector.source,
            observation_count=3,
            status="ok",
            **{field: True},
        )


def test_correlation_result_rejects_out_of_range_value() -> None:
    x_vector, y_vector = _vectors()

    with pytest.raises(ValidationError):
        create_correlation_result(
            result_id="corr_result",
            request_id="corr",
            method=CorrelationMethod.PEARSON,
            correlation=1.5,
            covariance=1.0,
            x_source=x_vector.source,
            y_source=y_vector.source,
            observation_count=3,
        )

