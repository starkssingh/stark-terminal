from __future__ import annotations

from dataclasses import dataclass
from importlib.util import find_spec
import sys
from typing import Any

from stark_terminal_core.retail_decision_console.state_view_model import (
    STATIC_STATE_SAFETY_BANNER,
    RetailDecisionConsoleShellViewModel,
    retail_decision_console_state_view_model,
)
from stark_terminal_core.retail_decision_console.layout import RetailDecisionConsoleLayoutZone
from stark_terminal_core.retail_decision_console.ui_descriptors import (
    SHELL_TITLE,
    RetailDecisionConsoleShellDescriptor,
    retail_decision_console_ui_shell_descriptor,
)
from stark_terminal_core.retail_decision_console.ui_shell import (
    assert_retail_decision_console_ui_shell_is_safe,
)


@dataclass(frozen=True)
class RetailDecisionConsoleDesktopFallback:
    descriptor: RetailDecisionConsoleShellDescriptor
    view_model: RetailDecisionConsoleShellViewModel
    pyside6_available: bool = False
    reason: str = (
        "PySide6 is not installed; Retail Decision Console static/demo view model "
        "is available for tests."
    )


def pyside6_available() -> bool:
    return find_spec("PySide6") is not None


def retail_decision_console_shell_descriptor() -> RetailDecisionConsoleShellDescriptor:
    return retail_decision_console_ui_shell_descriptor()


def retail_decision_console_shell_view_model() -> RetailDecisionConsoleShellViewModel:
    return retail_decision_console_state_view_model()


