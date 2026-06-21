"""market data batch metadata table

Revision ID: 0003_market_data_batch_metadata
Revises: 0002_operational_timeseries_tables
Create Date: 2026-06-21
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0003_market_data_batch_metadata"
down_revision = "0002_operational_timeseries_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "market_data_batch_records",
        sa.Column("batch_id", sa.String(length=128), nullable=False),
        sa.Column("instrument_id", sa.String(length=160), nullable=False),
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("exchange", sa.String(length=16), nullable=False),
        sa.Column("segment", sa.String(length=32), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("provider_name", sa.String(length=128), nullable=True),
        sa.Column("provider_type", sa.String(length=64), nullable=True),
        sa.Column("provider_version", sa.String(length=64), nullable=True),
        sa.Column("quality_status", sa.String(length=32), nullable=False),
        sa.Column("row_count", sa.Integer(), nullable=False),
        sa.Column("start_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_data_reference", sa.String(length=512), nullable=False),
        sa.Column("synthetic", sa.Boolean(), nullable=False),
        sa.Column("fixture_id", sa.String(length=128), nullable=True),
        sa.Column("dataset_manifest_id", sa.String(length=128), nullable=True),
        sa.Column("validation_report_id", sa.String(length=128), nullable=True),
        sa.Column("schema_version", sa.String(length=32), nullable=False),
        sa.Column("notes_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("batch_id", name="uq_market_data_batch_records_batch_id"),
    )
    op.create_index(op.f("ix_market_data_batch_records_batch_id"), "market_data_batch_records", ["batch_id"])
    op.create_index(op.f("ix_market_data_batch_records_dataset_manifest_id"), "market_data_batch_records", ["dataset_manifest_id"])
    op.create_index(op.f("ix_market_data_batch_records_end_timestamp"), "market_data_batch_records", ["end_timestamp"])
    op.create_index(op.f("ix_market_data_batch_records_exchange"), "market_data_batch_records", ["exchange"])
    op.create_index(op.f("ix_market_data_batch_records_fixture_id"), "market_data_batch_records", ["fixture_id"])
    op.create_index(op.f("ix_market_data_batch_records_instrument_id"), "market_data_batch_records", ["instrument_id"])
    op.create_index(op.f("ix_market_data_batch_records_provider_name"), "market_data_batch_records", ["provider_name"])
    op.create_index(op.f("ix_market_data_batch_records_segment"), "market_data_batch_records", ["segment"])
    op.create_index(op.f("ix_market_data_batch_records_start_timestamp"), "market_data_batch_records", ["start_timestamp"])
    op.create_index(op.f("ix_market_data_batch_records_symbol"), "market_data_batch_records", ["symbol"])
    op.create_index(op.f("ix_market_data_batch_records_timeframe"), "market_data_batch_records", ["timeframe"])
    op.create_index(op.f("ix_market_data_batch_records_validation_report_id"), "market_data_batch_records", ["validation_report_id"])
    op.create_index(
        "ix_market_data_batch_records_instrument_time_range",
        "market_data_batch_records",
        ["instrument_id", "timeframe", "start_timestamp", "end_timestamp"],
    )
    op.create_index(
        "ix_market_data_batch_records_synthetic_fixture",
        "market_data_batch_records",
        ["synthetic", "fixture_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_market_data_batch_records_synthetic_fixture", table_name="market_data_batch_records")
    op.drop_index("ix_market_data_batch_records_instrument_time_range", table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_validation_report_id"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_timeframe"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_symbol"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_start_timestamp"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_segment"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_provider_name"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_instrument_id"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_fixture_id"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_exchange"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_end_timestamp"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_dataset_manifest_id"), table_name="market_data_batch_records")
    op.drop_index(op.f("ix_market_data_batch_records_batch_id"), table_name="market_data_batch_records")
    op.drop_table("market_data_batch_records")
