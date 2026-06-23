from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, create_vector_contract
from stark_terminal_analytics.volatility.contracts import (
    VolatilityCalculationRequest,
    VolatilityMethod,
    create_volatility_request,
    create_volatility_result,
)
from stark_terminal_analytics.volatility.validation import (
    validate_return_vector_for_volatility,
    validate_volatility_request,
    validate_volatility_result,
)


def test_return_vector_validation_passes_for_finite_values() -> None:
    vector = create_vector_contract("returns", "Returns", [0.01, 0.02])

    result = validate_return_vector_for_volatility(vector)

    assert result.status == "ok"
    assert result.metrics["input_count"] == 2


def test_return_vector_validation_rejects_too_few_values() -> None:
    vector = create_vector_contract("returns", "Returns", [0.01])

    result = validate_return_vector_for_volatility(vector)

    assert result.status == "failed"


def test_return_vector_validation_rejects_real_market_data_source() -> None:
    source = NumericalSourceReference.model_construct(
        source_id="real",
        source_type="provider",
        source_data_reference="provider:real",
        synthetic=False,
        real_market_data=True,
        schema_version="v1",
    )
    vector = create_vector_contract("returns", "Returns", [0.01, 0.02]).model_copy(update={"source": source})

    result = validate_return_vector_for_volatility(vector)

    assert result.status == "failed"


def test_volatility_request_validation_checks_annualization_and_unsafe_flags() -> None:
    vector = create_vector_contract("returns", "Returns", [0.01, 0.02])
    request = VolatilityCalculationRequest.model_construct(
        request_id="vol",
        return_vector=vector,
        method=VolatilityMethod.SAMPLE_STDDEV,
        annualize=True,
        periods_per_year=0,
        require_source_reference=True,
        allow_real_data=False,
        allow_trade_signal=False,
        allow_recommendation=False,
        allow_decision_object=False,
    )

    result = validate_volatility_request(request)

    assert result.status == "failed"


def test_volatility_result_validation_rejects_unsafe_fields() -> None:
    vector = create_vector_contract("returns", "Returns", [0.01, 0.02])
    request = create_volatility_request("vol", vector)
    result = create_volatility_result(
        result_id="vol_result",
        request_id=request.request_id,
        method=request.method,
        volatility=0.1,
        source=vector.source,
        input_count=2,
    ).model_copy(update={"trade_signal": True})

    validation = validate_volatility_result(result)

    assert validation.status == "failed"
