from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Index, UniqueConstraint

from stark_terminal_core.domain.audit import AuditMetadata
from stark_terminal_core.domain.decision_object import DecisionObject
from stark_terminal_core.domain.enums import (
    ActionState,
    AssetClass,
    ConfidenceMethod,
    DataProviderType,
    DecisionSource,
    Exchange,
    InstrumentStatus,
    MarketSegment,
    RiskLevel,
)
from stark_terminal_core.domain.identifiers import AuditId, DataProviderId, InstrumentId
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_data_platform.db.base import Base
from stark_terminal_data_platform.db.models import (
    AuditRecordORM,
    DataProviderORM,
    DecisionObjectRecordORM,
    InstrumentORM,
)


def test_base_metadata_contains_expected_tables() -> None:
    assert {
        "instruments",
        "data_providers",
        "audit_records",
        "decision_object_records",
    }.issubset(Base.metadata.tables)


def test_expected_constraints_and_indexes_exist() -> None:
    instruments = Base.metadata.tables["instruments"]
    decisions = Base.metadata.tables["decision_object_records"]

    instrument_constraints = {
        constraint.name
        for constraint in instruments.constraints
        if isinstance(constraint, UniqueConstraint)
    }
    decision_constraints = {
        constraint.name
        for constraint in decisions.constraints
        if isinstance(constraint, CheckConstraint)
    }
    decision_indexes = {index.name for index in decisions.indexes if isinstance(index, Index)}

    assert "uq_instruments_identity" in instrument_constraints
    assert "ck_decision_object_records_confidence_range" in decision_constraints
    assert "ix_decision_records_lookup" in decision_indexes


def test_no_orm_model_uses_reserved_metadata_column_attribute() -> None:
    for model in [InstrumentORM, DataProviderORM, AuditRecordORM, DecisionObjectRecordORM]:
        assert "metadata" not in model.__table__.columns


def test_instrument_domain_model_maps_to_orm_and_back() -> None:
    instrument = Instrument(
        instrument_id=InstrumentId(
            symbol="reliance",
            exchange=Exchange.NSE,
            segment=MarketSegment.NSE_EQUITY,
        ),
        display_name="Reliance Industries",
        asset_class=AssetClass.EQUITY,
        status=InstrumentStatus.ACTIVE,
        lot_size=1,
        tick_size=0.05,
        sector="Energy",
        metadata={"source": "unit-test"},
    )

    orm = InstrumentORM.from_domain(instrument)
    restored = orm.to_domain()

    assert orm.symbol == "RELIANCE"
    assert orm.metadata_json == {"source": "unit-test"}
    assert restored == instrument


def test_data_provider_maps_to_orm_and_back() -> None:
    provider = DataProviderId(
        name="Local Sample",
        provider_type=DataProviderType.LOCAL_SAMPLE,
        version="v1",
    )

    orm = DataProviderORM.from_domain(provider)
    restored = orm.to_domain()

    assert orm.name == "Local Sample"
    assert restored == provider


def test_audit_metadata_maps_to_orm() -> None:
    audit = AuditMetadata(
        audit_id=AuditId(value="audit_unit"),
        created_at=datetime(2026, 6, 20, tzinfo=timezone.utc),
        source="unit-test",
        source_data_reference="fixture://audit",
        model_or_rule_version="rule-v0",
        notes=["created for mapping test"],
    )

    orm = AuditRecordORM.from_domain(audit)

    assert orm.audit_id == "audit_unit"
    assert orm.notes_json == ["created for mapping test"]
    assert orm.to_domain() == audit


def test_decision_object_maps_to_orm_and_back() -> None:
    decision = DecisionObject(
        instrument="RELIANCE",
        exchange="NSE",
        segment=MarketSegment.NSE_EQUITY,
        timeframe="1D",
        regime="TREND_EXPANSION",
        state="breakout",
        action_state=ActionState.BUY_BIAS,
        confidence=72.5,
        confidence_method=ConfidenceMethod.RULE_SCORE,
        risk=RiskLevel.MEDIUM,
        evidence=["Confirmed close above range."],
        invalidation="Close back inside prior range.",
        horizon="swing",
        source_data_reference="fixture://decision",
        decision_source=DecisionSource.RULE_BASED,
        audit_id="audit_decision",
        model_or_rule_version="rule-v0",
        generated_at=datetime(2026, 6, 20, 9, 15, tzinfo=timezone.utc),
    )

    orm = DecisionObjectRecordORM.from_domain(decision)
    restored = orm.to_domain()

    assert orm.evidence_json == ["Confirmed close above range."]
    assert restored == decision
