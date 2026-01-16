#!/usr/bin/env python3
"""
Creatio Browser Automation Test
Tests navigation, configuration menu, and code editing capabilities
"""

from playwright.sync_api import sync_playwright
import os
import time
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import SCREENSHOTS_DIR, ensure_dirs

ensure_dirs()

# Configuration
CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
SCREENSHOT_DIR = str(SCREENSHOTS_DIR)

def ensure_screenshot_dir():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def screenshot(page, name):
    """Take a screenshot with a descriptive name"""
    path = f"{SCREENSHOT_DIR}/{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"📸 Screenshot saved: {path}")
    return path

def wait_and_log(page, message, timeout=5000):
    """Wait for network idle and log progress"""
    print(f"⏳ {message}...")
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        print(f"   (network didn't fully idle, continuing)")
    print(f"✅ {message} - Done")

def main():
    ensure_screenshot_dir()

    with sync_playwright() as p:
        # Launch browser (headless for automation)
        print("🚀 Launching browser...")
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )

        # Create context with larger viewport
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True
        )

        page = context.new_page()

        # Enable console logging
        page.on("console", lambda msg: print(f"   [Console] {msg.type}: {msg.text}") if msg.type == "error" else None)

        try:
            # ============================================
            # STEP 1: Navigate to Creatio
            # ============================================
            print("\n" + "="*60)
            print("STEP 1: Navigate to Creatio Login")
            print("="*60)

            page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
            wait_and_log(page, "Loading login page")
            screenshot(page, "01_login_page")

            # ============================================
            # STEP 2: Login
            # ============================================
            print("\n" + "="*60)
            print("STEP 2: Logging in")
            print("="*60)

            # Wait for login form
            page.wait_for_selector('input[name="UserName"], #UserNameEdit, input[type="text"]', timeout=10000)

            # Try different possible selectors for username/password fields
            username_selectors = ['input[name="UserName"]', '#UserNameEdit', 'input[placeholder*="user" i]', 'input[type="text"]:first-of-type']
            password_selectors = ['input[name="Password"]', '#PasswordEdit', 'input[type="password"]']
            # Creatio uses <span> elements styled as buttons, not actual <button> tags
            login_button_selectors = [
                '[data-item-marker="btnLogin"]',  # Creatio's data marker
                '#t-comp18-textEl',               # Direct ID
                '.login-button-login',            # Class selector
                'span:has-text("Log In")',        # Span with text
                'span.t-btn-style-green',         # Green styled span
            ]

            # Fill username
            for selector in username_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.fill(selector, USERNAME)
                        print(f"   Filled username using: {selector}")
                        break
                except:
                    continue

            # Fill password
            for selector in password_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.fill(selector, PASSWORD)
                        print(f"   Filled password using: {selector}")
                        break
                except:
                    continue

            screenshot(page, "02_credentials_entered")

            # Click login
            login_clicked = False
            for selector in login_button_selectors:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0:
                        print(f"   Found login button: {selector} (count: {locator.count()})")
                        locator.first.click()
                        print(f"   ✓ Clicked login using: {selector}")
                        login_clicked = True
                        break
                except Exception as e:
                    print(f"   Failed {selector}: {e}")
                    continue

            if not login_clicked:
                print("   ⚠ Could not find login button, trying direct click on visible button")
                # Try clicking any visible button with LOG IN text
                page.get_by_role("button", name="LOG IN").click()

            # Wait for login to complete - look for URL change or dashboard elements
            print("   Waiting for login redirect...")
            page.wait_for_timeout(3000)

            # Check if we're still on login page
            if "Login" in page.url:
                print("   Still on login page, waiting longer...")
                page.wait_for_timeout(5000)

            wait_and_log(page, "Waiting for login to complete", timeout=30000)
            screenshot(page, "03_after_login")

            # Check for login errors
            error_selectors = ['.error-message', '.login-error', '[class*="error"]', 'text=Invalid', 'text=incorrect']
            for err_sel in error_selectors:
                try:
                    if page.locator(err_sel).count() > 0:
                        error_text = page.locator(err_sel).first.inner_text()
                        print(f"   ⚠ Login error detected: {error_text}")
                except:
                    pass

            # Check current URL
            print(f"   Current URL: {page.url}")

            # ============================================
            # STEP 3: Navigate to WorkspaceExplorer
            # ============================================
            print("\n" + "="*60)
            print("STEP 3: Navigate to WorkspaceExplorer")
            print("="*60)

            page.goto(f"{CREATIO_URL}/0/ClientApp/#/WorkspaceExplorer", timeout=30000)
            page.wait_for_timeout(3000)
            wait_and_log(page, "Loading WorkspaceExplorer", timeout=20000)
            screenshot(page, "04_workspace_explorer")

            # Inspect available elements
            print("\n   Inspecting page elements...")

            # Look for navigation/menu elements
            buttons = page.locator('button').all()
            print(f"   Found {len(buttons)} buttons")

            links = page.locator('a').all()
            print(f"   Found {len(links)} links")

            # Look for specific Creatio elements
            menu_items = page.locator('[class*="menu"], [class*="nav"], [class*="sidebar"]').all()
            print(f"   Found {len(menu_items)} menu/nav elements")

            # ============================================
            # STEP 4: Explore Configuration
            # ============================================
            print("\n" + "="*60)
            print("STEP 4: Explore Configuration")
            print("="*60)

            # Try to find and click configuration/settings
            config_selectors = [
                'text=Configuration',
                'text=Settings',
                'text=Advanced settings',
                '[title*="Configuration"]',
                '[title*="Settings"]',
                '[class*="config"]',
                '[data-item-marker*="Configuration"]'
            ]

            for selector in config_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        print(f"   Found config element: {selector}")
                        page.locator(selector).first.click()
                        page.wait_for_timeout(2000)
                        screenshot(page, f"05_config_{selector.replace('text=', '').replace(' ', '_')[:20]}")
                        break
                except Exception as e:
                    continue

            # Try direct URL to configuration
            print("   Trying direct configuration URL...")
            page.goto(f"{CREATIO_URL}/0/ClientApp/#/Configuration", timeout=30000)
            page.wait_for_timeout(3000)
            wait_and_log(page, "Loading Configuration page", timeout=20000)
            screenshot(page, "06_configuration_page")

            # ============================================
            # STEP 5: Look for Code Editor
            # ============================================
            print("\n" + "="*60)
            print("STEP 5: Look for Code Editor")
            print("="*60)

            # Common paths to code editing in Creatio
            code_paths = [
                f"{CREATIO_URL}/0/ClientApp/#/SchemaDesigner",
                f"{CREATIO_URL}/0/ClientApp/#/SourceCodeDesigner",
                f"{CREATIO_URL}/0/ClientApp/#/AdvancedSettings",
            ]

            for i, path in enumerate(code_paths):
                try:
                    print(f"   Trying: {path}")
                    page.goto(path, timeout=20000)
                    page.wait_for_timeout(3000)
                    wait_and_log(page, f"Loading {path.split('#/')[-1]}", timeout=15000)
                    screenshot(page, f"07_code_path_{i+1}_{path.split('#/')[-1]}")
                except Exception as e:
                    print(f"   Error: {e}")

            # ============================================
            # STEP 6: Document page structure
            # ============================================
            print("\n" + "="*60)
            print("STEP 6: Document Page Structure")
            print("="*60)

            # Get page content for analysis
            content = page.content()

            # Find all interactive elements
            print("\n   Interactive elements found:")

            # Buttons with text
            buttons_with_text = page.locator('button').all()
            print(f"\n   BUTTONS ({len(buttons_with_text)}):")
            for btn in buttons_with_text[:10]:  # First 10
                try:
                    text = btn.inner_text()[:50] if btn.inner_text() else "(no text)"
                    print(f"      - {text}")
                except:
                    pass

            # Menu items
            print("\n   Looking for menu structure...")
            menu_elements = page.locator('[class*="menu-item"], [class*="nav-item"], [role="menuitem"]').all()
            print(f"   Menu items found: {len(menu_elements)}")
            for item in menu_elements[:10]:
                try:
                    text = item.inner_text()[:50] if item.inner_text() else "(no text)"
                    print(f"      - {text}")
                except:
                    pass

            # Final screenshot
            screenshot(page, "08_final_state")

            print("\n" + "="*60)
            print("TEST COMPLETE")
            print("="*60)
            print(f"\n📁 Screenshots saved to: {SCREENSHOT_DIR}")
            print(f"🔗 Final URL: {page.url}")

        except Exception as e:
            print(f"\n❌ Error occurred: {e}")
            screenshot(page, "99_error_state")
            raise

        finally:
            browser.close()
            print("\n🔒 Browser closed")

if __name__ == "__main__":
    main()
