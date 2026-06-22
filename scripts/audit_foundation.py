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
    "docs/DATA_FOUNDATION_AUDIT.md",
    "docs/DATA_PERSISTENCE_BOUNDARY.md",
    "docs/SYNTHETIC_DATA_SAFETY_AUDIT.md",
    "docs/DATA_FOUNDATION_NEXT_PHASE.md",
    "docs/SYNTHETIC_OHLCV_STORAGE_FOUNDATION.md",
    "docs/TIMESCALE_SYNTHETIC_STORAGE_POLICY.md",
    "docs/SYNTHETIC_OHLCV_RESEARCH_LAKE_EXPORT.md",
    "docs/OHLCV_EXPORT_MANIFEST_POLICY.md",
    "docs/PROVIDER_ADAPTER_IMPLEMENTATION_PLAN.md",
    "docs/PROVIDER_GUARDRAIL_POLICY.md",
    "docs/PROVIDER_APPROVAL_WORKFLOW.md",
    "docs/PROVIDER_COMPLIANCE_CHECKLIST.md",
    "docs/LOCAL_SAMPLE_PROVIDER_ADAPTER.md",
    "docs/LOCAL_SAMPLE_PROVIDER_POLICY.md",
    "docs/DATA_FOUNDATION_MILESTONE_AUDIT.md",
    "docs/SYNTHETIC_STORAGE_EXPORT_AUDIT.md",
    "docs/PROVIDER_GUARDRAIL_AUDIT.md",
    "docs/LOCAL_SAMPLE_PROVIDER_AUDIT.md",
    "docs/DATA_FOUNDATION_MILESTONE_NEXT_PHASE.md",
    "docs/REAL_PROVIDER_READINESS_CHECKLIST.md",
    "docs/PROVIDER_CANDIDATE_SELECTION_POLICY.md",
    "docs/PROVIDER_RISK_SCORING_POLICY.md",
    "docs/PROVIDER_CAPABILITY_GAP_ANALYSIS.md",
    "docs/LOCAL_FILE_PROVIDER_ADAPTER.md",
    "docs/LOCAL_FILE_PROVIDER_POLICY.md",
    "docs/LOCAL_FILE_PATH_SAFETY.md",
    "docs/PROVIDER_ADAPTER_MILESTONE_AUDIT.md",
    "docs/PROVIDER_BOUNDARY_AUDIT.md",
    "docs/PROVIDER_NO_EXTERNAL_CALLS_AUDIT.md",
    "docs/PROVIDER_NEXT_PHASE_PLAN.md",
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
    "packages/data_platform/stark_terminal_data_platform/exports",
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
    "apps/api/stark_terminal_api/routes/synthetic_ohlcv_storage.py",
    "apps/api/stark_terminal_api/routes/synthetic_ohlcv_exports.py",
    "apps/api/stark_terminal_api/routes/provider_guardrails.py",
    "apps/api/stark_terminal_api/routes/provider_readiness.py",
    "apps/api/stark_terminal_api/routes/local_sample_provider.py",
    "apps/api/stark_terminal_api/routes/local_file_provider.py",
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

FORBIDDEN_DATA_FILE_TERMS = (
    "execution",
    "execute",
    "order",
    "broker",
    "scrape",
    "scraper",
    "real_ingestion",
    "live_provider",
    "live_data",
)

