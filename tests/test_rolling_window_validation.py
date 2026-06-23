from math import nan

from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, create_vector_contract
from stark_terminal_analytics.rolling.contracts import RollingMetric, RollingWindowRequest, create_rolling_request, create_rolling_result
from stark_terminal_analytics.rolling.validation import validate_rolling_request, validate_rolling_result


def test_rolling_validation_requires_finite_vector() -> None:
    vector = create_vector_contract("values", "Values", [1.0, 2.0, 3.0])
    unsafe_vector = vector.model_copy(update={"values": [1.0, nan, 3.0]})
    request = RollingWindowRequest.model_construct(
        request_id="rolling",
        vector=unsafe_vector,
        window=2,
        metric=RollingMetric.MEAN,
        require_finite_values=True,
        require_source_reference=True,
        allow_real_data=False,
        allow_trade_signal=False,
        allow_recommendation=False,
        allow_decision_object=False,
    )

    assert validate_rolling_request(request).status == "failed"


def test_rolling_validation_rejects_real_market_data_source() -> None:
    source = NumericalSourceReference.model_construct(
        source_id="real",
        source_type="provider",
        source_data_reference="provider-real",
        synthetic=False,
        real_market_data=True,
    )
    vector = create_vector_contract("values", "Values", [1.0, 2.0, 3.0]).model_copy(update={"source": source})
    request = RollingWindowRequest.model_construct(
        request_id="rolling",
        vector=vector,
        window=2,
        metric=RollingMetric.MEAN,
        require_finite_values=True,
        require_source_reference=True,
        allow_real_data=False,
        allow_trade_signal=False,
        allow_recommendation=False,
        allow_decision_object=False,
    )

    assert validate_rolling_request(request).status == "failed"


def test_rolling_validation_enforces_window_limits() -> None:
    vector = create_vector_contract("values", "Values", [1.0, 2.0, 3.0])

    too_large = create_rolling_request("rolling", vector, 4, RollingMetric.MEAN)
    too_wide = create_rolling_request("rolling", vector, 3, RollingMetric.MEAN)

    assert validate_rolling_request(too_large).status == "failed"
    assert validate_rolling_request(too_wide, max_window=2).status == "failed"


def test_rolling_validation_rejects_unsafe_constructed_flags_and_window() -> None:
    vector = create_vector_contract("values", "Values", [1.0, 2.0, 3.0])
    request = RollingWindowRequest.model_construct(
        request_id="rolling",
        vector=vector,
        window=0,
        metric=RollingMetric.MEAN,
        require_finite_values=True,
        require_source_reference=True,
        allow_real_data=False,
        allow_trade_signal=True,
        allow_recommendation=False,
        allow_decision_object=False,
    )

    assert validate_rolling_request(request).status == "failed"


def test_rolling_result_validation_rejects_unsafe_constructed_flags() -> None:
    vector = create_vector_contract("values", "Values", [1.0, 2.0, 3.0])
    result = create_rolling_result(
        result_id="result",
        request_id="rolling",
        metric=RollingMetric.MEAN,
        window=2,
        values=[1.5, 2.5],
        source=vector.source,
        input_count=3,
    )
    unsafe_result = result.model_copy(update={"recommendation": True})

    assert validate_rolling_result(result).status == "ok"
    assert validate_rolling_result(unsafe_result).status == "failed"
