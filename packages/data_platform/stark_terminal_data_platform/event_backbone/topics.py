from __future__ import annotations

import re
from enum import Enum

from stark_terminal_core.config.settings import Settings, get_settings
from stark_terminal_core.domain.enums import TopicNamespace


class TopicNameError(ValueError):
    """Raised when a topic name part is unsafe."""


_CONTROL_CHARACTER_RE = re.compile(r"[\x00-\x1f\x7f]")
_SAFE_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
_UNSAFE_TOPIC_TOKENS = (";", "'", '"', "`", "--", "/*", "*/", "://")
_DEFAULT_TOPIC_NAMESPACES: tuple[TopicNamespace, ...] = (
    TopicNamespace.INGESTION,
    TopicNamespace.NORMALIZATION,
    TopicNamespace.FEATURES,
    TopicNamespace.REGIME,
    TopicNamespace.OPTIONS,
    TopicNamespace.RISK,
    TopicNamespace.DECISIONS,
    TopicNamespace.BACKTESTS,
    TopicNamespace.PAPER_LAB,
    TopicNamespace.AUDIT,
    TopicNamespace.SYSTEM,
    TopicNamespace.WAREHOUSE,
    TopicNamespace.RESEARCH_LAKE,
)


def validate_topic_part(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("topic name parts must be strings")

    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    if not normalized:
        raise TopicNameError("topic name parts cannot be empty")
    if _CONTROL_CHARACTER_RE.search(normalized):
        raise TopicNameError("topic name parts cannot contain control characters")
    if "../" in normalized or "..\\" in normalized:
        raise TopicNameError("topic name parts cannot contain path traversal")
    if "/" in normalized or "\\" in normalized:
        raise TopicNameError("topic name parts cannot contain slashes")
    if any(token in normalized for token in _UNSAFE_TOPIC_TOKENS):
        raise TopicNameError("topic name parts contain unsafe tokens")
    if not _SAFE_SLUG_RE.fullmatch(normalized):
        raise TopicNameError("topic name parts must be safe slug-like strings")
    return normalized


def normalize_topic_namespace(namespace: TopicNamespace | Enum | str) -> str:
    if isinstance(namespace, TopicNamespace):
        value = namespace.value
    elif isinstance(namespace, Enum):
        value = str(namespace.value)
    elif isinstance(namespace, str):
        value = namespace
    else:
        raise TypeError("topic namespace must be an enum or string")
    return validate_topic_part(value)


def build_topic_name(
    namespace: TopicNamespace | Enum | str,
    *parts: str,
    settings: Settings | None = None,
) -> str:
    resolved_settings = settings or get_settings()
    prefix = validate_topic_part(resolved_settings.kafka_topic_prefix)
    environment = validate_topic_part(resolved_settings.kafka_environment_namespace)
    normalized_namespace = normalize_topic_namespace(namespace)
    normalized_parts = [validate_topic_part(part) for part in parts]
    return ".".join([prefix, environment, normalized_namespace, *normalized_parts])


def list_default_topic_names(settings: Settings | None = None) -> list[str]:
    return [
        build_topic_name(namespace, settings=settings)
        for namespace in _DEFAULT_TOPIC_NAMESPACES
    ]


class TopicNameBuilder:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def build(self, namespace: TopicNamespace | Enum | str, *parts: str) -> str:
        return build_topic_name(namespace, *parts, settings=self.settings)

    def defaults(self) -> list[str]:
        return list_default_topic_names(settings=self.settings)

