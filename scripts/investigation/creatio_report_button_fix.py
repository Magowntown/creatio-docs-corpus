#!/usr/bin/env python3
"""
Creatio Report Button Fix
Opens UsrPage_ebkv9e8 schema and inspects/fixes the Report button handler
"""

from playwright.sync_api import sync_playwright
import os
import json
import time
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

def screenshot(page, name):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = f"{SCREENSHOT_DIR}/{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"📸 {name}")
    return path

def wait_for_stable(page, timeout=5000):
    """Wait for page to stabilize"""
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

    # ============================================
    # STEP 1: Login
    # ============================================
    print("\n1️⃣ Logging in...")
    page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
    wait_for_stable(page)

    page.fill('input[type="text"]:first-of-type', USERNAME)
    page.fill('input[type="password"]', PASSWORD)
    page.click('[data-item-marker="btnLogin"]')
    page.wait_for_timeout(5000)
    wait_for_stable(page)
    print(f"   ✅ Logged in. URL: {page.url}")
    screenshot(page, "report_01_logged_in")

    # ============================================
    # STEP 2: Navigate to WorkspaceExplorer (Configuration)
    # ============================================
    print("\n2️⃣ Opening Configuration...")
    page.goto(f"{CREATIO_URL}/0/ClientApp/#/WorkspaceExplorer", timeout=30000)
    page.wait_for_timeout(4000)
    wait_for_stable(page)
    screenshot(page, "report_02_workspace")

    # ============================================
    # STEP 3: Search for the target schema
    # ============================================
    print(f"\n3️⃣ Searching for schema: {TARGET_SCHEMA}...")

    # Look for search input
    search_selectors = [
        'input[placeholder*="Search"]',
        'input[type="search"]',
        '[class*="search"] input',
        'input[placeholder*="search" i]',
        '[data-item-marker*="search" i] input',
    ]

    search_found = False
    for sel in search_selectors:
        try:
            locator = page.locator(sel)
            if locator.count() > 0:
                print(f"   Found search: {sel}")
                locator.first.fill(TARGET_SCHEMA)
                page.wait_for_timeout(2000)
                search_found = True
                screenshot(page, "report_03_search")
                break
        except Exception as e:
            print(f"   Search selector {sel} failed: {e}")

    if not search_found:
        print("   ⚠ Search input not found, trying alternative methods...")
        # Try keyboard shortcut or other methods
        page.keyboard.press("Control+f")
        page.wait_for_timeout(1000)

    # ============================================
    # STEP 4: Find and click on the schema
    # ============================================
    print(f"\n4️⃣ Looking for {TARGET_SCHEMA} in results...")

    schema_selectors = [
        f'text={TARGET_SCHEMA}',
        f'[title*="{TARGET_SCHEMA}"]',
        f'td:has-text("{TARGET_SCHEMA}")',
        f'span:has-text("{TARGET_SCHEMA}")',
        f'[data-item-marker*="{TARGET_SCHEMA}"]',
    ]

    schema_clicked = False
    for sel in schema_selectors:
        try:
            locator = page.locator(sel)
            count = locator.count()
            if count > 0:
                print(f"   Found schema with: {sel} (count: {count})")
                # Double-click to open
                locator.first.dblclick()
                page.wait_for_timeout(3000)
                wait_for_stable(page)
                schema_clicked = True
                screenshot(page, "report_04_schema_opened")
                break
        except Exception as e:
            print(f"   Selector {sel} failed: {e}")

    if not schema_clicked:
        print("   ⚠ Could not click schema directly, trying URL navigation...")
        # Try direct URL pattern for schema designer
        schema_urls = [
            f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{TARGET_SCHEMA}",
            f"{CREATIO_URL}/0/Nui/ViewModule.aspx#ClientUnitSchemaDesigner/{TARGET_SCHEMA}",
        ]
        for url in schema_urls:
            print(f"   Trying: {url.split('#')[-1]}")
            page.goto(url, timeout=20000)
            page.wait_for_timeout(3000)
            wait_for_stable(page)
            screenshot(page, f"report_04_direct_url")

    # ============================================
    # STEP 5: Look for Source Code tab/button
    # ============================================
    print("\n5️⃣ Looking for Source Code view...")

    source_selectors = [
        'text=Source code',
        'text=Source',
        '[data-item-marker*="source" i]',
        'button:has-text("Source")',
        '[title*="Source" i]',
        'tab:has-text("Source")',
        '[class*="tab"]:has-text("Source")',
    ]

    for sel in source_selectors:
        try:
            locator = page.locator(sel)
            if locator.count() > 0:
                print(f"   Found source option: {sel}")
                locator.first.click()
                page.wait_for_timeout(2000)
                wait_for_stable(page)
                screenshot(page, "report_05_source_view")
                break
        except:
            pass

    # ============================================
    # STEP 6: Extract code from editor
    # ============================================
    print("\n6️⃣ Looking for code editor content...")

    # Check for various editor types
    editor_info = {
        'ace': page.locator('[class*="ace"]').count(),
        'monaco': page.locator('[class*="monaco"]').count(),
        'codemirror': page.locator('[class*="CodeMirror"]').count(),
        'textarea': page.locator('textarea').count(),
    }
    print(f"   Editor elements: {editor_info}")

    # Try to get code content
    code_content = None

    # Method 1: Ace editor
    if editor_info['ace'] > 0:
        try:
            code_content = page.evaluate('''() => {
                const editors = document.querySelectorAll('.ace_editor');
                if (editors.length > 0) {
                    for (const ed of editors) {
                        const aceEditor = ace.edit(ed);
                        if (aceEditor) {
                            return aceEditor.getValue();
                        }
                    }
                }
                return null;
            }''')
            if code_content:
                print(f"   ✅ Got code from Ace editor ({len(code_content)} chars)")
        except Exception as e:
            print(f"   Ace extraction failed: {e}")

    # Method 2: Monaco editor
    if not code_content and editor_info['monaco'] > 0:
        try:
            code_content = page.evaluate('''() => {
                const editors = monaco.editor.getEditors();
                if (editors && editors.length > 0) {
                    return editors[0].getValue();
                }
                return null;
            }''')
            if code_content:
                print(f"   ✅ Got code from Monaco editor ({len(code_content)} chars)")
        except Exception as e:
            print(f"   Monaco extraction failed: {e}")

    # Method 3: Textarea
    if not code_content and editor_info['textarea'] > 0:
        try:
            code_content = page.locator('textarea').first.input_value()
            if code_content:
                print(f"   ✅ Got code from textarea ({len(code_content)} chars)")
        except Exception as e:
            print(f"   Textarea extraction failed: {e}")

    # ============================================
    # STEP 7: Analyze and save the schema
    # ============================================
    print("\n7️⃣ Analyzing schema structure...")

    if code_content:
        # Save the code to a file for analysis
        output_file = ARTIFACTS_DIR / f"creatio_{TARGET_SCHEMA}_schema.js"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code_content)
        print(f"   ✅ Saved schema to: {output_file}")

        # Look for key patterns
        patterns = {
            'handlers': 'SCHEMA_HANDLERS' in code_content,
            'viewConfig': 'viewConfigDiff' in code_content,
            'viewModel': 'viewModelConfigDiff' in code_content,
            'Button_bwctkw5': 'Button_bwctkw5' in code_content,
            'LookupAttribute': 'LookupAttribute_bsixu8a' in code_content,
        }
        print(f"   Schema patterns found: {patterns}")

        # Extract handlers section
        if 'SCHEMA_HANDLERS' in code_content:
            start = code_content.find('/**SCHEMA_HANDLERS*/')
            end = code_content.find('/**SCHEMA_HANDLERS*/', start + 1)
            if start != -1 and end != -1:
                handlers_section = code_content[start:end+len('/**SCHEMA_HANDLERS*/')]
                print(f"   Handlers section: {handlers_section[:200]}...")
    else:
        print("   ⚠ Could not extract code content")

    # ============================================
    # STEP 8: Capture page state
    # ============================================
    print("\n8️⃣ Documenting page structure...")

    # Get all visible text
    all_text = page.locator('body').inner_text()

    # Look for Freedom UI specific elements
    freedom_elements = {
        'crt-button': page.locator('[class*="crt-button"]').count(),
        'crt-component': page.locator('[class*="crt-component"]').count(),
        'data-item-marker': page.locator('[data-item-marker]').count(),
    }
    print(f"   Freedom UI elements: {freedom_elements}")

    # Get all data-item-markers (important for Creatio)
    markers = page.evaluate('''() => {
        const elements = document.querySelectorAll('[data-item-marker]');
        return Array.from(elements).map(el => ({
            marker: el.getAttribute('data-item-marker'),
            tag: el.tagName,
            text: el.innerText?.substring(0, 50) || ''
        })).slice(0, 30);
    }''')
    print(f"   Data item markers found: {len(markers)}")
    for m in markers[:10]:
        print(f"      - {m['marker']}: {m['tag']} '{m['text']}'")

    screenshot(page, "report_08_final")

    # ============================================
    # Summary
    # ============================================
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Final URL: {page.url}")
    print(f"Code extracted: {'Yes' if code_content else 'No'}")
    print(f"Screenshots saved to: {SCREENSHOT_DIR}")

    browser.close()
    print("\n✅ Analysis complete!")
