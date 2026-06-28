from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from stark_terminal_core.retail_decision_console.internal_preview_smoke import (
    INTERNAL_PREVIEW_SMOKE_SAFETY_BANNER,
    smoke_verify_retail_decision_console_internal_preview,
)


DEFAULT_PACKAGE_DIR = Path("tmp/retail_decision_console_internal_preview")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=INTERNAL_PREVIEW_SMOKE_SAFETY_BANNER)
    parser.add_argument(
        "--package-dir",
        type=Path,
        default=DEFAULT_PACKAGE_DIR,
        help="Local internal preview package directory to verify.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the smoke verification result as JSON.",
    )
    parser.add_argument(
        "--print-summary",
        action="store_true",
        help="Print a concise smoke verification summary.",
    )
    return parser


def _summary_lines(package_dir: Path, result) -> list[str]:
    lines = [
        INTERNAL_PREVIEW_SMOKE_SAFETY_BANNER,
        f"Package directory: {package_dir}",
        f"Passed: {str(result.passed).lower()}",
        "Checks:",
    ]
    lines.extend(
        f"- {'PASS' if check.passed else 'FAIL'} {check.check_id}: {check.detail}"
        for check in result.checks
    )
    return lines


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    result = smoke_verify_retail_decision_console_internal_preview(args.package_dir)
    if args.json:
        print(result.model_dump_json(indent=2))
    if args.print_summary or not args.json:
        print("\n".join(_summary_lines(args.package_dir, result)))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
