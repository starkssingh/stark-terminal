import pytest

from stark_terminal_data_platform.warehouse.ddl import (
    quote_identifier,
    render_all_create_table_sql,
    render_create_table_sql,
    render_drop_table_sql,
    validate_sql_identifier,
)
from stark_terminal_data_platform.warehouse.tables import (
    analytical_ohlcv_table_contract,
    list_default_warehouse_table_contracts,
)


def test_quote_identifier_and_validation() -> None:
    assert quote_identifier("analytical_ohlcv_bars") == "`analytical_ohlcv_bars`"
    assert validate_sql_identifier("stark_terminal") == "stark_terminal"
    with pytest.raises(ValueError):
        quote_identifier("bad;drop")


def test_render_create_table_sql_contains_clickhouse_clauses() -> None:
    sql = render_create_table_sql(analytical_ohlcv_table_contract(), database="stark_terminal")

    assert "CREATE TABLE IF NOT EXISTS" in sql
    assert "`stark_terminal`.`analytical_ohlcv_bars`" in sql
    assert "ENGINE = MergeTree()" in sql
    assert "PARTITION BY toYYYYMM(timestamp)" in sql
    assert "ORDER BY (`exchange`, `segment`, `symbol`, `timeframe`, `timestamp`)" in sql
    assert ";" not in sql


def test_render_drop_table_sql() -> None:
    assert (
        render_drop_table_sql("analytical_ohlcv_bars", database="stark_terminal")
        == "DROP TABLE IF EXISTS `stark_terminal`.`analytical_ohlcv_bars`"
    )
    with pytest.raises(ValueError):
        render_drop_table_sql("bad;drop")


def test_render_all_create_table_sql_is_deterministic() -> None:
    contracts = list_default_warehouse_table_contracts()
    sql = render_all_create_table_sql(contracts, database="stark_terminal")

    assert len(sql) == 6
    assert sql == render_all_create_table_sql(contracts, database="stark_terminal")
    assert sql[0].startswith("CREATE TABLE IF NOT EXISTS")
