from math import inf

from stark_terminal_analytics.numerical.contracts import (
    NumericalTableColumn,
    NumericalTableContract,
    NumericalValueType,
    create_synthetic_source_reference,
    create_vector_contract,
)
from stark_terminal_analytics.numerical.validation import (
    validate_finite_values,
    validate_no_signal_fields,
    validate_source_reference,
    validate_table_contract,
    validate_vector_shape,
)


def test_finite_values_validation_passes_and_fails() -> None:
    ok = validate_finite_values([1.0, 2.0, 3.0])
    failed = validate_finite_values([1.0, inf])

    assert ok.status == "ok"
    assert ok.metrics["finite"] is True
    assert failed.status == "failed"
    assert failed.trade_signal is False


def test_vector_shape_validation_enforces_max_length() -> None:
    vector = create_vector_contract("vec", "Vector", [1.0, 2.0, 3.0])

    assert validate_vector_shape(vector, max_length=3).status == "ok"
    assert validate_vector_shape(vector, max_length=2).status == "failed"


def test_source_reference_validation_requires_local_safe_source() -> None:
    source = create_synthetic_source_reference()
    result = validate_source_reference(source)

    assert result.status == "ok"
    assert result.metrics["real_market_data"] is False


def test_table_contract_validation() -> None:
    source = create_synthetic_source_reference()
    table = NumericalTableContract(
        table_id="table",
        name="Table",
        columns=[NumericalTableColumn(name="value", value_type=NumericalValueType.FLOAT)],
        row_count=1,
        source=source,
    )

    result = validate_table_contract(table)

    assert result.status == "ok"
    assert result.metrics["column_count"] == 1


def test_no_signal_validation_catches_unsafe_fields() -> None:
    safe = create_vector_contract("vec", "Vector", [1.0])

    class Unsafe:
        trade_signal = True

    assert validate_no_signal_fields(safe) is True
    assert validate_no_signal_fields(Unsafe()) is False