class RetailDecisionConsoleShell:
    def __init__(
        self,
        descriptor: RetailDecisionConsoleShellDescriptor | None = None,
        view_model: RetailDecisionConsoleShellViewModel | None = None,
    ) -> None:
        self.descriptor = descriptor or retail_decision_console_ui_shell_descriptor()
        self.view_model = view_model or retail_decision_console_state_view_model()
        assert_retail_decision_console_ui_shell_is_safe(self.descriptor)

    def create_window(self) -> Any:
        if not pyside6_available():
            return RetailDecisionConsoleDesktopFallback(descriptor=self.descriptor, view_model=self.view_model)

        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import (
            QApplication,
            QFrame,
            QGridLayout,
            QHBoxLayout,
            QLabel,
            QMainWindow,
            QScrollArea,
            QVBoxLayout,
            QWidget,
        )

        if QApplication.instance() is None:
            return RetailDecisionConsoleDesktopFallback(
                descriptor=self.descriptor,
                view_model=self.view_model,
                pyside6_available=True,
                reason="PySide6 is installed, but no QApplication is running; static/demo view-model fallback returned.",
            )

        window = QMainWindow()
        window.setWindowTitle(SHELL_TITLE)
        window.setMinimumSize(1180, 760)

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title = QLabel(SHELL_TITLE)
        title.setObjectName("retail-decision-console-title")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        layout.addWidget(title)

        banner = QLabel(STATIC_STATE_SAFETY_BANNER)
        banner.setObjectName("retail-decision-console-safety-banner")
        banner.setWordWrap(True)
        banner.setStyleSheet(
            "background: #15171a; color: #f5f7fa; padding: 10px 12px; "
            "border: 1px solid #3b4148; font-weight: 700;"
        )
        layout.addWidget(banner)

        provenance = QLabel(self.view_model.provenance_demo_label)
        provenance.setObjectName("retail-decision-console-provenance-label")
        provenance.setWordWrap(True)
        provenance.setStyleSheet("color: #5f6b77;")
        layout.addWidget(provenance)

        interactions_frame = QFrame()
        interactions_frame.setObjectName("retail-decision-console-static-interactions")
        interactions_frame.setFrameShape(QFrame.StyledPanel)
        interactions_frame.setStyleSheet("QFrame { border: 1px solid #d8dee6; background: #f7f9fb; }")
        interactions_layout = QVBoxLayout(interactions_frame)
        interactions_layout.setContentsMargins(12, 10, 12, 12)
        interactions_layout.setSpacing(6)

        interactions_heading = QLabel("Static interaction placeholders")
        interactions_heading.setObjectName("retail-decision-console-static-interactions-heading")
        interactions_heading.setStyleSheet("font-size: 13px; font-weight: 700; color: #27313c; border: 0;")
        interactions_layout.addWidget(interactions_heading)

        interactions_summary = QLabel(
            "Local-only demo controls: section toggle, static tabs, unavailable reasons, "
            "provenance labels, safety info, and placeholder refresh. No live data, "
            "no recommendations, no confidence score, no order controls, no execution."
        )
        interactions_summary.setWordWrap(True)
        interactions_summary.setStyleSheet("color: #4f5b66; border: 0;")
        interactions_layout.addWidget(interactions_summary)

        for interaction in self.view_model.interactions:
            interaction_label = QLabel(
                f"{interaction.label} -> {interaction.target_section_id} "
                f"({interaction.interaction_type.value}; demo only; unavailable; local only)"
            )
            interaction_label.setWordWrap(True)
            interaction_label.setStyleSheet("color: #344054; border: 0;")
            interactions_layout.addWidget(interaction_label)

        layout.addWidget(interactions_frame)

        zones_host = QWidget()
        zones_layout = QVBoxLayout(zones_host)
        zones_layout.setContentsMargins(0, 0, 0, 0)
        zones_layout.setSpacing(12)

        zone_labels = {
            RetailDecisionConsoleLayoutZone.HEADER: "Top zone",
            RetailDecisionConsoleLayoutZone.CONTROLS: "Control placeholders",
            RetailDecisionConsoleLayoutZone.PRIMARY: "Primary decision shell",
            RetailDecisionConsoleLayoutZone.SECONDARY: "Evidence and risk shell",
            RetailDecisionConsoleLayoutZone.CONTEXT: "Context shell",
            RetailDecisionConsoleLayoutZone.FOOTER: "Journal and settings shell",
        }
        zone_columns = {
            RetailDecisionConsoleLayoutZone.HEADER: 1,
            RetailDecisionConsoleLayoutZone.CONTROLS: 4,
            RetailDecisionConsoleLayoutZone.PRIMARY: 2,
            RetailDecisionConsoleLayoutZone.SECONDARY: 2,
            RetailDecisionConsoleLayoutZone.CONTEXT: 2,
            RetailDecisionConsoleLayoutZone.FOOTER: 2,
        }
        for zone in self.view_model.layout.zones:
            zone_sections = sorted(
                [section for section in self.view_model.sections if section.layout_zone == zone],
                key=lambda section: section.layout_priority,
            )
            if not zone_sections:
                continue

            zone_frame = QFrame()
            zone_frame.setObjectName(f"retail-decision-console-zone-{zone.value.lower()}")
            zone_frame.setFrameShape(QFrame.StyledPanel)
            zone_frame.setStyleSheet("QFrame { border: 1px solid #d4d9df; background: #fbfcfd; }")
            zone_frame_layout = QVBoxLayout(zone_frame)
            zone_frame_layout.setContentsMargins(12, 10, 12, 12)
            zone_frame_layout.setSpacing(8)

            zone_heading = QLabel(zone_labels[zone])
            zone_heading.setObjectName(f"retail-decision-console-zone-heading-{zone.value.lower()}")
            zone_heading.setStyleSheet("font-size: 13px; font-weight: 700; color: #27313c; border: 0;")
            zone_frame_layout.addWidget(zone_heading)

            section_grid_host = QWidget()
            section_grid = QGridLayout(section_grid_host)
            section_grid.setContentsMargins(0, 0, 0, 0)
            section_grid.setSpacing(10)
            columns = zone_columns[zone]

            for index, section in enumerate(zone_sections):
                panel = QFrame()
                panel.setObjectName(f"retail-decision-console-section-{section.section_id}")
                panel.setFrameShape(QFrame.StyledPanel)
                panel.setStyleSheet("QFrame { border: 1px solid #e3e7eb; background: #ffffff; }")
                panel_layout = QVBoxLayout(panel)
                panel_layout.setContentsMargins(10, 8, 10, 10)
                panel_layout.setSpacing(6)

                panel_header = QHBoxLayout()
                panel_title = QLabel(section.title)
                panel_title.setStyleSheet("font-weight: 700; color: #1f2a35; border: 0;")
                panel_badge = QLabel("Demo only")
                panel_badge.setStyleSheet(
                    "color: #344054; background: #eef2f6; padding: 2px 6px; border: 0;"
                )
                panel_header.addWidget(panel_title)
                panel_header.addStretch(1)
                panel_header.addWidget(panel_badge)
                panel_layout.addLayout(panel_header)

                panel_subtitle = QLabel(section.layout_subtitle)
                panel_subtitle.setStyleSheet("color: #667085; border: 0;")
                panel_subtitle.setWordWrap(True)
                panel_layout.addWidget(panel_subtitle)

                panel_body = QLabel(
                    f"{section.placeholder_text}\n{section.unavailable_demo_label}\n"
                    f"{section.layout_safety_label}\n{section.provenance_demo_label}\n"
                    "No live data, no recommendations, no confidence score, no order controls, no execution."
                )
                panel_body.setWordWrap(True)
                panel_body.setStyleSheet("color: #3f4a56; border: 0;")
                panel_layout.addWidget(panel_body)

                for card in section.cards:
                    card_label = QLabel(
                        f"{card.title}: {card.placeholder_text}\n"
                        f"{card.unavailable_demo_label}; {card.provenance_demo_label}"
                    )
                    card_label.setWordWrap(True)
                    card_label.setStyleSheet("color: #4f5b66; border: 0;")
                    panel_layout.addWidget(card_label)

                section_grid.addWidget(panel, index // columns, index % columns)

            zone_frame_layout.addWidget(section_grid_host)
            zones_layout.addWidget(zone_frame)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(zones_host)
        layout.addWidget(scroll)

        window.setCentralWidget(root)
        return window


def create_retail_decision_console_shell() -> RetailDecisionConsoleShell:
    return RetailDecisionConsoleShell()


def create_retail_decision_console_window() -> Any:
    return create_retail_decision_console_shell().create_window()


def main() -> int:
    if not pyside6_available():
        fallback = create_retail_decision_console_window()
        print(fallback.reason)
        return 0

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = create_retail_decision_console_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
