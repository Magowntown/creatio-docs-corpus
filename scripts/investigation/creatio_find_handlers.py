#!/usr/bin/env python3
"""
Find Freedom UI schemas with button handlers
"""

from playwright.sync_api import sync_playwright
import os
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import SCREENSHOTS_DIR, ARTIFACTS_DIR, ensure_dirs

ensure_dirs()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
SCREENSHOT_DIR = str(SCREENSHOTS_DIR)

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
    page.fill('input[type="text"]:first-of-type', USERNAME)
    page.fill('input[type="password"]', PASSWORD)
    page.click('[data-item-marker="btnLogin"]')
    page.wait_for_timeout(5000)
    wait_for_stable(page)
    print(f"   ✅ Logged in")

    # Get list of client unit schemas
    print("\n2️⃣ Querying client unit schemas...")

    schemas = page.evaluate('''async () => {
        try {
            const response = await fetch('/0/odata/SysSchema?$filter=ManagerName eq \\'ClientUnitSchemaManager\\'&$select=UId,Name&$top=100&$orderby=ModifiedOn desc');
            const data = await response.json();
            return data;
        } catch(e) {
            return {error: e.message};
        }
    }''')

    if schemas and 'value' in schemas:
        print(f"   Found {len(schemas['value'])} schemas")

        # Try to find schemas with non-empty handlers
        schemas_with_handlers = []

        # Check first 15 schemas for handlers
        for i, schema in enumerate(schemas['value'][:15]):
            uid = schema.get('UId')
            name = schema.get('Name')
            print(f"\n   [{i+1}/15] Checking {name}...")

            # Navigate to schema designer
            page.goto(f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{uid}", timeout=20000)
            page.wait_for_timeout(3000)
            wait_for_stable(page)

            # Try to extract handlers
            code = page.evaluate('''() => {
                // Try to get code from the page
                const body = document.body.innerText;
                if (body.includes('/**SCHEMA_HANDLERS*/')) {
                    const start = body.indexOf('/**SCHEMA_HANDLERS*/');
                    const end = body.indexOf('/**SCHEMA_HANDLERS*/', start + 20);
                    if (end > start) {
                        return body.substring(start, end + 21);
                    }
                }
                return '';
            }''')

            if code and len(code) > 50:
                # Check if handlers are not empty
                handlers_content = code.replace('/**SCHEMA_HANDLERS*/', '').strip()
                if handlers_content and handlers_content != '[]':
                    print(f"      ✅ Has handlers! ({len(handlers_content)} chars)")
                    schemas_with_handlers.append({
                        'name': name,
                        'uid': uid,
                        'handlers': handlers_content[:500]
                    })

                    # Save full code
                    full_code = page.evaluate('''() => {
                        const body = document.body.innerText;
                        const start = body.indexOf('define(');
                        if (start >= 0) {
                            return body.substring(start);
                        }
                        return '';
                    }''')

                    if full_code:
                        out_path = ARTIFACTS_DIR / f"{name}_with_handlers.js"
                        with open(out_path, 'w', encoding='utf-8') as f:
                            f.write(full_code)
                        print(f"      📄 Saved to {out_path}")

                    if len(schemas_with_handlers) >= 3:
                        break

        # Report findings
        print(f"\n" + "="*60)
        print(f"Found {len(schemas_with_handlers)} schemas with handlers:")
        for s in schemas_with_handlers:
            print(f"\n   {s['name']}:")
            print(f"   {s['handlers'][:200]}...")

    browser.close()
    print("\n✅ Done!")
