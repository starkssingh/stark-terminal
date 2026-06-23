from math import inf, nan

from pydantic import ValidationError
import pytest

from stark_terminal_analytics.numerical.contracts import (
    NumericalComputationKind,
    NumericalComputationRequest,
    NumericalComputationResult,
    NumericalDataKind,
    NumericalSourceReference,
    NumericalTableColumn,
    NumericalTableContract,
    NumericalValueType,
    NumericalVectorContract,
    create_safe_result,
    create_summary_request,
    create_synthetic_source_reference,
    create_vector_contract,
)


def test_valid_numerical_source_reference() -> None:
    source = create_synthetic_source_reference()

    assert source.synthetic is True
    assert source.real_market_data is False
    assert source.source_data_reference == "synthetic-local-test-only"
    assert source.created_at.tzinfo is not None


def test_numerical_source_reference_rejects_real_market_data() -> None:
    with pytest.raises(ValidationError):
        NumericalSourceReference(
            source_id="source",
            source_type="local",
            source_data_reference="real-provider",
            real_market_data=True,
        )


def test_valid_numerical_vector_contract() -> None:
    vector = create_vector_contract("vec", "Vector", [1.0, 2.0, 3.0])

    assert vector.data_kind == NumericalDataKind.VECTOR
    assert vector.descriptive_only is True
    assert vector.source.real_market_data is False


@pytest.mark.parametrize("values", [[], [1.0, nan], [1.0, inf]])
def test_numerical_vector_rejects_empty_or_non_finite_values(values: list[float]) -> None:
    with pytest.raises(ValidationError):
        create_vector_contract("vec", "Vector", values)


def test_valid_numerical_table_contract() -> None:
    source = create_synthetic_source_reference()
    table = NumericalTableContract(
        table_id="table",
        name="Table",
        columns=[NumericalTableColumn(name="value", value_type=NumericalValueType.FLOAT)],
        row_count=3,
        source=source,
    )

    assert table.data_kind == NumericalDataKind.TABLE
    assert table.row_count == 3
    assert table.descriptive_only is True


def test_numerical_computation_request_rejects_unsafe_flags() -> None:
    source = create_synthetic_source_reference()
    for field in ["allow_real_data", "allow_trade_signal", "allow_recommendation", "allow_decision_object"]:
        kwargs = {
            "request_id": "request",
            "computation_kind": NumericalComputationKind.SUMMARY,
            "input_ids": ["vec"],
            "source": source,
            field: True,
        }
        with pytest.raises(ValidationError):
            NumericalComputationRequest(**kwargs)


def test_numerical_computation_result_rejects_unsafe_flags() -> None:
    source = create_synthetic_source_reference()
    for field in ["trade_signal", "recommendation", "decision_object_generated"]:
        kwargs = {
            "result_id": "result",
            "request_id": "request",
            "computation_kind": NumericalComputationKind.SUMMARY,
            "metrics": {"count": 3},
            "source": source,
            "status": "ok",
            field: True,
        }
        with pytest.raises(ValidationError):
            NumericalComputationResult(**kwargs)


def test_numerical_helpers_create_safe_contracts_and_results() -> None:
    source = create_synthetic_source_reference(source_id="source")
    vector = create_vector_contract("vec", "Vector", [1.0, 2.0], source)
    request = create_summary_request("summary", [vector.vector_id], source)
    result = create_safe_result(
        result_id="result",
        request_id=request.request_id,
        computation_kind=NumericalComputationKind.SUMMARY,
        metrics={"count": 2, "mean": 1.5},
        source=source,
    )

    assert request.allow_trade_signal is False
    assert result.descriptive_only is True
    assert result.trade_signal is False
    assert result.recommendation is False
    assert result.decision_object_generated is False
