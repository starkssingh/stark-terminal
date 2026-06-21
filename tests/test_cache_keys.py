import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import CacheNamespace
from stark_terminal_data_platform.cache.keys import build_cache_key, normalize_namespace


def test_cache_key_construction_is_deterministic() -> None:
    settings = Settings(cache_key_prefix="stark", cache_environment_namespace="development")

    assert build_cache_key("health", "api", settings=settings) == "stark:development:health:api"
    assert build_cache_key("health", "api", settings=settings) == "stark:development:health:api"


def test_cache_key_accepts_enum_namespace() -> None:
    settings = Settings()

    key = build_cache_key(CacheNamespace.DECISION_OBJECT, "NSE", "RELIANCE", "DAILY", settings=settings)

    assert key == "stark:development:decision_object:NSE:RELIANCE:DAILY"
    assert normalize_namespace(CacheNamespace.RESEARCH_LAKE) == "research_lake"


@pytest.mark.parametrize("part", ["", "   "])
def test_cache_key_rejects_empty_parts(part: str) -> None:
    with pytest.raises(ValueError):
        build_cache_key(CacheNamespace.HEALTH, part, settings=Settings())


@pytest.mark.parametrize("part", ["../secret", "..\\secret"])
def test_cache_key_rejects_path_traversal(part: str) -> None:
    with pytest.raises(ValueError):
        build_cache_key(CacheNamespace.HEALTH, part, settings=Settings())


def test_cache_key_rejects_control_characters() -> None:
    with pytest.raises(ValueError):
        build_cache_key(CacheNamespace.HEALTH, "bad\nkey", settings=Settings())


def test_cache_key_rejects_url_like_values() -> None:
    with pytest.raises(ValueError):
        build_cache_key(CacheNamespace.HEALTH, "redis://localhost:6379", settings=Settings())

