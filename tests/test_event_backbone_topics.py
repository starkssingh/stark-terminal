import pytest

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import TopicNamespace
from stark_terminal_data_platform.event_backbone.topics import (
    TopicNameError,
    build_topic_name,
    list_default_topic_names,
    normalize_topic_namespace,
    validate_topic_part,
)


def test_topic_name_construction_is_deterministic() -> None:
    settings = Settings()

    assert build_topic_name(TopicNamespace.INGESTION, settings=settings) == "stark.development.ingestion"
    assert build_topic_name("features", "daily", settings=settings) == "stark.development.features.daily"


def test_topic_namespace_accepts_enum_and_string() -> None:
    assert normalize_topic_namespace(TopicNamespace.RESEARCH_LAKE) == "research_lake"
    assert normalize_topic_namespace("paper-lab") == "paper_lab"


@pytest.mark.parametrize("part", ["", "   ", "../secret", "..\\secret", "bad\npart", "bad;drop", '"bad"', "http://secret", "bad/part"])
def test_topic_parts_reject_unsafe_values(part: str) -> None:
    with pytest.raises(TopicNameError):
        validate_topic_part(part)


def test_default_topic_names_include_expected_namespaces() -> None:
    topics = list_default_topic_names(Settings())

    assert "stark.development.ingestion" in topics
    assert "stark.development.features" in topics
    assert "stark.development.decisions" in topics
    assert "stark.development.system" in topics
    assert "stark.development.warehouse" in topics

