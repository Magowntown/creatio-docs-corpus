#!/usr/bin/env python3
"""
Deploy UsrPage_ebkv9e8 handler to PROD via Playwright browser automation.
"""

from playwright.sync_api import sync_playwright
import time

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
            page.screenshot(path='/tmp/creatio_01_login.png')
            print("Screenshot saved: /tmp/creatio_01_login.png")

            # Step 2: Login - find inputs by their position (first input is username, second is password)
            print("Logging in...")

            # Wait for page to fully load
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            # Find visible input fields only (exclude hidden)
            visible_inputs = page.locator('input:visible')
            print(f"Found {visible_inputs.count()} visible input fields")

            # Fill username (first visible input)
            username_input = visible_inputs.first
            username_input.fill(USERNAME)
            print("Username filled")

            # Fill password (second visible input)
            password_input = visible_inputs.nth(1)
            password_input.fill(PASSWORD)
            print("Password filled")

            page.screenshot(path='/tmp/creatio_02_credentials.png')

            # Click login button - try multiple selectors
            login_button = page.locator('text=LOG IN').first
            if login_button.count() == 0:
                login_button = page.locator('button, input[type="submit"], a').filter(has_text="LOG IN").first
            login_button.click()
            print("Login button clicked")

            # Wait for login to complete
            page.wait_for_load_state('networkidle', timeout=60000)
            time.sleep(5)
            page.screenshot(path='/tmp/creatio_03_after_login.png')
            print("Screenshot saved: /tmp/creatio_03_after_login.png")

            # Step 3: Navigate to schema designer
            print(f"Navigating to schema designer...")
            page.goto(SCHEMA_DESIGNER_URL, wait_until='networkidle', timeout=120000)
            time.sleep(10)  # Give the designer time to fully load
            page.screenshot(path='/tmp/creatio_04_designer.png')
            print("Screenshot saved: /tmp/creatio_04_designer.png")

            # Step 4: Find the code editor and replace content
            print("Looking for code editor...")

            # Creatio uses a custom code editor - look for the code area with line numbers
            # The code area has numbered lines and shows JavaScript
            page_content = page.content()

            # Look for the code editor area - it shows numbered lines
            code_area = page.locator('.code-editor, [class*="editor"], pre, code').first
            if code_area.count() == 0:
                # Try clicking on the visible code area
                code_area = page.locator('text=define("UsrPage_ebkv9e8"').first

            if code_area.count() > 0:
                print("Found code area, clicking to focus...")
                code_area.click()
                time.sleep(1)
            else:
                # Click in the middle of the page where code is visible
                print("Clicking on code area by coordinates...")
                page.mouse.click(700, 400)
                time.sleep(1)

            # Select all text (Ctrl+A) and replace
            print("Selecting all code...")
            page.keyboard.press('Control+a')
            time.sleep(1)
            page.screenshot(path='/tmp/creatio_05_selected.png')
            print("Screenshot saved: /tmp/creatio_05_selected.png")

            # Paste the new code using keyboard simulation
            # First set clipboard content
            print("Pasting new code...")
            page.evaluate('''(code) => {
                // Create a temporary textarea to set clipboard
                const ta = document.createElement('textarea');
                ta.value = code;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
            }''', handler_code)
            time.sleep(0.5)

            page.keyboard.press('Control+v')
            print("Code pasted")

            time.sleep(3)
            page.screenshot(path='/tmp/creatio_06_code_pasted.png')
            print("Screenshot saved: /tmp/creatio_06_code_pasted.png")

            # Save the schema using ACTIONS menu or Ctrl+S
            print("Saving schema...")

            # Try clicking ACTIONS button first
            actions_button = page.locator('text=ACTIONS')
            if actions_button.count() > 0:
                print("Found ACTIONS button, clicking...")
                actions_button.click()
                time.sleep(1)
                page.screenshot(path='/tmp/creatio_07_actions_menu.png')

                # Look for Save option
                save_option = page.locator('text=Save')
                if save_option.count() > 0:
                    save_option.first.click()
                    print("Clicked Save in ACTIONS menu")
                    time.sleep(5)
            else:
                # Try Ctrl+S
                page.keyboard.press('Control+s')
                print("Pressed Ctrl+S to save")
                time.sleep(5)

            page.screenshot(path='/tmp/creatio_08_after_save.png')
            print("Screenshot saved: /tmp/creatio_08_after_save.png")

            print("Handler deployment completed!")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path='/tmp/creatio_error.png')
            print("Error screenshot saved: /tmp/creatio_error.png")
            raise
        finally:
            browser.close()
            print("Browser closed")

if __name__ == "__main__":
    main()
