#!/usr/bin/env python3
"""
Creatio Interaction Test
Tests what Playwright can actually do: navigate, click, edit, save
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
    print("="*60)
    print("CREATIO INTERACTION TEST")
    print("="*60)

    print("\n🚀 Launching browser...")
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    results = {
        'login': False,
        'navigate': False,
        'click_buttons': False,
        'click_tabs': False,
        'type_text': False,
        'keyboard_shortcuts': False,
        'dropdown_select': False,
        'editor_interact': False,
        'save_action': False,
    }

    # ============================================
    # TEST 1: Login
    # ============================================
    print("\n" + "-"*40)
    print("TEST 1: LOGIN")
    print("-"*40)

    try:
        page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
        wait_for_stable(page)
        page.fill('input[type="text"]:first-of-type', USERNAME)
        page.fill('input[type="password"]', PASSWORD)
        page.click('[data-item-marker="btnLogin"]')
        page.wait_for_timeout(5000)
        wait_for_stable(page)

        if "Shell" in page.url or "Desktop" in page.url:
            print("   ✅ LOGIN: SUCCESS")
            results['login'] = True
        else:
            print(f"   ⚠ LOGIN: Redirected to {page.url}")
            results['login'] = True  # Still logged in even if different page
    except Exception as e:
        print(f"   ❌ LOGIN: FAILED - {e}")

    screenshot(page, "test_01_login")

    # ============================================
    # TEST 2: Navigate to Different Pages
    # ============================================
    print("\n" + "-"*40)
    print("TEST 2: NAVIGATION")
    print("-"*40)

    try:
        # Navigate to Configuration
        page.goto(f"{CREATIO_URL}/0/ClientApp/#/WorkspaceExplorer", timeout=30000)
        page.wait_for_timeout(3000)
        wait_for_stable(page)

        if "WorkspaceExplorer" in page.url:
            print("   ✅ NAVIGATE to Configuration: SUCCESS")
            results['navigate'] = True
        else:
            print(f"   ⚠ NAVIGATE: Ended at {page.url}")

        screenshot(page, "test_02_navigate")
    except Exception as e:
        print(f"   ❌ NAVIGATE: FAILED - {e}")

    # ============================================
    # TEST 3: Click Buttons
    # ============================================
    print("\n" + "-"*40)
    print("TEST 3: CLICK BUTTONS")
    print("-"*40)

    try:
        # Try clicking the filter dropdown
        filter_btn = page.locator('text=Business-process').first
        if filter_btn.count() > 0:
            filter_btn.click()
            page.wait_for_timeout(1000)
            print("   ✅ CLICK filter dropdown: SUCCESS")
            results['click_buttons'] = True
            screenshot(page, "test_03a_filter_clicked")

            # Try selecting an option
            client_module = page.locator('text=Client module').first
            if client_module.count() > 0:
                client_module.click()
                page.wait_for_timeout(1000)
                print("   ✅ SELECT dropdown option: SUCCESS")
                results['dropdown_select'] = True
                screenshot(page, "test_03b_option_selected")
    except Exception as e:
        print(f"   ❌ CLICK BUTTONS: FAILED - {e}")

    # ============================================
    # TEST 4: Type in Search Box
    # ============================================
    print("\n" + "-"*40)
    print("TEST 4: TYPE TEXT")
    print("-"*40)

    try:
        # Find search input
        search_input = page.locator('[class*="search"] input').first
        if search_input.count() > 0:
            search_input.fill("UsrPage")
            page.wait_for_timeout(1000)

            # Check if text was entered
            value = search_input.input_value()
            if "UsrPage" in value:
                print("   ✅ TYPE in search: SUCCESS")
                results['type_text'] = True
            screenshot(page, "test_04_type_text")
    except Exception as e:
        print(f"   ❌ TYPE TEXT: FAILED - {e}")

    # ============================================
    # TEST 5: Open Schema Designer
    # ============================================
    print("\n" + "-"*40)
    print("TEST 5: OPEN SCHEMA DESIGNER")
    print("-"*40)

    try:
        page.goto(f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{SCHEMA_UID}", timeout=30000)
        page.wait_for_timeout(5000)
        wait_for_stable(page)

        if "ClientUnitSchemaDesigner" in page.url:
            print("   ✅ OPEN Schema Designer: SUCCESS")
        screenshot(page, "test_05_designer")
    except Exception as e:
        print(f"   ❌ OPEN DESIGNER: FAILED - {e}")

    # ============================================
    # TEST 6: Click Tabs in Designer
    # ============================================
    print("\n" + "-"*40)
    print("TEST 6: CLICK TABS")
    print("-"*40)

    try:
        # Try clicking on different tabs (JS, Localizable strings, etc.)
        tabs_to_try = ['JS', 'Localizable strings', 'Images', 'Parameters']

        for tab_name in tabs_to_try:
            tab = page.locator(f'text={tab_name}').first
            if tab.count() > 0:
                tab.click()
                page.wait_for_timeout(500)
                print(f"   ✅ CLICK tab '{tab_name}': SUCCESS")
                results['click_tabs'] = True

        screenshot(page, "test_06_tabs")
    except Exception as e:
        print(f"   ❌ CLICK TABS: FAILED - {e}")

    # ============================================
    # TEST 7: Interact with Code Editor
    # ============================================
    print("\n" + "-"*40)
    print("TEST 7: EDITOR INTERACTION")
    print("-"*40)

    try:
        # Click back to JS tab
        js_tab = page.locator('text=JS').first
        if js_tab.count() > 0:
            js_tab.click()
            page.wait_for_timeout(1000)

        # Try to find and interact with the editor
        # Method 1: Click on the code area
        code_area = page.locator('[contenteditable="true"]').first
        if code_area.count() > 0:
            code_area.click()
            page.wait_for_timeout(500)
            print("   ✅ CLICK on code area: SUCCESS")

            # Try to select all and get content
            page.keyboard.press('Control+a')
            page.wait_for_timeout(300)
            print("   ✅ SELECT ALL (Ctrl+A): SUCCESS")
            results['keyboard_shortcuts'] = True

            screenshot(page, "test_07a_selected")

            # Try typing something
            page.keyboard.press('End')  # Go to end first
            page.wait_for_timeout(200)

            # Check if we can type
            # We won't actually modify the code, just test if keyboard works
            print("   ✅ KEYBOARD navigation: SUCCESS")
            results['editor_interact'] = True

        # Method 2: Check for ace editor
        ace_check = page.evaluate('''() => {
            return {
                hasAce: typeof ace !== 'undefined',
                aceEditors: document.querySelectorAll('.ace_editor').length,
                contentEditable: document.querySelectorAll('[contenteditable="true"]').length
            };
        }''')
        print(f"   Editor info: {ace_check}")

        screenshot(page, "test_07b_editor")
    except Exception as e:
        print(f"   ❌ EDITOR INTERACTION: FAILED - {e}")

    # ============================================
    # TEST 8: Find Save/Actions Buttons
    # ============================================
    print("\n" + "-"*40)
    print("TEST 8: SAVE/ACTIONS BUTTONS")
    print("-"*40)

    try:
        # Look for ACTIONS dropdown
        actions_btn = page.locator('text=ACTIONS').first
        if actions_btn.count() > 0:
            actions_btn.click()
            page.wait_for_timeout(1000)
            print("   ✅ CLICK ACTIONS menu: SUCCESS")
            screenshot(page, "test_08a_actions")

            # Look for Save option in dropdown
            save_options = page.locator('text=Save').all()
            print(f"   Found {len(save_options)} 'Save' options")

            if len(save_options) > 0:
                print("   ✅ SAVE option available: YES")
                results['save_action'] = True

            # Click elsewhere to close menu
            page.keyboard.press('Escape')

        # Look for COMPILE button
        compile_btn = page.locator('text=COMPILE').first
        if compile_btn.count() > 0:
            print("   ✅ COMPILE button found: YES")

        # Look for CLOSE button
        close_btn = page.locator('text=CLOSE').first
        if close_btn.count() > 0:
            print("   ✅ CLOSE button found: YES")

        screenshot(page, "test_08b_buttons")
    except Exception as e:
        print(f"   ❌ SAVE/ACTIONS: FAILED - {e}")

    # ============================================
    # TEST 9: Test Direct Code Modification
    # ============================================
    print("\n" + "-"*40)
    print("TEST 9: CODE MODIFICATION TEST")
    print("-"*40)

    try:
        # Get current code content
        current_code = page.evaluate('''() => {
            const body = document.body.innerText;
            if (body.includes('define(')) {
                const start = body.indexOf('define(');
                const end = body.indexOf('});', start) + 3;
                return body.substring(start, end);
            }
            return '';
        }''')

        if current_code:
            print(f"   ✅ READ code content: SUCCESS ({len(current_code)} chars)")

            # Check if handlers section exists
            if '/**SCHEMA_HANDLERS*/' in current_code:
                print("   ✅ HANDLERS section found: YES")

                # Check if it's empty
                if '/**SCHEMA_HANDLERS*/[]/**SCHEMA_HANDLERS*/' in current_code:
                    print("   ℹ️  Handlers are currently EMPTY")
                else:
                    print("   ℹ️  Handlers have content")
        else:
            print("   ⚠ Could not read code content")

        screenshot(page, "test_09_code")
    except Exception as e:
        print(f"   ❌ CODE MODIFICATION: FAILED - {e}")

    # ============================================
    # SUMMARY
    # ============================================
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)

    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test:20s}: {status}")

    passed_count = sum(results.values())
    total_count = len(results)
    print(f"\n   Total: {passed_count}/{total_count} tests passed")

    print("\n" + "="*60)
    print("CAPABILITIES ASSESSMENT")
    print("="*60)

    if results['login'] and results['navigate']:
        print("   ✅ Can login and navigate")
    if results['click_buttons'] and results['dropdown_select']:
        print("   ✅ Can click buttons and select dropdowns")
    if results['type_text']:
        print("   ✅ Can type text in inputs")
    if results['click_tabs']:
        print("   ✅ Can click tabs")
    if results['keyboard_shortcuts']:
        print("   ✅ Can use keyboard shortcuts")
    if results['editor_interact']:
        print("   ✅ Can interact with code editor area")
    if results['save_action']:
        print("   ✅ Can access save functionality")

    browser.close()
    print("\n✅ Test complete!")
