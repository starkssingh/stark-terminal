from pydantic import ValidationError
import pytest

from stark_terminal_analytics.correlation.contracts import CorrelationMethod, create_correlation_request, create_correlation_result
from stark_terminal_analytics.correlation.validation import (
    validate_correlation_request,
    validate_correlation_result,
    validate_paired_vectors_for_correlation,
)
from stark_terminal_analytics.numerical.contracts import NumericalSourceReference, create_vector_contract


def test_paired_vectors_for_correlation_pass() -> None:
    x_vector = create_vector_contract("x", "X", [1.0, 2.0, 3.0])
    y_vector = create_vector_contract("y", "Y", [2.0, 3.0, 5.0])

    result = validate_paired_vectors_for_correlation(x_vector, y_vector)

    assert result.status == "ok"
    assert result.metrics["equal_lengths"] is True
    assert result.metrics["finite"] is True


def test_correlation_validation_requires_enough_observations() -> None:
    x_vector = create_vector_contract("x", "X", [1.0])
    y_vector = create_vector_contract("y", "Y", [2.0])

    result = validate_paired_vectors_for_correlation(x_vector, y_vector)

    assert result.status == "failed"


def test_correlation_validation_rejects_unequal_lengths_safely() -> None:
    x_vector = create_vector_contract("x", "X", [1.0, 2.0, 3.0])
    y_vector = create_vector_contract("y", "Y", [2.0])

    result = validate_paired_vectors_for_correlation(x_vector, y_vector)

    assert result.status == "failed"


def test_correlation_validation_rejects_non_finite_values() -> None:
    with pytest.raises(ValidationError):
        create_vector_contract("x", "X", [1.0, float("nan")])


def test_correlation_validation_rejects_real_market_source() -> None:
    source = NumericalSourceReference.model_construct(
        source_id="real",
        source_type="provider",
        source_data_reference="real",
        synthetic=False,
        real_market_data=True,
        schema_version="v1",
    )
    x_vector = create_vector_contract("x", "X", [1.0, 2.0, 3.0])
    y_vector = create_vector_contract("y", "Y", [2.0, 3.0, 4.0])
    x_vector = x_vector.model_copy(update={"source": source})

    result = validate_paired_vectors_for_correlation(x_vector, y_vector)

    assert result.status == "failed"


def test_correlation_validation_rejects_zero_variance() -> None:
    x_vector = create_vector_contract("x", "X", [1.0, 1.0, 1.0])
    y_vector = create_vector_contract("y", "Y", [2.0, 3.0, 4.0])

    result = validate_paired_vectors_for_correlation(x_vector, y_vector)

    assert result.status == "failed"


def test_correlation_request_and_result_validation() -> None:
    x_vector = create_vector_contract("x", "X", [1.0, 2.0, 3.0])
    y_vector = create_vector_contract("y", "Y", [2.0, 4.0, 6.0])
    request = create_correlation_request("corr", x_vector, y_vector)
    result = create_correlation_result(
        "corr_result",
        "corr",
        CorrelationMethod.PEARSON,
        1.0,
        1.0,
        x_vector.source,
        y_vector.source,
        3,
    )

    assert validate_correlation_request(request).status == "ok"
    assert validate_correlation_result(result).status == "ok"
