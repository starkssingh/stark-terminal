from pydantic import ValidationError
import pytest

from stark_terminal_core.domain.enums import WarehouseTableKind
from stark_terminal_data_platform.warehouse.tables import (
    WarehouseColumn,
    WarehouseTableContract,
    analytical_ohlcv_table_contract,
    list_default_warehouse_table_contracts,
)


def test_default_table_contracts_exist_and_validate() -> None:
    contracts = list_default_warehouse_table_contracts()

    assert len(contracts) == 6
    assert [contract.table_name for contract in contracts] == [
        "analytical_ohlcv_bars",
        "analytical_options_chain_snapshots",
        "analytical_futures_basis_snapshots",
        "analytical_market_state_snapshots",
        "analytical_regime_snapshots",
        "analytical_decision_objects",
    ]
    assert contracts[0].kind == WarehouseTableKind.OHLCV_ANALYTICAL


def test_warehouse_contract_validation_rejects_bad_shape() -> None:
    column = WarehouseColumn(name="symbol", type="String")
    with pytest.raises(ValidationError):
        WarehouseTableContract(table_name="x", kind=WarehouseTableKind.UNKNOWN, columns=[], order_by=["symbol"])
    with pytest.raises(ValidationError):
        WarehouseTableContract(table_name="x", kind=WarehouseTableKind.UNKNOWN, columns=[column], order_by=[])
    with pytest.raises(ValidationError):
        WarehouseTableContract(table_name="x", kind=WarehouseTableKind.UNKNOWN, columns=[column], order_by=["missing"])
    with pytest.raises(ValidationError):
        WarehouseTableContract(
            table_name="x",
            kind=WarehouseTableKind.UNKNOWN,
            columns=[column],
            order_by=["symbol"],
            primary_key=["missing"],
        )


@pytest.mark.parametrize("name", ["bad table", "bad;table", "../table", "1table"])
def test_unsafe_table_and_column_names_rejected(name: str) -> None:
    with pytest.raises(ValidationError):
        WarehouseColumn(name=name, type="String")
    with pytest.raises(ValidationError):
        WarehouseTableContract(
            table_name=name,
            kind=WarehouseTableKind.UNKNOWN,
            columns=[WarehouseColumn(name="symbol", type="String")],
            order_by=["symbol"],
        )


def test_ohlcv_contract_contains_expected_partition_and_order() -> None:
    contract = analytical_ohlcv_table_contract()

    assert contract.partition_by == "toYYYYMM(timestamp)"
    assert contract.order_by == ["exchange", "segment", "symbol", "timeframe", "timestamp"]
    assert any(column.name == "open" and column.type == "Float64" for column in contract.columns)
