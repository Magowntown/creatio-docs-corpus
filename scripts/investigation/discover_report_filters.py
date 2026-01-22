#!/usr/bin/env python3
"""
Discover filter fields for each report by interacting with the Reports page.
Uses Playwright to select each report and capture what filter fields appear.
"""

from playwright.sync_api import sync_playwright
import os
import json
import time
from pathlib import Path

# Configuration
CREATIO_URL = os.environ.get("CREATIO_URL", "https://pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# Reports page URL
REPORTS_PAGE_URL = f"{CREATIO_URL}/0/ClientApp/#/UsrPage_ebkv9e8"

SCREENSHOT_DIR = Path(__file__).parent.parent.parent / "test-artifacts" / "report-discovery"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = Path(__file__).parent.parent.parent / "docs" / "REPORT_FILTER_MAPPING.md"

def screenshot(page, name):
    path = SCREENSHOT_DIR / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    print(f"  Screenshot: {name}")
    return path

def wait_for_stable(page, timeout=5000):
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    page.wait_for_timeout(1000)

def login(page):
    """Login to Creatio"""
    print("\n1. Logging in to Creatio...")
    page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
    wait_for_stable(page)
    page.wait_for_timeout(3000)

    # Try various selectors for username
    username_selectors = [
        'input[placeholder*="Username"]',
        'input[placeholder*="username"]',
        'input[type="text"]',
        '#loginEdit-el',
        '[data-item-marker="login-edit"] input',
    ]

    for sel in username_selectors:
        try:
            loc = page.locator(sel).first
            if loc.count() > 0 and loc.is_visible():
                loc.click()
                page.wait_for_timeout(200)
                loc.fill(USERNAME)
                print(f"  Filled username via: {sel}")
                break
        except:
            continue

    # Try various selectors for password
    password_selectors = [
        'input[placeholder*="Password"]',
        'input[placeholder*="password"]',
        'input[type="password"]',
        '#passwordEdit-el',
        '[data-item-marker="password-edit"] input',
    ]

    for sel in password_selectors:
        try:
            loc = page.locator(sel).first
            if loc.count() > 0 and loc.is_visible():
                loc.click()
                page.wait_for_timeout(200)
                loc.fill(PASSWORD)
                print(f"  Filled password via: {sel}")
                break
        except:
            continue

    # Click login button
    login_selectors = [
        'button:has-text("Log in")',
        'button:has-text("Login")',
        '[data-item-marker="login-button"]',
        '.login-button',
        'button[type="submit"]',
    ]

    for sel in login_selectors:
        try:
            loc = page.locator(sel).first
            if loc.count() > 0 and loc.is_visible():
                loc.click()
                print(f"  Clicked login via: {sel}")
                break
        except:
            continue

    # Wait for login to complete
    page.wait_for_timeout(5000)
    wait_for_stable(page)
    print("  Login completed")

def get_visible_filter_fields(page):
    """Get currently visible filter field labels/names"""
    fields = []

    # Look for label elements that might indicate filter fields
    label_selectors = [
        '[class*="label"]',
        '[class*="field-label"]',
        'label',
        '[class*="caption"]',
    ]

    for sel in label_selectors:
        try:
            labels = page.locator(sel).all()
            for label in labels:
                try:
                    text = label.inner_text().strip()
                    if text and len(text) < 50 and text not in fields:
                        fields.append(text)
                except:
                    continue
        except:
            continue

    # Also look for input placeholders
    try:
        inputs = page.locator('input[placeholder]').all()
        for inp in inputs:
            try:
                placeholder = inp.get_attribute('placeholder')
                if placeholder and placeholder not in fields:
                    fields.append(f"[input] {placeholder}")
            except:
                continue
    except:
        pass

    # Look for dropdown/combobox labels
    try:
        combos = page.locator('[class*="combobox"], [class*="dropdown"], [class*="lookup"]').all()
        for combo in combos:
            try:
                # Try to get associated label
                parent = combo.locator('xpath=..').first
                label = parent.locator('[class*="label"]').first
                if label.count() > 0:
                    text = label.inner_text().strip()
                    if text and text not in fields:
                        fields.append(f"[combo] {text}")
            except:
                continue
    except:
        pass

    return fields

def discover_reports(page):
    """Navigate to reports page and discover all reports with their filter fields"""
    print("\n2. Navigating to Reports page...")
    page.goto(REPORTS_PAGE_URL, timeout=30000)
    wait_for_stable(page)
    page.wait_for_timeout(3000)
    screenshot(page, "01_reports_page_initial")

    reports = {}

    # Find the report dropdown/lookup
    print("\n3. Finding report selector...")

    # Look for the report selection dropdown
    report_selector = None
    dropdown_selectors = [
        '[data-item-marker*="Report"]',
        '[data-item-marker*="report"]',
        '[class*="lookup"][class*="report"]',
        'crt-combobox-edit',
        '[class*="combobox"]',
    ]

    # First, let's capture the page structure
    print("\n4. Capturing page structure...")

    # Get all visible text on the page
    try:
        body_text = page.locator('body').inner_text()
        print(f"  Page text length: {len(body_text)} chars")

        # Look for common report-related terms
        if 'Report' in body_text or 'report' in body_text:
            print("  Found 'Report' on page")
        if 'Commission' in body_text:
            print("  Found 'Commission' on page")
        if 'Year' in body_text or 'Month' in body_text:
            print("  Found Year/Month on page")
        if 'Sales' in body_text:
            print("  Found 'Sales' on page")
    except Exception as e:
        print(f"  Error getting page text: {e}")

    # Try to find all combobox/lookup elements
    print("\n5. Looking for dropdown elements...")
    try:
        # Freedom UI often uses these patterns
        dropdowns = page.locator('[class*="combobox"], [class*="lookup"], [class*="dropdown"], [class*="select"]').all()
        print(f"  Found {len(dropdowns)} dropdown-like elements")

        for i, dd in enumerate(dropdowns):
            try:
                # Get attributes and text
                classes = dd.get_attribute('class') or ''
                marker = dd.get_attribute('data-item-marker') or ''
                text = dd.inner_text()[:100] if dd.inner_text() else ''
                print(f"    [{i}] marker={marker}, classes={classes[:50]}, text={text[:30]}")
            except:
                pass
    except Exception as e:
        print(f"  Error finding dropdowns: {e}")

    # Try to click on the report dropdown and get options
    print("\n6. Trying to interact with report dropdown...")

    # First, let's look at the console logs to see data loading
    console_messages = []
    page.on('console', lambda msg: console_messages.append(msg.text))

    # Look for the specific lookup attribute from our handler code
    # LookupAttribute_bsixu8a is the report dropdown
    try:
        # Try clicking on elements that might be the report dropdown
        click_targets = [
            '[data-item-marker*="bsixu8a"]',
            '[data-item-marker*="Report"]',
            'text=Select report',
            'text=Commission',
            '[class*="lookup"]',
        ]

        for target in click_targets:
            try:
                elem = page.locator(target).first
                if elem.count() > 0 and elem.is_visible():
                    print(f"  Clicking: {target}")
                    elem.click()
                    page.wait_for_timeout(2000)
                    screenshot(page, f"02_after_click_{target.replace('[', '').replace(']', '').replace('*', '').replace('=', '_')[:20]}")

                    # Look for dropdown options that appeared
                    options = page.locator('[class*="option"], [class*="list-item"], [class*="menu-item"], [role="option"]').all()
                    print(f"  Found {len(options)} options after clicking")

                    for opt in options[:10]:  # Limit to first 10
                        try:
                            opt_text = opt.inner_text().strip()
                            if opt_text:
                                print(f"    - {opt_text}")
                        except:
                            pass

                    break
            except Exception as e:
                print(f"  Error with {target}: {e}")
                continue
    except Exception as e:
        print(f"  Error interacting with dropdowns: {e}")

    # Print console messages
    if console_messages:
        print("\n7. Console messages (last 20):")
        for msg in console_messages[-20:]:
            if 'UsrPage' in msg or 'Report' in msg or 'Filter' in msg:
                print(f"  {msg[:200]}")

    screenshot(page, "03_final_state")

    return reports

def main():
    print("=" * 60)
    print("REPORT FILTER FIELD DISCOVERY")
    print("=" * 60)
    print(f"URL: {CREATIO_URL}")
    print(f"Output: {OUTPUT_FILE}")

    if not USERNAME or not PASSWORD:
        print("\nERROR: Set CREATIO_USERNAME and CREATIO_PASSWORD environment variables")
        print("Example: source .env && python3 scripts/investigation/discover_report_filters.py")
        return

    with sync_playwright() as p:
        print("\nLaunching browser...")
        browser = p.chromium.launch(headless=False, args=['--no-sandbox'])  # headless=False to see what's happening
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        try:
            login(page)
            reports = discover_reports(page)

            # Write results
            print("\n" + "=" * 60)
            print("DISCOVERY RESULTS")
            print("=" * 60)
            print(json.dumps(reports, indent=2))

        except Exception as e:
            print(f"\nError: {e}")
            screenshot(page, "error_state")
            raise
        finally:
            print("\nClosing browser in 10 seconds (inspect if needed)...")
            page.wait_for_timeout(10000)
            browser.close()

if __name__ == "__main__":
    main()
