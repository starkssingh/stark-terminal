from __future__ import annotations

import sys


def main() -> int:
    try:
        from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
    except ImportError:
        print(
            "PySide6 is not installed. Install the optional desktop dependency with "
            '`python -m pip install -e ".[desktop]"` to run the Stark Terminal shell.'
        )
        return 0

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Stark Terminal")
    window.setMinimumSize(960, 540)
    window.setCentralWidget(QLabel("Stark Terminal — Institutional Foundation Shell"))
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
