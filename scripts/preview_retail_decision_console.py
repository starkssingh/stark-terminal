from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from stark_terminal_desktop.retail_decision_console import (
    RetailDecisionConsoleDesktopFallback,
    create_retail_decision_console_window,
    pyside6_available,
    retail_decision_console_shell_view_model,
)
from stark_terminal_core.retail_decision_console.snapshot_export import (
    RetailDecisionConsoleSnapshotFormat,
    retail_decision_console_preview_snapshot,
    retail_decision_console_snapshot_to_dict,
    retail_decision_console_snapshot_to_markdown,
    retail_decision_console_snapshot_to_text,
    write_retail_decision_console_snapshot,
)


SAFETY_BANNER = "Demo/static preview only — no live data, no recommendations, no execution"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=SAFETY_BANNER)
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Print the safe descriptor summary and do not open a desktop window.",
    )
    parser.add_argument(
        "--print-snapshot",
        action="store_true",
        help="Print the safe local preview snapshot and do not open a desktop window.",
    )
    parser.add_argument(
        "--export-snapshot",
        type=Path,
        help="Write the safe local preview snapshot to PATH.",
    )
    parser.add_argument(
        "--snapshot-format",
        choices=[snapshot_format.value for snapshot_format in RetailDecisionConsoleSnapshotFormat],
        default=RetailDecisionConsoleSnapshotFormat.JSON.value,
        help="Snapshot output format.",
    )
    return parser


def _print_preview_summary() -> None:
    view_model = retail_decision_console_shell_view_model()
    print(SAFETY_BANNER)
    print(f"Title: {view_model.title}")
    print(f"Stage: {view_model.stage}")
    print(f"Layout stage: {view_model.layout.stage}")
    print("State: demo-only, unavailable, read-only")
    print(f"Static interactions: {len(view_model.interactions)}")
    for interaction in view_model.interactions:
        print(
            f"- [{interaction.interaction_type.value}] {interaction.label}: "
            f"{interaction.target_section_id}; demo-only unavailable local-only"
        )
    print("Layout zones:")
    for zone in view_model.layout.zones:
        zone_sections = [section for section in view_model.sections if section.layout_zone == zone]
        if zone_sections:
            print(f"- {zone.value}: {len(zone_sections)} sections")
    print(f"Sections: {len(view_model.sections)}")
    zone_order = {zone: index for index, zone in enumerate(view_model.layout.zones)}
    for section in sorted(view_model.sections, key=lambda item: (zone_order[item.layout_zone], item.layout_priority)):
        print(f"- [{section.layout_zone.value}] {section.title}: {section.unavailable_demo_label}")


def _print_snapshot(snapshot_format: str) -> None:
    snapshot = retail_decision_console_preview_snapshot()
    current_format = RetailDecisionConsoleSnapshotFormat(snapshot_format)
    if current_format is RetailDecisionConsoleSnapshotFormat.JSON:
        print(json.dumps(retail_decision_console_snapshot_to_dict(snapshot), indent=2, sort_keys=True))
        return
    if current_format is RetailDecisionConsoleSnapshotFormat.MARKDOWN:
        print(retail_decision_console_snapshot_to_markdown(snapshot), end="")
        return
    print(retail_decision_console_snapshot_to_text(snapshot), end="")


def _launch_gui() -> int:
    if not pyside6_available():
        print("PySide6 is not installed; descriptor/view-model fallback only.")
        return 0

    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    owns_app = app is None
    if app is None:
        app = QApplication([Path(__file__).name])

    window = create_retail_decision_console_window()
    if isinstance(window, RetailDecisionConsoleDesktopFallback):
        print(window.reason)
        return 0

    window.show()
    if owns_app:
        return int(app.exec())
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    _print_preview_summary()
    if args.print_snapshot:
        _print_snapshot(args.snapshot_format)
    if args.export_snapshot:
        output_path = write_retail_decision_console_snapshot(
            args.export_snapshot,
            snapshot_format=args.snapshot_format,
        )
        print(f"Snapshot written: {output_path}")
        print(SAFETY_BANNER)
    if args.no_gui or args.print_snapshot or args.export_snapshot:
        return 0
    return _launch_gui()


if __name__ == "__main__":
    raise SystemExit(main())
