#!/usr/bin/env python3
"""
Extract OrderPageV2 schema from PROD via browser automation.
Analyzes for PaymentStatus default settings.
"""

from playwright.sync_api import sync_playwright
import os
import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / ".env")

PROD_URL = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_PROD_USERNAME", "Supervisor")
PASSWORD = os.environ.get("CREATIO_PROD_PASSWORD", "")

# OrderPageV2 in IWQBIntegration
SCHEMA_UID = "6c9e5e8b-9d0b-41b4-b24d-bec395eb68bf"

OUTPUT_DIR = REPO_ROOT / "client-module"


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
    print(f"   Screenshot: {path.name}")
    return path


def main():
    print("=" * 60)
    print("EXTRACTING OrderPageV2 FROM PROD (IWQBIntegration)")
    print("=" * 60)
    print(f"Target: {PROD_URL}")
    print(f"Schema UID: {SCHEMA_UID}")
    print("")

    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        try:
            # Login
            print("\n1. Logging into PROD...")
            page.goto(f"{PROD_URL}/Login/NuiLogin.aspx", timeout=60000)
            wait_for_stable(page)
            page.fill('input[type="text"]:first-of-type', USERNAME)
            page.fill('input[type="password"]', PASSWORD)
            page.click('[data-item-marker="btnLogin"]')
            page.wait_for_timeout(8000)
            wait_for_stable(page)
            print("   Logged in")

            # Navigate to schema designer
            print(f"\n2. Opening OrderPageV2 in Schema Designer...")
            designer_url = f"{PROD_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{SCHEMA_UID}"
            page.goto(designer_url, timeout=60000)
            page.wait_for_timeout(8000)
            wait_for_stable(page, 10000)
            screenshot(page, "orderpagev2_01_designer")

            # Extract code from editor
            print("\n3. Extracting schema code...")
            code = page.evaluate('''() => {
                // Try Monaco editor
                if (typeof monaco !== 'undefined') {
                    const editors = monaco.editor.getEditors();
                    if (editors && editors.length > 0) {
                        return { source: 'monaco', code: editors[0].getValue() };
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
                                if (val && val.includes('define(')) {
                                    return { source: 'ace', code: val };
                                }
                            }
                        } catch(e) {}
                    }
                }

                // Try DOM extraction
                const lines = document.querySelectorAll('.ace_line, .view-line');
                let text = '';
                lines.forEach(line => { text += line.textContent + '\\n'; });
                if (text.includes('define(')) {
                    return { source: 'dom', code: text };
                }

                return { source: null, code: null };
            }''')

            if code and code.get('code'):
                schema_code = code['code']
                print(f"   Extracted via {code['source']}: {len(schema_code)} chars")

                # Save to file
                output_file = OUTPUT_DIR / "OrderPageV2_IWQBIntegration_PROD.js"
                output_file.write_text(schema_code, encoding="utf-8")
                print(f"   Saved to: {output_file.name}")

                # Analyze for PaymentStatus
                print("\n4. Analyzing for PaymentStatus references...")

                findings = []

                if "PaymentStatus" in schema_code:
                    findings.append("FOUND: 'PaymentStatus' in schema")
                    lines = schema_code.split('\n')
                    for i, line in enumerate(lines):
                        if "PaymentStatus" in line:
                            print(f"   Line {i+1}: {line.strip()[:100]}")

                if "Planned" in schema_code:
                    findings.append("FOUND: 'Planned' string")
                    lines = schema_code.split('\n')
                    for i, line in enumerate(lines):
                        if "Planned" in line:
                            print(f"   Line {i+1}: {line.strip()[:100]}")

                # Check for the Planned GUID
                if "bfe38d3d" in schema_code.lower():
                    findings.append("FOUND: Planned status GUID (bfe38d3d...)")

                # Check for defValue or defaultValue
                if "defValue" in schema_code.lower() or "defaultValue" in schema_code.lower():
                    findings.append("FOUND: Default value definition")
                    lines = schema_code.split('\n')
                    for i, line in enumerate(lines):
                        if "defValue" in line.lower() or "defaultValue" in line.lower():
                            print(f"   Line {i+1}: {line.strip()[:100]}")

                # Check for attribute handlers
                if "HandleViewModelAttributeChangeRequest" in schema_code:
                    findings.append("FOUND: HandleViewModelAttributeChangeRequest handler")

                if "LoadDataRequest" in schema_code:
                    findings.append("FOUND: LoadDataRequest handler")

                print("\n5. Summary of Findings:")
                if findings:
                    for f in findings:
                        print(f"   - {f}")
                else:
                    print("   - No PaymentStatus references found in client code")
                    print("   - Default may be set at entity level or in page descriptor")

            else:
                print("   Could not extract schema code")
                screenshot(page, "orderpagev2_02_no_code")

            # Also check the page for any visible PaymentStatus config
            print("\n6. Checking page content for PaymentStatus...")
            page_content = page.content()
            if "PaymentStatus" in page_content:
                print("   FOUND: PaymentStatus in page HTML")
            if "Planned" in page_content:
                print("   FOUND: 'Planned' in page HTML")

            screenshot(page, "orderpagev2_03_final")

        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
            screenshot(page, "orderpagev2_error")

        browser.close()

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print("\nNext: Check the extracted file for PaymentStatus default settings")
    print(f"File: {OUTPUT_DIR / 'OrderPageV2_IWQBIntegration_PROD.js'}")


if __name__ == "__main__":
    main()
