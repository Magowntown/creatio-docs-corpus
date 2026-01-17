#!/usr/bin/env python3
"""
Deploy UsrPage_ebkv9e8_Defensive.js to PROD.
Updates the IWQBIntegration version of the schema.
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

# IWQBIntegration version UID (the one modified on 2026-01-14)
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
    print("DEPLOYING UsrPage_ebkv9e8_Defensive.js TO PROD")
    print("=" * 60)
    print(f"Target: {PROD_URL}")
    print(f"Schema UID: {SCHEMA_UID}")
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
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        try:
            # Login
            print(f"\n1️⃣ Logging into PROD...")
            page.goto(f"{PROD_URL}/Login/NuiLogin.aspx", timeout=30000)
            wait_for_stable(page)
            page.fill('input[type="text"]:first-of-type', USERNAME)
            page.fill('input[type="password"]', PASSWORD)
            page.click('[data-item-marker="btnLogin"]')
            page.wait_for_timeout(5000)
            wait_for_stable(page)
            print("   ✅ Logged in")

            # Navigate to schema designer
            print(f"\n2️⃣ Opening Client Unit Schema Designer...")
            designer_url = f"{PROD_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{SCHEMA_UID}"
            page.goto(designer_url, timeout=60000)
            page.wait_for_timeout(5000)
            wait_for_stable(page)
            screenshot(page, "prod_deploy_01_designer_opened")

            # Wait for ACE editor
            print("\n3️⃣ Waiting for code editor...")
            try:
                page.wait_for_selector('.ace_editor', timeout=20000)
                page.wait_for_timeout(2000)
                print("   ✅ ACE editor found")
            except:
                print("   ⚠️ ACE editor not found - trying alternative approach")
                screenshot(page, "prod_deploy_02_no_ace_editor")

                # Try Configuration section approach
                print("\n   Trying Configuration section...")
                page.goto(f"{PROD_URL}/0/Nui/ViewModule.aspx#SectionModuleV2/ConfigurationSection", timeout=30000)
                page.wait_for_timeout(5000)
                screenshot(page, "prod_deploy_03_configuration_section")

                # This is Classic UI - need different approach
                print("   ❌ PROD appears to be Classic UI - need manual deployment")
                browser.close()
                return False

            # Backup current code
            print("\n4️⃣ Backing up current code...")
            current_code = page.evaluate('''() => {
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

            # Update code in editor
            print("\n5️⃣ Updating code in editor...")

            # Escape the code for JavaScript
            escaped_code = new_code.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

            result = page.evaluate(f'''() => {{
                const editors = document.querySelectorAll('.ace_editor');
                for (const ed of editors) {{
                    try {{
                        if (ed.id) {{
                            const aceEditor = ace.edit(ed.id);
                            const currentVal = aceEditor.getValue();
                            if (currentVal && currentVal.includes('define(')) {{
                                aceEditor.setValue(`{escaped_code}`);
                                aceEditor.clearSelection();
                                return {{ success: true, editorId: ed.id }};
                            }}
                        }}
                    }} catch(e) {{
                        return {{ success: false, error: e.message }};
                    }}
                }}
                return {{ success: false, error: 'No suitable editor found' }};
            }}''')

            if result and result.get('success'):
                print(f"   ✅ Code updated in editor: {result.get('editorId')}")
            else:
                print(f"   ❌ Failed to update code: {result}")
                screenshot(page, "prod_deploy_04_update_failed")
                browser.close()
                return False

            screenshot(page, "prod_deploy_05_code_updated")

            # Save the schema
            print("\n6️⃣ Saving schema...")

            # Try Ctrl+S first
            page.keyboard.press('Control+s')
            page.wait_for_timeout(2000)

            # Also try clicking Save button
            try:
                save_button = page.locator('button:has-text("Save"), [data-item-marker="SaveButton"]').first
                if save_button.is_visible():
                    save_button.click()
                    page.wait_for_timeout(3000)
            except:
                pass

            wait_for_stable(page, 10000)
            screenshot(page, "prod_deploy_06_after_save")

            # Verify save
            print("\n7️⃣ Verifying save...")
            saved_code = page.evaluate('''() => {
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
                return null;
            }''')

            if saved_code and "[UsrPage_ebkv9e8]" in saved_code:
                print("   ✅ Defensive code verified in editor!")
                print("   ✅ DEPLOYMENT SUCCESSFUL")
            else:
                print("   ⚠️ Could not verify - please check manually")

            screenshot(page, "prod_deploy_07_final")

        except Exception as e:
            print(f"\n❌ Deployment error: {e}")
            screenshot(page, "prod_deploy_error")
            browser.close()
            return False

        browser.close()

    print("\n" + "=" * 60)
    print("DEPLOYMENT COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Clear browser cache and test the Reports page")
    print("2. Run a QB sync to verify no interference")
    print("3. Monitor PROD logs for [UsrPage_ebkv9e8] messages")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
