from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator, model_validator

from stark_terminal_core.domain.enums import WarehouseEngine, WarehouseTableKind


SAFE_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def validate_table_identifier(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("identifier must be a string")
    normalized = name.strip()
    if not normalized:
        raise ValueError("identifier cannot be empty")
    if any(ord(char) < 32 for char in normalized):
        raise ValueError("identifier cannot contain control characters")
    if any(token in normalized for token in (";", "'", '"', "`", "../", "..\\", "/", "\\")):
        raise ValueError("identifier contains unsafe characters")
    if not SAFE_IDENTIFIER_PATTERN.fullmatch(normalized):
        raise ValueError("identifier must be alphanumeric with underscores")
    return normalized


class WarehouseColumn(BaseModel):
    name: str
    type: str
    nullable: bool = False
    comment: str | None = None

    @field_validator("name")
    @classmethod
    def name_must_be_safe(cls, value: str) -> str:
        return validate_table_identifier(value)

    @field_validator("type")
    @classmethod
    def type_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("column type cannot be empty")
        if ";" in normalized or "--" in normalized:
            raise ValueError("column type contains unsafe SQL tokens")
        return normalized


class WarehouseTableContract(BaseModel):
    table_name: str
    kind: WarehouseTableKind
    engine: WarehouseEngine = WarehouseEngine.MERGE_TREE
    columns: list[WarehouseColumn]
    order_by: list[str]
    partition_by: str | None = None
    primary_key: list[str] = Field(default_factory=list)
    schema_version: str = "v1"
    description: str | None = None

    @field_validator("table_name")
    @classmethod
    def table_name_must_be_safe(cls, value: str) -> str:
        return validate_table_identifier(value)

    @field_validator("columns")
    @classmethod
    def columns_cannot_be_empty(cls, value: list[WarehouseColumn]) -> list[WarehouseColumn]:
        if not value:
            raise ValueError("warehouse table columns cannot be empty")
        return value

    @field_validator("order_by")
    @classmethod
    def order_by_cannot_be_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("warehouse table order_by cannot be empty")
        return [validate_table_identifier(item) for item in value]

    @field_validator("primary_key")
    @classmethod
    def primary_key_fields_must_be_safe(cls, value: list[str]) -> list[str]:
        return [validate_table_identifier(item) for item in value]

    @field_validator("schema_version")
    @classmethod
    def schema_version_must_be_non_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("schema_version cannot be empty")
        return normalized

    @model_validator(mode="after")
    def referenced_columns_must_exist(self) -> WarehouseTableContract:
        column_names = {column.name for column in self.columns}
        missing_order = [column for column in self.order_by if column not in column_names]
        missing_primary = [column for column in self.primary_key if column not in column_names]
        if missing_order:
            raise ValueError(f"order_by references missing columns: {', '.join(missing_order)}")
        if missing_primary:
            raise ValueError(f"primary_key references missing columns: {', '.join(missing_primary)}")
        return self


def _columns(spec: list[tuple[str, str]]) -> list[WarehouseColumn]:
    return [WarehouseColumn(name=name, type=type_) for name, type_ in spec]


def analytical_ohlcv_table_contract() -> WarehouseTableContract:
    return WarehouseTableContract(
        table_name="analytical_ohlcv_bars",
        kind=WarehouseTableKind.OHLCV_ANALYTICAL,
        columns=_columns(
            [
                ("instrument_id", "String"),
                ("symbol", "String"),
                ("exchange", "String"),
                ("segment", "String"),
                ("timeframe", "String"),
                ("timestamp", "DateTime64(3, 'UTC')"),
                ("open", "Float64"),
                ("high", "Float64"),
                ("low", "Float64"),
                ("close", "Float64"),
                ("volume", "Nullable(Float64)"),
                ("open_interest", "Nullable(Float64)"),
                ("provider_id", "Nullable(String)"),
                ("quality_status", "String"),
                ("source_data_reference", "Nullable(String)"),
                ("ingested_at", "DateTime64(3, 'UTC')"),
            ]
        ),
        order_by=["exchange", "segment", "symbol", "timeframe", "timestamp"],
        partition_by="toYYYYMM(timestamp)",
        description="Analytical OHLCV bar copies for historical scans.",
    )


def analytical_options_chain_table_contract() -> WarehouseTableContract:
    return WarehouseTableContract(
        table_name="analytical_options_chain_snapshots",
        kind=WarehouseTableKind.OPTIONS_CHAIN_ANALYTICAL,
        columns=_columns(
            [
                ("underlying_instrument_id", "String"),
                ("underlying_symbol", "String"),
                ("exchange", "String"),
                ("segment", "String"),
                ("expiry", "Date"),
                ("timestamp", "DateTime64(3, 'UTC')"),
                ("provider_id", "Nullable(String)"),
                ("contract_count", "UInt32"),
                ("quality_status", "String"),
                ("source_data_reference", "Nullable(String)"),
                ("payload_json", "String"),
                ("ingested_at", "DateTime64(3, 'UTC')"),
            ]
        ),
        order_by=["exchange", "underlying_symbol", "expiry", "timestamp"],
        partition_by="toYYYYMM(timestamp)",
        description="Analytical options-chain snapshot copies.",
    )


def analytical_futures_basis_table_contract() -> WarehouseTableContract:
    return WarehouseTableContract(
        table_name="analytical_futures_basis_snapshots",
        kind=WarehouseTableKind.FUTURES_BASIS_ANALYTICAL,
        columns=_columns(
            [
                ("underlying_instrument_id", "String"),
                ("underlying_symbol", "String"),
                ("exchange", "String"),
                ("segment", "String"),
                ("contract_symbol", "String"),
                ("expiry", "Date"),
                ("timestamp", "DateTime64(3, 'UTC')"),
                ("spot_price", "Nullable(Float64)"),
                ("futures_price", "Nullable(Float64)"),
                ("basis", "Nullable(Float64)"),
                ("basis_percent", "Nullable(Float64)"),
                ("provider_id", "Nullable(String)"),
                ("quality_status", "String"),
                ("source_data_reference", "Nullable(String)"),
                ("ingested_at", "DateTime64(3, 'UTC')"),
            ]
        ),
        order_by=["exchange", "underlying_symbol", "contract_symbol", "expiry", "timestamp"],
        partition_by="toYYYYMM(timestamp)",
        description="Analytical futures-basis snapshot copies.",
    )


def analytical_market_state_table_contract() -> WarehouseTableContract:
    return WarehouseTableContract(
        table_name="analytical_market_state_snapshots",
        kind=WarehouseTableKind.MARKET_STATE_ANALYTICAL,
        columns=_columns(
            [
                ("instrument_id", "String"),
                ("symbol", "String"),
                ("exchange", "String"),
                ("segment", "String"),
                ("timeframe", "String"),
                ("timestamp", "DateTime64(3, 'UTC')"),
                ("state", "Nullable(String)"),
                ("regime", "Nullable(String)"),
                ("action_state", "Nullable(String)"),
                ("confidence", "Nullable(Float64)"),
                ("risk", "Nullable(String)"),
                ("source", "String"),
                ("source_data_reference", "Nullable(String)"),
                ("payload_json", "String"),
                ("ingested_at", "DateTime64(3, 'UTC')"),
            ]
        ),
        order_by=["exchange", "segment", "symbol", "timeframe", "timestamp"],
        partition_by="toYYYYMM(timestamp)",
        description="Analytical market-state snapshot copies.",
    )


def analytical_regime_table_contract() -> WarehouseTableContract:
    return WarehouseTableContract(
        table_name="analytical_regime_snapshots",
        kind=WarehouseTableKind.REGIME_ANALYTICAL,
        columns=_columns(
            [
                ("instrument_id", "String"),
                ("symbol", "String"),
                ("exchange", "String"),
                ("segment", "String"),
                ("timeframe", "String"),
                ("timestamp", "DateTime64(3, 'UTC')"),
                ("regime_label", "String"),
                ("confidence", "Nullable(Float64)"),
                ("method", "Nullable(String)"),
                ("model_or_rule_version", "Nullable(String)"),
                ("evidence_json", "String"),
                ("source_data_reference", "Nullable(String)"),
                ("ingested_at", "DateTime64(3, 'UTC')"),
            ]
        ),
        order_by=["exchange", "segment", "symbol", "timeframe", "timestamp"],
        partition_by="toYYYYMM(timestamp)",
        description="Analytical regime snapshot copies.",
    )


def analytical_decision_object_table_contract() -> WarehouseTableContract:
    return WarehouseTableContract(
        table_name="analytical_decision_objects",
        kind=WarehouseTableKind.DECISION_OBJECT_ANALYTICAL,
        columns=_columns(
            [
                ("instrument", "String"),
                ("exchange", "String"),
                ("segment", "String"),
                ("timeframe", "String"),
                ("generated_at", "DateTime64(3, 'UTC')"),
                ("regime", "Nullable(String)"),
                ("state", "Nullable(String)"),
                ("action_state", "String"),
                ("confidence", "Float64"),
                ("confidence_method", "String"),
                ("risk", "String"),
                ("evidence_json", "String"),
                ("invalidation", "Nullable(String)"),
                ("horizon", "Nullable(String)"),
                ("source_data_reference", "Nullable(String)"),
                ("decision_source", "String"),
                ("audit_id", "Nullable(String)"),
                ("model_or_rule_version", "Nullable(String)"),
                ("ingested_at", "DateTime64(3, 'UTC')"),
            ]
        ),
        order_by=["exchange", "segment", "instrument", "timeframe", "generated_at"],
        partition_by="toYYYYMM(generated_at)",
        description="Analytical DecisionObject history copies.",
    )


def list_default_warehouse_table_contracts() -> list[WarehouseTableContract]:
    return [
        analytical_ohlcv_table_contract(),
        analytical_options_chain_table_contract(),
        analytical_futures_basis_table_contract(),
        analytical_market_state_table_contract(),
        analytical_regime_table_contract(),
        analytical_decision_object_table_contract(),
    ]
