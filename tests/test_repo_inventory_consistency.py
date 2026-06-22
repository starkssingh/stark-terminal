import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_foundation import run_audit

MAJOR_DATA_PLATFORM_SUBPACKAGES = [
    "db",
    "timeseries",
    "lake",
    "cache",
    "streams",
    "event_backbone",
    "quality",
    "fixtures",
    "repositories",
    "services",
    "exports",
    "workers",
    "instruments",
    "providers",
    "warehouse",
    "features",
]


def test_project_map_and_repo_inventory_mention_major_packages() -> None:
    project_map = (ROOT / "PROJECT_MAP.md").read_text(encoding="utf-8")
    repo_inventory = (ROOT / "docs/REPO_INVENTORY.md").read_text(encoding="utf-8")

    for package in ["apps/api", "apps/desktop", "packages/core", "packages/data_platform"]:
        assert package in project_map

    for subpackage in MAJOR_DATA_PLATFORM_SUBPACKAGES:
        assert subpackage in project_map
        assert subpackage in repo_inventory
        assert (ROOT / f"packages/data_platform/stark_terminal_data_platform/{subpackage}").is_dir()


def test_audit_and_verifier_scripts_exist() -> None:
    assert (ROOT / "scripts/audit_foundation.py").exists()
    assert (ROOT / "scripts/verify_foundation.py").exists()


def test_audit_foundation_importable_checks_pass() -> None:
    failures = [result for result in run_audit() if not result.passed]

    assert failures == []


def test_audit_foundation_script_runs_successfully() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/audit_foundation.py"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Audit passed." in result.stdout
