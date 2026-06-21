"""initial metadata tables

Revision ID: 0001_initial_metadata_tables
Revises:
Create Date: 2026-06-20
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_metadata_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_records",
        sa.Column("audit_id", sa.String(length=96), nullable=False),
        sa.Column("source", sa.String(length=128), nullable=False),
        sa.Column("source_data_reference", sa.String(length=512), nullable=True),
        sa.Column("model_or_rule_version", sa.String(length=128), nullable=True),
        sa.Column("notes_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_records_audit_id"), "audit_records", ["audit_id"], unique=True)
    op.create_table(
        "data_providers",
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("provider_type", sa.String(length=32), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "provider_type", "version", name="uq_data_providers_identity"),
    )
    op.create_index(
        "ix_data_providers_identity",
        "data_providers",
        ["name", "provider_type", "version"],
        unique=False,
    )
    op.create_table(
        "decision_object_records",
        sa.Column("instrument", sa.String(length=64), nullable=False),
        sa.Column("exchange", sa.String(length=16), nullable=False),
        sa.Column("segment", sa.String(length=32), nullable=False),
        sa.Column("timeframe", sa.String(length=32), nullable=False),
        sa.Column("regime", sa.String(length=64), nullable=True),
        sa.Column("state", sa.String(length=64), nullable=True),
        sa.Column("action_state", sa.String(length=32), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("confidence_method", sa.String(length=64), nullable=False),
        sa.Column("risk", sa.String(length=32), nullable=False),
        sa.Column("evidence_json", sa.JSON(), nullable=False),
        sa.Column("invalidation", sa.String(length=512), nullable=True),
        sa.Column("horizon", sa.String(length=128), nullable=True),
        sa.Column("source_data_reference", sa.String(length=512), nullable=True),
        sa.Column("decision_source", sa.String(length=64), nullable=False),
        sa.Column("audit_id", sa.String(length=96), nullable=True),
        sa.Column("model_or_rule_version", sa.String(length=128), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.CheckConstraint(
            "confidence >= 0 AND confidence <= 100",
            name="ck_decision_object_records_confidence_range",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_decision_object_records_audit_id"), "decision_object_records", ["audit_id"], unique=False)
    op.create_index(
        "ix_decision_records_lookup",
        "decision_object_records",
        ["instrument", "exchange", "segment", "timeframe", "generated_at"],
        unique=False,
    )
    op.create_table(
        "instruments",
        sa.Column("symbol", sa.String(length=64), nullable=False),
        sa.Column("exchange", sa.String(length=16), nullable=False),
        sa.Column("segment", sa.String(length=32), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("asset_class", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("lot_size", sa.Integer(), nullable=True),
        sa.Column("tick_size", sa.Float(), nullable=True),
        sa.Column("isin", sa.String(length=32), nullable=True),
        sa.Column("sector", sa.String(length=128), nullable=True),
        sa.Column("industry", sa.String(length=128), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol", "exchange", "segment", name="uq_instruments_identity"),
    )
    op.create_index(op.f("ix_instruments_exchange"), "instruments", ["exchange"], unique=False)
    op.create_index("ix_instruments_identity", "instruments", ["symbol", "exchange", "segment"], unique=False)
    op.create_index(op.f("ix_instruments_isin"), "instruments", ["isin"], unique=False)
    op.create_index(op.f("ix_instruments_segment"), "instruments", ["segment"], unique=False)
    op.create_index(op.f("ix_instruments_symbol"), "instruments", ["symbol"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_instruments_symbol"), table_name="instruments")
    op.drop_index(op.f("ix_instruments_segment"), table_name="instruments")
    op.drop_index(op.f("ix_instruments_isin"), table_name="instruments")
    op.drop_index("ix_instruments_identity", table_name="instruments")
    op.drop_index(op.f("ix_instruments_exchange"), table_name="instruments")
    op.drop_table("instruments")
    op.drop_index("ix_decision_records_lookup", table_name="decision_object_records")
    op.drop_index(op.f("ix_decision_object_records_audit_id"), table_name="decision_object_records")
    op.drop_table("decision_object_records")
    op.drop_index("ix_data_providers_identity", table_name="data_providers")
    op.drop_table("data_providers")
    op.drop_index(op.f("ix_audit_records_audit_id"), table_name="audit_records")
    op.drop_table("audit_records")
