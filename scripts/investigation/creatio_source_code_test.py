#!/usr/bin/env python3
"""
Creatio Source Code Editor Test
Opens a specific schema and accesses its source code
"""

from playwright.sync_api import sync_playwright
import os
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

def screenshot(page, name):
    path = f"{SCREENSHOT_DIR}/{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"📸 {name}")
    return path

with sync_playwright() as p:
    print("🚀 Launching browser...")
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    # Login
    print("\n1️⃣ Logging in...")
    page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
    page.wait_for_load_state('networkidle')
    page.fill('input[type="text"]:first-of-type', USERNAME)
    page.fill('input[type="password"]', PASSWORD)
    page.click('[data-item-marker="btnLogin"]')
    page.wait_for_timeout(5000)
    print(f"   ✅ Logged in")

    # Navigate to Configuration
    print("\n2️⃣ Opening Configuration...")
    page.goto(f"{CREATIO_URL}/0/ClientApp/#/WorkspaceExplorer", timeout=30000)
    page.wait_for_timeout(4000)
    page.wait_for_load_state('networkidle')
    screenshot(page, "20_config_list")

    # Look for the "Source code" filter or Client module schemas
    print("\n3️⃣ Looking for Client modules (JavaScript code)...")

    # Try clicking on Object dropdown to change view type
    try:
        # Look for type filter dropdown
        filter_selectors = [
            'text=Object',
            '[class*="filter"]',
            '[class*="dropdown"]',
            'button:has-text("Object")',
            'span:has-text("Object")'
        ]

        for sel in filter_selectors:
            try:
                locator = page.locator(sel)
                if locator.count() > 0:
                    print(f"   Found filter: {sel}")
                    locator.first.click()
                    page.wait_for_timeout(1000)
                    screenshot(page, "21_filter_dropdown")
                    break
            except:
                pass
    except:
        pass

    # Look for Source code or Client module options
    print("\n4️⃣ Searching for source code options...")
    source_options = [
        'text=Source code',
        'text=Client module',
        'text=Client schema',
        'text=JavaScript',
        'text=Source',
        '[data-item-marker*="source" i]',
        '[data-item-marker*="client" i]'
    ]

    for opt in source_options:
        try:
            locator = page.locator(opt)
            if locator.count() > 0:
                print(f"   ✅ Found: {opt} (count: {locator.count()})")
                locator.first.click()
                page.wait_for_timeout(2000)
                screenshot(page, f"22_clicked_{opt[:20].replace(' ', '_')}")
        except:
            pass

    # Navigate to a specific schema using the left panel
    print("\n5️⃣ Expanding package and finding schemas...")

    # Click on Custom or PampaBay package to expand
    packages = ['Custom', 'PampaBay', 'PampaBayVer2']
    for pkg in packages:
        try:
            pkg_locator = page.locator(f'text={pkg}').first
            if pkg_locator.count() > 0:
                print(f"   Clicking package: {pkg}")
                pkg_locator.click()
                page.wait_for_timeout(1500)
                screenshot(page, f"23_package_{pkg}")
                break
        except:
            pass

    # Look for schema types in the expanded package
    print("\n6️⃣ Looking for schema types...")
    schema_types = [
        'text=Schemas',
        'text=Client modules',
        'text=Source code schemas',
        'text=Objects',
    ]

    for st in schema_types:
        try:
            locator = page.locator(st)
            if locator.count() > 0:
                print(f"   Found schema type: {st}")
        except:
            pass

    # Try to open Advanced Settings which has source code
    print("\n7️⃣ Trying Advanced Settings route...")
    page.goto(f"{CREATIO_URL}/0/Nui/ViewModule.aspx#CardModuleV2/SysSettingPage", timeout=30000)
    page.wait_for_timeout(3000)
    screenshot(page, "24_advanced_settings")

    # Try the old configuration section URL
    print("\n8️⃣ Trying classic configuration...")
    page.goto(f"{CREATIO_URL}/0/Nui/ViewModule.aspx#SectionModuleV2/SysWorkplace", timeout=30000)
    page.wait_for_timeout(3000)
    screenshot(page, "25_classic_view")

    # Try direct schema designer URL pattern
    print("\n9️⃣ Trying Schema Designer patterns...")
    designer_urls = [
        f"{CREATIO_URL}/0/Nui/ViewModule.aspx#SchemaDesigner",
        f"{CREATIO_URL}/0/Nui/ViewModule.aspx#ClientUnitSchemaDesigner",
        f"{CREATIO_URL}/0/ClientApp/#/IntegrationDesigner",
    ]

    for url in designer_urls:
        try:
            print(f"   Trying: {url.split('#')[-1]}")
            page.goto(url, timeout=15000)
            page.wait_for_timeout(2000)
            screenshot(page, f"26_{url.split('#')[-1][:30]}")

            # Check if we got code editor elements
            ace_count = page.locator('[class*="ace"]').count()
            monaco_count = page.locator('[class*="monaco"]').count()
            if ace_count > 0 or monaco_count > 0:
                print(f"   ✅ Found code editor! ace={ace_count}, monaco={monaco_count}")
        except Exception as e:
            print(f"   Failed: {e}")

    # Document what we found
    print("\n🔍 Final Page Analysis:")
    print(f"   URL: {page.url}")

    # List all available routes/links
    links = page.locator('a[href*="#"]').all()
    print(f"   Internal links found: {len(links)}")

    screenshot(page, "29_final")
    browser.close()
    print("\n✅ Test complete!")
