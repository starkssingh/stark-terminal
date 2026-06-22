from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_data_foundation_audit_docs_exist() -> None:
    for path in [
        "docs/DATA_FOUNDATION_AUDIT.md",
        "docs/DATA_PERSISTENCE_BOUNDARY.md",
        "docs/SYNTHETIC_DATA_SAFETY_AUDIT.md",
        "docs/DATA_FOUNDATION_NEXT_PHASE.md",
    ]:
        assert (ROOT / path).exists(), path


def test_data_foundation_audit_docs_cover_required_scope() -> None:
    combined = "\n".join(
        [
            (ROOT / "docs/DATA_FOUNDATION_AUDIT.md").read_text(encoding="utf-8"),
            (ROOT / "docs/DATA_PERSISTENCE_BOUNDARY.md").read_text(encoding="utf-8"),
            (ROOT / "docs/SYNTHETIC_DATA_SAFETY_AUDIT.md").read_text(encoding="utf-8"),
            (ROOT / "docs/DATA_FOUNDATION_NEXT_PHASE.md").read_text(encoding="utf-8"),
        ]
    )

    for phrase in [
        "Prompts 14-16",
        "synthetic fixtures",
        "instrument metadata persistence",
        "market data batch metadata persistence",
        "data quality gates",
        "no real ingestion",
        "no execution APIs",
        "no full OHLCV production persistence",
        "TimescaleDB Synthetic OHLCV Storage Foundation",
        "Mac mini M2",
        "Windows-native",
    ]:
        assert phrase in combined


def test_data_persistence_boundary_lists_store_ownership() -> None:
    text = (ROOT / "docs/DATA_PERSISTENCE_BOUNDARY.md").read_text(encoding="utf-8")

    for phrase in [
        "PostgreSQL",
        "TimescaleDB",
        "DuckDB/Parquet",
        "ClickHouse",
        "Redis",
        "Redis Streams",
        "Kafka/Redpanda",
        "No store currently receives real market data",
    ]:
        assert phrase in text
