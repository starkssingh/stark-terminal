from __future__ import annotations

import sys

from stark_terminal_desktop.retail_decision_console import create_retail_decision_console_window


def main() -> int:
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print(
            "PySide6 is not installed. Install the optional desktop dependency with "
            '`python -m pip install -e ".[desktop]"` to run the Stark Terminal shell.'
        )
        return 0

    app = QApplication(sys.argv)
    window = create_retail_decision_console_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
