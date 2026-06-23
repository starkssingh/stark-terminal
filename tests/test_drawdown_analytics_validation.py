from stark_terminal_analytics.drawdown.contracts import create_drawdown_request, create_drawdown_result
from stark_terminal_analytics.drawdown.validation import (
    validate_drawdown_request,
    validate_drawdown_result,
    validate_value_vector_for_drawdown,
)
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, create_vector_contract


def test_value_vector_validation_passes_for_positive_values() -> None:
    vector = create_vector_contract("values", "Values", [100.0, 95.0])

    result = validate_value_vector_for_drawdown(vector)

    assert result.status == "ok"
    assert result.metrics["input_count"] == 2


def test_value_vector_validation_rejects_zero_or_negative_values() -> None:
    vector = create_vector_contract("values", "Values", [100.0, 0.0])

    result = validate_value_vector_for_drawdown(vector)

    assert result.status == "failed"


def test_value_vector_validation_rejects_real_market_data_source() -> None:
    source = NumericalSourceReference.model_construct(
        source_id="real",
        source_type="provider",
        source_data_reference="provider:real",
        synthetic=False,
        real_market_data=True,
        schema_version="v1",
    )
    vector = create_vector_contract("values", "Values", [100.0, 95.0]).model_copy(update={"source": source})

    result = validate_value_vector_for_drawdown(vector)

    assert result.status == "failed"


def test_drawdown_request_validation_rejects_unsafe_fields() -> None:
    vector = create_vector_contract("values", "Values", [100.0, 95.0])
    request = create_drawdown_request("drawdown", vector).model_copy(update={"allow_trade_signal": True})

    result = validate_drawdown_request(request)

    assert result.status == "failed"


def test_drawdown_result_validation_rejects_positive_result_values() -> None:
    vector = create_vector_contract("values", "Values", [100.0, 95.0])
    result = create_drawdown_result(
        result_id="drawdown_result",
        request_id="drawdown",
        drawdown_values=[0.0, -0.05],
        max_drawdown=-0.05,
        source=vector.source,
        input_count=2,
    ).model_copy(update={"drawdown_values": [0.0, 0.05]})

    validation = validate_drawdown_result(result)

    assert validation.status == "failed"
