#!/usr/bin/env python3
"""
Creatio UI Schema Access
Opens schema through the Configuration UI designer
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

# Schema UID from API discovery
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

    # Navigate to Configuration
    print("\n2️⃣ Opening Configuration...")
    page.goto(f"{CREATIO_URL}/0/ClientApp/#/WorkspaceExplorer", timeout=30000)
    page.wait_for_timeout(4000)
    wait_for_stable(page)
    screenshot(page, "ui_01_config")

    # Try to find UsrTestApp package and expand it
    print("\n3️⃣ Expanding UsrTestApp package...")

    # First look in the packages list on the left
    usr_test_app = page.locator('text=UsrTestApp')
    if usr_test_app.count() > 0:
        print("   Found UsrTestApp, clicking to expand...")
        usr_test_app.first.click()
        page.wait_for_timeout(2000)
        screenshot(page, "ui_02_package")

    # Try direct URL with schema UID
    print(f"\n4️⃣ Trying direct designer URL with UID...")
    designer_url = f"{CREATIO_URL}/0/Nui/ViewModule.aspx#ClientUnitSchemaDesigner/{SCHEMA_UID}"
    print(f"   URL: {designer_url}")
    page.goto(designer_url, timeout=30000)
    page.wait_for_timeout(5000)
    wait_for_stable(page)
    screenshot(page, "ui_03_designer")

    # Check for code editor
    print("\n5️⃣ Looking for code editor...")
    editor_types = {
        'ace': page.locator('[class*="ace"]').count(),
        'monaco': page.locator('[class*="monaco"]').count(),
        'textarea': page.locator('textarea').count(),
    }
    print(f"   Editor elements: {editor_types}")

    # If no editor, try the new Angular-based designer URL
    if sum(editor_types.values()) == 0:
        print("\n6️⃣ Trying Angular ClientApp designer...")
        angular_urls = [
            f"{CREATIO_URL}/0/ClientApp/#/SchemaDesigner/{SCHEMA_UID}",
            f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{SCHEMA_UID}",
            f"{CREATIO_URL}/0/ClientApp/#/WorkspaceExplorer/ClientUnitSchemaDesigner/{SCHEMA_UID}",
        ]

        for url in angular_urls:
            print(f"   Trying: {url.split('#')[-1][:50]}")
            page.goto(url, timeout=20000)
            page.wait_for_timeout(4000)
            wait_for_stable(page)

            # Check for editor or schema content
            ace_count = page.locator('[class*="ace"]').count()
            monaco_count = page.locator('[class*="monaco"]').count()
            print(f"      ace={ace_count}, monaco={monaco_count}")

            if ace_count > 0 or monaco_count > 0:
                screenshot(page, "ui_04_editor_found")
                break

            screenshot(page, f"ui_04_{url.split('#')[-1].replace('/','-')[:30]}")

    # Try to click on Open Source Code link if visible
    print("\n7️⃣ Looking for 'Open source code' option...")
    source_options = [
        'text=Open source code',
        'text=Source code',
        '[data-item-marker="OpenSourceCodeButton"]',
        'a:has-text("Source")',
        'button:has-text("Source")',
    ]

    for opt in source_options:
        try:
            locator = page.locator(opt)
            if locator.count() > 0:
                print(f"   Found: {opt}")
                locator.first.click()
                page.wait_for_timeout(3000)
                wait_for_stable(page)
                screenshot(page, "ui_05_source_clicked")
                break
        except:
            pass

    # Get page information
    print("\n8️⃣ Getting page information...")

    # Check for Freedom UI elements
    freedom_elements = page.evaluate('''() => {
        const elements = [];
        // Look for crt- prefixed components (Creatio Freedom UI)
        document.querySelectorAll('[class*="crt-"]').forEach(el => {
            const classes = el.className;
            if (typeof classes === 'string') {
                elements.push(classes.split(' ').find(c => c.startsWith('crt-')));
            }
        });
        return [...new Set(elements)].slice(0, 20);
    }''')
    print(f"   Freedom UI components: {freedom_elements}")

    # Document all buttons and actions available
    buttons = page.locator('button, [role="button"]').all()
    print(f"\n   Available buttons ({len(buttons)}):")
    for btn in buttons[:20]:
        try:
            text = btn.inner_text()[:40].strip() if btn.inner_text() else ''
            marker = btn.get_attribute('data-item-marker') or ''
            if text or marker:
                print(f"      - '{text}' [{marker}]")
        except:
            pass

    # Try to extract schema content from page
    print("\n9️⃣ Attempting to extract schema content...")

    # Try various methods
    code_content = page.evaluate('''() => {
        // Try ace editor
        const aceEditors = document.querySelectorAll('.ace_editor');
        for (const ed of aceEditors) {
            try {
                if (typeof ace !== 'undefined') {
                    const aceEditor = ace.edit(ed);
                    const val = aceEditor.getValue();
                    if (val && val.length > 100) return {source: 'ace', content: val};
                }
            } catch(e) {}
        }

        // Try monaco
        if (typeof monaco !== 'undefined') {
            const editors = monaco.editor.getEditors();
            if (editors && editors.length) {
                return {source: 'monaco', content: editors[0].getValue()};
            }
        }

        // Try to find schema in window object
        if (typeof window.schema !== 'undefined') {
            return {source: 'window.schema', content: JSON.stringify(window.schema)};
        }

        // Try Terrasoft
        if (typeof Terrasoft !== 'undefined') {
            try {
                const schemas = Terrasoft.ClientSchemaManager?.schemas;
                if (schemas) {
                    return {source: 'Terrasoft', content: JSON.stringify(Object.keys(schemas))};
                }
            } catch(e) {}
        }

        return null;
    }''')

    if code_content:
        print(f"   ✅ Found code from: {code_content.get('source')}")
        content = code_content.get('content', '')
        print(f"   Content length: {len(content)} chars")

        # Save the content
        output_file = ARTIFACTS_DIR / f"creatio_{TARGET_SCHEMA}_code.js"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   Saved to: {output_file}")

        # Show handlers if present
        if '/**SCHEMA_HANDLERS*/' in content:
            start = content.find('/**SCHEMA_HANDLERS*/')
            end = content.find('/**SCHEMA_HANDLERS*/', start + 20)
            if start >= 0 and end > start:
                handlers = content[start:end+len('/**SCHEMA_HANDLERS*/')]
                print(f"\n   HANDLERS SECTION:\n{handlers}")
    else:
        print("   ⚠ No code content extracted")

    # Final screenshot
    screenshot(page, "ui_10_final")

    print("\n" + "="*60)
    print(f"Final URL: {page.url}")
    print("="*60)

    browser.close()
    print("\n✅ Done!")
