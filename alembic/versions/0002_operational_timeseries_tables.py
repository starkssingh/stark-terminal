"""operational timeseries tables

Revision ID: 0002_operational_timeseries_tables
Revises: 0001_initial_metadata_tables
Create Date: 2026-06-20
"""

from __future__ import annotations

import os

from alembic import op
import sqlalchemy as sa


revision = "0002_operational_timeseries_tables"
down_revision = "0001_initial_metadata_tables"
branch_labels = None
depends_on = None

HYPERTABLE_CANDIDATES = [
    "ohlcv_bars",
    "options_chain_snapshots",
    "futures_basis_snapshots",
    "market_state_snapshots",
    "regime_snapshots",
]


def _enabled(name: str) -> bool:
    return os.getenv(name, "false").strip().lower() in {"1", "true", "yes", "on"}


def _maybe_prepare_timescaledb() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    if _enabled("TIMESCALE_CREATE_EXTENSION"):
        op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")

    if _enabled("TIMESCALE_CREATE_HYPERTABLES"):
        for table_name in HYPERTABLE_CANDIDATES:
            op.execute(
                "SELECT create_hypertable("
                f"'{table_name}', "
                "'timestamp', "
                "if_not_exists => TRUE"
                ");"
            )


def upgrade() -> None:
    op.create_table(
        "ohlcv_bars",
        sa.Column("instrument_id", sa.String(length=160), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("exchange", sa.String(length=16), nullable=False),
        sa.Column("segment", sa.String(length=32), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.Float(), nullable=True),
        sa.Column("open_interest", sa.Float(), nullable=True),
        sa.Column("provider_id", sa.String(length=256), nullable=True),
        sa.Column("quality_status", sa.String(length=32), nullable=False),
        sa.Column("source_data_reference", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "instrument_id",
            "timeframe",
            "timestamp",
            "provider_id",
            name="uq_ohlcv_bars_identity",
        ),
    )
    op.create_index("ix_ohlcv_bars_lookup", "ohlcv_bars", ["symbol", "exchange", "segment", "timeframe", "timestamp"])
    op.create_index(op.f("ix_ohlcv_bars_exchange"), "ohlcv_bars", ["exchange"])
    op.create_index(op.f("ix_ohlcv_bars_instrument_id"), "ohlcv_bars", ["instrument_id"])
    op.create_index(op.f("ix_ohlcv_bars_provider_id"), "ohlcv_bars", ["provider_id"])
    op.create_index(op.f("ix_ohlcv_bars_segment"), "ohlcv_bars", ["segment"])
    op.create_index(op.f("ix_ohlcv_bars_symbol"), "ohlcv_bars", ["symbol"])
    op.create_index(op.f("ix_ohlcv_bars_timeframe"), "ohlcv_bars", ["timeframe"])
    op.create_index(op.f("ix_ohlcv_bars_timestamp"), "ohlcv_bars", ["timestamp"])

    op.create_table(
        "options_chain_snapshots",
        sa.Column("underlying_instrument_id", sa.String(length=160), nullable=False),
        sa.Column("underlying_symbol", sa.String(length=64), nullable=False),
        sa.Column("exchange", sa.String(length=16), nullable=False),
        sa.Column("segment", sa.String(length=32), nullable=False),
        sa.Column("expiry", sa.Date(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("provider_id", sa.String(length=256), nullable=True),
        sa.Column("contract_count", sa.Integer(), nullable=False),
        sa.Column("source_data_reference", sa.String(length=512), nullable=True),
        sa.Column("quality_status", sa.String(length=32), nullable=False),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_options_chain_snapshots_lookup", "options_chain_snapshots", ["underlying_symbol", "exchange", "segment", "expiry", "timestamp"])
    op.create_index(op.f("ix_options_chain_snapshots_exchange"), "options_chain_snapshots", ["exchange"])
    op.create_index(op.f("ix_options_chain_snapshots_expiry"), "options_chain_snapshots", ["expiry"])
    op.create_index(op.f("ix_options_chain_snapshots_provider_id"), "options_chain_snapshots", ["provider_id"])
    op.create_index(op.f("ix_options_chain_snapshots_segment"), "options_chain_snapshots", ["segment"])
    op.create_index(op.f("ix_options_chain_snapshots_timestamp"), "options_chain_snapshots", ["timestamp"])
    op.create_index(op.f("ix_options_chain_snapshots_underlying_instrument_id"), "options_chain_snapshots", ["underlying_instrument_id"])
    op.create_index(op.f("ix_options_chain_snapshots_underlying_symbol"), "options_chain_snapshots", ["underlying_symbol"])

    op.create_table(
        "futures_basis_snapshots",
        sa.Column("underlying_instrument_id", sa.String(length=160), nullable=False),
        sa.Column("underlying_symbol", sa.String(length=64), nullable=False),
        sa.Column("exchange", sa.String(length=16), nullable=False),
        sa.Column("segment", sa.String(length=32), nullable=False),
        sa.Column("contract_symbol", sa.String(length=128), nullable=False),
        sa.Column("expiry", sa.Date(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("spot_price", sa.Float(), nullable=True),
        sa.Column("futures_price", sa.Float(), nullable=True),
        sa.Column("basis", sa.Float(), nullable=True),
        sa.Column("basis_percent", sa.Float(), nullable=True),
        sa.Column("provider_id", sa.String(length=256), nullable=True),
        sa.Column("quality_status", sa.String(length=32), nullable=False),
        sa.Column("source_data_reference", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_futures_basis_snapshots_lookup", "futures_basis_snapshots", ["underlying_symbol", "exchange", "segment", "contract_symbol", "timestamp"])
    op.create_index(op.f("ix_futures_basis_snapshots_contract_symbol"), "futures_basis_snapshots", ["contract_symbol"])
    op.create_index(op.f("ix_futures_basis_snapshots_exchange"), "futures_basis_snapshots", ["exchange"])
    op.create_index(op.f("ix_futures_basis_snapshots_expiry"), "futures_basis_snapshots", ["expiry"])
    op.create_index(op.f("ix_futures_basis_snapshots_segment"), "futures_basis_snapshots", ["segment"])
    op.create_index(op.f("ix_futures_basis_snapshots_timestamp"), "futures_basis_snapshots", ["timestamp"])
    op.create_index(op.f("ix_futures_basis_snapshots_underlying_instrument_id"), "futures_basis_snapshots", ["underlying_instrument_id"])
    op.create_index(op.f("ix_futures_basis_snapshots_underlying_symbol"), "futures_basis_snapshots", ["underlying_symbol"])

    op.create_table(
        "market_state_snapshots",
        sa.Column("instrument_id", sa.String(length=160), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("exchange", sa.String(length=16), nullable=False),
        sa.Column("segment", sa.String(length=32), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("state", sa.String(length=64), nullable=True),
        sa.Column("regime", sa.String(length=64), nullable=True),
        sa.Column("action_state", sa.String(length=32), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("risk", sa.String(length=32), nullable=True),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("source_data_reference", sa.String(length=512), nullable=True),
        sa.Column("payload_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_market_state_snapshots_lookup", "market_state_snapshots", ["symbol", "exchange", "segment", "timeframe", "timestamp"])
    op.create_index(op.f("ix_market_state_snapshots_exchange"), "market_state_snapshots", ["exchange"])
    op.create_index(op.f("ix_market_state_snapshots_instrument_id"), "market_state_snapshots", ["instrument_id"])
    op.create_index(op.f("ix_market_state_snapshots_segment"), "market_state_snapshots", ["segment"])
    op.create_index(op.f("ix_market_state_snapshots_symbol"), "market_state_snapshots", ["symbol"])
    op.create_index(op.f("ix_market_state_snapshots_timeframe"), "market_state_snapshots", ["timeframe"])
    op.create_index(op.f("ix_market_state_snapshots_timestamp"), "market_state_snapshots", ["timestamp"])

    op.create_table(
        "regime_snapshots",
        sa.Column("instrument_id", sa.String(length=160), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("exchange", sa.String(length=16), nullable=False),
        sa.Column("segment", sa.String(length=32), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("regime_label", sa.String(length=64), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("method", sa.String(length=128), nullable=True),
        sa.Column("model_or_rule_version", sa.String(length=128), nullable=True),
        sa.Column("evidence_json", sa.JSON(), nullable=False),
        sa.Column("source_data_reference", sa.String(length=512), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_regime_snapshots_lookup", "regime_snapshots", ["symbol", "exchange", "segment", "timeframe", "timestamp"])
    op.create_index(op.f("ix_regime_snapshots_exchange"), "regime_snapshots", ["exchange"])
    op.create_index(op.f("ix_regime_snapshots_instrument_id"), "regime_snapshots", ["instrument_id"])
    op.create_index(op.f("ix_regime_snapshots_segment"), "regime_snapshots", ["segment"])
    op.create_index(op.f("ix_regime_snapshots_symbol"), "regime_snapshots", ["symbol"])
    op.create_index(op.f("ix_regime_snapshots_timeframe"), "regime_snapshots", ["timeframe"])
    op.create_index(op.f("ix_regime_snapshots_timestamp"), "regime_snapshots", ["timestamp"])

    # TimescaleDB preparation is opt-in for PostgreSQL deployments:
    # set TIMESCALE_CREATE_EXTENSION=true and/or TIMESCALE_CREATE_HYPERTABLES=true.
    # SQLite tests inspect this migration text but do not execute TimescaleDB SQL.
    _maybe_prepare_timescaledb()


def downgrade() -> None:
    op.drop_index(op.f("ix_regime_snapshots_timestamp"), table_name="regime_snapshots")
    op.drop_index(op.f("ix_regime_snapshots_timeframe"), table_name="regime_snapshots")
    op.drop_index(op.f("ix_regime_snapshots_symbol"), table_name="regime_snapshots")
    op.drop_index(op.f("ix_regime_snapshots_segment"), table_name="regime_snapshots")
    op.drop_index(op.f("ix_regime_snapshots_instrument_id"), table_name="regime_snapshots")
    op.drop_index(op.f("ix_regime_snapshots_exchange"), table_name="regime_snapshots")
    op.drop_index("ix_regime_snapshots_lookup", table_name="regime_snapshots")
    op.drop_table("regime_snapshots")
    op.drop_index(op.f("ix_market_state_snapshots_timestamp"), table_name="market_state_snapshots")
    op.drop_index(op.f("ix_market_state_snapshots_timeframe"), table_name="market_state_snapshots")
    op.drop_index(op.f("ix_market_state_snapshots_symbol"), table_name="market_state_snapshots")
    op.drop_index(op.f("ix_market_state_snapshots_segment"), table_name="market_state_snapshots")
    op.drop_index(op.f("ix_market_state_snapshots_instrument_id"), table_name="market_state_snapshots")
    op.drop_index(op.f("ix_market_state_snapshots_exchange"), table_name="market_state_snapshots")
    op.drop_index("ix_market_state_snapshots_lookup", table_name="market_state_snapshots")
    op.drop_table("market_state_snapshots")
    op.drop_index(op.f("ix_futures_basis_snapshots_underlying_symbol"), table_name="futures_basis_snapshots")
    op.drop_index(op.f("ix_futures_basis_snapshots_underlying_instrument_id"), table_name="futures_basis_snapshots")
    op.drop_index(op.f("ix_futures_basis_snapshots_timestamp"), table_name="futures_basis_snapshots")
    op.drop_index(op.f("ix_futures_basis_snapshots_segment"), table_name="futures_basis_snapshots")
    op.drop_index(op.f("ix_futures_basis_snapshots_expiry"), table_name="futures_basis_snapshots")
    op.drop_index(op.f("ix_futures_basis_snapshots_exchange"), table_name="futures_basis_snapshots")
    op.drop_index(op.f("ix_futures_basis_snapshots_contract_symbol"), table_name="futures_basis_snapshots")
    op.drop_index("ix_futures_basis_snapshots_lookup", table_name="futures_basis_snapshots")
    op.drop_table("futures_basis_snapshots")
    op.drop_index(op.f("ix_options_chain_snapshots_underlying_symbol"), table_name="options_chain_snapshots")
    op.drop_index(op.f("ix_options_chain_snapshots_underlying_instrument_id"), table_name="options_chain_snapshots")
    op.drop_index(op.f("ix_options_chain_snapshots_timestamp"), table_name="options_chain_snapshots")
    op.drop_index(op.f("ix_options_chain_snapshots_segment"), table_name="options_chain_snapshots")
    op.drop_index(op.f("ix_options_chain_snapshots_provider_id"), table_name="options_chain_snapshots")
    op.drop_index(op.f("ix_options_chain_snapshots_expiry"), table_name="options_chain_snapshots")
    op.drop_index(op.f("ix_options_chain_snapshots_exchange"), table_name="options_chain_snapshots")
    op.drop_index("ix_options_chain_snapshots_lookup", table_name="options_chain_snapshots")
    op.drop_table("options_chain_snapshots")
    op.drop_index(op.f("ix_ohlcv_bars_timestamp"), table_name="ohlcv_bars")
    op.drop_index(op.f("ix_ohlcv_bars_timeframe"), table_name="ohlcv_bars")
    op.drop_index(op.f("ix_ohlcv_bars_symbol"), table_name="ohlcv_bars")
    op.drop_index(op.f("ix_ohlcv_bars_segment"), table_name="ohlcv_bars")
    op.drop_index(op.f("ix_ohlcv_bars_provider_id"), table_name="ohlcv_bars")
    op.drop_index(op.f("ix_ohlcv_bars_instrument_id"), table_name="ohlcv_bars")
    op.drop_index(op.f("ix_ohlcv_bars_exchange"), table_name="ohlcv_bars")
    op.drop_index("ix_ohlcv_bars_lookup", table_name="ohlcv_bars")
    op.drop_table("ohlcv_bars")
