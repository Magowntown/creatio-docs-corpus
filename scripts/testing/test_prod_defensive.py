#!/usr/bin/env python3
"""
Test the defensive UsrPage_ebkv9e8 deployment in PROD.
Opens browser for manual testing and captures console logs.
"""

from playwright.sync_api import sync_playwright
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from dotenv import load_dotenv
load_dotenv(REPO_ROOT / ".env")

PROD_URL = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_PROD_USERNAME", "Supervisor")
PASSWORD = os.environ.get("CREATIO_PROD_PASSWORD", "")


def wait_for_stable(page, timeout=5000):
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    page.wait_for_timeout(1000)


def screenshot(page, name):
    screenshots_dir = REPO_ROOT / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)
    path = screenshots_dir / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    print(f"   📸 Screenshot: {path.name}")
    return path


def main():
    print("=" * 60)
    print("TESTING DEFENSIVE UsrPage_ebkv9e8 IN PROD")
    print("=" * 60)
    print(f"Target: {PROD_URL}")
    print("")

    console_logs = []

    with sync_playwright() as p:
        print("\n🚀 Launching browser (non-headless)...")
        browser = p.chromium.launch(headless=False, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        # Capture console logs
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))

        try:
            # Login
            print(f"\n1️⃣ Logging into PROD...")
            page.goto(f"{PROD_URL}/Login/NuiLogin.aspx", timeout=60000)
            wait_for_stable(page)
            page.fill('input[type="text"]:first-of-type', USERNAME)
            page.fill('input[type="password"]', PASSWORD)
            page.click('[data-item-marker="btnLogin"]')
            page.wait_for_timeout(8000)
            wait_for_stable(page)
            print("   ✅ Logged in")
            screenshot(page, "test_defensive_01_logged_in")

            # Navigate to Reports page
            print(f"\n2️⃣ Opening Reports page (UsrPage_ebkv9e8)...")
            # Try direct navigation to the page
            reports_url = f"{PROD_URL}/0/ClientApp/#/UsrPage_ebkv9e8"
            page.goto(reports_url, timeout=60000)
            page.wait_for_timeout(5000)
            wait_for_stable(page, 10000)
            screenshot(page, "test_defensive_02_reports_page")

            # Check console for defensive logs
            print("\n3️⃣ Checking console logs for defensive markers...")
            defensive_logs = [log for log in console_logs if "[UsrPage_ebkv9e8]" in log]
            if defensive_logs:
                print("   ✅ Defensive code is active! Found logs:")
                for log in defensive_logs[:5]:
                    print(f"      {log}")
            else:
                print("   ℹ️ No defensive logs yet (normal if no errors occurred)")

            # Test: Look for report dropdown
            print("\n4️⃣ Looking for report components...")
            try:
                # Wait for any dropdown or combobox
                page.wait_for_selector('[class*="combobox"], [class*="dropdown"], [class*="lookup"]', timeout=10000)
                print("   ✅ Report components found")
            except:
                print("   ⚠️ Report components not detected (page may use different layout)")

            screenshot(page, "test_defensive_03_components")

            # Manual test instructions
            print("\n" + "=" * 60)
            print("MANUAL TESTING PHASE")
            print("=" * 60)
            print("""
Please perform these tests in the browser:

1. SELECT A REPORT
   - Click the Report dropdown
   - Select "Commission"

2. SELECT YEAR-MONTH
   - Click the Year-Month dropdown
   - Select any month (e.g., "2024-12")

3. OBSERVE SALES GROUP CASCADE
   - The Sales Group dropdown should filter based on Year-Month
   - If it shows all groups or filters correctly = SUCCESS
   - If page freezes or errors = PROBLEM

4. GENERATE REPORT
   - Click "Generate" or "Export" button
   - Report should download

5. CHECK CONSOLE (F12 > Console)
   - Look for [UsrPage_ebkv9e8] messages
   - Any errors should be logged but NOT block functionality

Press Enter when testing is complete...
""")

            input()

            # Capture final state
            screenshot(page, "test_defensive_04_after_manual")

            # Print all console logs
            print("\n📋 Console Log Summary:")
            print("-" * 40)

            defensive_logs = [log for log in console_logs if "[UsrPage_ebkv9e8]" in log]
            error_logs = [log for log in console_logs if log.startswith("[error]")]

            if defensive_logs:
                print("\nDefensive Code Logs:")
                for log in defensive_logs:
                    print(f"  {log}")

            if error_logs:
                print("\nErrors:")
                for log in error_logs[:10]:
                    print(f"  {log}")

            print(f"\nTotal logs captured: {len(console_logs)}")
            print(f"Defensive logs: {len(defensive_logs)}")
            print(f"Errors: {len(error_logs)}")

        except Exception as e:
            print(f"\n❌ Test error: {e}")
            import traceback
            traceback.print_exc()
            screenshot(page, "test_defensive_error")

        print("\n⏳ Browser will close in 5 seconds...")
        page.wait_for_timeout(5000)
        browser.close()

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
