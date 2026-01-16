#!/usr/bin/env python3
"""Deploy DL-003 fix to Creatio DEV (v8/Freedom UI).

This script automates the manual steps described in CLAUDE.md:
- Deploy backend source code schema (UsrExcelReportService)
- Deploy client unit schema (UsrPage_ebkv9e8)

Security:
- Credentials are loaded from .env via scripts._env.load_dotenv().
- This script MUST NOT print secrets.

Artifacts:
- Screenshots and a small JSON summary are written under test-artifacts/deploy/dl003/<timestamp>/

Usage:
  python3 scripts/deploy/deploy_dl003_fix.py

Notes:
- Creatio UI can change; this script uses multiple selector fallbacks.
- If publishing cannot be automated reliably, it will exit non-zero and leave screenshots.
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from playwright.sync_api import TimeoutError as PwTimeoutError
from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv
from scripts._paths import ARTIFACTS_DIR

USR_EXCEL_REPORT_SERVICE_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"
USR_PAGE_UID = "1d5dfc4d-732d-48d7-af21-9e3d70794734"

BACKEND_FILE = REPO_ROOT / "source-code" / "UsrExcelReportService_Updated.cs"
HANDLER_FILE = REPO_ROOT / "client-module" / "UsrPage_ebkv9e8_Updated.js"


@dataclass
class DeployResult:
    ts_utc: str
    env_url: str
    backend_saved: bool
    backend_published: bool
    handler_saved: bool
    notes: str


def _utc_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _safe(s: Optional[str]) -> str:
    return (s or "").strip()


def _snap(page, out_dir: Path, name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out_dir / f"{name}.png"), full_page=True)


def _wait_stable(page, timeout_ms: int = 20000) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=timeout_ms)
    except Exception:
        pass
    page.wait_for_timeout(500)


def _login(page, base_url: str, username: str, password: str) -> None:
    page.goto(f"{base_url}/Login/NuiLogin.aspx", timeout=60000)
    _wait_stable(page)

    # Login form variants
    if page.locator("#loginEdit-el").count() > 0:
        page.fill("#loginEdit-el", username)
    else:
        page.fill('input[type="text"]:first-of-type', username)

    if page.locator("#passwordEdit-el").count() > 0:
        page.fill("#passwordEdit-el", password)
    else:
        page.fill('input[type="password"]:first-of-type', password)

    for sel in [
        '[data-item-marker="btnLogin"]',
        "#t-comp18-textEl",
        ".login-button-login",
        "text=LOG IN",
        "text=Log in",
        "text=Log In",
    ]:
        loc = page.locator(sel)
        if loc.count() > 0:
            loc.first.click(force=True)
            break

    page.wait_for_timeout(6000)
    _wait_stable(page)

    # Fail fast if still at login
    if "Login/NuiLogin.aspx" in page.url:
        raise RuntimeError("Login did not complete")


def _ensure_logged_in(page, base_url: str, username: str, password: str) -> None:
    # If we're redirected to login, perform login.
    if "/Login/NuiLogin.aspx" in page.url:
        _login(page, base_url, username, password)


def _set_monaco_value(page, code: str) -> None:
    # Wait for monaco and set via model API (fast and reliable for large files).
    page.wait_for_function(
        "() => window.monaco && monaco.editor && monaco.editor.getModels && monaco.editor.getModels().length > 0",
        timeout=120000,
    )

    # Focus editor in case Ctrl+S requires focus.
    try:
        page.locator(".monaco-editor").first.click(force=True)
    except Exception:
        pass

    page.evaluate(
        "(content) => { const m = monaco.editor.getModels()[0]; m.setValue(content); }",
        code,
    )


def _press_save(page) -> None:
    page.keyboard.press("Control+s")
    page.wait_for_timeout(2500)


def _click_first_visible(page, selectors: list[str], *, timeout_ms: int = 15000) -> bool:
    deadline = time.time() + (timeout_ms / 1000.0)
    last_err: Optional[Exception] = None
    while time.time() < deadline:
        for sel in selectors:
            loc = page.locator(sel)
            try:
                if loc.count() > 0 and loc.first.is_visible():
                    loc.first.click(force=True)
                    return True
            except Exception as e:
                last_err = e
                continue
        page.wait_for_timeout(500)
    if last_err:
        # Keep it internal; do not print sensitive details.
        return False
    return False


def _publish_if_possible(page) -> bool:
    # Creatio designers vary. Try common patterns.
    # 1) Direct Publish button
    if _click_first_visible(
        page,
        [
            'button:has-text("Publish")',
            'button:has-text("PUBLISH")',
            'text=Publish',
            '[data-item-marker="PublishButton"]',
            '[data-item-marker="btnPublish"]',
        ],
        timeout_ms=8000,
    ):
        page.wait_for_timeout(6000)
        return True

    # 2) Actions menu -> Publish
    if _click_first_visible(
        page,
        [
            'button:has-text("Actions")',
            'text=Actions',
            '[data-item-marker="ActionsButton"]',
            '[data-item-marker="btnActions"]',
        ],
        timeout_ms=8000,
    ):
        page.wait_for_timeout(500)
        if _click_first_visible(
            page,
            [
                'text=Publish',
                'button:has-text("Publish")',
                '[data-item-marker="PublishMenuItem"]',
            ],
            timeout_ms=8000,
        ):
            page.wait_for_timeout(6000)
            return True

    return False


def _deploy_source_code_schema(page, base_url: str, code: str, out_dir: Path) -> tuple[bool, bool]:
    url = f"{base_url}/0/ClientApp/#/SourceCodeSchemaDesigner/{USR_EXCEL_REPORT_SERVICE_UID}"
    page.goto(url, timeout=60000)
    _wait_stable(page)
    _ensure_logged_in(page, base_url, os.environ.get("CREATIO_USERNAME", ""), os.environ.get("CREATIO_PASSWORD", ""))
    _wait_stable(page, timeout_ms=45000)

    _snap(page, out_dir, "01_backend_open")

    _set_monaco_value(page, code)
    _snap(page, out_dir, "02_backend_code_set")

    _press_save(page)
    _snap(page, out_dir, "03_backend_saved")

    published = _publish_if_possible(page)
    _snap(page, out_dir, "04_backend_publish_attempt")

    return True, published


def _deploy_client_unit_schema(page, base_url: str, code: str, out_dir: Path) -> bool:
    url = f"{base_url}/0/ClientApp/#/ClientUnitSchemaDesigner/{USR_PAGE_UID}"
    page.goto(url, timeout=60000)
    _wait_stable(page)
    _ensure_logged_in(page, base_url, os.environ.get("CREATIO_USERNAME", ""), os.environ.get("CREATIO_PASSWORD", ""))
    _wait_stable(page, timeout_ms=45000)

    _snap(page, out_dir, "05_handler_open")

    _set_monaco_value(page, code)
    _snap(page, out_dir, "06_handler_code_set")

    _press_save(page)
    _snap(page, out_dir, "07_handler_saved")

    return True


def main() -> int:
    load_dotenv()

    base_url = _safe(os.environ.get("CREATIO_URL"))
    username = _safe(os.environ.get("CREATIO_USERNAME"))
    password = _safe(os.environ.get("CREATIO_PASSWORD"))
    if not base_url or not username or not password:
        print("Missing CREATIO_URL/CREATIO_USERNAME/CREATIO_PASSWORD in environment")
        return 2

    backend_code = BACKEND_FILE.read_text(encoding="utf-8")
    handler_code = HANDLER_FILE.read_text(encoding="utf-8")

    out_dir = ARTIFACTS_DIR / "deploy" / "dl003" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir.mkdir(parents=True, exist_ok=True)

    result = DeployResult(
        ts_utc=_utc_ts(),
        env_url=base_url,
        backend_saved=False,
        backend_published=False,
        handler_saved=False,
        notes="",
    )

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            context = browser.new_context(viewport={"width": 1600, "height": 900})
            page = context.new_page()

            _login(page, base_url, username, password)
            _snap(page, out_dir, "00_after_login")

            saved, published = _deploy_source_code_schema(page, base_url, backend_code, out_dir)
            result.backend_saved = saved
            result.backend_published = published

            handler_saved = _deploy_client_unit_schema(page, base_url, handler_code, out_dir)
            result.handler_saved = handler_saved

            browser.close()

    except PwTimeoutError:
        result.notes = "Timeout while interacting with Creatio UI. See screenshots for context."
    except Exception as e:
        # Do not leak credentials; generic error only.
        result.notes = f"Error: {type(e).__name__}: {str(e)[:200]}"

    (out_dir / "summary.json").write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")

    # Exit non-zero if publish failed; publishing is required for backend.
    if not result.backend_saved:
        return 10
    if not result.backend_published:
        return 11
    if not result.handler_saved:
        return 12

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
