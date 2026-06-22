from __future__ import annotations

from datetime import datetime

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from stark_terminal_core.domain.enums import Timeframe
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.market_data import MarketDataBar, normalize_datetime_to_utc
from stark_terminal_data_platform.db.models.timeseries import OHLCVBarORM, _provider_to_id


class OHLCVBarRepository:
    """SQLAlchemy repository for synthetic OHLCV bars using the operational time-series ORM."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_bar(self, bar: MarketDataBar) -> MarketDataBar:
        existing = self._get_orm(bar.instrument_id, bar.timeframe, bar.timestamp, bar.provider)
        if existing is None:
            orm = OHLCVBarORM.from_domain(bar)
            self.session.add(orm)
            self.session.flush()
            return orm.to_domain()

        self._update_orm(existing, bar)
        self.session.flush()
        return existing.to_domain()

    def upsert_many(self, bars: list[MarketDataBar]) -> list[MarketDataBar]:
        return [self.upsert_bar(bar) for bar in bars]

    def get_bar(
        self,
        instrument_id: InstrumentId,
        timeframe: Timeframe,
        timestamp: datetime,
        provider: DataProviderId | None = None,
    ) -> MarketDataBar | None:
        orm = self._get_orm(instrument_id, timeframe, timestamp, provider)
        return orm.to_domain() if orm is not None else None

    def list_bars(
        self,
        instrument_id: InstrumentId,
        timeframe: Timeframe,
        start: datetime | None = None,
        end: datetime | None = None,
        limit: int = 1000,
        offset: int = 0,
    ) -> list[MarketDataBar]:
        self._validate_limit_offset(limit, offset)
        normalized_start = normalize_datetime_to_utc(start) if start is not None else None
        normalized_end = normalize_datetime_to_utc(end) if end is not None else None
        if normalized_start is not None and normalized_end is not None and normalized_start > normalized_end:
            raise ValueError("start must be before or equal to end")

        statement = (
            select(OHLCVBarORM)
            .where(
                OHLCVBarORM.instrument_id == str(instrument_id),
                OHLCVBarORM.timeframe == Timeframe(timeframe).value,
            )
            .order_by(OHLCVBarORM.timestamp, OHLCVBarORM.provider_id)
            .limit(limit)
            .offset(offset)
        )
        if normalized_start is not None:
            statement = statement.where(OHLCVBarORM.timestamp >= normalized_start)
        if normalized_end is not None:
            statement = statement.where(OHLCVBarORM.timestamp <= normalized_end)
        return [row.to_domain() for row in self.session.scalars(statement).all()]

    def count(self, instrument_id: InstrumentId | None = None, timeframe: Timeframe | None = None) -> int:
        statement = select(func.count()).select_from(OHLCVBarORM)
        if instrument_id is not None:
            statement = statement.where(OHLCVBarORM.instrument_id == str(instrument_id))
        if timeframe is not None:
            statement = statement.where(OHLCVBarORM.timeframe == Timeframe(timeframe).value)
        return int(self.session.scalar(statement) or 0)

    def delete_synthetic_bars(self, source_data_reference: str | None = None) -> int:
        if source_data_reference is not None:
            normalized = source_data_reference.strip()
            if not normalized:
                raise ValueError("source_data_reference cannot be empty")
            statement = delete(OHLCVBarORM).where(OHLCVBarORM.source_data_reference == normalized)
        else:
            statement = delete(OHLCVBarORM).where(
                OHLCVBarORM.source_data_reference.is_not(None),
                func.lower(OHLCVBarORM.source_data_reference).like("%synthetic%"),
            )
        result = self.session.execute(statement)
        self.session.flush()
        return int(result.rowcount or 0)

    def _get_orm(
        self,
        instrument_id: InstrumentId,
        timeframe: Timeframe,
        timestamp: datetime,
        provider: DataProviderId | None,
    ) -> OHLCVBarORM | None:
        normalized_timestamp = normalize_datetime_to_utc(timestamp)
        provider_id = _provider_to_id(provider)
        statement = select(OHLCVBarORM).where(
            OHLCVBarORM.instrument_id == str(instrument_id),
            OHLCVBarORM.timeframe == Timeframe(timeframe).value,
            OHLCVBarORM.timestamp == normalized_timestamp,
            OHLCVBarORM.provider_id == provider_id,
        )
        return self.session.scalar(statement)

    @staticmethod
    def _update_orm(orm: OHLCVBarORM, bar: MarketDataBar) -> None:
        orm.instrument_id = str(bar.instrument_id)
        orm.symbol = bar.instrument_id.symbol
        orm.exchange = bar.instrument_id.exchange.value
        orm.segment = bar.instrument_id.segment.value
        orm.timeframe = bar.timeframe.value
        orm.timestamp = bar.timestamp
        orm.open = bar.open
        orm.high = bar.high
        orm.low = bar.low
        orm.close = bar.close
        orm.volume = bar.volume
        orm.open_interest = bar.open_interest
        orm.provider_id = _provider_to_id(bar.provider)
        orm.quality_status = bar.quality_status.value
        orm.source_data_reference = bar.source_data_reference

    @staticmethod
    def _validate_limit_offset(limit: int, offset: int) -> None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        if offset < 0:
            raise ValueError("offset must be non-negative")
