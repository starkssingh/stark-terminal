from __future__ import annotations

from stark_terminal_data_platform.features.definitions import (
    FeatureDefinition,
    contains_forbidden_feature_terms,
    feature_key,
)
from stark_terminal_data_platform.features.feature_sets import FeatureSet, feature_set_key
from stark_terminal_data_platform.features.lineage import FeatureLineageRecord
from stark_terminal_data_platform.features.quality import FeatureQualityReport


class FeatureRegistryError(ValueError):
    """Raised when feature registry operations violate governance contracts."""


class StarkFeatureRegistry:
    """In-memory feature metadata registry for Prompt 10."""

    def __init__(self) -> None:
        self._features: dict[str, FeatureDefinition] = {}
        self._feature_sets: dict[str, FeatureSet] = {}
        self._quality_reports: list[FeatureQualityReport] = []
        self._lineage_records: list[FeatureLineageRecord] = []

    def register_feature(self, feature: FeatureDefinition, replace: bool = False) -> None:
        self._reject_forbidden(feature.name)
        key = feature_key(feature.name, feature.version)
        if key in self._features and not replace:
            raise FeatureRegistryError(f"feature already registered: {key}")
        self._features[key] = feature

    def register_feature_set(self, feature_set: FeatureSet, replace: bool = False) -> None:
        self._reject_forbidden(feature_set.name)
        key = feature_set_key(feature_set.name, feature_set.version)
        if key in self._feature_sets and not replace:
            raise FeatureRegistryError(f"feature set already registered: {key}")
        for feature in feature_set.features:
            self._reject_forbidden(feature.name)
        self._feature_sets[key] = feature_set

    def register_quality_report(self, report: FeatureQualityReport) -> None:
        self._quality_reports.append(report)

    def register_lineage(self, record: FeatureLineageRecord) -> None:
        self._reject_forbidden(record.feature_name)
        self._lineage_records.append(record)

    def get_feature(self, name: str, version: str = "v1") -> FeatureDefinition | None:
        return self._features.get(feature_key(name, version))

    def get_feature_set(self, name: str, version: str = "v1") -> FeatureSet | None:
        return self._feature_sets.get(feature_set_key(name, version))

    def list_features(self) -> list[FeatureDefinition]:
        return list(self._features.values())

    def list_feature_sets(self) -> list[FeatureSet]:
        return list(self._feature_sets.values())

    def list_quality_reports(self) -> list[FeatureQualityReport]:
        return list(self._quality_reports)

    def list_lineage(self) -> list[FeatureLineageRecord]:
        return list(self._lineage_records)

    def clear(self) -> None:
        self._features.clear()
        self._feature_sets.clear()
        self._quality_reports.clear()
        self._lineage_records.clear()

    @staticmethod
    def _reject_forbidden(value: str) -> None:
        if contains_forbidden_feature_terms(value):
            raise FeatureRegistryError("execution, broker, order, and live-trading features are forbidden")

