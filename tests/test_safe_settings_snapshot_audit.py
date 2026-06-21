from stark_terminal_core.config.settings import Settings


def test_safe_settings_snapshot_excludes_raw_sensitive_values() -> None:
    settings = Settings(
        database_url="postgresql://user:database-secret@localhost/stark",
        timescale_database_url="postgresql+psycopg://user:timescale-secret@localhost/stark",
        redis_url="redis://:redis-secret@localhost:6379/0",
        clickhouse_url="http://clickhouse-secret@localhost:8123",
        clickhouse_user="clickhouse-user-secret",
        clickhouse_password="clickhouse-password-secret",
        kafka_bootstrap_servers="kafka-secret:9092",
        kafka_sasl_username="kafka-user-secret",
        kafka_sasl_password="kafka-password-secret",
    )

    snapshot = settings.safe_settings_snapshot()
    snapshot_text = repr(snapshot)

    forbidden_keys = {
        "database_url",
        "timescale_database_url",
        "redis_url",
        "clickhouse_url",
        "clickhouse_user",
        "clickhouse_password",
        "kafka_bootstrap_servers",
        "kafka_sasl_username",
        "kafka_sasl_password",
    }
    forbidden_values = {
        "database-secret",
        "timescale-secret",
        "redis-secret",
        "clickhouse-secret",
        "clickhouse-user-secret",
        "clickhouse-password-secret",
        "kafka-secret",
        "kafka-user-secret",
        "kafka-password-secret",
    }

    assert forbidden_keys.isdisjoint(snapshot)
    for value in forbidden_values:
        assert value not in snapshot_text

    assert snapshot["database_configured"] is True
    assert snapshot["timescale_configured"] is True
    assert snapshot["redis_configured"] is True
    assert snapshot["clickhouse_configured"] is True
    assert snapshot["kafka_configured"] is True
    assert snapshot["data_quality_enabled"] is True
    assert snapshot["data_quality_external_validation_enabled"] is False
    assert snapshot["execution_apis_enabled"] is False
    assert snapshot["broker_integrations_enabled"] is False
    assert snapshot["live_trading_enabled"] is False
