from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def load_dotenv(dotenv_path: Optional[Path] = None, *, override: bool = False) -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ.

    - Does not require python-dotenv.
    - Ignores blank lines and lines starting with '#'.
    - Supports optional quoting with single or double quotes.

    Parameters
    - dotenv_path: defaults to repo root '.env' when available.
    - override: if True, overwrite existing os.environ keys.
    """

    if dotenv_path is None:
        # Local import to avoid cycles in scripts that also import _paths.
        from scripts._paths import ROOT

        dotenv_path = ROOT / ".env"

    try:
        raw = dotenv_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return

    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        # Strip optional quotes
        if len(value) >= 2 and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
            value = value[1:-1]

        if not key:
            continue

        if not override and key in os.environ:
            continue

        os.environ[key] = value
