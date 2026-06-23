from math import inf, nan

from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, create_synthetic_source_reference, create_vector_contract
from stark_terminal_analytics.returns.contracts import ReturnCalculationRequest, ReturnMethod, create_return_request, create_return_result
from stark_terminal_analytics.returns.validation import (
    validate_price_vector_for_returns,
    validate_return_request,
    validate_return_result,
)


def test_return_validation_needs_at_least_two_prices() -> None:
    vector = create_vector_contract("prices", "Prices", [100.0])

    result = validate_price_vector_for_returns(vector)

    assert result.status == "failed"


def test_return_validation_rejects_non_finite_prices() -> None:
    source = create_synthetic_source_reference()
    vector = create_vector_contract("prices", "Prices", [100.0, 101.0])
    unsafe_vector = vector.model_copy(update={"values": [100.0, nan]})

    result = validate_price_vector_for_returns(unsafe_vector)

    assert source.real_market_data is False
    assert result.status == "failed"
    unsafe_vector = vector.model_copy(update={"values": [100.0, inf]})
    assert validate_price_vector_for_returns(unsafe_vector).status == "failed"


def test_return_validation_rejects_non_positive_prices_when_required_or_log() -> None:
    vector = create_vector_contract("prices", "Prices", [100.0, 0.0])
    simple_request = create_return_request("simple", vector, ReturnMethod.SIMPLE)
    log_request = ReturnCalculationRequest(
        request_id="log",
        price_vector=vector,
        method=ReturnMethod.LOG,
        require_positive_prices=True,
    )

    assert validate_return_request(simple_request).status == "failed"
    assert validate_return_request(log_request).status == "failed"


def test_return_validation_rejects_real_market_data_source() -> None:
    source = NumericalSourceReference.model_construct(
        source_id="real",
        source_type="provider",
        source_data_reference="provider-real",
        synthetic=False,
        real_market_data=True,
    )
    vector = create_vector_contract("prices", "Prices", [100.0, 101.0]).model_copy(update={"source": source})
    request = create_return_request("request", vector, ReturnMethod.SIMPLE)

    assert validate_price_vector_for_returns(vector).status == "failed"
    assert validate_return_request(request).status == "failed"


def test_return_validation_rejects_unsafe_constructed_flags() -> None:
    vector = create_vector_contract("prices", "Prices", [100.0, 101.0])
    request = ReturnCalculationRequest.model_construct(
        request_id="request",
        price_vector=vector,
        method=ReturnMethod.SIMPLE,
        require_positive_prices=True,
        require_source_reference=True,
        allow_real_data=False,
        allow_trade_signal=True,
        allow_recommendation=False,
        allow_decision_object=False,
    )

    assert validate_return_request(request).status == "failed"


def test_return_result_validation_rejects_unsafe_constructed_flags() -> None:
    result = create_return_result(
        result_id="result",
        request_id="request",
        method=ReturnMethod.SIMPLE,
        values=[0.01],
        source=create_synthetic_source_reference(),
        input_count=2,
    )
    unsafe_result = result.model_copy(update={"trade_signal": True})

    assert validate_return_result(result).status == "ok"
    assert validate_return_result(unsafe_result).status == "failed"
