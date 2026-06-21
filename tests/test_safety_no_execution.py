from pathlib import Path

from stark_terminal_core.config.settings import Settings
from stark_terminal_core.domain.enums import WorkerRole
from stark_terminal_data_platform.workers.roles import is_execution_forbidden_role


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_FILE_TERMS = (
    "execution",
    "execute",
    "order",
    "broker",
    "live_trading",
    "live-trading",
    "real_money",
    "real-money",
)


def test_no_route_file_name_implies_execution_or_broker_behavior() -> None:
    route_dir = ROOT / "apps/api/stark_terminal_api/routes"

    for path in route_dir.glob("*.py"):
        lowered = path.name.lower()
        assert not any(term in lowered for term in FORBIDDEN_FILE_TERMS)


def test_canonical_worker_roles_do_not_represent_execution() -> None:
    for role in WorkerRole:
        if role is WorkerRole.UNKNOWN:
            continue
        assert not is_execution_forbidden_role(role)


def test_execution_flags_default_false() -> None:
    settings = Settings()

    assert settings.execution_apis_enabled is False
    assert settings.broker_integrations_enabled is False
    assert settings.live_trading_enabled is False


def test_safety_docs_forbid_execution_apis() -> None:
    safety_docs = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ["docs/SAFETY_RULES.md", "docs/SAFETY_AUDIT.md"]
    )

    assert "no execution APIs" in safety_docs
    assert "No broker execution" in safety_docs or "no broker execution" in safety_docs
    assert "future milestone audits must search" in safety_docs.lower()
