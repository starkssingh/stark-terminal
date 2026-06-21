from stark_terminal_core.config.settings import Settings
from stark_terminal_data_platform.fixtures.health import check_fixture_health


def test_fixture_health_default_ok() -> None:
    status = check_fixture_health()

    assert status.enabled is True
    assert status.sample_generation_ok is True
    assert status.validation_ok is True
    assert status.disk_writes_allowed is False
    assert status.catalog_count == 5
    assert status.status == "healthy"


def test_fixture_health_disabled_status() -> None:
    status = check_fixture_health(Settings(synthetic_fixtures_enabled=False))

    assert status.enabled is False
    assert status.status == "disabled"
