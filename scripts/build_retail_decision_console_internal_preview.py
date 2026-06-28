from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from stark_terminal_core.retail_decision_console.internal_preview_package import (
    INTERNAL_PREVIEW_SAFETY_BANNER,
    build_retail_decision_console_internal_preview_package,
)


DEFAULT_OUTPUT_DIR = Path("tmp/retail_decision_console_internal_preview")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=INTERNAL_PREVIEW_SAFETY_BANNER)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Local directory for generated internal preview artifacts.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the selected output directory before writing artifacts.",
    )
    parser.add_argument(
        "--print-manifest",
        action="store_true",
        help="Print the generated manifest JSON after writing the package.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    manifest = build_retail_decision_console_internal_preview_package(args.output_dir, clean=args.clean)
    print(INTERNAL_PREVIEW_SAFETY_BANNER)
    print(f"Output directory: {Path(args.output_dir)}")
    print("Artifacts written:")
    for artifact in manifest.artifacts:
        print(f"- {artifact.path}")
    if args.print_manifest:
        print(manifest.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
