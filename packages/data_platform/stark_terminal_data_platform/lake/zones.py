from __future__ import annotations

from stark_terminal_core.domain.enums import DataLakeZone


ZONE_DIRECTORY_NAMES: dict[DataLakeZone, str] = {
    DataLakeZone.RAW: "raw",
    DataLakeZone.CLEANED: "cleaned",
    DataLakeZone.NORMALIZED: "normalized",
    DataLakeZone.FEATURE_READY: "feature_ready",
    DataLakeZone.BACKTEST_READY: "backtest_ready",
    DataLakeZone.RESEARCH_ARTIFACTS: "research_artifacts",
}

CANONICAL_LAKE_ZONES: tuple[DataLakeZone, ...] = tuple(ZONE_DIRECTORY_NAMES)


def normalize_zone(zone: DataLakeZone | str) -> DataLakeZone:
    if isinstance(zone, DataLakeZone):
        return zone

    normalized = zone.strip().upper().replace("-", "_")
    for candidate, directory_name in ZONE_DIRECTORY_NAMES.items():
        if normalized in {candidate.name, candidate.value, directory_name.upper()}:
            return candidate
    raise ValueError(f"Unknown data lake zone: {zone}")
