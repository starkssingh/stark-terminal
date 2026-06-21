from __future__ import annotations

from enum import Enum
from typing import Any

from stark_terminal_core.domain.enums import WorkerRole


CANONICAL_WORKER_ROLES: tuple[WorkerRole, ...] = (
    WorkerRole.INGESTION_WORKER,
    WorkerRole.NORMALIZATION_WORKER,
    WorkerRole.FEATURE_WORKER,
    WorkerRole.REGIME_WORKER,
    WorkerRole.OPTIONS_WORKER,
    WorkerRole.RISK_WORKER,
    WorkerRole.DECISION_WORKER,
    WorkerRole.BACKTEST_WORKER,
    WorkerRole.PAPER_LAB_WORKER,
    WorkerRole.AUDIT_WORKER,
    WorkerRole.SYSTEM_HEALTH_WORKER,
    WorkerRole.TEST_WORKER,
)


_ROLE_DESCRIPTIONS = {
    WorkerRole.INGESTION_WORKER: "Future ingestion orchestration placeholder; no provider ingestion yet.",
    WorkerRole.NORMALIZATION_WORKER: "Future normalization orchestration placeholder.",
    WorkerRole.FEATURE_WORKER: "Future feature computation orchestration placeholder.",
    WorkerRole.REGIME_WORKER: "Future regime update orchestration placeholder.",
    WorkerRole.OPTIONS_WORKER: "Future options update orchestration placeholder.",
    WorkerRole.RISK_WORKER: "Future risk update orchestration placeholder.",
    WorkerRole.DECISION_WORKER: "Future decision generation orchestration placeholder.",
    WorkerRole.BACKTEST_WORKER: "Future backtest orchestration placeholder.",
    WorkerRole.PAPER_LAB_WORKER: "Future Paper Lab orchestration placeholder.",
    WorkerRole.AUDIT_WORKER: "Future audit orchestration placeholder.",
    WorkerRole.SYSTEM_HEALTH_WORKER: "Future system health orchestration placeholder.",
    WorkerRole.TEST_WORKER: "Local/test worker role.",
    WorkerRole.UNKNOWN: "Unknown worker role.",
}


_FORBIDDEN_EXECUTION_TERMS = (
    "execution",
    "execute",
    "order",
    "broker",
    "trade",
    "trading",
    "live_trading",
    "live-trading",
    "real_money",
    "real-money",
    "routing",
    "placement",
    "credential",
)


def _role_value(role_or_name: WorkerRole | Enum | str | Any) -> str:
    if isinstance(role_or_name, WorkerRole):
        return role_or_name.value
    if isinstance(role_or_name, Enum):
        return str(role_or_name.value)
    return str(role_or_name)


def role_to_default_queue(role: WorkerRole) -> str:
    normalized = WorkerRole(role)
    return normalized.value.lower()


def role_to_description(role: WorkerRole) -> str:
    normalized = WorkerRole(role)
    return _ROLE_DESCRIPTIONS.get(normalized, _ROLE_DESCRIPTIONS[WorkerRole.UNKNOWN])


def is_execution_forbidden_role(role_or_name: WorkerRole | Enum | str | Any) -> bool:
    normalized = _role_value(role_or_name).lower()
    return any(term in normalized for term in _FORBIDDEN_EXECUTION_TERMS)

