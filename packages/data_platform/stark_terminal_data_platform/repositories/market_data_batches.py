from __future__ import annotations

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from stark_terminal_core.domain.identifiers import InstrumentId
from stark_terminal_core.domain.market_data_batch import MarketDataBatchMetadata
from stark_terminal_data_platform.db.models.market_data_batch import MarketDataBatchRecordORM


class MarketDataBatchRepository:
    """SQLAlchemy repository for market data batch metadata only."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert(self, metadata: MarketDataBatchMetadata) -> MarketDataBatchMetadata:
        existing = self._get_orm(metadata.batch_id)
        if existing is None:
            orm = MarketDataBatchRecordORM.from_domain(metadata)
            self.session.add(orm)
            self.session.flush()
            return orm.to_domain()
        existing.update_from_domain(metadata)
        self.session.flush()
        return existing.to_domain()

    def get(self, batch_id: str) -> MarketDataBatchMetadata | None:
        orm = self._get_orm(batch_id)
        return orm.to_domain() if orm is not None else None

    def list_all(self, limit: int = 100, offset: int = 0) -> list[MarketDataBatchMetadata]:
        self._validate_limit_offset(limit, offset)
        statement = (
            select(MarketDataBatchRecordORM)
            .order_by(MarketDataBatchRecordORM.start_timestamp, MarketDataBatchRecordORM.batch_id)
            .limit(limit)
            .offset(offset)
        )
        return [row.to_domain() for row in self.session.scalars(statement).all()]

    def list_by_instrument(
        self,
        instrument_id: InstrumentId,
        limit: int = 100,
        offset: int = 0,
    ) -> list[MarketDataBatchMetadata]:
        self._validate_limit_offset(limit, offset)
        statement = (
            select(MarketDataBatchRecordORM)
            .where(MarketDataBatchRecordORM.instrument_id == str(instrument_id))
            .order_by(MarketDataBatchRecordORM.start_timestamp, MarketDataBatchRecordORM.batch_id)
            .limit(limit)
            .offset(offset)
        )
        return [row.to_domain() for row in self.session.scalars(statement).all()]

    def search_by_fixture(self, fixture_id: str, limit: int = 100, offset: int = 0) -> list[MarketDataBatchMetadata]:
        self._validate_limit_offset(limit, offset)
        normalized = fixture_id.strip()
        if not normalized:
            raise ValueError("fixture_id cannot be empty")
        statement = (
            select(MarketDataBatchRecordORM)
            .where(MarketDataBatchRecordORM.fixture_id == normalized)
            .order_by(MarketDataBatchRecordORM.start_timestamp, MarketDataBatchRecordORM.batch_id)
            .limit(limit)
            .offset(offset)
        )
        return [row.to_domain() for row in self.session.scalars(statement).all()]

    def count(self) -> int:
        return int(self.session.scalar(select(func.count()).select_from(MarketDataBatchRecordORM)) or 0)

    def delete(self, batch_id: str) -> bool:
        normalized = batch_id.strip()
        if not normalized:
            raise ValueError("batch_id cannot be empty")
        result = self.session.execute(
            delete(MarketDataBatchRecordORM).where(MarketDataBatchRecordORM.batch_id == normalized)
        )
        self.session.flush()
        return bool(result.rowcount)

    def _get_orm(self, batch_id: str) -> MarketDataBatchRecordORM | None:
        normalized = batch_id.strip()
        if not normalized:
            raise ValueError("batch_id cannot be empty")
        return self.session.scalar(
            select(MarketDataBatchRecordORM).where(MarketDataBatchRecordORM.batch_id == normalized)
        )

    @staticmethod
    def _validate_limit_offset(limit: int, offset: int) -> None:
        if limit <= 0:
            raise ValueError("limit must be positive")
        if offset < 0:
            raise ValueError("offset must be non-negative")
