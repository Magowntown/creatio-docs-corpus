#!/usr/bin/env python3
"""
Capture network requests when clicking the Report button in PROD.
This helps debug which endpoint is being called for GetReport.
"""

from playwright.sync_api import sync_playwright
import time
import json

CREATIO_URL = "https://pampabay.creatio.com"
USERNAME = "Supervisor"
PASSWORD = "123*Pampa?"

# Go to Pampa Reports page
REPORTS_PAGE_URL = f"{CREATIO_URL}/0/ClientApp/#/UsrReportesPampa_FormPage/view/a6e4beab-1c7c-4cfa-be14-2d20b03f22a5"

def main():
    captured_requests = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        # Capture network requests
        def handle_request(request):
            url = request.url
            if 'ExcelReport' in url or 'GetReport' in url or 'Generate' in url:
                captured_requests.append({
                    'method': request.method,
                    'url': url,
                    'time': time.time()
                })
                print(f"  [REQ] {request.method} {url}")

        def handle_response(response):
            url = response.url
            if 'ExcelReport' in url or 'GetReport' in url or 'Generate' in url:
                print(f"  [RES] {response.status} {url}")

        page.on('request', handle_request)
        page.on('response', handle_response)

        try:
            # Step 1: Login
            print("[1] Logging in...")
            page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", wait_until='networkidle', timeout=60000)
            page.wait_for_load_state('networkidle')
            time.sleep(2)

            visible_inputs = page.locator('input:visible')
            visible_inputs.first.fill(USERNAME)
            visible_inputs.nth(1).fill(PASSWORD)
            page.locator('text=LOG IN').first.click()

            page.wait_for_load_state('networkidle', timeout=60000)
            time.sleep(5)
            print("    Login complete")

            # Step 2: Navigate to reports page
            print("[2] Navigating to reports page...")
            page.goto(REPORTS_PAGE_URL, wait_until='networkidle', timeout=60000)
            time.sleep(5)
            page.screenshot(path='/tmp/capture_01_page.png')
            print("    Screenshot: /tmp/capture_01_page.png")

            # Step 3: Find the "Generar Reporte Pampa" button
            print("[3] Looking for report button...")

            # Look for buttons with Report-related text
            buttons = page.locator('button, [role="button"]').all()
            report_button = None
            for btn in buttons:
                try:
                    text = btn.inner_text().lower()
                    if 'reporte' in text or 'report' in text or 'generar' in text:
                        print(f"    Found button: '{btn.inner_text()}'")
                        report_button = btn
                        break
                except:
                    pass

            if not report_button:
                # Try looking for the specific button by data attribute
                report_button = page.locator('[data-item-marker*="Report"], [data-item-marker*="Excel"]').first
                if report_button.count() == 0:
                    report_button = None

            if not report_button:
                print("    No report button found, listing all buttons:")
                for i, btn in enumerate(buttons[:20]):
                    try:
                        print(f"    [{i}] '{btn.inner_text()}'")
                    except:
                        pass
                page.screenshot(path='/tmp/capture_02_buttons.png')
                return

            # Step 4: Click the button and capture requests
            print("[4] Clicking report button and capturing requests...")
            print("-" * 50)

            report_button.click()

            # Wait for requests
            time.sleep(30)  # Wait up to 30 seconds for the report flow

            print("-" * 50)
            page.screenshot(path='/tmp/capture_03_after_click.png')
            print("    Screenshot: /tmp/capture_03_after_click.png")

            # Step 5: Summary
            print()
            print("=" * 60)
            print("CAPTURED REQUESTS:")
            print("=" * 60)
            for req in captured_requests:
                print(f"  {req['method']} {req['url']}")

            if not captured_requests:
                print("  No Excel/Report-related requests captured")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path='/tmp/capture_error.png')
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    main()
