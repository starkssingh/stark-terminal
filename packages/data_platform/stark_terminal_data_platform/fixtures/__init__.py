"""Synthetic local-only fixture contracts for Stark Terminal tests/dev."""

from stark_terminal_data_platform.fixtures.catalog import FixtureCatalog, create_default_synthetic_fixture_catalog
from stark_terminal_data_platform.fixtures.health import FixtureHealthStatus, check_fixture_health
from stark_terminal_data_platform.fixtures.manifests import FixtureManifest, create_fixture_manifest
from stark_terminal_data_platform.fixtures.synthetic_ohlcv import (
    SyntheticOHLCVConfig,
    generate_synthetic_market_data_batch,
    generate_synthetic_ohlcv_bars,
)

__all__ = [
    "FixtureCatalog",
    "FixtureHealthStatus",
    "FixtureManifest",
    "SyntheticOHLCVConfig",
    "check_fixture_health",
    "create_default_synthetic_fixture_catalog",
    "create_fixture_manifest",
    "generate_synthetic_market_data_batch",
    "generate_synthetic_ohlcv_bars",
]
