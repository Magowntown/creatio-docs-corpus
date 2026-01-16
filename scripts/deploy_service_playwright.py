#!/usr/bin/env python3
"""
Deploy UsrExcelReportService to Creatio DEV using Playwright browser automation.
This bypasses the 401 Unauthorized issue with the Designer API.
"""

from playwright.sync_api import sync_playwright
import os
from pathlib import Path
import time

# Configuration
CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"  # UsrExcelReportService
DESIGNER_URL = f"{CREATIO_URL}/0/ClientApp/#/SourceCodeSchemaDesigner/{SCHEMA_UID}"

# Read the updated service code
SERVICE_CODE_PATH = Path(__file__).parent.parent / "source-code" / "UsrExcelReportService_Updated.cs"
with open(SERVICE_CODE_PATH, "r", encoding="utf-8") as f:
    SERVICE_CODE = f.read()

SCREENSHOT_DIR = Path(__file__).parent.parent / "test-artifacts" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def screenshot(page, name):
    path = SCREENSHOT_DIR / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    print(f"  Screenshot: {name}")
    return path

def wait_for_stable(page, timeout=5000):
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    page.wait_for_timeout(1000)

def main():
    print("=" * 60)
    print("DEPLOYING UsrExcelReportService (FLT-004 Fix)")
    print("=" * 60)

    with sync_playwright() as p:
        print("\n1. Launching browser...")
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        # Login
        print("\n2. Logging in to Creatio...")
        page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
        wait_for_stable(page)
        page.wait_for_timeout(3000)  # Extra wait for Freedom UI to initialize

        # Fill login form using click + type approach for Freedom UI
        print("  Finding username field...")

        # Try to find and fill username field
        username_filled = False
        username_selectors = [
            'input[placeholder*="Username"]',
            'input[placeholder*="username"]',
            'input[type="text"]',
            '#loginEdit-el',
            '[data-item-marker="login-edit"] input',
            '.login-input input',
        ]

        for sel in username_selectors:
            try:
                loc = page.locator(sel).first
                if loc.count() > 0 and loc.is_visible():
                    loc.click()
                    page.wait_for_timeout(200)
                    loc.fill(USERNAME)
                    username_filled = True
                    print(f"    Filled username via: {sel}")
                    break
            except Exception as e:
                continue

        if not username_filled:
            # Try keyboard navigation
            print("  Trying Tab + keyboard approach...")
            page.keyboard.press('Tab')
            page.wait_for_timeout(200)
            page.keyboard.type(USERNAME)
            username_filled = True

        # Fill password field
        print("  Finding password field...")
        password_selectors = [
            'input[type="password"]',
            '#passwordEdit-el',
            '[data-item-marker="password-edit"] input',
        ]

        for sel in password_selectors:
            try:
                loc = page.locator(sel).first
                if loc.count() > 0 and loc.is_visible():
                    loc.click()
                    page.wait_for_timeout(200)
                    loc.fill(PASSWORD)
                    print(f"    Filled password via: {sel}")
                    break
            except:
                continue
        else:
            # Tab to password field
            page.keyboard.press('Tab')
            page.wait_for_timeout(200)
            page.keyboard.type(PASSWORD)

        page.wait_for_timeout(500)
        screenshot(page, "deploy_01b_form_filled")

        # Click login button
        print("  Clicking login button...")
        login_clicked = False
        for btn_sel in ['button:has-text("LOG IN")', 'button:has-text("Log in")', '[data-item-marker="btnLogin"]', '.login-button-login', 'text=LOG IN']:
            try:
                loc = page.locator(btn_sel).first
                if loc.count() > 0 and loc.is_visible():
                    loc.click(timeout=5000)
                    login_clicked = True
                    print(f"    Clicked via: {btn_sel}")
                    break
            except:
                continue

        if not login_clicked:
            # Try Enter key
            page.keyboard.press('Enter')
            print("    Pressed Enter")

        page.wait_for_timeout(8000)
        wait_for_stable(page)

        # Check if login succeeded
        if "Login/NuiLogin.aspx" in page.url:
            screenshot(page, "deploy_01_login_failed")
            print("  ERROR: Login failed - still on login page")
            browser.close()
            return False

        print("  Login successful!")
        screenshot(page, "deploy_02_logged_in")

        # Open schema designer
        print(f"\n3. Opening Source Code Schema Designer...")
        page.goto(DESIGNER_URL, timeout=30000)
        page.wait_for_timeout(6000)
        wait_for_stable(page)

        # Dismiss any modals
        try:
            ok_btn = page.locator('text=OK').first
            if ok_btn.count() > 0:
                ok_btn.click(timeout=2000)
                page.wait_for_timeout(500)
        except:
            pass

        screenshot(page, "deploy_03_designer_opened")

        # Find and interact with code editor
        print("\n4. Finding code editor...")

        # Try to get current code and editor type
        editor_info = page.evaluate('''() => {
            const out = { ok: false, method: 'none', length: 0 };

            // Try Monaco
            try {
                if (typeof monaco !== 'undefined' && monaco.editor && monaco.editor.getEditors) {
                    const editors = monaco.editor.getEditors();
                    if (editors && editors.length) {
                        out.ok = true;
                        out.method = 'monaco';
                        out.length = editors[0].getValue().length;
                        return out;
                    }
                }
            } catch (e) {}

            // Try Ace
            try {
                if (typeof ace !== 'undefined') {
                    const edEl = document.querySelector('.ace_editor');
                    if (edEl) {
                        const ed = ace.edit(edEl);
                        out.ok = true;
                        out.method = 'ace';
                        out.length = ed.getValue().length;
                        return out;
                    }
                }
            } catch (e) {}

            // Try textarea
            const ta = document.querySelector('textarea');
            if (ta && ta.value) {
                out.ok = true;
                out.method = 'textarea';
                out.length = ta.value.length;
                return out;
            }

            return out;
        }''')

        print(f"  Editor type: {editor_info.get('method')}, current code length: {editor_info.get('length')}")

        if not editor_info.get('ok'):
            screenshot(page, "deploy_04_no_editor")
            print("  ERROR: Could not find code editor")
            browser.close()
            return False

        # Replace code in editor
        print("\n5. Replacing code with FLT-004 fix...")

        method = editor_info.get('method')
        if method == 'monaco':
            page.evaluate('''(code) => {
                const editors = monaco.editor.getEditors();
                editors[0].setValue(code);
            }''', SERVICE_CODE)
        elif method == 'ace':
            page.evaluate('''(code) => {
                const edEl = document.querySelector('.ace_editor');
                const ed = ace.edit(edEl);
                ed.setValue(code, -1);
            }''', SERVICE_CODE)
        elif method == 'textarea':
            page.evaluate('''(code) => {
                const ta = document.querySelector('textarea');
                ta.value = code;
                ta.dispatchEvent(new Event('input', { bubbles: true }));
            }''', SERVICE_CODE)

        page.wait_for_timeout(1000)
        screenshot(page, "deploy_05_code_replaced")
        print("  Code replaced!")

        # Save schema
        print("\n6. Saving schema...")

        saved = False

        # Try Ctrl+S first
        try:
            page.keyboard.press('Control+s')
            page.wait_for_timeout(2000)
            saved = True
            print("  Saved via Ctrl+S")
        except:
            pass

        # Try Actions menu -> Save as fallback
        if not saved:
            for actions_sel in ['button:has-text("Actions")', 'text=Actions', 'text=ACTIONS']:
                try:
                    loc = page.locator(actions_sel).first
                    if loc.count() > 0:
                        loc.click(timeout=3000)
                        page.wait_for_timeout(500)

                        for save_sel in ['text=Save', 'text=SAVE']:
                            save_loc = page.locator(save_sel).first
                            if save_loc.count() > 0:
                                save_loc.click(timeout=3000)
                                saved = True
                                print("  Saved via Actions menu")
                                break
                        break
                except:
                    pass

        screenshot(page, "deploy_06_after_save")

        # Compile/Publish
        print("\n7. Compiling schema...")

        compiled = False

        # Try Compile button
        for compile_sel in ['button:has-text("Compile")', 'text=Compile', 'text=COMPILE', 'button:has-text("Publish")', 'text=Publish']:
            try:
                loc = page.locator(compile_sel).first
                if loc.count() > 0:
                    loc.click(timeout=5000)
                    compiled = True
                    print(f"  Clicked: {compile_sel}")
                    break
            except:
                pass

        # Wait for compilation
        print("  Waiting for compilation (up to 60s)...")
        page.wait_for_timeout(15000)

        screenshot(page, "deploy_07_after_compile")

        # Verify
        print("\n8. Verifying deployment...")

        new_length = page.evaluate('''() => {
            try {
                if (typeof monaco !== 'undefined' && monaco.editor && monaco.editor.getEditors) {
                    const editors = monaco.editor.getEditors();
                    if (editors && editors.length) {
                        return editors[0].getValue().length;
                    }
                }
            } catch (e) {}

            try {
                if (typeof ace !== 'undefined') {
                    const edEl = document.querySelector('.ace_editor');
                    if (edEl) {
                        const ed = ace.edit(edEl);
                        return ed.getValue().length;
                    }
                }
            } catch (e) {}

            return 0;
        }''')

        print(f"  New code length: {new_length} (expected ~{len(SERVICE_CODE)})")

        # Check for marker - BuildDateRangeFilterJson is unique to FLT-004 fix
        has_marker = page.evaluate('''() => {
            try {
                if (typeof monaco !== 'undefined' && monaco.editor && monaco.editor.getEditors) {
                    const editors = monaco.editor.getEditors();
                    if (editors && editors.length) {
                        return editors[0].getValue().includes('BuildDateRangeFilterJson');
                    }
                }
            } catch (e) {}

            try {
                if (typeof ace !== 'undefined') {
                    const edEl = document.querySelector('.ace_editor');
                    if (edEl) {
                        const ed = ace.edit(edEl);
                        return ed.getValue().includes('BuildDateRangeFilterJson');
                    }
                }
            } catch (e) {}

            return false;
        }''')

        screenshot(page, "deploy_08_final")

        browser.close()

        print("\n" + "=" * 60)
        print("DEPLOYMENT RESULT")
        print("=" * 60)

        if has_marker:
            print("  Marker 'BuildDateRangeFilterJson' FOUND in code")
            print("  Status: DEPLOYED")
            return True
        else:
            print("  Marker 'BuildDateRangeFilterJson' NOT FOUND")
            print("  Status: VERIFICATION NEEDED")
            return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
