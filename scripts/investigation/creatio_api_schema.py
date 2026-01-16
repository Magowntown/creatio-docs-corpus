#!/usr/bin/env python3
"""
Creatio API Schema Access
Uses REST API to fetch schema content directly
"""

from playwright.sync_api import sync_playwright
import os
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import SCREENSHOTS_DIR, ensure_dirs

ensure_dirs()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
SCREENSHOT_DIR = str(SCREENSHOTS_DIR)
TARGET_SCHEMA = "UsrPage_ebkv9e8"

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
    page.fill('input[type="text"]:first-of-type', USERNAME)
    page.fill('input[type="password"]', PASSWORD)
    page.click('[data-item-marker="btnLogin"]')
    page.wait_for_timeout(5000)
    wait_for_stable(page)
    print(f"   ✅ Logged in. URL: {page.url}")

    # Now use the authenticated session to query the API
    print("\n2️⃣ Querying schema via API...")

    # Try to find schema UID first via OData
    schema_info = page.evaluate(f'''async () => {{
        try {{
            // Query for schema metadata
            const response = await fetch('/0/odata/SysSchema?$filter=Name eq \\'{TARGET_SCHEMA}\\'&$select=UId,Name,ManagerName');
            const data = await response.json();
            return data;
        }} catch(e) {{
            return {{error: e.message}};
        }}
    }}''')
    print(f"   Schema query result: {json.dumps(schema_info, indent=2)[:500]}")

    # Try to get the schema content using SourceCodeService
    print("\n3️⃣ Fetching schema content...")

    schema_content = page.evaluate(f'''async () => {{
        try {{
            // Alternative: Use the client schema manager
            const response = await fetch('/0/rest/SchemaDesignerService/GetSchema', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    schemaName: '{TARGET_SCHEMA}'
                }})
            }});
            const data = await response.json();
            return data;
        }} catch(e) {{
            return {{error: e.message}};
        }}
    }}''')
    print(f"   SchemaDesignerService result: {json.dumps(schema_content, indent=2)[:1000]}")

    # Try PackageSchemaDataService
    print("\n4️⃣ Trying PackageSchemaDataService...")

    package_schema = page.evaluate(f'''async () => {{
        try {{
            const response = await fetch('/0/rest/PackageSchemaDataService/GetSchemaSource', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    schemaName: '{TARGET_SCHEMA}'
                }})
            }});
            const data = await response.json();
            return data;
        }} catch(e) {{
            return {{error: e.message}};
        }}
    }}''')
    print(f"   PackageSchemaDataService result: {json.dumps(package_schema, indent=2)[:1000]}")

    # Try SourceCodeSchemaDesignerService
    print("\n5️⃣ Trying SourceCodeSchemaDesignerService...")

    source_code = page.evaluate(f'''async () => {{
        try {{
            const response = await fetch('/0/rest/SourceCodeSchemaDesignerService/GetSchemaSource', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json'
                }},
                body: JSON.stringify({{
                    schemaName: '{TARGET_SCHEMA}'
                }})
            }});
            const text = await response.text();
            return text;
        }} catch(e) {{
            return e.message;
        }}
    }}''')
    print(f"   SourceCodeSchemaDesignerService result: {source_code[:1000] if source_code else 'None'}")

    # Navigate to the actual page to see what schema it uses
    print("\n6️⃣ Navigating to UsrPage to inspect...")
    # Try direct navigation to the page URL
    page.goto(f"{CREATIO_URL}/0/ClientApp/#/{TARGET_SCHEMA}", timeout=30000)
    page.wait_for_timeout(4000)
    wait_for_stable(page)
    screenshot(page, "api_01_page")

    # Check what the current page's schema is
    page_schema = page.evaluate('''() => {
        try {
            // Try to access Terrasoft client schema manager
            if (typeof Terrasoft !== 'undefined' && Terrasoft.ClientSchemaManager) {
                return Terrasoft.ClientSchemaManager.getItems();
            }
            return 'Terrasoft not available';
        } catch(e) {
            return e.message;
        }
    }''')
    print(f"   Page schema info: {str(page_schema)[:500]}")

    # Try the Configuration URL to open the schema in designer
    print("\n7️⃣ Opening in Configuration designer...")

    # Get list of all client schemas from API
    all_schemas = page.evaluate('''async () => {
        try {
            const response = await fetch('/0/odata/SysSchema?$filter=ManagerName eq \\'ClientUnitSchemaManager\\'&$select=UId,Name&$top=50');
            const data = await response.json();
            return data;
        } catch(e) {
            return {error: e.message};
        }
    }''')
    print(f"\n   Client unit schemas found: {len(all_schemas.get('value', [])) if isinstance(all_schemas, dict) else 'error'}")

    if isinstance(all_schemas, dict) and 'value' in all_schemas:
        # Find our schema
        for schema in all_schemas['value']:
            if 'UsrPage' in schema.get('Name', ''):
                print(f"      - {schema.get('Name')}: {schema.get('UId')}")

    # Look for schema with the exact name
    print(f"\n8️⃣ Searching for {TARGET_SCHEMA} specifically...")

    specific_schema = page.evaluate(f'''async () => {{
        try {{
            const response = await fetch('/0/odata/SysSchema?$filter=contains(Name,\\'{TARGET_SCHEMA}\\')&$select=UId,Name,ManagerName');
            const data = await response.json();
            return data;
        }} catch(e) {{
            return {{error: e.message}};
        }}
    }}''')
    print(f"   Specific schema search: {json.dumps(specific_schema, indent=2)}")

    # If we found a UID, try to get the source
    if isinstance(specific_schema, dict) and specific_schema.get('value'):
        schema_uid = specific_schema['value'][0].get('UId')
        print(f"\n   Found schema UID: {schema_uid}")

        # Try to get source by UID
        source_by_uid = page.evaluate(f'''async () => {{
            try {{
                const response = await fetch('/0/rest/SourceCodeSchemaDesignerService/GetSchemaSource', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{schemaUId: '{schema_uid}'}})
                }});
                return await response.text();
            }} catch(e) {{
                return e.message;
            }}
        }}''')
        print(f"   Source by UID: {source_by_uid[:500] if source_by_uid else 'None'}")

    screenshot(page, "api_02_final")

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Final URL: {page.url}")

    browser.close()
    print("\n✅ Done!")
