from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "docs/MILESTONE_A_B_AUDIT.md",
    "docs/REPO_INVENTORY.md",
    "docs/API_SURFACE_INVENTORY.md",
    "docs/SAFETY_AUDIT.md",
    "docs/NEXT_PHASE_PLAN.md",
    "docs/KAFKA_REDPANDA_FOUNDATION.md",
    "docs/EVENT_BACKBONE_TOPIC_POLICY.md",
    "docs/DURABLE_EVENT_ENVELOPE_SPEC.md",
    "docs/DATA_QUALITY_FRAMEWORK.md",
    "docs/VALIDATION_RULE_SPEC.md",
    "docs/QUALITY_GATE_POLICY.md",
    "docs/DATA_QUALITY_REPORT_SPEC.md",
    "docs/SYNTHETIC_MARKET_DATA_FIXTURES.md",
    "docs/OHLCV_FIXTURE_CONTRACTS.md",
    "docs/SAMPLE_DATA_POLICY.md",
    "docs/INSTRUMENT_PERSISTENCE_FOUNDATION.md",
    "docs/INSTRUMENT_REPOSITORY_POLICY.md",
    "docs/MARKET_DATA_BATCH_PERSISTENCE.md",
    "docs/BATCH_METADATA_POLICY.md",
    "docs/NORTH_STAR.md",
    "docs/PROMPT_LOG.md",
    "docs/TECH_STACK.md",
    "docs/INFRASTRUCTURE_STACK.md",
    "docs/ANALYTICS_STACK.md",
    "docs/SAFETY_RULES.md",
    "docs/DATA_POLICY.md",
    "docs/CONFIGURATION.md",
]

REQUIRED_PACKAGE_DIRS = [
    "apps/api/stark_terminal_api",
    "apps/api/stark_terminal_api/routes",
    "apps/desktop/stark_terminal_desktop",
    "packages/core/stark_terminal_core",
    "packages/core/stark_terminal_core/config",
    "packages/core/stark_terminal_core/domain",
    "packages/core/stark_terminal_core/serialization",
    "packages/data_platform/stark_terminal_data_platform",
    "packages/data_platform/stark_terminal_data_platform/db",
    "packages/data_platform/stark_terminal_data_platform/timeseries",
    "packages/data_platform/stark_terminal_data_platform/lake",
    "packages/data_platform/stark_terminal_data_platform/cache",
    "packages/data_platform/stark_terminal_data_platform/streams",
    "packages/data_platform/stark_terminal_data_platform/event_backbone",
    "packages/data_platform/stark_terminal_data_platform/quality",
    "packages/data_platform/stark_terminal_data_platform/fixtures",
    "packages/data_platform/stark_terminal_data_platform/repositories",
    "packages/data_platform/stark_terminal_data_platform/services",
    "packages/data_platform/stark_terminal_data_platform/workers",
    "packages/data_platform/stark_terminal_data_platform/instruments",
    "packages/data_platform/stark_terminal_data_platform/providers",
    "packages/data_platform/stark_terminal_data_platform/warehouse",
    "packages/data_platform/stark_terminal_data_platform/features",
    "packages/analytics/stark_terminal_analytics",
    "packages/research/stark_terminal_research",
]

REQUIRED_ROUTE_FILES = [
    "apps/api/stark_terminal_api/routes/health.py",
    "apps/api/stark_terminal_api/routes/config.py",
    "apps/api/stark_terminal_api/routes/database.py",
    "apps/api/stark_terminal_api/routes/timeseries.py",
    "apps/api/stark_terminal_api/routes/research_lake.py",
    "apps/api/stark_terminal_api/routes/cache.py",
    "apps/api/stark_terminal_api/routes/streams.py",
    "apps/api/stark_terminal_api/routes/event_backbone.py",
    "apps/api/stark_terminal_api/routes/data_quality.py",
    "apps/api/stark_terminal_api/routes/fixtures.py",
    "apps/api/stark_terminal_api/routes/instrument_metadata.py",
    "apps/api/stark_terminal_api/routes/market_data_batches.py",
    "apps/api/stark_terminal_api/routes/workers.py",
    "apps/api/stark_terminal_api/routes/instruments.py",
    "apps/api/stark_terminal_api/routes/warehouse.py",
    "apps/api/stark_terminal_api/routes/features.py",
]

