from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_key_prompt_00_docs_exist() -> None:
    required_docs = [
        "README.md",
        "AGENTS.md",
        "PROJECT_MAP.md",
        "docs/NORTH_STAR.md",
        "docs/ARCHITECTURE.md",
        "docs/TECH_STACK.md",
        "docs/INFRASTRUCTURE_STACK.md",
        "docs/ANALYTICS_STACK.md",
        "docs/SAFETY_RULES.md",
        "docs/DOMAIN_MODEL.md",
        "docs/CONFIGURATION.md",
        "docs/DATABASE_FOUNDATION.md",
        "docs/TIMESCALEDB_FOUNDATION.md",
        "docs/TIMESERIES_SCHEMA.md",
        "docs/RESEARCH_LAKE_FOUNDATION.md",
        "docs/PARQUET_DATA_ZONES.md",
        "docs/DUCKDB_FOUNDATION.md",
        "docs/REDIS_CACHE_FOUNDATION.md",
        "docs/CACHE_KEY_POLICY.md",
        "docs/REDIS_STREAMS_FOUNDATION.md",
        "docs/EVENT_PIPELINE_POLICY.md",
        "docs/EVENT_ENVELOPE_SPEC.md",
        "docs/WORKER_SYSTEM_FOUNDATION.md",
        "docs/WORKER_ROLE_POLICY.md",
        "docs/JOB_ENVELOPE_SPEC.md",
        "docs/INSTRUMENT_MASTER_FOUNDATION.md",
        "docs/MARKET_DATA_PROVIDER_CONTRACTS.md",
        "docs/SYMBOL_NORMALIZATION_POLICY.md",
        "docs/CLICKHOUSE_WAREHOUSE_FOUNDATION.md",
        "docs/ANALYTICAL_TABLE_CONTRACTS.md",
        "docs/WAREHOUSE_QUERY_POLICY.md",
        "docs/FEATURE_REGISTRY_FOUNDATION.md",
        "docs/FEATURE_DEFINITION_SPEC.md",
        "docs/FEATURE_QUALITY_POLICY.md",
        "docs/TRAINING_SERVING_CONSISTENCY_POLICY.md",
        "docs/KAFKA_REDPANDA_FOUNDATION.md",
        "docs/EVENT_BACKBONE_TOPIC_POLICY.md",
        "docs/DURABLE_EVENT_ENVELOPE_SPEC.md",
        "docs/DATA_QUALITY_FRAMEWORK.md",
        "docs/VALIDATION_RULE_SPEC.md",
        "docs/QUALITY_GATE_POLICY.md",
        "docs/DATA_QUALITY_REPORT_SPEC.md",
        "docs/DECISION_OBJECT_SPEC.md",
        "docs/PROMPT_LOG.md",
    ]

    missing = [path for path in required_docs if not (ROOT / path).exists()]

    assert missing == []


def test_prompt_10_docs_reflect_current_status() -> None:
    prompt_log = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    north_star = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")

    assert "Prompt 10 - Feature Store / Stark Feature Registry Foundation" in prompt_log
    assert "Current Prompt: 13" in north_star
    assert "Completed Prompts: 13 before this prompt, 14 after completion" in north_star
    assert "Feature Registry foundation" in project_map
    assert "Kafka/Redpanda Event Backbone foundation" in project_map
    assert "Data Quality + Validation Framework" in project_map
