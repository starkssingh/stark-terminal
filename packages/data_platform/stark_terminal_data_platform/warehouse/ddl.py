from __future__ import annotations

from stark_terminal_core.domain.enums import WarehouseEngine
from stark_terminal_data_platform.warehouse.tables import (
    WarehouseColumn,
    WarehouseTableContract,
    validate_table_identifier,
)


ENGINE_SQL = {
    WarehouseEngine.MERGE_TREE: "MergeTree",
    WarehouseEngine.REPLACING_MERGE_TREE: "ReplacingMergeTree",
    WarehouseEngine.SUMMING_MERGE_TREE: "SummingMergeTree",
    WarehouseEngine.AGGREGATING_MERGE_TREE: "AggregatingMergeTree",
}


def validate_sql_identifier(name: str) -> str:
    return validate_table_identifier(name)


def quote_identifier(name: str) -> str:
    return f"`{validate_sql_identifier(name)}`"


def _qualified_table_name(table_name: str, database: str | None = None) -> str:
    table = quote_identifier(table_name)
    if database is None:
        return table
    return f"{quote_identifier(database)}.{table}"


def render_column(column: WarehouseColumn) -> str:
    rendered = f"{quote_identifier(column.name)} {column.type}"
    if column.comment:
        escaped = column.comment.replace("\\", "\\\\").replace("'", "\\'")
        rendered = f"{rendered} COMMENT '{escaped}'"
    return rendered


def render_create_table_sql(
    contract: WarehouseTableContract,
    database: str | None = None,
    if_not_exists: bool = True,
) -> str:
    table_name = _qualified_table_name(contract.table_name, database)
    clause = " IF NOT EXISTS" if if_not_exists else ""
    columns = ",\n  ".join(render_column(column) for column in contract.columns)
    engine = ENGINE_SQL.get(contract.engine)
    if engine is None:
        raise ValueError(f"unsupported warehouse engine: {contract.engine}")
    sql = [
        f"CREATE TABLE{clause} {table_name} (",
        f"  {columns}",
        ")",
        f"ENGINE = {engine}()",
    ]
    if contract.partition_by:
        sql.append(f"PARTITION BY {contract.partition_by}")
    if contract.primary_key:
        sql.append(
            "PRIMARY KEY (" + ", ".join(quote_identifier(column) for column in contract.primary_key) + ")"
        )
    sql.append("ORDER BY (" + ", ".join(quote_identifier(column) for column in contract.order_by) + ")")
    return "\n".join(sql)


def render_drop_table_sql(
    table_name: str,
    database: str | None = None,
    if_exists: bool = True,
) -> str:
    clause = " IF EXISTS" if if_exists else ""
    return f"DROP TABLE{clause} {_qualified_table_name(table_name, database)}"


def render_all_create_table_sql(
    contracts: list[WarehouseTableContract],
    database: str | None = None,
) -> list[str]:
    return [render_create_table_sql(contract, database=database) for contract in contracts]
