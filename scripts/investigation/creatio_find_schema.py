#!/usr/bin/env python3
"""
Creatio Schema Finder - Uses grid search and opens schema designer
"""

from playwright.sync_api import sync_playwright
import os
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

    # Change to Client module filter
    print("\n3️⃣ Changing filter to Client module...")
    try:
        page.locator('text=Business-process').first.click()
        page.wait_for_timeout(1000)
        page.locator('text=Client module').first.click()
        page.wait_for_timeout(2000)
        wait_for_stable(page)
    except Exception as e:
        print(f"   Filter change: {e}")

    # Use the grid search (the one with magnifier icon on the right)
    print(f"\n4️⃣ Using grid search for: {TARGET_SCHEMA}...")

    # Find the search input in the grid area (right side)
    grid_search = page.locator('input[placeholder="Search"]').last
    if grid_search.count() > 0:
        print("   Found grid search input")
        grid_search.fill(TARGET_SCHEMA)
        page.keyboard.press('Enter')
        page.wait_for_timeout(3000)
        wait_for_stable(page)
    screenshot(page, "find_01_search")

    # Check if schema appears
    print(f"\n5️⃣ Looking for {TARGET_SCHEMA} in results...")

    # Print what we see in the grid
    rows = page.locator('tr').all()
    print(f"   Total rows: {len(rows)}")

    for row in rows[:20]:
        try:
            text = row.inner_text()
            if TARGET_SCHEMA.lower() in text.lower() or 'UsrPage' in text:
                print(f"   ✅ FOUND: {text[:100]}")
        except:
            pass

    # Try clicking directly on link with schema name
    schema_link = page.locator(f'a:has-text("{TARGET_SCHEMA}")')
    if schema_link.count() > 0:
        print(f"   Found schema link, double-clicking...")
        schema_link.first.dblclick()
        page.wait_for_timeout(4000)
        wait_for_stable(page)
        screenshot(page, "find_02_opened")

    # If not found, try searching for "UsrPage" to see all user pages
    if schema_link.count() == 0:
        print("\n6️⃣ Searching for 'UsrPage' to list all user pages...")
        grid_search = page.locator('input[placeholder="Search"]').last
        grid_search.fill('UsrPage')
        page.keyboard.press('Enter')
        page.wait_for_timeout(3000)
        wait_for_stable(page)
        screenshot(page, "find_03_usrpage_search")

        # List all visible items
        links = page.locator('a[href*="UsrPage"], td:has-text("UsrPage")').all()
        print(f"   Found {len(links)} UsrPage items")
        for link in links[:10]:
            try:
                print(f"      - {link.inner_text()[:60]}")
            except:
                pass

    # Try the URL-based approach with proper schema manager
    print("\n7️⃣ Trying direct URL to schema manager...")

    # Freedom UI schemas use different designer URLs
    designer_urls = [
        f"{CREATIO_URL}/0/ClientApp/#/SchemaDesigner/{TARGET_SCHEMA}",
        f"{CREATIO_URL}/0/Nui/ViewModule.aspx#SchemaDesigner/{TARGET_SCHEMA}",
        f"{CREATIO_URL}/0/ClientApp/#/ClientModuleDesigner/{TARGET_SCHEMA}",
    ]

    for url in designer_urls:
        print(f"   Trying: {url.split('#')[-1][:50]}...")
        try:
            page.goto(url, timeout=15000)
            page.wait_for_timeout(3000)
            wait_for_stable(page)

            # Check if we got an editor
            ace_count = page.locator('[class*="ace"]').count()
            monaco_count = page.locator('[class*="monaco"]').count()

            if ace_count > 0 or monaco_count > 0:
                print(f"   ✅ Found editor! ace={ace_count}, monaco={monaco_count}")
                screenshot(page, f"find_04_editor")
                break
        except Exception as e:
            print(f"      Failed: {e}")

    # Final state
    screenshot(page, "find_05_final")
    print(f"\n🔗 Final URL: {page.url}")

    # Try to get any code content
    code_content = None
    try:
        code_content = page.evaluate('''() => {
            // Try ace
            if (typeof ace !== 'undefined') {
                const editors = document.querySelectorAll('.ace_editor');
                for (const ed of editors) {
                    try {
                        const aceEditor = ace.edit(ed);
                        const val = aceEditor.getValue();
                        if (val && val.length > 50) return val;
                    } catch(e) {}
                }
            }
            // Try monaco
            if (typeof monaco !== 'undefined') {
                const editors = monaco.editor.getEditors();
                if (editors && editors.length) {
                    return editors[0].getValue();
                }
            }
            // Try textarea
            const ta = document.querySelector('textarea');
            if (ta) return ta.value;
            return null;
        }''')
    except:
        pass

    if code_content:
        print(f"\n📄 Got code content ({len(code_content)} chars)")
        out_path = ARTIFACTS_DIR / f"creatio_{TARGET_SCHEMA}_code.js"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(code_content)
        print(f"   Saved to {out_path}")

        # Show handlers section
        if 'SCHEMA_HANDLERS' in code_content:
            idx = code_content.find('/**SCHEMA_HANDLERS*/')
            end_idx = code_content.find('/**SCHEMA_HANDLERS*/', idx+20)
            if idx >= 0 and end_idx > idx:
                handlers = code_content[idx:end_idx+len('/**SCHEMA_HANDLERS*/')]
                print(f"\n   HANDLERS:\n{handlers}")
    else:
        print("\n⚠ No code content found")

    browser.close()
    print("\n✅ Done!")
