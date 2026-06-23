import math

import pytest

from stark_terminal_analytics.numerical.contracts import create_vector_contract
from stark_terminal_analytics.volatility.calculations import (
    calculate_population_stddev,
    calculate_sample_stddev,
    calculate_volatility,
)
from stark_terminal_analytics.volatility.contracts import VolatilityMethod, create_volatility_request


def test_population_stddev_is_deterministic() -> None:
    assert calculate_population_stddev([1.0, 2.0, 3.0]) == pytest.approx(math.sqrt(2.0 / 3.0))


def test_sample_stddev_is_deterministic() -> None:
    assert calculate_sample_stddev([1.0, 2.0, 3.0]) == pytest.approx(1.0)


def test_annualized_volatility_is_deterministic() -> None:
    vector = create_vector_contract("returns", "Returns", [1.0, 2.0, 3.0])
    request = create_volatility_request(
        "vol",
        vector,
        method=VolatilityMethod.SAMPLE_STDDEV,
        annualize=True,
        periods_per_year=4,
    )

    result = calculate_volatility(request)

    assert result.status == "ok"
    assert result.volatility == pytest.approx(1.0)
    assert result.annualized_volatility == pytest.approx(2.0)
    assert result.source == vector.source
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False


def test_invalid_volatility_input_fails_safely() -> None:
    vector = create_vector_contract("returns", "Returns", [0.01])
    request = create_volatility_request("vol", vector, method=VolatilityMethod.SAMPLE_STDDEV)

    result = calculate_volatility(request)

    assert result.status == "failed"
    assert result.volatility is None
    assert result.annualized_volatility is None


def test_volatility_result_has_no_other_risk_or_strategy_metrics() -> None:
    vector = create_vector_contract("returns", "Returns", [0.01, 0.02, -0.01])
    result = calculate_volatility(create_volatility_request("vol", vector))

    assert result.status == "ok"
    assert not hasattr(result, "drawdown")
    assert not hasattr(result, "correlation")
    assert not hasattr(result, "beta")
    assert not hasattr(result, "regime")
