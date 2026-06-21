from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, Index, Integer, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from stark_terminal_core.domain.enums import DataProviderType, DataQualityStatus, Exchange, MarketSegment, Timeframe
from stark_terminal_core.domain.identifiers import DataProviderId, InstrumentId
from stark_terminal_core.domain.market_data_batch import MarketDataBatchMetadata
from stark_terminal_data_platform.db.base import Base, IdMixin, TimestampMixin


class MarketDataBatchRecordORM(IdMixin, TimestampMixin, Base):
    __tablename__ = "market_data_batch_records"
    __table_args__ = (
        UniqueConstraint("batch_id", name="uq_market_data_batch_records_batch_id"),
        Index(
            "ix_market_data_batch_records_instrument_time_range",
            "instrument_id",
            "timeframe",
            "start_timestamp",
            "end_timestamp",
        ),
        Index("ix_market_data_batch_records_synthetic_fixture", "synthetic", "fixture_id"),
    )

    batch_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    instrument_id: Mapped[str] = mapped_column(String(160), index=True, nullable=False)
    symbol: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    exchange: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    segment: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    timeframe: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    provider_name: Mapped[str | None] = mapped_column(String(128), index=True, nullable=True)
    provider_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    provider_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    quality_status: Mapped[str] = mapped_column(String(32), nullable=False)
    row_count: Mapped[int] = mapped_column(Integer, nullable=False)
    start_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    end_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    source_data_reference: Mapped[str] = mapped_column(String(512), nullable=False)
    synthetic: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fixture_id: Mapped[str | None] = mapped_column(String(128), index=True, nullable=True)
    dataset_manifest_id: Mapped[str | None] = mapped_column(String(128), index=True, nullable=True)
    validation_report_id: Mapped[str | None] = mapped_column(String(128), index=True, nullable=True)
    schema_version: Mapped[str] = mapped_column(String(32), nullable=False)
    notes_json: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    @classmethod
    def from_domain(cls, metadata: MarketDataBatchMetadata) -> MarketDataBatchRecordORM:
        provider = metadata.provider
        return cls(
            batch_id=metadata.batch_id,
            instrument_id=str(metadata.instrument_id),
            symbol=metadata.instrument_id.symbol,
            exchange=metadata.instrument_id.exchange.value,
            segment=metadata.instrument_id.segment.value,
            timeframe=metadata.timeframe.value,
            provider_name=provider.name if provider else None,
            provider_type=provider.provider_type.value if provider else None,
            provider_version=provider.version if provider else None,
            quality_status=metadata.quality_status.value,
            row_count=metadata.row_count,
            start_timestamp=metadata.start_timestamp,
            end_timestamp=metadata.end_timestamp,
            source_data_reference=metadata.source_data_reference,
            synthetic=metadata.synthetic,
            fixture_id=metadata.fixture_id,
            dataset_manifest_id=metadata.dataset_manifest_id,
            validation_report_id=metadata.validation_report_id,
            schema_version=metadata.schema_version,
            notes_json=list(metadata.notes),
            created_at=metadata.created_at,
        )

    def to_domain(self) -> MarketDataBatchMetadata:
        provider = None
        if self.provider_name and self.provider_type:
            provider = DataProviderId(
                name=self.provider_name,
                provider_type=DataProviderType(self.provider_type),
                version=self.provider_version,
            )
        return MarketDataBatchMetadata(
            batch_id=self.batch_id,
            instrument_id=InstrumentId(
                symbol=self.symbol,
                exchange=Exchange(self.exchange),
                segment=MarketSegment(self.segment),
            ),
            timeframe=Timeframe(self.timeframe),
            provider=provider,
            quality_status=DataQualityStatus(self.quality_status),
            row_count=self.row_count,
            start_timestamp=self.start_timestamp,
            end_timestamp=self.end_timestamp,
            source_data_reference=self.source_data_reference,
            synthetic=self.synthetic,
            fixture_id=self.fixture_id,
            dataset_manifest_id=self.dataset_manifest_id,
            validation_report_id=self.validation_report_id,
            schema_version=self.schema_version,
            created_at=self.created_at,
            notes=list(self.notes_json or []),
        )

    def update_from_domain(self, metadata: MarketDataBatchMetadata) -> None:
        updated = self.from_domain(metadata)
        for key, value in {
            "instrument_id": updated.instrument_id,
            "symbol": updated.symbol,
            "exchange": updated.exchange,
            "segment": updated.segment,
            "timeframe": updated.timeframe,
            "provider_name": updated.provider_name,
            "provider_type": updated.provider_type,
            "provider_version": updated.provider_version,
            "quality_status": updated.quality_status,
            "row_count": updated.row_count,
            "start_timestamp": updated.start_timestamp,
            "end_timestamp": updated.end_timestamp,
            "source_data_reference": updated.source_data_reference,
            "synthetic": updated.synthetic,
            "fixture_id": updated.fixture_id,
            "dataset_manifest_id": updated.dataset_manifest_id,
            "validation_report_id": updated.validation_report_id,
            "schema_version": updated.schema_version,
            "notes_json": updated.notes_json,
        }.items():
            setattr(self, key, value)