REQUIRED_DATA_FOUNDATION_FILES = [
    "packages/data_platform/stark_terminal_data_platform/fixtures/manifests.py",
    "packages/data_platform/stark_terminal_data_platform/fixtures/synthetic_ohlcv.py",
    "packages/data_platform/stark_terminal_data_platform/fixtures/catalog.py",
    "packages/data_platform/stark_terminal_data_platform/fixtures/validation.py",
    "packages/data_platform/stark_terminal_data_platform/fixtures/parquet.py",
    "packages/data_platform/stark_terminal_data_platform/repositories/instruments.py",
    "packages/data_platform/stark_terminal_data_platform/services/instruments.py",
    "packages/core/stark_terminal_core/domain/market_data_batch.py",
    "packages/data_platform/stark_terminal_data_platform/db/models/market_data_batch.py",
    "packages/data_platform/stark_terminal_data_platform/repositories/market_data_batches.py",
    "packages/data_platform/stark_terminal_data_platform/services/market_data_batches.py",
    "packages/data_platform/stark_terminal_data_platform/repositories/ohlcv_bars.py",
    "packages/data_platform/stark_terminal_data_platform/services/synthetic_ohlcv_storage.py",
    "packages/data_platform/stark_terminal_data_platform/exports/synthetic_ohlcv.py",
    "packages/data_platform/stark_terminal_data_platform/exports/README.md",
    "packages/data_platform/stark_terminal_data_platform/providers/guardrails.py",
    "packages/data_platform/stark_terminal_data_platform/providers/approval.py",
    "packages/data_platform/stark_terminal_data_platform/providers/readiness.py",
    "packages/data_platform/stark_terminal_data_platform/providers/local_sample.py",
    "packages/data_platform/stark_terminal_data_platform/providers/candidates.py",
    "packages/data_platform/stark_terminal_data_platform/providers/selection.py",
    "packages/data_platform/stark_terminal_data_platform/providers/local_file.py",
    "docs/PROVIDER_ADAPTER_MILESTONE_AUDIT.md",
    "docs/PROVIDER_BOUNDARY_AUDIT.md",
    "docs/PROVIDER_NO_EXTERNAL_CALLS_AUDIT.md",
    "docs/PROVIDER_NEXT_PHASE_PLAN.md",
    "apps/api/stark_terminal_api/routes/synthetic_ohlcv_storage.py",
    "apps/api/stark_terminal_api/routes/synthetic_ohlcv_exports.py",
    "apps/api/stark_terminal_api/routes/provider_guardrails.py",
    "apps/api/stark_terminal_api/routes/provider_readiness.py",
    "apps/api/stark_terminal_api/routes/fixtures.py",
    "apps/api/stark_terminal_api/routes/instrument_metadata.py",
    "apps/api/stark_terminal_api/routes/market_data_batches.py",
    "alembic/versions/0003_market_data_batch_metadata.py",
]

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
    "Data Foundation Audit",
    "Data Persistence Boundary",
    "Synthetic Data Safety Audit",
    "TimescaleDB Synthetic OHLCV Storage Foundation",
    "Synthetic OHLCV Storage",
    "Timescale Synthetic Storage Policy",
    "validation-before-storage",
    "Synthetic OHLCV Research Lake Export",
    "DatasetManifest",
    "Parquet",
    "DuckDB",
    "validation-before-export",
    "no production research lake writes by default",
    "Provider Adapter",
    "Provider Adapter Guardrails",
    "Local Sample Provider",
    "Data Foundation Milestone Audit",
    "Synthetic Storage Export Audit",
    "Provider Guardrail Audit",
    "Local Sample Provider Audit",
    "Data Foundation Milestone Next Phase",
    "no analytics/signals/decisions",
    "Guardrail",
    "approval workflow",
    "compliance checklist",
    "no credentials",
    "no provider SDKs",
    "LOCAL_SAMPLE",
    "no real provider implementation",
    "no trading signals",
    "Real Provider Readiness",
    "Candidate Selection",
    "risk scoring",
    "capability gap",
    "no SDKs",
    "no production approval",
    "Local File Provider",
    "local-file-only",
    "path safety",
    "no arbitrary file read API",
    "Provider Adapter Milestone Audit",
    "Provider Boundary Audit",
    "Provider No External Calls Audit",
    "Provider Next Phase Plan",
    "batch metadata",
    "no full OHLCV bars",
    "no full OHLCV production persistence",
    "validation-before-persistence",
    "Feature Registry",
    "Mac mini M2",
    "Windows-native",
]

PROVIDER_EXTERNAL_IMPORT_PHRASES = (
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "import aiohttp",
    "from aiohttp",
    "import urllib.request",
    "from urllib.request",
    "import socket",
)

FORBIDDEN_PROVIDER_DEPENDENCIES = (
    "kiteconnect",
    "upstox",
    "nsepython",
    "nsepy",
    "yfinance",
    "beautifulsoup",
    "bs4",
    "selenium",
    "scrapy",
    "alpaca-trade-api",
    "ib_insync",
    "ccxt",
)


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


def _check_required_data_foundation_files() -> AuditResult:
    missing = [path for path in REQUIRED_DATA_FOUNDATION_FILES if not _exists(path)]
    detail = ", ".join(missing) if missing else "Prompt 14-25 data foundation/provider readiness artifacts present"
    return AuditResult("data foundation files", not missing, detail)


