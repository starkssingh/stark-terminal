from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import FixtureKind
from stark_terminal_data_platform.fixtures.catalog import FixtureCatalog, create_default_synthetic_fixture_catalog
from stark_terminal_data_platform.fixtures.manifests import create_fixture_manifest


def test_default_catalog_contains_expected_sample_instruments() -> None:
    catalog = create_default_synthetic_fixture_catalog(Settings())
    manifests = catalog.list_manifests()
    keys = {manifest.instrument_key for manifest in manifests}

    assert len(manifests) == 5
    assert "NSE:RELIANCE:NSE_EQUITY" in keys
    assert "NSE:HDFCBANK:NSE_EQUITY" in keys
    assert "NSE:TCS:NSE_EQUITY" in keys
    assert "NSE:NIFTY:INDEX" in keys
    assert "NSE:BANKNIFTY:INDEX" in keys


def test_catalog_register_list_get_clear() -> None:
    manifest = create_fixture_manifest("fixture", "Synthetic", FixtureKind.SYNTHETIC_OHLCV)
    catalog = FixtureCatalog()

    catalog.register_manifest(manifest)

    assert catalog.get_manifest("fixture") == manifest
    assert catalog.list_manifests() == [manifest]
    catalog.clear()
    assert catalog.list_manifests() == []


def test_catalog_duplicate_rejected_unless_replace() -> None:
    manifest = create_fixture_manifest("fixture", "Synthetic", FixtureKind.SYNTHETIC_OHLCV)
    catalog = FixtureCatalog([manifest])

    try:
        catalog.register_manifest(manifest)
    except ValueError as exc:
        assert "already registered" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("duplicate fixture should be rejected")

    catalog.register_manifest(manifest, replace=True)
    assert catalog.get_manifest("fixture") == manifest


def test_catalog_creation_does_not_generate_bars() -> None:
    manifest = create_default_synthetic_fixture_catalog(Settings()).list_manifests()[0]

    assert not hasattr(manifest, "bars")
    assert manifest.row_count == 30
