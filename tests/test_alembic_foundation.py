from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_alembic_foundation_files_exist() -> None:
    assert (ROOT / "alembic.ini").exists()
    assert (ROOT / "alembic/env.py").exists()
    assert (ROOT / "alembic/versions").is_dir()


def test_initial_migration_references_expected_tables() -> None:
    migration = ROOT / "alembic/versions/0001_initial_metadata_tables.py"

    assert migration.exists()
    text = migration.read_text(encoding="utf-8")
    for table_name in [
        "instruments",
        "data_providers",
        "audit_records",
        "decision_object_records",
    ]:
        assert table_name in text