FORBIDDEN_ROUTE_TERMS = (
    "execution",
    "execute",
    "order",
    "broker",
    "live_trading",
    "live-trading",
    "real_money",
    "real-money",
)

REQUIRED_SAFETY_PHRASES = [
    "no execution APIs",
    "no real market ingestion",
    "no broker execution",
    "Kafka/Redpanda Event Backbone",
    "durable event backbone",
    "Data Quality",
    "validation framework",
    "synthetic",
    "OHLCV",
    "local-only",
    "test/dev only",
    "no external calls",
    "no real market data",
    "Instrument Metadata Persistence",
    "InstrumentRepository",
    "InstrumentMetadataService",
    "Market Data Batch Persistence",
    "batch metadata",
    "no full OHLCV bars",
    "validation-before-persistence",
    "Feature Registry",
    "Mac mini M2",
    "Windows-native",
]


@dataclass(frozen=True)
class AuditResult:
    name: str
    passed: bool
    detail: str


def _exists(path: str) -> bool:
    return (ROOT / path).exists()


def _docs_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("*.md"))


def _check_required_docs() -> AuditResult:
    missing = [path for path in REQUIRED_DOCS if not _exists(path)]
    return AuditResult("required docs", not missing, ", ".join(missing) if missing else "all required docs present")


def _check_required_dirs() -> AuditResult:
    missing = [path for path in REQUIRED_PACKAGE_DIRS if not (ROOT / path).is_dir()]
    return AuditResult("required package dirs", not missing, ", ".join(missing) if missing else "all required dirs present")


def _check_required_routes() -> AuditResult:
    missing = [path for path in REQUIRED_ROUTE_FILES if not _exists(path)]
    return AuditResult("required API routes", not missing, ", ".join(missing) if missing else "all required route files present")


def _check_forbidden_route_names() -> AuditResult:
    bad: list[str] = []
    for route in (ROOT / "apps/api/stark_terminal_api/routes").glob("*.py"):
        lowered = route.name.lower()
        if any(term in lowered for term in FORBIDDEN_ROUTE_TERMS):
            bad.append(route.name)
    return AuditResult("forbidden route names", not bad, ", ".join(bad) if bad else "no forbidden route file names")


def _check_required_safety_phrases() -> AuditResult:
    docs_text = _docs_text()
    missing = [phrase for phrase in REQUIRED_SAFETY_PHRASES if phrase not in docs_text]
    return AuditResult("safety phrases", not missing, ", ".join(missing) if missing else "required safety phrases present")


def _check_prompt_log() -> AuditResult:
    text = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    expected = [f"Prompt {number:02d}" for number in range(10)] + ["Prompt 10", "Prompt 11", "Prompt 12", "Prompt 13", "Prompt 14", "Prompt 15", "Prompt 16"]
    missing = [entry for entry in expected if entry not in text]
    return AuditResult("prompt log", not missing, ", ".join(missing) if missing else "Prompt 00 through Prompt 16 present")


def _check_north_star_status() -> AuditResult:
    text = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    required = [
        "Current Prompt: 16",
        "Completed Prompts: 16 before this prompt, 17 after completion",
        "Event Backbone Status: Kafka/Redpanda contracts/foundation only, no production pipelines",
        "Data Quality Status: Validation framework/contracts only, no production ingestion pipeline",
        "Fixture Status: Synthetic local-only test/dev fixtures implemented; no real market data",
        "Instrument Persistence Status: Instrument metadata repository/service wiring implemented; no OHLCV persistence",
        "Market Data Batch Persistence Status: Batch metadata repository/service wiring implemented; no full OHLCV bars persisted",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    return AuditResult("north star status", not missing, ", ".join(missing) if missing else "North Star Prompt 16 status present")


def run_audit() -> list[AuditResult]:
    return [
        _check_required_docs(),
        _check_required_dirs(),
        _check_required_routes(),
        _check_forbidden_route_names(),
        _check_required_safety_phrases(),
        _check_prompt_log(),
        _check_north_star_status(),
    ]


def main() -> int:
    print("Stark Terminal Milestone A/B foundation audit")
    results = run_audit()
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}: {result.detail}")
    failures = [result for result in results if not result.passed]
    if failures:
        print(f"Audit failed: {len(failures)} failing checks")
        return 1
    print("Audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
