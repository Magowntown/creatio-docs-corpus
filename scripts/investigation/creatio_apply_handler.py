#!/usr/bin/env python3
"""
Creatio Apply Handler
Applies the Report button handler to UsrPage_ebkv9e8 schema
"""

from playwright.sync_api import sync_playwright
import os
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import SCREENSHOTS_DIR, CLIENT_MODULE_DIR, ARTIFACTS_DIR, ensure_dirs

ensure_dirs()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
SCREENSHOT_DIR = str(SCREENSHOTS_DIR)
TARGET_SCHEMA = "UsrPage_ebkv9e8"
SCHEMA_UID = "1d5dfc4d-732d-48d7-af21-9e3d70794734"

# Read the updated schema code
with open(CLIENT_MODULE_DIR / 'UsrPage_ebkv9e8_Updated.js', 'r', encoding='utf-8') as f:
    NEW_SCHEMA_CODE = f.read()

def screenshot(page, name):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = f"{SCREENSHOT_DIR}/{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"📸 {name}")
    return path

def wait_for_stable(page, timeout=5000):
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    page.wait_for_timeout(1000)

with sync_playwright() as p:
    print("🚀 Launching browser...")
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    # Login
    print("\n1️⃣ Logging in...")
    page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
    wait_for_stable(page)

    # Creatio login pages vary (marker-based vs legacy IDs). Try both.
    try:
        if page.locator('#loginEdit-el').count() > 0:
            page.fill('#loginEdit-el', USERNAME)
        else:
            page.fill('input[type="text"]:first-of-type', USERNAME)
    except Exception:
        pass

    try:
        if page.locator('#passwordEdit-el').count() > 0:
            page.fill('#passwordEdit-el', PASSWORD)
        else:
            page.fill('input[type="password"]:first-of-type', PASSWORD)
    except Exception:
        pass

    login_clicked = False
    for sel in [
        '[data-item-marker="btnLogin"]',
        '#t-comp18-textEl',
        '.login-button-login',
        'text=LOG IN',
    ]:
        try:
            loc = page.locator(sel)
            if loc.count() > 0:
                try:
                    loc.first.click(timeout=5000)
                except Exception:
                    loc.first.click(timeout=5000, force=True)
                login_clicked = True
                break
        except Exception:
            pass

    if not login_clicked:
        screenshot(page, "apply_00_login_not_found")
        raise RuntimeError("Login button not found; cannot continue")

    page.wait_for_timeout(6000)
    wait_for_stable(page)

    # Basic sanity check: if we're still on Login page, fail early.
    if "Login/NuiLogin.aspx" in page.url:
        screenshot(page, "apply_00_login_failed")
        raise RuntimeError("Login did not complete (still on login page)")

    print("   ✅ Logged in")

    # Open schema designer
    print(f"\n2️⃣ Opening schema designer...")
    designer_url = f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{SCHEMA_UID}"
    page.goto(designer_url, timeout=30000)
    page.wait_for_timeout(6000)
    wait_for_stable(page)

    # Dismiss blocking modal dialogs (e.g., package/schema not found)
    try:
        ok_btn = page.locator('text=OK').first
        if ok_btn.count() > 0:
            ok_btn.click(timeout=2000)
            page.wait_for_timeout(500)
    except Exception:
        pass

    screenshot(page, "apply_01_designer_opened")

    # Click on JS tab to ensure we're in the code editor
    print("\n3️⃣ Ensuring JS tab is active...")
    try:
        js_tab = page.locator('text=JS').first
        if js_tab.count() > 0:
            js_tab.click(timeout=5000)
            page.wait_for_timeout(1000)
    except Exception:
        pass

    # Identify editor type and extract current code
    print("\n4️⃣ Extracting current schema code...")

    extracted = page.evaluate('''() => {
        const out = { ok: false, method: 'none', content: '', error: null };
        try {
            // Ace
            if (typeof ace !== 'undefined') {
                const edEl = document.querySelector('.ace_editor');
                if (edEl) {
                    const ed = ace.edit(edEl);
                    out.ok = true;
                    out.method = 'ace';
                    out.content = ed.getValue();
                    return out;
                }
            }
        } catch (e) {
            out.error = 'ace:' + (e && e.message ? e.message : String(e));
        }

        try {
            // Monaco
            if (typeof monaco !== 'undefined' && monaco.editor && monaco.editor.getEditors) {
                const editors = monaco.editor.getEditors();
                if (editors && editors.length) {
                    out.ok = true;
                    out.method = 'monaco';
                    out.content = editors[0].getValue();
                    return out;
                }
            }
        } catch (e) {
            out.error = (out.error || '') + ' monaco:' + (e && e.message ? e.message : String(e));
        }

        // Textarea fallback
        const ta = document.querySelector('textarea');
        if (ta && (ta.value || '').length > 0) {
            out.ok = true;
            out.method = 'textarea';
            out.content = ta.value;
            return out;
        }

        // contenteditable fallback
        const ce = document.querySelector('[contenteditable="true"]');
        if (ce) {
            out.ok = true;
            out.method = 'contenteditable';
            out.content = ce.innerText || ce.textContent || '';
            return out;
        }

        return out;
    }''')

    print(f"   Extracted via: {extracted.get('method')} (len={len(extracted.get('content',''))})")

    current_code = extracted.get('content') or ''
    if 'usr.GenerateExcelReportRequest' not in current_code:
        screenshot(page, "apply_01_no_handler_found")
        raise RuntimeError("Could not locate usr.GenerateExcelReportRequest in extracted code")

    # Deploy the full known-good schema code from client-module/UsrPage_ebkv9e8_Updated.js.
    # This avoids brittle in-place patches and ensures the latest download approach (hidden iframe)
    # is what is deployed.
    if 'usr.GenerateExcelReportRequest' not in NEW_SCHEMA_CODE:
        raise RuntimeError("NEW_SCHEMA_CODE is missing usr.GenerateExcelReportRequest")
    patched_code = NEW_SCHEMA_CODE

    # Apply back into editor depending on editor type
    method = extracted.get('method')
    if method == 'ace':
        page.evaluate('''(code) => {
            const edEl = document.querySelector('.ace_editor');
            const ed = ace.edit(edEl);
            ed.setValue(code, -1);
        }''', patched_code)
    elif method == 'monaco':
        page.evaluate('''(code) => {
            const editors = monaco.editor.getEditors();
            editors[0].setValue(code);
        }''', patched_code)
    elif method == 'textarea':
        page.evaluate('''(code) => {
            const ta = document.querySelector('textarea');
            ta.value = code;
            ta.dispatchEvent(new Event('input', { bubbles: true }));
        }''', patched_code)
    else:
        # contenteditable or unknown: use keyboard to ensure editor change tracking
        ce = page.locator('[contenteditable="true"]').first
        if ce.count() == 0:
            screenshot(page, "apply_02_no_editor")
            raise RuntimeError("No editable code editor found")
        ce.click(timeout=5000)
        page.keyboard.press('Control+a')
        page.keyboard.press('Backspace')
        page.keyboard.insert_text(patched_code)

    screenshot(page, "apply_02_after_update")

    # Save + compile
    print("\n7️⃣ Saving schema...")

    def click_first(selectors, label: str) -> bool:
        for sel in selectors:
            try:
                loc = page.locator(sel).first
                if loc.count() > 0:
                    print(f"   Clicking {label}: {sel}")
                    try:
                        loc.scroll_into_view_if_needed(timeout=2000)
                    except Exception:
                        pass
                    try:
                        loc.click(timeout=5000)
                    except Exception:
                        loc.click(timeout=5000, force=True)
                    page.wait_for_timeout(800)
                    return True
            except Exception:
                pass
        return False

    saved = False

    # Preferred: Actions menu -> Save
    actions_selectors = [
        'button:has-text("Actions")',
        'button:has-text("ACTIONS")',
        'text=Actions',
        'text=ACTIONS',
    ]

    if click_first(actions_selectors, "Actions"):
        # Menu item
        if click_first(['text=Save', 'text=SAVE'], "Save"):
            saved = True
        else:
            # Close menu if open
            try:
                page.keyboard.press('Escape')
            except Exception:
                pass

    # Fallback: Ctrl+S
    if not saved:
        try:
            page.keyboard.press('Control+S')
            page.wait_for_timeout(1500)
            saved = True
            print("   Saved via Ctrl+S")
        except Exception:
            pass

    screenshot(page, "apply_03_after_save")

    print("\n8️⃣ Compiling schema...")

    compiled = False

    # Try toolbar Compile button first
    compile_selectors = [
        'button:has-text("Compile")',
        'button:has-text("COMPILE")',
        'text=Compile',
        'text=COMPILE',
    ]
    if click_first(compile_selectors, "Compile"):
        compiled = True

    # Fallback: Actions menu -> Compile
    if not compiled and click_first(actions_selectors, "Actions"):
        if click_first(['text=Compile', 'text=COMPILE'], "Compile"):
            compiled = True
        else:
            try:
                page.keyboard.press('Escape')
            except Exception:
                pass

    # Give compilation time (DEV can be slow)
    page.wait_for_timeout(15000)
    screenshot(page, "apply_04_after_compile")

    # Check current state
    print("\n9️⃣ Verifying current code...")

    current_code = page.evaluate('''() => {
        // Try to get current code from ace
        const aceEditors = document.querySelectorAll('.ace_editor');
        for (const ed of aceEditors) {
            if (ed.id) {
                try {
                    const editor = ace.edit(ed.id);
                    return editor.getValue();
                } catch(e) {}
            }
        }
        return '';
    }''')

    if current_code:
        print(f"   Current code length: {len(current_code)} chars")
        if 'usr.GenerateExcelReportRequest' in current_code:
            print("   ✅ Handler appears to be in the code!")
        else:
            print("   ⚠ Handler not found in code")

        # Save current code to file for review
        out_path = ARTIFACTS_DIR / f"{TARGET_SCHEMA}_current.js"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(current_code)
        print(f"   📄 Current code saved to {out_path}")

    screenshot(page, "apply_03_final")

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Schema UID: {SCHEMA_UID}")
    print(f"Designer URL: {designer_url}")
    print("\n⚠ NOTE: Code update was attempted but may need manual verification.")
    print("Please review the schema in Creatio Designer to confirm changes.")
    print("="*60)

    browser.close()
    print("\n✅ Done!")
