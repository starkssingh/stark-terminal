from __future__ import annotations

import re
from pathlib import Path

from stark_terminal_api.main import app


ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    ROOT / "docs/ACTIVE_DECISION_ARCHITECTURE_TARGET.md",
    ROOT / "docs/DECISION_CANDIDATE_PIPELINE_TARGET.md",
    ROOT / "docs/VERIFIER_LAYER_TARGET_ARCHITECTURE.md",
    ROOT / "docs/HUMAN_REVIEW_PAPER_TRADE_GATE_TARGET.md",
    ROOT / "docs/AUDIT_LOG_JOURNAL_TARGET.md",
]


def test_target_docs_do_not_claim_current_trade_commit_implementation() -> None:
    combined = "\n".join(doc.read_text(encoding="utf-8").lower() for doc in DOCS)

    forbidden_claims = [
        "trade commit is implemented",
        "active decision engine is implemented",
        "execution api is enabled",
        "execution apis are enabled",
        "broker controls are enabled",
        "paper trading is implemented",
        "market-data ingestion is implemented",
        "strategy generation is implemented",
        "backtesting is implemented",
    ]
    for claim in forbidden_claims:
        assert claim not in combined


def test_no_new_order_broker_execution_routes_exist() -> None:
    forbidden_path_parts = [
        "trade-commit",
        "execute",
        "execution",
        "order",
        "broker",
        "paper-trade",
        "recommendation",
    ]

    route_paths = [getattr(route, "path", "") for route in app.routes]
    for path in route_paths:
        normalized = path.lower()
        for part in forbidden_path_parts:
            assert part not in normalized, path


def test_no_active_decision_or_trading_engine_functions_added() -> None:
    forbidden_defs = [
        "trade_commit",
        "commit_trade",
        "execute_trade",
        "place_order",
        "generate_active_decision",
        "generate_recommendation",
        "score_confidence",
        "ingest_market_data",
        "generate_strategy",
        "run_backtest",
        "paper_trade",
    ]
    pattern = re.compile(r"^\s*def\s+(" + "|".join(forbidden_defs) + r")\s*\(", re.MULTILINE)

    for source_root in [ROOT / "apps", ROOT / "packages"]:
        for path in source_root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert pattern.search(text) is None, str(path.relative_to(ROOT))

