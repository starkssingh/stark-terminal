from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter

from stark_terminal_core.config.settings import get_settings
from stark_terminal_core.domain.enums import Timeframe
from stark_terminal_core.serialization.json import to_jsonable
from stark_terminal_data_platform.exports.synthetic_ohlcv import (
    SyntheticOHLCVResearchLakeExportService,
    build_synthetic_ohlcv_dataset_name,
    create_synthetic_ohlcv_export_request,
)
from stark_terminal_data_platform.instruments.fixtures import create_sample_instruments

router = APIRouter()


@router.get("/synthetic-ohlcv-exports/health")
def synthetic_ohlcv_exports_health() -> dict[str, Any]:
    status = SyntheticOHLCVResearchLakeExportService().health()
    return {
        "service": "stark-terminal-synthetic-ohlcv-exports",
        **status.model_dump(),
    }


@router.get("/synthetic-ohlcv-exports/contracts")
def synthetic_ohlcv_exports_contracts() -> dict[str, Any]:
    settings = get_settings()
    return {
        "service": "stark-terminal-synthetic-ohlcv-exports",
        "schema_version": settings.synthetic_ohlcv_export_schema_version,
        "synthetic_only": True,
        "real_market_data_allowed": False,
        "export_scope": "stored synthetic OHLCV bars to Parquet research artifacts with DatasetManifest linkage",
        "manifest_required": True,
        "validation_required": settings.synthetic_ohlcv_export_require_validation,
        "writes_files": False,
        "external_calls": False,
        "trading_signals": False,
    }


@router.get("/synthetic-ohlcv-exports/sample")
def synthetic_ohlcv_exports_sample() -> dict[str, Any]:
    settings = get_settings()
    instrument = create_sample_instruments()[0]
    request = create_synthetic_ohlcv_export_request(
        export_id="synthetic_ohlcv_export_sample",
        instrument_id=instrument.instrument_id,
        timeframe=Timeframe.DAILY,
        dataset_name=build_synthetic_ohlcv_dataset_name(instrument.instrument_id, Timeframe.DAILY),
        source_data_reference="synthetic-local-test-only",
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 1, 3, tzinfo=timezone.utc),
        schema_version=settings.synthetic_ohlcv_export_schema_version,
    )
    return {
        "service": "stark-terminal-synthetic-ohlcv-exports",
        "synthetic_only": True,
        "real_market_data_allowed": False,
        "writes_files": False,
        "returns_bars": False,
        "sample_request": to_jsonable(request),
        "note": "metadata-only synthetic export sample; no files are written and no live market data is returned",
    }
