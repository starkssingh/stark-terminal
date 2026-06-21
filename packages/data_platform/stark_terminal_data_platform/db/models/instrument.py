from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from stark_terminal_core.domain.enums import AssetClass, Exchange, InstrumentStatus, MarketSegment
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_data_platform.db.base import Base, IdMixin, TimestampMixin


class InstrumentORM(IdMixin, TimestampMixin, Base):
    __tablename__ = "instruments"
    __table_args__ = (
        UniqueConstraint("symbol", "exchange", "segment", name="uq_instruments_identity"),
        Index("ix_instruments_identity", "symbol", "exchange", "segment"),
    )

    symbol: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    exchange: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    segment: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    asset_class: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    lot_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tick_size: Mapped[float | None] = mapped_column(Float, nullable=True)
    isin: Mapped[str | None] = mapped_column(String(32), index=True, nullable=True)
    sector: Mapped[str | None] = mapped_column(String(128), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(128), nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    @classmethod
    def from_domain(cls, instrument: Instrument) -> InstrumentORM:
        return cls(
            symbol=instrument.instrument_id.symbol,
            exchange=instrument.instrument_id.exchange.value,
            segment=instrument.instrument_id.segment.value,
            display_name=instrument.display_name,
            asset_class=instrument.asset_class.value,
            status=instrument.status.value,
            lot_size=instrument.lot_size,
            tick_size=instrument.tick_size,
            isin=instrument.isin,
            sector=instrument.sector,
            industry=instrument.industry,
            metadata_json=dict(instrument.metadata),
        )

    def to_domain(self) -> Instrument:
        return Instrument(
            instrument_id=InstrumentId(
                symbol=self.symbol,
                exchange=Exchange(self.exchange),
                segment=MarketSegment(self.segment),
            ),
            display_name=self.display_name,
            asset_class=AssetClass(self.asset_class),
            status=InstrumentStatus(self.status),
            lot_size=self.lot_size,
            tick_size=self.tick_size,
            isin=self.isin,
            sector=self.sector,
            industry=self.industry,
            metadata=dict(self.metadata_json or {}),
        )
