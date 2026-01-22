#!/usr/bin/env python3
"""
Test script to verify the UsrPage_ebkv9e8 visibility handler is working.
Uses Playwright to:
1. Navigate to Reports page
2. Select different reports
3. Verify filter visibility toggles correctly
"""

import os
import asyncio
from playwright.async_api import async_playwright

# Load environment
env_path = "/home/magown/creatio-report-fix/.env"
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value


async def test_visibility(env_name):
    """Test filter visibility toggling"""

    if env_name == "DEV":
        url = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
        username = os.environ.get("CREATIO_USERNAME", "Supervisor")
        password = os.environ.get("CREATIO_PASSWORD", "")
    else:
        url = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com")
        username = os.environ.get("CREATIO_PROD_USERNAME", "Supervisor")
        password = os.environ.get("CREATIO_PROD_PASSWORD", "")

    print(f"\n{'='*70}")
    print(f"TESTING VISIBILITY HANDLER - {env_name}")
    print(f"{'='*70}")
    print(f"URL: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1400, "height": 900})
        page = await context.new_page()

        # Enable console logging
        page.on("console", lambda msg: print(f"[CONSOLE] {msg.text}") if "[UsrPage_ebkv9e8" in msg.text else None)

        try:
            # Step 1: Login
            print(f"\n[1] Logging in...")
            await page.goto(f"{url}/Login/NuiLogin.aspx", timeout=60000)
            await page.fill('input[name="UserName"]', username)
            await page.fill('input[name="UserPassword"]', password)
            await page.click('button[type="submit"], .login-button')
            await page.wait_for_load_state("networkidle", timeout=60000)
            print(f"    Login successful")

            # Step 2: Navigate to Reports page
            print(f"\n[2] Navigating to Reports page...")
            reports_url = f"{url}/0/Nui/ViewModule.aspx#SectionModuleV2/UsrPage_ebkv9e8Section"
            await page.goto(reports_url, timeout=60000)
            await asyncio.sleep(5)  # Wait for page to fully load

            # Take initial screenshot
            await page.screenshot(path="/tmp/visibility_test_initial.png")
            print(f"    Screenshot: /tmp/visibility_test_initial.png")

            # Step 3: Find report dropdown
            print(f"\n[3] Finding report dropdown...")
            # Look for the report selector by various selectors
            report_dropdown = await page.query_selector('[data-item-marker="ComboBox_bo00lsk"]')
            if not report_dropdown:
                report_dropdown = await page.query_selector('.t-combo-box-edit')
            if not report_dropdown:
                report_dropdown = await page.query_selector('input[placeholder*="Report"]')

            if report_dropdown:
                print(f"    Found report dropdown")

                # Step 4: Test Commission report selection
                print(f"\n[4] Selecting 'Commission' report...")
                await report_dropdown.click()
                await asyncio.sleep(1)

                # Find Commission option in dropdown
                commission_option = await page.query_selector('text=Commission')
                if commission_option:
                    await commission_option.click()
                    await asyncio.sleep(2)

                    # Take screenshot after Commission selection
                    await page.screenshot(path="/tmp/visibility_test_commission.png")
                    print(f"    Screenshot: /tmp/visibility_test_commission.png")

                    # Check for Commission filters
                    year_month = await page.query_selector('[data-item-marker="YearMonthCombo"]')
                    sales_group = await page.query_selector('[data-item-marker="SalesGroupCombo"]')
                    warning_label = await page.query_selector('text=QuickBooks')

                    print(f"\n    Commission filter visibility:")
                    print(f"      Year-Month: {'VISIBLE' if year_month else 'HIDDEN'}")
                    print(f"      Sales Group: {'VISIBLE' if sales_group else 'HIDDEN'}")
                    print(f"      Warning label: {'VISIBLE' if warning_label else 'HIDDEN'}")

                    # Check date filters
                    created_from = await page.query_selector('[data-item-marker="CreatedFrom"]')
                    shipping_from = await page.query_selector('[data-item-marker="ShippingFrom"]')

                    print(f"\n    Date filter visibility:")
                    print(f"      CreatedFrom: {'VISIBLE' if created_from else 'HIDDEN'}")
                    print(f"      ShippingFrom: {'VISIBLE' if shipping_from else 'HIDDEN'}")

                else:
                    print(f"    ERROR: Commission option not found in dropdown")

                # Step 5: Test non-Commission report selection
                print(f"\n[5] Selecting 'Sales By Line' report...")
                await report_dropdown.click()
                await asyncio.sleep(1)

                sales_line_option = await page.query_selector('text=Sales By Line')
                if sales_line_option:
                    await sales_line_option.click()
                    await asyncio.sleep(2)

                    # Take screenshot after Sales By Line selection
                    await page.screenshot(path="/tmp/visibility_test_sales_line.png")
                    print(f"    Screenshot: /tmp/visibility_test_sales_line.png")

                    # Check for Commission filters (should be hidden)
                    year_month = await page.query_selector('[data-item-marker="YearMonthCombo"]')
                    sales_group = await page.query_selector('[data-item-marker="SalesGroupCombo"]')

                    print(f"\n    Commission filter visibility:")
                    print(f"      Year-Month: {'VISIBLE' if year_month else 'HIDDEN'}")
                    print(f"      Sales Group: {'VISIBLE' if sales_group else 'HIDDEN'}")

                    # Check date filters (should be visible)
                    created_from = await page.query_selector('[data-item-marker="CreatedFrom"]')
                    shipping_from = await page.query_selector('[data-item-marker="ShippingFrom"]')

                    print(f"\n    Date filter visibility:")
                    print(f"      CreatedFrom: {'VISIBLE' if created_from else 'HIDDEN'}")
                    print(f"      ShippingFrom: {'VISIBLE' if shipping_from else 'HIDDEN'}")

                else:
                    print(f"    ERROR: Sales By Line option not found")

            else:
                print(f"    ERROR: Report dropdown not found")
                await page.screenshot(path="/tmp/visibility_test_error.png")
                print(f"    Screenshot: /tmp/visibility_test_error.png")

            print(f"\n{'='*70}")
            print(f"TEST COMPLETED")
            print(f"{'='*70}")

            # Keep browser open for manual inspection
            print("\nBrowser will stay open for 30 seconds for manual inspection...")
            await asyncio.sleep(30)

        except Exception as e:
            print(f"\n[ERROR] {e}")
            await page.screenshot(path="/tmp/visibility_test_error.png")
            print(f"Screenshot: /tmp/visibility_test_error.png")

        finally:
            await browser.close()


if __name__ == "__main__":
    import sys
    env = sys.argv[1] if len(sys.argv) > 1 else "DEV"
    asyncio.run(test_visibility(env))
