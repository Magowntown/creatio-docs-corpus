#!/usr/bin/env python3
"""
Creatio Schema Extractor
Extracts full schema code and finds button handler examples
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
TARGET_SCHEMA = "UsrPage_ebkv9e8"
SCHEMA_UID = "1d5dfc4d-732d-48d7-af21-9e3d70794734"

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
    print(f"   ✅ Logged in")

    # Open schema designer directly
    print(f"\n2️⃣ Opening schema designer for {TARGET_SCHEMA}...")
    designer_url = f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{SCHEMA_UID}"
    page.goto(designer_url, timeout=30000)
    page.wait_for_timeout(5000)
    wait_for_stable(page)
    screenshot(page, "extract_01_designer")

    # Wait for Ace editor to fully load
    page.wait_for_selector('.ace_editor', timeout=15000)
    page.wait_for_timeout(2000)

    # Extract code using multiple methods
    print("\n3️⃣ Extracting schema code...")

    code_content = page.evaluate('''() => {
        // Method 1: Use ace.edit on each editor element
        const editors = document.querySelectorAll('.ace_editor');
        const results = [];

        for (let i = 0; i < editors.length; i++) {
            try {
                // Get the editor ID
                const editorId = editors[i].id;
                if (editorId) {
                    const aceEditor = ace.edit(editorId);
                    const value = aceEditor.getValue();
                    if (value && value.length > 50) {
                        results.push({
                            id: editorId,
                            index: i,
                            length: value.length,
                            content: value
                        });
                    }
                }
            } catch(e) {
                // Try getting content directly from DOM
                try {
                    const lines = editors[i].querySelectorAll('.ace_line');
                    let text = '';
                    lines.forEach(line => { text += line.textContent + '\\n'; });
                    if (text.length > 50) {
                        results.push({
                            id: 'dom-extract-' + i,
                            index: i,
                            length: text.length,
                            content: text
                        });
                    }
                } catch(e2) {}
            }
        }

        // Method 2: Try to find ace in global scope
        if (results.length === 0 && typeof ace !== 'undefined') {
            try {
                // Get all editor instances
                if (ace.edit) {
                    const allEditors = document.querySelectorAll('.ace_editor');
                    allEditors.forEach((el, i) => {
                        try {
                            const ed = ace.edit(el);
                            const val = ed.getValue();
                            if (val) results.push({id: 'global-' + i, length: val.length, content: val});
                        } catch(e) {}
                    });
                }
            } catch(e) {}
        }

        return results;
    }''')

    if code_content and len(code_content) > 0:
        print(f"   ✅ Found {len(code_content)} editor(s) with content")

        for editor in code_content:
            print(f"      - Editor {editor.get('id')}: {editor.get('length')} chars")

            # Save the main schema code
            content = editor.get('content', '')
            if 'define(' in content and TARGET_SCHEMA in content:
                output_file = ARTIFACTS_DIR / f"{TARGET_SCHEMA}_schema.js"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   📄 Saved schema to: {output_file}")

                # Analyze the schema
                print(f"\n   Schema Analysis:")
                print(f"      - Contains viewConfigDiff: {'viewConfigDiff' in content}")
                print(f"      - Contains viewModelConfigDiff: {'viewModelConfigDiff' in content}")
                print(f"      - Contains handlers: {'handlers:' in content}")
                print(f"      - Contains Button_bwctkw5: {'Button_bwctkw5' in content}")
                print(f"      - Contains LookupAttribute_bsixu8a: {'LookupAttribute_bsixu8a' in content}")

                # Extract handlers section
                if '/**SCHEMA_HANDLERS*/' in content:
                    start = content.find('/**SCHEMA_HANDLERS*/')
                    end = content.find('/**SCHEMA_HANDLERS*/', start + 20)
                    if start >= 0 and end > start:
                        handlers = content[start:end+len('/**SCHEMA_HANDLERS*/')]
                        print(f"\n   Current handlers section:\n   {handlers}")
    else:
        print("   ⚠ No code extracted via JavaScript")

        # Try DOM-based extraction
        print("   Trying DOM-based extraction...")
        lines = page.locator('.ace_line').all()
        if lines:
            content_lines = []
            for line in lines:
                try:
                    content_lines.append(line.inner_text())
                except:
                    pass
            content = '\n'.join(content_lines)
            if content:
                print(f"   Got {len(content)} chars from DOM")
                output_file = ARTIFACTS_DIR / f"{TARGET_SCHEMA}_schema_dom.js"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   📄 Saved to: {output_file}")

    # Now find a working button handler example
    print("\n4️⃣ Finding button handler examples...")

    # Look for BGIntExcelreportMixin which handles Excel reports
    example_schemas = [
        "BGIntExcelreportMixin",
        "BGHome_Homepage",
        "BGFactoryOrders1Page",
    ]

    for schema_name in example_schemas:
        print(f"\n   Searching for {schema_name}...")

        # Query for schema UID
        schema_info = page.evaluate(f'''async () => {{
            try {{
                const response = await fetch('/0/odata/SysSchema?$filter=Name eq \\'{schema_name}\\'&$select=UId,Name,ManagerName&$top=1');
                const data = await response.json();
                return data;
            }} catch(e) {{
                return {{error: e.message}};
            }}
        }}''')

        if schema_info and 'value' in schema_info and len(schema_info['value']) > 0:
            example_uid = schema_info['value'][0].get('UId')
            print(f"      Found UID: {example_uid}")

            # Navigate to this schema to see its code
            page.goto(f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{example_uid}", timeout=30000)
            page.wait_for_timeout(4000)
            wait_for_stable(page)

            # Extract its code
            example_code = page.evaluate('''() => {
                const editors = document.querySelectorAll('.ace_editor');
                for (const ed of editors) {
                    try {
                        if (ed.id) {
                            const aceEditor = ace.edit(ed.id);
                            const val = aceEditor.getValue();
                            if (val && val.includes('handlers')) return val;
                        }
                    } catch(e) {}
                }

                // DOM fallback
                const lines = document.querySelectorAll('.ace_line');
                let text = '';
                lines.forEach(line => { text += line.textContent + '\\n'; });
                return text;
            }''')

            if example_code and 'handlers' in example_code:
                output_file = ARTIFACTS_DIR / f"{schema_name}_example.js"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(example_code)
                print(f"      📄 Saved example to: {output_file}")

                # Extract handlers from example
                if '/**SCHEMA_HANDLERS*/' in example_code:
                    start = example_code.find('/**SCHEMA_HANDLERS*/')
                    end = example_code.find('/**SCHEMA_HANDLERS*/', start + 20)
                    if end > start:
                        handlers = example_code[start:end+len('/**SCHEMA_HANDLERS*/')]
                        if len(handlers) > 50:
                            print(f"      HANDLERS FOUND ({len(handlers)} chars):")
                            print(f"      {handlers[:500]}...")
                            break

    screenshot(page, "extract_02_final")

    print("\n" + "="*60)
    print("EXTRACTION COMPLETE")
    print("="*60)

    browser.close()
    print("\n✅ Done!")
