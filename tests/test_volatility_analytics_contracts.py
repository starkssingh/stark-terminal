from pydantic import ValidationError
import pytest

from stark_terminal_analytics.numerical.contracts import create_synthetic_source_reference, create_vector_contract
from stark_terminal_analytics.volatility.contracts import (
    VolatilityCalculationRequest,
    VolatilityMethod,
    VolatilityResult,
    create_volatility_request,
    create_volatility_result,
)


def _return_vector():
    return create_vector_contract("returns", "Synthetic returns", [0.01, -0.02, 0.03])


def test_valid_volatility_calculation_request() -> None:
    request = create_volatility_request("volatility_request", _return_vector(), VolatilityMethod.SAMPLE_STDDEV)

    assert request.method == VolatilityMethod.SAMPLE_STDDEV
    assert request.return_vector.descriptive_only is True
    assert request.allow_real_data is False
    assert request.created_at.tzinfo is not None


@pytest.mark.parametrize(
    "field",
    ["allow_real_data", "allow_trade_signal", "allow_recommendation", "allow_decision_object"],
)
def test_volatility_request_rejects_unsafe_flags(field: str) -> None:
    with pytest.raises(ValidationError):
        VolatilityCalculationRequest(request_id="request", return_vector=_return_vector(), **{field: True})


def test_volatility_request_rejects_unknown_method() -> None:
    with pytest.raises(ValidationError):
        VolatilityCalculationRequest(request_id="request", return_vector=_return_vector(), method=VolatilityMethod.UNKNOWN)


def test_annualized_request_requires_positive_periods_per_year() -> None:
    with pytest.raises(ValidationError):
        VolatilityCalculationRequest(request_id="request", return_vector=_return_vector(), annualize=True)

    with pytest.raises(ValidationError):
        VolatilityCalculationRequest(
            request_id="request",
            return_vector=_return_vector(),
            annualize=True,
            periods_per_year=0,
        )


def test_volatility_result_preserves_source_and_annualization_fields() -> None:
    source = create_synthetic_source_reference()
    result = create_volatility_result(
        result_id="result",
        request_id="request",
        method=VolatilityMethod.SAMPLE_STDDEV,
        volatility=0.1,
        annualized_volatility=0.2,
        annualize=True,
        periods_per_year=4,
        source=source,
        input_count=3,
    )

    assert result.source == source
    assert result.volatility == 0.1
    assert result.annualized_volatility == 0.2
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


@pytest.mark.parametrize("field", ["trade_signal", "recommendation", "decision_object_generated"])
def test_volatility_result_rejects_unsafe_flags(field: str) -> None:
    kwargs = {
        "result_id": "result",
        "request_id": "request",
        "method": VolatilityMethod.SAMPLE_STDDEV,
        "volatility": 0.1,
        "source": create_synthetic_source_reference(),
        "input_count": 3,
        "status": "ok",
        field: True,
    }
    with pytest.raises(ValidationError):
        VolatilityResult(**kwargs)


def test_volatility_result_validates_annualization_consistency() -> None:
    with pytest.raises(ValidationError):
        VolatilityResult(
            result_id="result",
            request_id="request",
            method=VolatilityMethod.SAMPLE_STDDEV,
            volatility=0.1,
            annualized_volatility=0.2,
            annualize=False,
            source=create_synthetic_source_reference(),
            input_count=3,
            status="ok",
        )
