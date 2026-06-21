from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import JSON, Date, DateTime, Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates

from stark_terminal_core.domain.enums import DataProviderType, DataQualityStatus, Exchange, MarketSegment, Timeframe
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBar
from stark_terminal_core.domain.options import OptionsChainSnapshot
from stark_terminal_data_platform.db.base import Base, IdMixin, utc_now


def _provider_to_id(provider: DataProviderId | None) -> str | None:
    if provider is None:
        return None
    version = provider.version or ""
    return f"{provider.provider_type.value}:{provider.name}:{version}"


def _provider_from_id(provider_id: str | None) -> DataProviderId | None:
    if provider_id is None:
        return None
    provider_type, name, version = provider_id.split(":", 2)
    return DataProviderId(
        name=name,
        provider_type=DataProviderType(provider_type),
        version=version or None,
    )


class OHLCVBarORM(IdMixin, Base):
    __tablename__ = "ohlcv_bars"
    __table_args__ = (
        UniqueConstraint(
            "instrument_id",
            "timeframe",
            "timestamp",
            "provider_id",
            name="uq_ohlcv_bars_identity",
        ),
        Index(
            "ix_ohlcv_bars_lookup",
            "symbol",
            "exchange",
            "segment",
            "timeframe",
            "timestamp",
        ),
    )

    instrument_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    exchange: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    segment: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    timeframe: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float | None] = mapped_column(Float, nullable=True)
    open_interest: Mapped[float | None] = mapped_column(Float, nullable=True)
    provider_id: Mapped[str | None] = mapped_column(String(256), index=True, nullable=True)
    quality_status: Mapped[str] = mapped_column(String(32), nullable=False)
    source_data_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    @classmethod
    def from_domain(cls, bar: MarketDataBar) -> OHLCVBarORM:
        return cls(
            instrument_id=str(bar.instrument_id),
            symbol=bar.instrument_id.symbol,
            exchange=bar.instrument_id.exchange.value,
            segment=bar.instrument_id.segment.value,
            timeframe=bar.timeframe.value,
            timestamp=bar.timestamp,
            open=bar.open,
            high=bar.high,
            low=bar.low,
            close=bar.close,
            volume=bar.volume,
            open_interest=bar.open_interest,
            provider_id=_provider_to_id(bar.provider),
            quality_status=bar.quality_status.value,
            source_data_reference=bar.source_data_reference,
        )

    def to_domain(self) -> MarketDataBar:
        return MarketDataBar(
            instrument_id=InstrumentId(
                symbol=self.symbol,
                exchange=Exchange(self.exchange),
                segment=MarketSegment(self.segment),
            ),
            timeframe=Timeframe(self.timeframe),
            timestamp=self.timestamp,
            open=self.open,
            high=self.high,
            low=self.low,
            close=self.close,
            volume=self.volume,
            open_interest=self.open_interest,
            provider=_provider_from_id(self.provider_id),
            quality_status=DataQualityStatus(self.quality_status),
            source_data_reference=self.source_data_reference,
        )


class OptionsChainSnapshotORM(IdMixin, Base):
    __tablename__ = "options_chain_snapshots"
    __table_args__ = (
        Index(
            "ix_options_chain_snapshots_lookup",
            "underlying_symbol",
            "exchange",
            "segment",
            "expiry",
            "timestamp",
        ),
    )

    underlying_instrument_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    underlying_symbol: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    exchange: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    segment: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    expiry: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    provider_id: Mapped[str | None] = mapped_column(String(256), index=True, nullable=True)
    contract_count: Mapped[int] = mapped_column(Integer, nullable=False)
    source_data_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    quality_status: Mapped[str] = mapped_column(String(32), nullable=False)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    @classmethod
    def from_domain(cls, snapshot: OptionsChainSnapshot) -> OptionsChainSnapshotORM:
        return cls(
            underlying_instrument_id=str(snapshot.underlying),
            underlying_symbol=snapshot.underlying.symbol,
            exchange=snapshot.underlying.exchange.value,
            segment=snapshot.underlying.segment.value,
            expiry=snapshot.expiry,
            timestamp=snapshot.timestamp,
            provider_id=_provider_to_id(snapshot.provider),
            contract_count=len(snapshot.contracts),
            source_data_reference=snapshot.source_data_reference,
            quality_status=DataQualityStatus.RAW.value,
            payload_json={
                "contract_symbols": [contract.contract_symbol for contract in snapshot.contracts],
                "strikes": [contract.strike for contract in snapshot.contracts],
                "option_types": [contract.option_type.value for contract in snapshot.contracts],
            },
        )


class FuturesBasisSnapshotORM(IdMixin, Base):
    __tablename__ = "futures_basis_snapshots"
    __table_args__ = (
        Index(
            "ix_futures_basis_snapshots_lookup",
            "underlying_symbol",
            "exchange",
            "segment",
            "contract_symbol",
            "timestamp",
        ),
    )

    underlying_instrument_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    underlying_symbol: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    exchange: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    segment: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    contract_symbol: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    expiry: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    spot_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    futures_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    basis: Mapped[float | None] = mapped_column(Float, nullable=True)
    basis_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    provider_id: Mapped[str | None] = mapped_column(String(256), nullable=True)
    quality_status: Mapped[str] = mapped_column(String(32), nullable=False)
    source_data_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    @validates("spot_price", "futures_price")
    def validate_non_negative_price(self, key: str, value: float | None) -> float | None:
        if value is not None and value < 0:
            raise ValueError(f"{key} must be non-negative when provided")
        return value


class MarketStateSnapshotORM(IdMixin, Base):
    __tablename__ = "market_state_snapshots"
    __table_args__ = (
        Index(
            "ix_market_state_snapshots_lookup",
            "symbol",
            "exchange",
            "segment",
            "timeframe",
            "timestamp",
        ),
    )

    instrument_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    exchange: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    segment: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    timeframe: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    state: Mapped[str | None] = mapped_column(String(64), nullable=True)
    regime: Mapped[str | None] = mapped_column(String(64), nullable=True)
    action_state: Mapped[str | None] = mapped_column(String(32), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk: Mapped[str | None] = mapped_column(String(32), nullable=True)
    source: Mapped[str] = mapped_column(String(128), nullable=False)
    source_data_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )


class RegimeSnapshotORM(IdMixin, Base):
    __tablename__ = "regime_snapshots"
    __table_args__ = (
        Index(
            "ix_regime_snapshots_lookup",
            "symbol",
            "exchange",
            "segment",
            "timeframe",
            "timestamp",
        ),
    )

    instrument_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    exchange: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    segment: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    timeframe: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    regime_label: Mapped[str] = mapped_column(String(64), nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    method: Mapped[str | None] = mapped_column(String(128), nullable=True)
    model_or_rule_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    evidence_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    source_data_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
