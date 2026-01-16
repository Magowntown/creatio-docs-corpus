#!/usr/bin/env python3
"""
Creatio Schema Navigator
Navigates Configuration, changes filter, and opens the target schema
"""

from playwright.sync_api import sync_playwright
import os
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
    print(f"   ✅ Logged in")

    # ============================================
    # STEP 2: Navigate to Configuration
    # ============================================
    print("\n2️⃣ Opening Configuration...")
    page.goto(f"{CREATIO_URL}/0/ClientApp/#/WorkspaceExplorer", timeout=30000)
    page.wait_for_timeout(4000)
    wait_for_stable(page)
    screenshot(page, "schema_01_config")

    # ============================================
    # STEP 3: Change filter from Business-process to Client module
    # ============================================
    print("\n3️⃣ Changing schema type filter...")

    # Click on the Business-process dropdown to change it
    filter_clicked = False
    filter_selectors = [
        'text=Business-process',
        'button:has-text("Business-process")',
        '[class*="filter"]:has-text("Business-process")',
        'span:has-text("Business-process")',
    ]

    for sel in filter_selectors:
        try:
            locator = page.locator(sel)
            if locator.count() > 0:
                print(f"   Found filter dropdown: {sel}")
                locator.first.click()
                page.wait_for_timeout(1500)
                filter_clicked = True
                screenshot(page, "schema_02_filter_open")
                break
        except Exception as e:
            print(f"   {sel} failed: {e}")

    # Select Client module or similar option
    if filter_clicked:
        client_options = [
            'text=Client module',
            'text=Client schema',
            'text=Client unit schema',
            'text=Source code',
            '[class*="dropdown"] >> text=Client',
            'li:has-text("Client")',
            '[role="option"]:has-text("Client")',
        ]

        for opt in client_options:
            try:
                locator = page.locator(opt)
                if locator.count() > 0:
                    print(f"   Found client option: {opt} (count: {locator.count()})")
                    locator.first.click()
                    page.wait_for_timeout(2000)
                    wait_for_stable(page)
                    screenshot(page, "schema_03_filter_changed")
                    break
            except:
                pass

    # ============================================
    # STEP 4: Search for the target schema
    # ============================================
    print(f"\n4️⃣ Searching for: {TARGET_SCHEMA}...")

    # Find search input and type schema name
    search_selectors = [
        'input[placeholder*="Search"]',
        '[class*="search"] input',
        'input[type="search"]',
        'input.input-inner',
    ]

    for sel in search_selectors:
        try:
            locator = page.locator(sel)
            if locator.count() > 0:
                print(f"   Found search input: {sel}")
                # Clear and type
                locator.first.fill('')
                locator.first.fill(TARGET_SCHEMA)
                page.wait_for_timeout(2000)
                wait_for_stable(page)
                screenshot(page, "schema_04_search")
                break
        except:
            pass

    # ============================================
    # STEP 5: Click on the schema in results
    # ============================================
    print(f"\n5️⃣ Looking for {TARGET_SCHEMA} in results...")

    # First check what's visible in the grid
    grid_rows = page.locator('tr').count()
    print(f"   Grid rows visible: {grid_rows}")

    # Try to find and click the schema
    schema_selectors = [
        f'text="{TARGET_SCHEMA}"',
        f'a:has-text("{TARGET_SCHEMA}")',
        f'td:has-text("{TARGET_SCHEMA}")',
        f'[title*="{TARGET_SCHEMA}"]',
        f'span:has-text("{TARGET_SCHEMA}")',
    ]

    schema_found = False
    for sel in schema_selectors:
        try:
            locator = page.locator(sel)
            count = locator.count()
            if count > 0:
                print(f"   ✅ Found schema: {sel} (count: {count})")
                # Double-click to open
                locator.first.dblclick()
                page.wait_for_timeout(3000)
                wait_for_stable(page)
                schema_found = True
                screenshot(page, "schema_05_opened")
                break
        except Exception as e:
            print(f"   {sel}: {e}")

    # ============================================
    # STEP 6: If not found, try expanding packages in left panel
    # ============================================
    if not schema_found:
        print("\n6️⃣ Trying to find schema in package tree...")

        # Look for UsrTestApp or similar package that might contain the page
        packages_to_try = ['UsrTestApp', 'Custom', 'PampaBay', 'PampaBayVer2']

        for pkg in packages_to_try:
            try:
                pkg_locator = page.locator(f'text={pkg}')
                if pkg_locator.count() > 0:
                    print(f"   Expanding package: {pkg}")
                    # Click to expand
                    pkg_locator.first.click()
                    page.wait_for_timeout(1500)

                    # Look for Schemas or Client modules folder
                    folders = ['Schemas', 'Client modules', 'Source code']
                    for folder in folders:
                        folder_loc = page.locator(f'text={folder}')
                        if folder_loc.count() > 0:
                            print(f"      Found folder: {folder}")
                            folder_loc.first.click()
                            page.wait_for_timeout(1500)
                            break
            except:
                pass

        screenshot(page, "schema_06_packages")

    # ============================================
    # STEP 7: Look for code editor or Source Code tab
    # ============================================
    print("\n7️⃣ Looking for Source Code view...")

    # Check if we're in a schema designer
    current_url = page.url
    print(f"   Current URL: {current_url}")

    # Look for tabs or source code option
    source_selectors = [
        'text=Source code',
        '[data-item-marker="SourceCodeDesignerButton"]',
        'button:has-text("Source")',
        '[class*="tab"]:has-text("Source")',
        'span:has-text("Source code")',
    ]

    for sel in source_selectors:
        try:
            locator = page.locator(sel)
            if locator.count() > 0:
                print(f"   Found source option: {sel}")
                locator.first.click()
                page.wait_for_timeout(2000)
                wait_for_stable(page)
                screenshot(page, "schema_07_source")
                break
        except:
            pass

    # ============================================
    # STEP 8: Check for code editor
    # ============================================
    print("\n8️⃣ Checking for code editor...")

    editor_types = {
        'ace': page.locator('[class*="ace_editor"]').count(),
        'monaco': page.locator('[class*="monaco-editor"]').count(),
        'textarea': page.locator('textarea').count(),
    }
    print(f"   Editor elements: {editor_types}")

    # Try to extract code
    code_content = None

    if editor_types['ace'] > 0:
        try:
            code_content = page.evaluate('''() => {
                const editors = document.querySelectorAll('.ace_editor');
                for (const ed of editors) {
                    try {
                        const aceEditor = ace.edit(ed);
                        const value = aceEditor.getValue();
                        if (value && value.length > 10) return value;
                    } catch(e) {}
                }
                return null;
            }''')
            if code_content:
                print(f"   ✅ Got code from Ace ({len(code_content)} chars)")
        except Exception as e:
            print(f"   Ace extraction failed: {e}")

    if code_content:
        output_file = ARTIFACTS_DIR / f"creatio_{TARGET_SCHEMA}_code.js"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(code_content)
        print(f"\n   📄 Schema code saved to: {output_file}")

        # Analyze key sections
        if '/**SCHEMA_HANDLERS*/' in code_content:
            start = code_content.find('/**SCHEMA_HANDLERS*/')
            end = code_content.find('/**SCHEMA_HANDLERS*/', start + 20)
            if end > start:
                handlers = code_content[start+len('/**SCHEMA_HANDLERS*/'):end].strip()
                print(f"\n   HANDLERS SECTION:")
                print(f"   {handlers[:500]}")

    # Final screenshot
    screenshot(page, "schema_08_final")

    print("\n" + "="*60)
    print(f"Final URL: {page.url}")
    print(f"Code extracted: {'Yes' if code_content else 'No'}")
    print("="*60)

    browser.close()
    print("\n✅ Done!")
