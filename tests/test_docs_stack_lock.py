from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_docs_lock_institutional_target_stack_keywords() -> None:
    docs_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("*.md"))

    required_keywords = [
        "PostgreSQL",
        "TimescaleDB",
        "DuckDB",
        "Parquet",
        "Redis",
        "Redis Streams",
        "Kafka",
        "Redpanda",
        "ClickHouse",
        "Feast",
        "NumPy",
        "SciPy",
        "Polars",
        "Numba",
        "JAX",
        "CuPy",
        "XGBoost",
        "LightGBM",
        "CatBoost",
        "QuantLib",
        "CVXPY",
        "VaR",
        "Expected Shortfall",
        "Transformers",
        "Sentence Transformers",
    ]

    missing = [keyword for keyword in required_keywords if keyword not in docs_text]

    assert missing == []
