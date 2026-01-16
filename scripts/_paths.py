from __future__ import annotations

from pathlib import Path

# Repository root: .../creatio-report-fix
ROOT = Path(__file__).resolve().parents[1]

DOCS_DIR = ROOT / "docs"
SOURCE_CODE_DIR = ROOT / "source-code"
CLIENT_MODULE_DIR = ROOT / "client-module"
SCRIPTS_DIR = ROOT / "scripts"

ARTIFACTS_DIR = ROOT / "test-artifacts"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"


def ensure_dirs() -> None:
    """Create common artifact directories."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
