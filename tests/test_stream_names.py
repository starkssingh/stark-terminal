import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import StreamNamespace
from stark_terminal_data_platform.streams.names import build_stream_name, normalize_stream_namespace


def test_stream_name_construction_is_deterministic() -> None:
    settings = Settings()

    assert build_stream_name("ingestion", settings=settings) == "stark:development:ingestion"
    assert build_stream_name("ingestion", settings=settings) == "stark:development:ingestion"


def test_stream_name_accepts_enum_namespace_and_parts() -> None:
    settings = Settings()

    assert build_stream_name(StreamNamespace.FEATURES, settings=settings) == "stark:development:features"
    assert build_stream_name(StreamNamespace.DECISIONS, "latest", settings=settings) == (
        "stark:development:decisions:latest"
    )
    assert normalize_stream_namespace(StreamNamespace.PAPER_LAB) == "paper_lab"


@pytest.mark.parametrize("part", ["", "   "])
def test_stream_name_rejects_empty_parts(part: str) -> None:
    with pytest.raises(ValueError):
        build_stream_name(StreamNamespace.SYSTEM, part, settings=Settings())


@pytest.mark.parametrize("part", ["../secret", "..\\secret"])
def test_stream_name_rejects_path_traversal(part: str) -> None:
    with pytest.raises(ValueError):
        build_stream_name(StreamNamespace.SYSTEM, part, settings=Settings())


def test_stream_name_rejects_control_characters() -> None:
    with pytest.raises(ValueError):
        build_stream_name(StreamNamespace.SYSTEM, "bad\nkey", settings=Settings())


def test_stream_name_rejects_url_like_values() -> None:
    with pytest.raises(ValueError):
        build_stream_name(StreamNamespace.SYSTEM, "redis://localhost:6379", settings=Settings())

