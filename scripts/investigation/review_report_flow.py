#!/usr/bin/env python3
"""Automated review of the Reports page download flow.

Runs against DEV or PROD (credentials sourced from .env, including commented PROD lines)
without printing secrets.

Outputs:
- test-artifacts/flow-review/<env>/summary.json
- test-artifacts/flow-review/<env>/screenshots/*.png
- test-artifacts/flow-review/<env>/downloads/* (if Playwright detects a download)

Usage:
  python3 scripts/investigation/review_report_flow.py --env dev
  python3 scripts/investigation/review_report_flow.py --env prod

Notes:
- This uses UI automation to match how real users download.
- It records network responses for relevant endpoints and download headers.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / ".env"


@dataclass
class HttpEvent:
    ts: float
    kind: str  # response | requestfailed | console | pageerror | download | popup
    url: Optional[str] = None
    method: Optional[str] = None
    status: Optional[int] = None
    content_type: Optional[str] = None
    content_disposition: Optional[str] = None
    location: Optional[str] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


RELEVANT_URL_SUBSTRS = [
    "UsrExcelReportService",
    "IntExcelReportService",
    "IntExcelExport",
    "ExportToExcel",
    "DownloadExportFile",
    "FileDownload",
    ".ashx",
]


def _parse_env_with_commented_blocks(path: Path) -> Dict[str, Dict[str, str]]:
    """Parse .env and return {"dev": {...}, "prod": {...}}.

    Supports this layout:
      # DEV
      CREATIO_URL=...
      CREATIO_USERNAME=...
      CREATIO_PASSWORD=...

      # PROD
      # CREATIO_URL=...
      # CREATIO_USERNAME=...
      # CREATIO_PASSWORD=...

    It will read uncommented lines for dev, and commented '# CREATIO_*=' lines
    under the PROD block for prod.
    """
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    blocks: Dict[str, Dict[str, str]] = {"dev": {}, "prod": {}}

    current: Optional[str] = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Block headers
        if stripped.startswith("#"):
            header = stripped.lstrip("#").strip().lower()
            if header == "dev":
                current = "dev"
                continue
            if header == "prod":
                current = "prod"
                continue

        if current is None:
            continue

        # For dev, accept uncommented assignments.
        if current == "dev" and not stripped.startswith("#"):
            if "=" in stripped:
                k, v = stripped.split("=", 1)
                blocks["dev"][k.strip()] = v.strip().strip('"').strip("'")
            continue

        # For prod, accept commented assignments like '# CREATIO_URL=...'
        if current == "prod" and stripped.startswith("#"):
            s = stripped.lstrip("#").strip()
            if "=" in s:
                k, v = s.split("=", 1)
                blocks["prod"][k.strip()] = v.strip().strip('"').strip("'")

    return blocks


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
    page.goto(f"{base_url}/Login/NuiLogin.aspx", timeout=30000)
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


def _select_from_lookup(page, aria_label: str, value_text: str, search_text: Optional[str] = None) -> None:
    icon_sel = f'mat-icon[aria-label="Select value {aria_label}"]'
    page.locator(icon_sel).first.click(force=True)
    page.wait_for_timeout(800)

    pane = page.locator(".cdk-overlay-container .cdk-overlay-pane").last

    if search_text:
        search_loc = pane.locator(
            'input[placeholder*="Search" i], input[aria-label*="Search" i], input[type="search"], input[type="text"]'
        )
        for i in range(min(search_loc.count(), 6)):
            cand = search_loc.nth(i)
            try:
                if cand.is_visible():
                    cand.click(force=True)
                    cand.fill(search_text)
                    page.wait_for_timeout(800)
                    break
            except Exception:
                continue

    pane.locator(f"text={value_text}").first.wait_for(state="visible", timeout=25000)
    pane.locator(f"text={value_text}").first.click(force=True)
    page.wait_for_timeout(200)

    for btn_sel in ["button:has-text(\"Select\")", "button:has-text(\"OK\")", "button:has-text(\"Choose\")"]:
        btn = pane.locator(btn_sel)
        if btn.count() > 0:
            btn.first.click(force=True)
            break

    page.wait_for_timeout(1200)


def _is_relevant(url: str, key_hint: Optional[str] = None) -> bool:
    if key_hint and key_hint in url:
        return True
    return any(s in url for s in RELEVANT_URL_SUBSTRS)


def run(env_name: str) -> int:
    blocks = _parse_env_with_commented_blocks(ENV_PATH)
    cfg = blocks.get(env_name)
    if not cfg:
        raise RuntimeError(f"No config for env={env_name}")

    base_url = cfg.get("CREATIO_URL", "").rstrip("/")
    username = cfg.get("CREATIO_USERNAME", "")
    password = cfg.get("CREATIO_PASSWORD", "")
    if not base_url or not username or not password:
        raise RuntimeError(f"Missing CREATIO_URL/CREATIO_USERNAME/CREATIO_PASSWORD for env={env_name}")

    reports_url = f"{base_url}/Navigation/Navigation.aspx?schemaName=UsrPage_ebkv9e8"

    out_root = REPO_ROOT / "test-artifacts" / "flow-review" / env_name
    screenshots_dir = out_root / "screenshots"
    downloads_dir = out_root / "downloads"
    payloads_dir = out_root / "payloads"
    out_root.mkdir(parents=True, exist_ok=True)
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    downloads_dir.mkdir(parents=True, exist_ok=True)
    payloads_dir.mkdir(parents=True, exist_ok=True)

    events: List[HttpEvent] = []

    def add(ev: HttpEvent) -> None:
        events.append(ev)

    # Mutable state shared by event handlers
    state: Dict[str, Any] = {"key": None}

    report_name = "Commission"
    year_month = "2025-10"
    sales_group = "Pampa Bay - Online"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            downloads_path=str(downloads_dir),
            args=["--no-sandbox", "--disable-popup-blocking"],
        )
        context = browser.new_context(viewport={"width": 1600, "height": 900}, accept_downloads=True)

        def on_download(dl) -> None:
            try:
                add(
                    HttpEvent(
                        ts=time.time(),
                        kind="download",
                        url=dl.url,
                        details={"suggested_filename": dl.suggested_filename},
                    )
                )
                # Save to our downloads dir
                save_path = downloads_dir / dl.suggested_filename
                dl.save_as(str(save_path))
                add(
                    HttpEvent(
                        ts=time.time(),
                        kind="download_saved",
                        url=dl.url,
                        details={"path": str(save_path), "size": save_path.stat().st_size},
                    )
                )
            except Exception as e:
                add(HttpEvent(ts=time.time(), kind="download_error", error=str(e)))

        context.on("download", on_download)

        def attach_page(pg, label: str) -> None:
            # Frame navigations (helps identify download URLs opened in popups)
            try:
                pg.on(
                    "framenavigated",
                    lambda frame: add(
                        HttpEvent(
                            ts=time.time(),
                            kind="navigate",
                            url=(frame.url if frame else None),
                            details={"page": label, "name": (frame.name if frame else None)},
                        )
                    ),
                )
            except Exception:
                pass

            # Console and page errors (no secrets)
            pg.on(
                "console",
                lambda msg: add(
                    HttpEvent(
                        ts=time.time(),
                        kind="console",
                        url=pg.url,
                        details={"page": label, "type": msg.type, "text": msg.text[:400]},
                    )
                ),
            )
            pg.on(
                "pageerror",
                lambda err: add(
                    HttpEvent(ts=time.time(), kind="pageerror", url=pg.url, error=str(err)[:600], details={"page": label})
                ),
            )

            # Network response logging
            def on_response(resp) -> None:
                url = resp.url

                try:
                    headers = resp.headers
                except Exception:
                    headers = {}

                ct = headers.get("content-type")
                cd = headers.get("content-disposition")
                is_attachment = bool(cd and cd.lower().startswith("attachment"))
                is_excelish = bool(ct and ("spreadsheet" in ct.lower() or "excel" in ct.lower() or "octet-stream" in ct.lower()))

                key_hint = state.get("key")
                if not (is_attachment or is_excelish or _is_relevant(url, key_hint=key_hint)):
                    return

                ev = HttpEvent(
                    ts=time.time(),
                    kind="response",
                    url=url,
                    status=resp.status,
                    content_type=ct,
                    content_disposition=cd,
                    location=headers.get("location"),
                    details={"page": label},
                )

                try:
                    if url.endswith("/0/rest/UsrExcelReportService/Generate") or url.endswith(
                        "/0/rest/IntExcelReportService/GetExportFiltersKey"
                    ):
                        data = resp.json()
                        if isinstance(data, dict) and data.get("key"):
                            state["key"] = data.get("key")
                            # Store a safe preview of the payload: keep scalars, and summarize complex types.
                            preview: Dict[str, Any] = {}
                            for k, v in data.items():
                                if isinstance(v, (str, int, float, bool)) or v is None:
                                    preview[k] = v
                                else:
                                    preview[k] = {"_type": type(v).__name__}

                            ev.details = {
                                **(ev.details or {}),
                                "key": data.get("key"),
                                "payload_preview": preview,
                            }
                            add(ev)
                            add(HttpEvent(ts=time.time(), kind="key", details={"key": data.get("key"), "source_url": url, "page": label}))
                            return
                except Exception:
                    pass

                add(ev)

            pg.on("response", on_response)

            # Outgoing requests (track key follow-on, exports/downloads)
            def on_request(req) -> None:
                url = req.url
                key_hint = state.get("key")

                details = {"page": label}

                # Capture request payload for the key-generating endpoints (no secrets expected in body).
                try:
                    if req.method == "POST" and (
                        url.endswith("/0/rest/IntExcelReportService/GetExportFiltersKey")
                        or url.endswith("/0/rest/UsrExcelReportService/Generate")
                    ):
                        post_data = req.post_data or ""
                        details["post_data_preview"] = post_data[:2000]
                        # Write full payload for replay/debugging (no secrets expected).
                        safe_endpoint = "GetExportFiltersKey" if url.endswith("GetExportFiltersKey") else "Generate"
                        payload_path = payloads_dir / f"{env_name}_{label}_{safe_endpoint}.json"
                        try:
                            payload_path.write_text(post_data, encoding="utf-8")
                            details["post_data_path"] = str(payload_path)
                        except Exception:
                            pass
                except Exception:
                    pass

                if _is_relevant(url, key_hint=key_hint) or (key_hint and key_hint in url):
                    add(HttpEvent(ts=time.time(), kind="request", url=url, method=req.method, details=details))
                else:
                    # Still record the key-generating POSTs even if filters miss them.
                    if req.method == "POST" and (
                        url.endswith("/0/rest/IntExcelReportService/GetExportFiltersKey")
                        or url.endswith("/0/rest/UsrExcelReportService/Generate")
                    ):
                        add(HttpEvent(ts=time.time(), kind="request", url=url, method=req.method, details=details))

            pg.on("request", on_request)

            # Request failures
            def on_request_failed(req) -> None:
                failure = None
                try:
                    failure = req.failure
                except Exception:
                    failure = None

                if failure is None:
                    err_text = "unknown"
                elif isinstance(failure, str):
                    err_text = failure
                else:
                    err_text = getattr(failure, "error_text", None) or str(failure)

                add(
                    HttpEvent(
                        ts=time.time(),
                        kind="requestfailed",
                        url=req.url,
                        method=req.method,
                        error=str(err_text)[:600],
                        details={"page": label},
                    )
                )

            pg.on("requestfailed", on_request_failed)

        # Track popups
        popup_count = {"n": 0}

        def on_page(pg) -> None:
            popup_count["n"] += 1
            label = f"popup{popup_count['n']}"
            try:
                add(HttpEvent(ts=time.time(), kind="popup", url=pg.url, details={"page": label}))
            except Exception:
                add(HttpEvent(ts=time.time(), kind="popup", url=None, details={"page": label}))
            attach_page(pg, label)

        context.on("page", on_page)

        page = context.new_page()
        attach_page(page, "main")

        # Run flow
        add(HttpEvent(ts=time.time(), kind="info", details={"step": "login"}))
        _login(page, base_url, username, password)
        _snap(page, screenshots_dir, "01_after_login")

        add(HttpEvent(ts=time.time(), kind="info", details={"step": "goto_reports"}))
        page.goto(reports_url, timeout=30000)
        page.wait_for_timeout(7000)
        _wait_stable(page, timeout_ms=30000)
        _snap(page, screenshots_dir, "02_reports_loaded")

        add(HttpEvent(ts=time.time(), kind="info", details={"step": "select_filters"}))
        _select_from_lookup(page, "Report", report_name)
        _select_from_lookup(page, "Year - Month", year_month, search_text=year_month)
        _select_from_lookup(page, "Sales Group", sales_group, search_text="Pampa Bay")
        _snap(page, screenshots_dir, "03_filled_form")

        # Capture DOM markers to help verify whether our handler is running.
        try:
            dom = page.evaluate(
                """() => {
                const buttons = Array.from(document.querySelectorAll('crt-button, button'))
                  .slice(0, 30)
                  .map((el) => {
                    const attrs = {};
                    for (const a of Array.from(el.attributes || [])) {
                      const n = a.name;
                      if (n.toLowerCase().includes('password') || n.toLowerCase().includes('token')) continue;
                      attrs[n] = (a.value || '').slice(0, 200);
                    }
                    return {
                      tag: el.tagName.toLowerCase(),
                      text: (el.textContent || '').trim().slice(0, 80),
                      id: el.id || null,
                      class: (el.className && ('' + el.className).slice(0, 200)) || null,
                      attrs,
                      outerHTMLPreview: (el.outerHTML || '').slice(0, 300)
                    };
                  });

                const iframe = document.getElementById('reportDownloadFrame');
                return {
                  reportDownloadFrame: iframe ? { exists: true, src: (iframe.getAttribute('src') || iframe.src || '').slice(0, 300) } : { exists: false },
                  iframeCount: document.querySelectorAll('iframe').length,
                  buttons
                };
              }"""
            )
            add(HttpEvent(ts=time.time(), kind="dom", url=page.url, details={"step": "before_click", **dom}))
        except Exception as e:
            add(HttpEvent(ts=time.time(), kind="dom_error", url=page.url, error=str(e)[:600], details={"step": "before_click"}))

        # Click the main Report button (not the IView one)
        report_btn = page.locator('crt-button:has-text("Report")').first
        if report_btn.count() == 0:
            report_btn = page.locator('button:has-text("Report")').first
        report_btn.wait_for(state="visible", timeout=20000)

        add(HttpEvent(ts=time.time(), kind="info", details={"step": "click_report"}))
        report_btn.click(force=True)
        page.wait_for_timeout(1000)

        # Immediately check whether the hidden iframe was created / navigated.
        try:
            after = page.evaluate(
                """() => {
                const iframe = document.getElementById('reportDownloadFrame');
                return iframe
                  ? { exists: true, src: (iframe.getAttribute('src') || iframe.src || '').slice(0, 500) }
                  : { exists: false };
              }"""
            )
            add(HttpEvent(ts=time.time(), kind="dom", url=page.url, details={"step": "after_click", "reportDownloadFrame": after}))
        except Exception as e:
            add(HttpEvent(ts=time.time(), kind="dom_error", url=page.url, error=str(e)[:600], details={"step": "after_click"}))

        _snap(page, screenshots_dir, "04_after_click")

        # Wait for some signal of download activity
        t0 = time.time()
        seen_download = False
        while time.time() - t0 < 120:
            if any(ev.kind in ("download", "download_saved") for ev in events):
                seen_download = True
                break
            # Also treat a 200 response with content-disposition attachment as a success signal
            if any(
                ev.kind == "response"
                and ev.status == 200
                and (ev.content_disposition or "").lower().startswith("attachment")
                for ev in events
            ):
                break
            page.wait_for_timeout(1000)

        _snap(page, screenshots_dir, "05_after_wait")

        add(
            HttpEvent(
                ts=time.time(),
                kind="result",
                details={
                    "seen_download_event": seen_download,
                    "final_url": page.url,
                },
            )
        )

        browser.close()

    summary = {
        "env": env_name,
        "base_url": base_url,
        "reports_url": reports_url,
        "ts": time.time(),
        "events": [asdict(e) for e in events],
    }

    (out_root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", choices=["dev", "prod"], required=True)
    args = ap.parse_args()
    raise SystemExit(run(args.env))


if __name__ == "__main__":
    main()
