#!/usr/bin/env python3
"""
Deploy UsrPage_ebkv9e8 handler to PROD via Playwright browser automation.
V2: Uses Monaco Editor API directly for code replacement.
"""

from playwright.sync_api import sync_playwright
import time
import json

# PROD credentials
CREATIO_URL = "https://pampabay.creatio.com"
USERNAME = "Supervisor"
PASSWORD = "123*Pampa?"

# Schema designer URL
SCHEMA_DESIGNER_URL = f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734"

# Path to the updated handler code
HANDLER_CODE_PATH = "/home/magown/creatio-report-fix/client-module/UsrPage_ebkv9e8_Updated.js"

def main():
    # Read the handler code
    with open(HANDLER_CODE_PATH, 'r') as f:
        handler_code = f.read()

    print(f"Handler code loaded: {len(handler_code)} characters")

    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        try:
            # Step 1: Navigate to login page
            print("Navigating to Creatio login...")
            page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", wait_until='networkidle', timeout=60000)
            page.screenshot(path='/tmp/creatio_v2_01_login.png')
            print("Screenshot saved: /tmp/creatio_v2_01_login.png")

            # Step 2: Login
            print("Logging in...")
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Find visible input fields only
            visible_inputs = page.locator('input:visible')
            print(f"Found {visible_inputs.count()} visible input fields")

            # Fill username and password
            visible_inputs.first.fill(USERNAME)
            print("Username filled")
            visible_inputs.nth(1).fill(PASSWORD)
            print("Password filled")

            page.screenshot(path='/tmp/creatio_v2_02_credentials.png')

            # Click login button
            login_button = page.locator('text=LOG IN').first
            login_button.click()
            print("Login button clicked")

            # Wait for login to complete
            page.wait_for_load_state('networkidle', timeout=60000)
            time.sleep(5)
            page.screenshot(path='/tmp/creatio_v2_03_after_login.png')
            print("Screenshot saved: /tmp/creatio_v2_03_after_login.png")

            # Step 3: Navigate to schema designer
            print(f"Navigating to schema designer...")
            page.goto(SCHEMA_DESIGNER_URL, wait_until='networkidle', timeout=120000)
            time.sleep(10)  # Give the designer time to fully load
            page.screenshot(path='/tmp/creatio_v2_04_designer.png')
            print("Screenshot saved: /tmp/creatio_v2_04_designer.png")

            # Step 4: Wait for Monaco editor to be fully loaded
            print("Waiting for Monaco editor to initialize...")
            time.sleep(5)

            # Check if Monaco is available
            monaco_check = page.evaluate('''() => {
                if (typeof monaco !== 'undefined' && monaco.editor) {
                    const editors = monaco.editor.getEditors();
                    return {
                        available: true,
                        editorCount: editors.length,
                        modelCount: monaco.editor.getModels().length
                    };
                }
                return { available: false };
            }''')
            print(f"Monaco status: {monaco_check}")

            if not monaco_check.get('available'):
                # Try alternate approach - look for CodeMirror or custom editor
                print("Monaco not found directly, trying alternate approach...")

                # Check for CodeMirror
                codemirror_check = page.evaluate('''() => {
                    const cmElements = document.querySelectorAll('.CodeMirror');
                    if (cmElements.length > 0 && cmElements[0].CodeMirror) {
                        return { available: true, type: 'CodeMirror' };
                    }
                    return { available: false };
                }''')
                print(f"CodeMirror status: {codemirror_check}")

                # Check for Ace editor
                ace_check = page.evaluate('''() => {
                    if (typeof ace !== 'undefined') {
                        const editors = document.querySelectorAll('.ace_editor');
                        return { available: true, type: 'Ace', count: editors.length };
                    }
                    return { available: false };
                }''')
                print(f"Ace status: {ace_check}")

            # Step 5: Try to set code via Monaco API
            print("Attempting to set code via Monaco API...")

            # Escape the code for JavaScript embedding
            escaped_code = json.dumps(handler_code)

            set_result = page.evaluate(f'''() => {{
                try {{
                    // Try Monaco first
                    if (typeof monaco !== 'undefined' && monaco.editor) {{
                        const models = monaco.editor.getModels();
                        if (models.length > 0) {{
                            models[0].setValue({escaped_code});
                            return {{ success: true, method: 'monaco' }};
                        }}

                        const editors = monaco.editor.getEditors();
                        if (editors.length > 0) {{
                            editors[0].setValue({escaped_code});
                            return {{ success: true, method: 'monaco-editor' }};
                        }}
                    }}

                    // Try CodeMirror
                    const cmElements = document.querySelectorAll('.CodeMirror');
                    if (cmElements.length > 0 && cmElements[0].CodeMirror) {{
                        cmElements[0].CodeMirror.setValue({escaped_code});
                        return {{ success: true, method: 'codemirror' }};
                    }}

                    // Try Ace
                    if (typeof ace !== 'undefined') {{
                        const aceEditors = document.querySelectorAll('.ace_editor');
                        if (aceEditors.length > 0) {{
                            const editor = ace.edit(aceEditors[0]);
                            editor.setValue({escaped_code}, -1);
                            return {{ success: true, method: 'ace' }};
                        }}
                    }}

                    // Try finding any textarea or contenteditable
                    const textareas = document.querySelectorAll('textarea');
                    for (const ta of textareas) {{
                        if (ta.offsetParent !== null) {{ // visible
                            ta.value = {escaped_code};
                            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            return {{ success: true, method: 'textarea' }};
                        }}
                    }}

                    return {{ success: false, reason: 'No editor found' }};
                }} catch (e) {{
                    return {{ success: false, error: e.message }};
                }}
            }}''')

            print(f"Set code result: {set_result}")

            time.sleep(2)
            page.screenshot(path='/tmp/creatio_v2_05_code_set.png')
            print("Screenshot saved: /tmp/creatio_v2_05_code_set.png")

            # Step 6: Try to save using Ctrl+S
            print("Attempting to save with Ctrl+S...")
            page.keyboard.press('Control+s')
            time.sleep(3)
            page.screenshot(path='/tmp/creatio_v2_06_after_ctrl_s.png')
            print("Screenshot saved: /tmp/creatio_v2_06_after_ctrl_s.png")

            # Step 7: Look for save confirmation or try ACTIONS menu
            print("Checking for save confirmation or using ACTIONS menu...")

            # Look for any save-related UI
            save_buttons = page.locator('text=Save').all()
            print(f"Found {len(save_buttons)} elements with 'Save' text")

            publish_buttons = page.locator('text=Publish').all()
            print(f"Found {len(publish_buttons)} elements with 'Publish' text")

            # Click ACTIONS and look for save
            actions_button = page.locator('text=ACTIONS')
            if actions_button.count() > 0:
                print("Opening ACTIONS menu...")
                actions_button.click()
                time.sleep(1)
                page.screenshot(path='/tmp/creatio_v2_07_actions_menu.png')
                print("Screenshot saved: /tmp/creatio_v2_07_actions_menu.png")

                # Look for Save option
                menu_items = page.locator('[role="menuitem"], .menu-item, li').all_inner_texts()
                print(f"Menu items: {menu_items}")

                # Close menu by clicking elsewhere
                page.keyboard.press('Escape')
                time.sleep(0.5)

            # Step 8: Try to find and click toolbar save button
            print("Looking for toolbar save button...")
            toolbar_buttons = page.locator('button, [role="button"]').all()
            for i, btn in enumerate(toolbar_buttons[:20]):  # Check first 20 buttons
                try:
                    text = btn.inner_text()
                    title = btn.get_attribute('title') or ''
                    if 'save' in text.lower() or 'save' in title.lower():
                        print(f"Found save button {i}: '{text}' / '{title}'")
                except:
                    pass

            page.screenshot(path='/tmp/creatio_v2_08_final.png')
            print("Screenshot saved: /tmp/creatio_v2_08_final.png")

            print("\n=== DEPLOYMENT STATUS ===")
            if set_result.get('success'):
                print(f"Code was set via: {set_result.get('method')}")
                print("NOTE: Manual save may be required if Ctrl+S didn't work")
            else:
                print(f"Code setting failed: {set_result}")
                print("Manual deployment may be required")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path='/tmp/creatio_v2_error.png')
            print("Error screenshot saved: /tmp/creatio_v2_error.png")
            raise
        finally:
            browser.close()
            print("Browser closed")

if __name__ == "__main__":
    main()
