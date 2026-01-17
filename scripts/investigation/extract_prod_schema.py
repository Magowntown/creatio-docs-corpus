#!/usr/bin/env python3
"""
Extract UsrPage_ebkv9e8 schema code directly from PROD via browser automation.
"""

from playwright.sync_api import sync_playwright
import os
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / ".env")

PROD_URL = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_PROD_USERNAME", "Supervisor")
PASSWORD = os.environ.get("CREATIO_PROD_PASSWORD", "")

# All three schema UIDs found in PROD
SCHEMA_UIDS = [
    ("4e6a5aa6-86b7-48c1-9147-7b09e96ee59e", "BGlobalLookerStudio"),
    ("561d9dd4-8bf2-4f63-a781-54ac48a74972", "BGApp_eykaguu"),
    ("1d5dfc4d-732d-48d7-af21-9e3d70794734", "IWQBIntegration"),
]

OUTPUT_DIR = REPO_ROOT / "client-module"


def wait_for_stable(page, timeout=5000):
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    page.wait_for_timeout(1000)


def extract_code_from_editor(page):
    """Extract code from ACE editor on the page."""
    code = page.evaluate('''() => {
        // Method 1: Use ace.edit on each editor element
        const editors = document.querySelectorAll('.ace_editor');
        for (let i = 0; i < editors.length; i++) {
            try {
                const editorId = editors[i].id;
                if (editorId) {
                    const aceEditor = ace.edit(editorId);
                    const value = aceEditor.getValue();
                    if (value && value.length > 50 && value.includes('define(')) {
                        return value;
                    }
                }
            } catch(e) {}
        }

        // Method 2: DOM extraction
        const lines = document.querySelectorAll('.ace_line');
        let text = '';
        lines.forEach(line => { text += line.textContent + '\\n'; });
        if (text.includes('define(')) {
            return text;
        }

        return null;
    }''')
    return code


with sync_playwright() as p:
    print("=" * 60)
    print("EXTRACTING UsrPage_ebkv9e8 FROM PROD")
    print("=" * 60)

    print("\n🚀 Launching browser...")
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    # Login
    print(f"\n1️⃣ Logging into PROD ({PROD_URL})...")
    page.goto(f"{PROD_URL}/Login/NuiLogin.aspx", timeout=30000)
    wait_for_stable(page)
    page.fill('input[type="text"]:first-of-type', USERNAME)
    page.fill('input[type="password"]', PASSWORD)
    page.click('[data-item-marker="btnLogin"]')
    page.wait_for_timeout(5000)
    wait_for_stable(page)
    print(f"   ✅ Logged in")

    # Extract each schema version
    for uid, package_name in SCHEMA_UIDS:
        print(f"\n2️⃣ Opening schema designer for {package_name} version...")
        print(f"   UID: {uid}")

        designer_url = f"{PROD_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{uid}"
        page.goto(designer_url, timeout=30000)
        page.wait_for_timeout(5000)
        wait_for_stable(page)

        # Wait for ACE editor
        try:
            page.wait_for_selector('.ace_editor', timeout=15000)
            page.wait_for_timeout(2000)
        except:
            print(f"   ⚠️ No ACE editor found for {package_name}")
            continue

        # Extract code
        code = extract_code_from_editor(page)

        if code and len(code) > 100:
            output_file = OUTPUT_DIR / f"UsrPage_ebkv9e8_PROD_{package_name}.js"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"   ✅ Saved: {output_file.name} ({len(code)} chars)")

            # Analyze
            print(f"   Analysis:")
            print(f"      - Has handlers: {'handlers:' in code or 'handlers/**' in code}")
            print(f"      - Has viewConfigDiff: {'viewConfigDiff' in code}")
            print(f"      - Has LoadDataRequest: {'LoadDataRequest' in code}")
            print(f"      - Has IWPayments: {'IWPayments' in code}")
            print(f"      - Has QuickBooks/QB: {'QuickBooks' in code or 'QB' in code}")

            # Count handlers
            handler_count = code.count('request:')
            print(f"      - Handler count (approx): {handler_count}")
        else:
            print(f"   ❌ Could not extract code for {package_name}")

            # Try screenshot for debugging
            screenshot_path = OUTPUT_DIR / f"UsrPage_ebkv9e8_PROD_{package_name}_screenshot.png"
            page.screenshot(path=str(screenshot_path))
            print(f"   📸 Screenshot saved: {screenshot_path.name}")

    browser.close()

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
