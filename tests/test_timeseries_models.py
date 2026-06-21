from datetime import date, datetime, timezone

import pytest
from sqlalchemy import UniqueConstraint

from stark_terminal_core.domain.enums import (
    DataQualityStatus,
    Exchange,
    MarketSegment,
    OptionType,
    Timeframe,
)
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBar
from stark_terminal_core.domain.options import OptionContract, OptionsChainSnapshot
from stark_terminal_data_platform.db.base import Base
from stark_terminal_data_platform.db.models import (
    FuturesBasisSnapshotORM,
    MarketStateSnapshotORM,
    OHLCVBarORM,
    OptionsChainSnapshotORM,
    RegimeSnapshotORM,
)


def nifty() -> InstrumentId:
    return InstrumentId(symbol="NIFTY", exchange=Exchange.NSE, segment=MarketSegment.INDEX)


def test_base_metadata_contains_timeseries_tables() -> None:
    assert {
        "ohlcv_bars",
        "options_chain_snapshots",
        "futures_basis_snapshots",
        "market_state_snapshots",
        "regime_snapshots",
    }.issubset(Base.metadata.tables)


def test_ohlcv_unique_constraint_exists() -> None:
    table = Base.metadata.tables["ohlcv_bars"]
    constraints = {
        constraint.name
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "uq_ohlcv_bars_identity" in constraints
    assert "ix_ohlcv_bars_lookup" in {index.name for index in table.indexes}


def test_no_timeseries_model_uses_reserved_metadata_column_attribute() -> None:
    for model in [
        OHLCVBarORM,
        OptionsChainSnapshotORM,
        FuturesBasisSnapshotORM,
        MarketStateSnapshotORM,
        RegimeSnapshotORM,
    ]:
        assert "metadata" not in model.__table__.columns


def test_market_data_bar_maps_to_ohlcv_orm_and_back() -> None:
    bar = MarketDataBar(
        instrument_id=nifty(),
        timeframe=Timeframe.FIVE_MINUTE,
        timestamp=datetime(2026, 6, 20, 9, 15, tzinfo=timezone.utc),
        open=100.0,
        high=105.0,
        low=99.0,
        close=103.0,
        volume=10000.0,
        open_interest=500.0,
        quality_status=DataQualityStatus.NORMALIZED,
        source_data_reference="fixture://ohlcv",
    )

    orm = OHLCVBarORM.from_domain(bar)
    restored = orm.to_domain()

    assert orm.symbol == "NIFTY"
    assert orm.exchange == "NSE"
    assert orm.segment == "INDEX"
    assert orm.timeframe == "FIVE_MINUTE"
    assert orm.timestamp == bar.timestamp
    assert orm.open == 100.0
    assert orm.high == 105.0
    assert orm.low == 99.0
    assert orm.close == 103.0
    assert restored == bar


def test_options_chain_snapshot_maps_to_orm_summary() -> None:
    contract = OptionContract(
        underlying=nifty(),
        contract_symbol="NIFTY26JUN23000CE",
        expiry=date(2026, 6, 25),
        strike=23000.0,
        option_type=OptionType.CALL,
        lot_size=50,
    )
    snapshot = OptionsChainSnapshot(
        underlying=nifty(),
        timestamp=datetime(2026, 6, 20, 9, 15, tzinfo=timezone.utc),
        expiry=date(2026, 6, 25),
        contracts=[contract],
        source_data_reference="fixture://options",
    )

    orm = OptionsChainSnapshotORM.from_domain(snapshot)

    assert orm.contract_count == 1
    assert orm.underlying_symbol == "NIFTY"
    assert orm.expiry == date(2026, 6, 25)
    assert orm.timestamp == snapshot.timestamp
    assert orm.payload_json["contract_symbols"] == ["NIFTY26JUN23000CE"]


def test_options_chain_full_to_domain_reconstruction_is_intentionally_limited() -> None:
    assert not hasattr(OptionsChainSnapshotORM, "to_domain")


def test_futures_basis_snapshot_can_be_created() -> None:
    snapshot = FuturesBasisSnapshotORM(
        underlying_instrument_id=str(nifty()),
        underlying_symbol="NIFTY",
        exchange="NSE",
        segment="INDEX",
        contract_symbol="NIFTY26JUNFUT",
        expiry=date(2026, 6, 25),
        timestamp=datetime(2026, 6, 20, 9, 15, tzinfo=timezone.utc),
        spot_price=23000.0,
        futures_price=23050.0,
        basis=50.0,
        basis_percent=0.217,
        quality_status="RAW",
    )

    assert snapshot.contract_symbol == "NIFTY26JUNFUT"


def test_futures_basis_snapshot_rejects_negative_prices() -> None:
    with pytest.raises(ValueError):
        FuturesBasisSnapshotORM(
            underlying_instrument_id=str(nifty()),
            underlying_symbol="NIFTY",
            exchange="NSE",
            segment="INDEX",
            contract_symbol="NIFTY26JUNFUT",
            expiry=date(2026, 6, 25),
            timestamp=datetime(2026, 6, 20, 9, 15, tzinfo=timezone.utc),
            spot_price=-1.0,
            quality_status="RAW",
        )


def test_market_state_snapshot_can_be_created() -> None:
    snapshot = MarketStateSnapshotORM(
        instrument_id=str(nifty()),
        symbol="NIFTY",
        exchange="NSE",
        segment="INDEX",
        timeframe="DAILY",
        timestamp=datetime(2026, 6, 20, 9, 15, tzinfo=timezone.utc),
        source="unit-test",
        payload_json={"state_version": "placeholder"},
    )

    assert snapshot.source == "unit-test"


def test_regime_snapshot_can_be_created() -> None:
    snapshot = RegimeSnapshotORM(
        instrument_id=str(nifty()),
        symbol="NIFTY",
        exchange="NSE",
        segment="INDEX",
        timeframe="DAILY",
        timestamp=datetime(2026, 6, 20, 9, 15, tzinfo=timezone.utc),
        regime_label="UNKNOWN",
        evidence_json=["placeholder only"],
    )

    assert snapshot.regime_label == "UNKNOWN"