def _check_forbidden_data_file_names() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "apps/api/stark_terminal_api/routes",
        ROOT / "packages/core/stark_terminal_core/domain",
        ROOT / "packages/data_platform/stark_terminal_data_platform",
    ]
    for root in roots:
        for path in root.rglob("*.py"):
            lowered = path.name.lower()
            if any(term in lowered for term in FORBIDDEN_DATA_FILE_TERMS):
                bad.append(str(path.relative_to(ROOT)))
    detail = ", ".join(bad) if bad else "no forbidden data foundation file names"
    return AuditResult("forbidden data file names", not bad, detail)


def _check_required_safety_phrases() -> AuditResult:
    docs_text = _docs_text()
    missing = [phrase for phrase in REQUIRED_SAFETY_PHRASES if phrase not in docs_text]
    return AuditResult("safety phrases", not missing, ", ".join(missing) if missing else "required safety phrases present")


def _check_provider_modules_no_external_imports() -> AuditResult:
    bad: list[str] = []
    roots = [
        ROOT / "packages/data_platform/stark_terminal_data_platform/providers",
        ROOT / "apps/api/stark_terminal_api/routes",
    ]
    provider_route_names = {
        "provider_guardrails.py",
        "provider_readiness.py",
        "local_sample_provider.py",
        "local_file_provider.py",
    }
    for root in roots:
        for path in root.glob("*.py"):
            if root.name == "routes" and path.name not in provider_route_names:
                continue
            text = path.read_text(encoding="utf-8")
            for phrase in PROVIDER_EXTERNAL_IMPORT_PHRASES:
                if phrase in text:
                    bad.append(f"{path.relative_to(ROOT)}:{phrase}")
    detail = ", ".join(bad) if bad else "provider modules import no external-call clients"
    return AuditResult("provider external imports", not bad, detail)


def _check_provider_dependency_boundaries() -> AuditResult:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8").lower()
    bad = [dependency for dependency in FORBIDDEN_PROVIDER_DEPENDENCIES if dependency in text]
    detail = ", ".join(bad) if bad else "no provider SDK, scraping, or broker/trading dependencies"
    return AuditResult("provider dependencies", not bad, detail)


def _check_prompt_log() -> AuditResult:
    text = (ROOT / "docs/PROMPT_LOG.md").read_text(encoding="utf-8")
    expected = [
        f"Prompt {number:02d}" for number in range(10)
    ] + [
        "Prompt 10",
        "Prompt 11",
        "Prompt 12",
        "Prompt 13",
        "Prompt 14",
        "Prompt 15",
        "Prompt 16",
        "Prompt 17",
        "Prompt 18",
        "Prompt 19",
        "Prompt 20",
        "Prompt 21",
        "Prompt 22",
        "Prompt 23",
        "Prompt 24",
        "Prompt 25",
    ]
    missing = [entry for entry in expected if entry not in text]
    return AuditResult("prompt log", not missing, ", ".join(missing) if missing else "Prompt 00 through Prompt 25 present")


def _check_north_star_status() -> AuditResult:
    text = (ROOT / "docs/NORTH_STAR.md").read_text(encoding="utf-8")
    required = [
        "Current Prompt: 25",
        "Completed Prompts: 25 before this prompt, 26 after completion",
        "Event Backbone Status: Kafka/Redpanda contracts/foundation only, no production pipelines",
        "Data Quality Status: Validation framework active for synthetic/local provider boundaries",
        "Fixture Status: Synthetic local-only test/dev fixtures implemented and audited",
        "Synthetic OHLCV Storage Status: Synthetic-only repository/service wiring implemented; no real market data",
        "Synthetic OHLCV Export Status: Synthetic-only Parquet export contract with DatasetManifest linkage implemented; no real market data",
        "Provider Status: Guardrails, readiness/candidate selection, local sample provider, and local file provider implemented and audited; no real provider implementation; no external calls",
        "Audit Verdict: Provider foundation ready for next analytics-planning phase if tests pass",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    return AuditResult("north star status", not missing, ", ".join(missing) if missing else "North Star Prompt 25 status present")


def run_audit() -> list[AuditResult]:
    return [
        _check_required_docs(),
        _check_required_dirs(),
        _check_required_routes(),
        _check_forbidden_route_names(),
        _check_required_data_foundation_files(),
        _check_forbidden_data_file_names(),
        _check_required_safety_phrases(),
        _check_provider_modules_no_external_imports(),
        _check_provider_dependency_boundaries(),
        _check_prompt_log(),
        _check_north_star_status(),
    ]


def main() -> int:
    print("Stark Terminal foundation and data foundation audit")
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
