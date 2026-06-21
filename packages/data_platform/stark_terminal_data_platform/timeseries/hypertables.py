from __future__ import annotations

import re


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def validate_hypertable_target(table_name: str, time_column: str) -> None:
    if not _IDENTIFIER.fullmatch(table_name):
        raise ValueError("table_name must be a safe SQL identifier")
    if not _IDENTIFIER.fullmatch(time_column):
        raise ValueError("time_column must be a safe SQL identifier")


def create_timescaledb_extension_sql(extension_name: str = "timescaledb") -> str:
    validate_hypertable_target(extension_name, "timestamp")
    return f"CREATE EXTENSION IF NOT EXISTS {extension_name};"


def create_hypertable_sql(
    table_name: str,
    time_column: str = "timestamp",
    if_not_exists: bool = True,
) -> str:
    validate_hypertable_target(table_name, time_column)
    if_not_exists_sql = "TRUE" if if_not_exists else "FALSE"
    return (
        "SELECT create_hypertable("
        f"'{table_name}', "
        f"'{time_column}', "
        f"if_not_exists => {if_not_exists_sql}"
        ");"
    )
