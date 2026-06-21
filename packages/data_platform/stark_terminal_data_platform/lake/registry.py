from __future__ import annotations

from stark_terminal_data_platform.lake.manifest import DatasetManifest


class DatasetRegistry:
    """In-memory registry placeholder; persistence comes later via PostgreSQL/Feature Registry."""

    def __init__(self) -> None:
        self._manifests: dict[str, DatasetManifest] = {}

    def register(self, manifest: DatasetManifest) -> DatasetManifest:
        self._manifests[manifest.dataset_id] = manifest
        return manifest

    def list_manifests(self) -> list[DatasetManifest]:
        return list(self._manifests.values())

    def get(self, dataset_id: str) -> DatasetManifest | None:
        return self._manifests.get(dataset_id)
