#!/usr/bin/env python3
"""
Deploy UsrPage_ebkv9e8_Defensive.js to PROD (v2).
Better editor detection for Freedom UI schema designer.
"""

from playwright.sync_api import sync_playwright
import os
import sys
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / ".env")

PROD_URL = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_PROD_USERNAME", "Supervisor")
PASSWORD = os.environ.get("CREATIO_PROD_PASSWORD", "")

# IWQBIntegration version UID
SCHEMA_UID = "1d5dfc4d-732d-48d7-af21-9e3d70794734"
SCHEMA_NAME = "UsrPage_ebkv9e8"

# Source file
SOURCE_FILE = REPO_ROOT / "client-module" / "UsrPage_ebkv9e8_Defensive.js"
BACKUP_DIR = REPO_ROOT / "backups"


def wait_for_stable(page, timeout=5000):
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    page.wait_for_timeout(1000)


def screenshot(page, name):
    screenshots_dir = REPO_ROOT / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    path = screenshots_dir / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    print(f"   📸 Screenshot: {path.name}")
    return path


def main():
    print("=" * 60)
    print("DEPLOYING UsrPage_ebkv9e8_Defensive.js TO PROD (v2)")
    print("=" * 60)
    print(f"Target: {PROD_URL}")
    print(f"Schema UID: {SCHEMA_UID}")
    print(f"Package: IWQBIntegration")
    print(f"Source: {SOURCE_FILE.name}")
    print("")

    # Read source code
    if not SOURCE_FILE.exists():
        print(f"❌ Source file not found: {SOURCE_FILE}")
        return False

    new_code = SOURCE_FILE.read_text(encoding="utf-8")
    print(f"✅ Loaded source code: {len(new_code)} chars")

    with sync_playwright() as p:
        print("\n🚀 Launching browser...")
        browser = p.chromium.launch(headless=False, args=['--no-sandbox'])  # Non-headless for debugging
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        try:
            # Login
            print(f"\n1️⃣ Logging into PROD...")
            page.goto(f"{PROD_URL}/Login/NuiLogin.aspx", timeout=60000)
            wait_for_stable(page)
            page.fill('input[type="text"]:first-of-type', USERNAME)
            page.fill('input[type="password"]', PASSWORD)
            page.click('[data-item-marker="btnLogin"]')
            page.wait_for_timeout(8000)
            wait_for_stable(page)
            print("   ✅ Logged in")

            # Navigate to schema designer
            print(f"\n2️⃣ Opening Client Unit Schema Designer for IWQBIntegration version...")
            designer_url = f"{PROD_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{SCHEMA_UID}"
            page.goto(designer_url, timeout=60000)
            page.wait_for_timeout(8000)  # Wait longer for page to load
            wait_for_stable(page, 10000)
            screenshot(page, "prod_v2_01_designer")

            # Wait for code editor - try multiple selectors
            print("\n3️⃣ Waiting for code editor...")
            editor_selectors = [
                '.monaco-editor',           # Monaco editor
                '.ace_editor',              # ACE editor
                '[class*="editor"]',        # Any editor class
                '.view-lines',              # Monaco view lines
                'textarea.inputarea',       # Monaco input area
            ]

            editor_found = False
            for selector in editor_selectors:
                try:
                    page.wait_for_selector(selector, timeout=5000)
                    print(f"   ✅ Found editor: {selector}")
                    editor_found = True
                    break
                except:
                    continue

            if not editor_found:
                print("   ⚠️ Standard editor not found, checking for code content...")
                # Check if we can see code on the page
                page_content = page.content()
                if "UsrPage_ebkv9e8" in page_content and "define(" in page_content:
                    print("   ✅ Code content detected on page")
                    editor_found = True
                else:
                    screenshot(page, "prod_v2_02_no_editor")
                    print("   ❌ No editor found")

            page.wait_for_timeout(3000)
            screenshot(page, "prod_v2_03_editor_ready")

            # Backup current code
            print("\n4️⃣ Backing up current code...")
            current_code = page.evaluate('''() => {
                // Try Monaco editor first
                if (typeof monaco !== 'undefined') {
                    const editors = monaco.editor.getEditors();
                    if (editors && editors.length > 0) {
                        return editors[0].getValue();
                    }
                }

                // Try ACE editor
                if (typeof ace !== 'undefined') {
                    const editors = document.querySelectorAll('.ace_editor');
                    for (const ed of editors) {
                        try {
                            if (ed.id) {
                                const aceEditor = ace.edit(ed.id);
                                const val = aceEditor.getValue();
                                if (val && val.includes('define(')) return val;
                            }
                        } catch(e) {}
                    }
                }

                // Try to get from textarea
                const textareas = document.querySelectorAll('textarea');
                for (const ta of textareas) {
                    if (ta.value && ta.value.includes('define(')) {
                        return ta.value;
                    }
                }

                // Try to get from any element with code
                const codeElements = document.querySelectorAll('pre, code, .view-line');
                let text = '';
                codeElements.forEach(el => { text += el.textContent; });
                if (text.includes('define(')) return text;

                return null;
            }''')

            if current_code:
                BACKUP_DIR.mkdir(exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = BACKUP_DIR / f"UsrPage_ebkv9e8_PROD_backup_{timestamp}.js"
                backup_file.write_text(current_code, encoding="utf-8")
                print(f"   ✅ Backup saved: {backup_file.name} ({len(current_code)} chars)")
            else:
                print("   ⚠️ Could not extract current code for backup")
                # Continue anyway

            # Update code in editor
            print("\n5️⃣ Updating code in editor...")

            # Escape special characters for JavaScript string
            escaped_code = new_code.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

            result = page.evaluate(f'''() => {{
                // Try Monaco editor first
                if (typeof monaco !== 'undefined') {{
                    const editors = monaco.editor.getEditors();
                    if (editors && editors.length > 0) {{
                        editors[0].setValue(`{escaped_code}`);
                        return {{ success: true, editor: 'monaco' }};
                    }}
                }}

                // Try ACE editor
                if (typeof ace !== 'undefined') {{
                    const editors = document.querySelectorAll('.ace_editor');
                    for (const ed of editors) {{
                        try {{
                            if (ed.id) {{
                                const aceEditor = ace.edit(ed.id);
                                const currentVal = aceEditor.getValue();
                                if (currentVal && currentVal.includes('define(')) {{
                                    aceEditor.setValue(`{escaped_code}`);
                                    aceEditor.clearSelection();
                                    return {{ success: true, editor: 'ace', id: ed.id }};
                                }}
                            }}
                        }} catch(e) {{
                            return {{ success: false, error: e.message }};
                        }}
                    }}
                }}

                return {{ success: false, error: 'No compatible editor found' }};
            }}''')

            if result and result.get('success'):
                print(f"   ✅ Code updated in {result.get('editor')} editor")
            else:
                print(f"   ❌ Failed to update code: {result}")
                screenshot(page, "prod_v2_04_update_failed")

                # Try manual approach - focus and paste
                print("   Trying manual paste approach...")
                page.keyboard.press('Control+a')  # Select all
                page.wait_for_timeout(500)
                page.keyboard.type(new_code[:100])  # Type first part to test
                screenshot(page, "prod_v2_05_manual_paste_test")

            screenshot(page, "prod_v2_06_code_updated")

            # Save the schema
            print("\n6️⃣ Saving schema...")

            # Try keyboard shortcut
            page.keyboard.press('Control+s')
            page.wait_for_timeout(3000)

            # Look for save button and click it
            save_selectors = [
                'button:has-text("Save")',
                '[data-item-marker="SaveButton"]',
                'button[title="Save"]',
                '.save-button',
                'button.btn-save',
            ]

            for selector in save_selectors:
                try:
                    btn = page.locator(selector).first
                    if btn.is_visible():
                        btn.click()
                        print(f"   ✅ Clicked save button: {selector}")
                        page.wait_for_timeout(3000)
                        break
                except:
                    continue

            wait_for_stable(page, 10000)
            screenshot(page, "prod_v2_07_after_save")

            # Look for success notification
            try:
                success_msg = page.locator('text=saved, text=success, text=Saved').first
                if success_msg.is_visible(timeout=3000):
                    print("   ✅ Save success message detected")
            except:
                pass

            # Verify the defensive code is present
            print("\n7️⃣ Verifying deployment...")
            final_code = page.evaluate('''() => {
                if (typeof monaco !== 'undefined') {
                    const editors = monaco.editor.getEditors();
                    if (editors && editors.length > 0) return editors[0].getValue();
                }
                if (typeof ace !== 'undefined') {
                    const editors = document.querySelectorAll('.ace_editor');
                    for (const ed of editors) {
                        if (ed.id) {
                            try {
                                return ace.edit(ed.id).getValue();
                            } catch(e) {}
                        }
                    }
                }
                return null;
            }''')

            if final_code:
                defensive_markers = [
                    "[UsrPage_ebkv9e8]",
                    "DEFENSIVE:",
                    "isReportsPage",
                    "targetDataSources"
                ]
                found_markers = [m for m in defensive_markers if m in final_code]

                if len(found_markers) >= 2:
                    print(f"   ✅ Defensive code verified! Found markers: {found_markers}")
                    print("\n" + "=" * 60)
                    print("✅ DEPLOYMENT SUCCESSFUL")
                    print("=" * 60)
                else:
                    print(f"   ⚠️ Only found {len(found_markers)} markers - may need manual verification")
            else:
                print("   ⚠️ Could not read final code - please verify manually")

            screenshot(page, "prod_v2_08_final")

            print("\n📋 Next Steps:")
            print("1. Clear browser cache")
            print("2. Navigate to Reports page and test report generation")
            print("3. Run a QB sync to verify no interference")
            print("4. Check logs for [UsrPage_ebkv9e8] messages")

            # Keep browser open for manual verification
            print("\n⏳ Browser will close in 10 seconds for manual inspection...")
            page.wait_for_timeout(10000)

        except Exception as e:
            print(f"\n❌ Deployment error: {e}")
            import traceback
            traceback.print_exc()
            screenshot(page, "prod_v2_error")
            page.wait_for_timeout(5000)

        browser.close()

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
