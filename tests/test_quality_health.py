from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.quality.health import check_data_quality_health
from stark_terminal_data_platform.quality.registry import create_default_validation_registry


def test_default_data_quality_health_does_not_crash() -> None:
    status = check_data_quality_health()

    assert status.enabled is True
    assert status.status == "healthy"
    assert status.validator_count == 10
    assert "MARKET_DATA_BAR" in status.registered_scopes


def test_health_with_registry_reports_counts() -> None:
    registry = create_default_validation_registry()

    status = check_data_quality_health(registry=registry)

    assert status.validator_count == 10
    assert status.error is None


def test_external_validation_enabled_reports_caution_without_external_calls() -> None:
    status = check_data_quality_health(
        settings=Settings(data_quality_external_validation_enabled=True)
    )

    assert status.external_validation_enabled is True
    assert status.status == "caution_external_validation_enabled"


def test_data_quality_health_model_does_not_expose_secrets() -> None:
    status = check_data_quality_health(
        settings=Settings(database_url="postgresql://secret", kafka_bootstrap_servers="secret:9092")
    )

    payload = status.model_dump()

    assert "database_url" not in payload
    assert "kafka_bootstrap_servers" not in payload
