from __future__ import annotations

from sqlalchemy import delete, func, or_, select
from sqlalchemy.orm import Session

from stark_terminal_core.domain.enums import Exchange, MarketSegment
from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.instrument import Instrument
from stark_terminal_data_platform.db.models.instrument import InstrumentORM
from stark_terminal_data_platform.instruments.normalization import (
    normalize_exchange,
    normalize_segment,
    normalize_symbol,
)


class InstrumentRepository:
    """SQLAlchemy repository for instrument metadata only."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert(self, instrument: Instrument) -> Instrument:
        instrument_id = instrument.instrument_id
        existing = self._get_orm(instrument_id.symbol, instrument_id.exchange, instrument_id.segment)
        if existing is None:
            orm = InstrumentORM.from_domain(instrument)
            self.session.add(orm)
            self.session.flush()
            return orm.to_domain()

        existing.display_name = instrument.display_name
        existing.asset_class = instrument.asset_class.value
        existing.status = instrument.status.value
        existing.lot_size = instrument.lot_size
        existing.tick_size = instrument.tick_size
        existing.isin = instrument.isin
        existing.sector = instrument.sector
        existing.industry = instrument.industry
        existing.metadata_json = dict(instrument.metadata)
        self.session.flush()
        return existing.to_domain()

    def get(
        self,
        symbol: str,
        exchange: str | Exchange,
        segment: str | MarketSegment,
    ) -> Instrument | None:
        orm = self._get_orm(symbol, exchange, segment)
        return orm.to_domain() if orm is not None else None

    def get_by_id(self, instrument_id: InstrumentId) -> Instrument | None:
        return self.get(instrument_id.symbol, instrument_id.exchange, instrument_id.segment)

    def list_all(self, limit: int = 100, offset: int = 0) -> list[Instrument]:
        self._validate_limit_offset(limit, offset)
        statement = (
            select(InstrumentORM)
            .order_by(InstrumentORM.exchange, InstrumentORM.segment, InstrumentORM.symbol)
            .limit(limit)
            .offset(offset)
        )
        return [row.to_domain() for row in self.session.scalars(statement).all()]

    def search(self, query: str, limit: int = 20) -> list[Instrument]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        normalized_query = query.strip().lower()
        if not normalized_query:
            raise ValueError("query cannot be empty")
        statement = (
            select(InstrumentORM)
            .where(
                or_(
                    func.lower(InstrumentORM.symbol).contains(normalized_query),
                    func.lower(InstrumentORM.display_name).contains(normalized_query),
                )
            )
            .order_by(InstrumentORM.exchange, InstrumentORM.segment, InstrumentORM.symbol)
            .limit(limit)
        )
        return [row.to_domain() for row in self.session.scalars(statement).all()]

    def delete(
        self,
        symbol: str,
        exchange: str | Exchange,
        segment: str | MarketSegment,
    ) -> bool:
        normalized_symbol = normalize_symbol(symbol)
        normalized_exchange = normalize_exchange(exchange)
        normalized_segment = normalize_segment(segment)
        statement = delete(InstrumentORM).where(
            InstrumentORM.symbol == normalized_symbol,
            InstrumentORM.exchange == normalized_exchange.value,
            InstrumentORM.segment == normalized_segment.value,
        )
        result = self.session.execute(statement)
        self.session.flush()
        return bool(result.rowcount)

    def count(self) -> int:
        return int(self.session.scalar(select(func.count()).select_from(InstrumentORM)) or 0)

    def _get_orm(
        self,
        symbol: str,
        exchange: str | Exchange,
        segment: str | MarketSegment,
    ) -> InstrumentORM | None:
        normalized_symbol = normalize_symbol(symbol)
        normalized_exchange = normalize_exchange(exchange)
        normalized_segment = normalize_segment(segment)
        statement = select(InstrumentORM).where(
            InstrumentORM.symbol == normalized_symbol,
            InstrumentORM.exchange == normalized_exchange.value,
            InstrumentORM.segment == normalized_segment.value,
        )
        return self.session.scalar(statement)

    @staticmethod
    def _validate_limit_offset(limit: int, offset: int) -> None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        if offset < 0:
            raise ValueError("offset must be non-negative")
