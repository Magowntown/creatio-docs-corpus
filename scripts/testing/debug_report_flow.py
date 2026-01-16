#!/usr/bin/env python3
"""
Debug the report download flow in PROD.
Captures all network requests to see what endpoints are being called.
"""

from playwright.sync_api import sync_playwright
import time
import json

CREATIO_URL = "https://pampabay.creatio.com"
USERNAME = "Supervisor"
PASSWORD = "123*Pampa?"

def main():
    all_requests = []
    all_responses = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        # Capture ALL network activity
        def on_request(request):
            all_requests.append({
                'time': time.time(),
                'method': request.method,
                'url': request.url,
                'post_data': request.post_data[:200] if request.post_data else None
            })
            if 'Excel' in request.url or 'Report' in request.url or 'Generate' in request.url:
                print(f"  >>> {request.method} {request.url}")
                if request.post_data:
                    print(f"      POST: {request.post_data[:100]}...")

        def on_response(response):
            all_responses.append({
                'time': time.time(),
                'status': response.status,
                'url': response.url
            })
            if 'Excel' in response.url or 'Report' in response.url or 'Generate' in response.url:
                print(f"  <<< {response.status} {response.url}")

        page.on('request', on_request)
        page.on('response', on_response)

        # Capture console logs
        def on_console(msg):
            text = msg.text
            if 'report' in text.lower() or 'download' in text.lower() or 'error' in text.lower() or 'url' in text.lower():
                print(f"  [CONSOLE] {msg.type}: {text[:200]}")

        page.on('console', on_console)

        try:
            # Login
            print("[1] Logging in...")
            page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", wait_until='networkidle', timeout=60000)
            time.sleep(2)

            visible_inputs = page.locator('input:visible')
            visible_inputs.first.fill(USERNAME)
            visible_inputs.nth(1).fill(PASSWORD)
            page.locator('text=LOG IN').first.click()

            page.wait_for_load_state('networkidle', timeout=60000)
            time.sleep(5)
            print("    Logged in")

            # Navigate to a page with Commission report
            # Try the main shell first
            print("[2] Navigating to main app...")
            page.goto(f"{CREATIO_URL}/0/Shell", wait_until='networkidle', timeout=60000)
            time.sleep(5)
            page.screenshot(path='/tmp/debug_01_shell.png')
            print("    Screenshot: /tmp/debug_01_shell.png")

            # Look for any report-related elements
            print("[3] Looking for report elements...")

            # Search for text containing "Commission" or "Reporte"
            commission_elements = page.locator('text=Commission').all()
            reporte_elements = page.locator('text=Reporte').all()

            print(f"    Found {len(commission_elements)} 'Commission' elements")
            print(f"    Found {len(reporte_elements)} 'Reporte' elements")

            # Try to find and click on Pampa Reports section
            print("[4] Looking for Pampa Reports...")

            # Click on menu items that might lead to reports
            menu_items = page.locator('[class*="menu"], [class*="nav"], [role="menuitem"]').all()
            print(f"    Found {len(menu_items)} menu-like elements")

            # Take a screenshot of current state
            page.screenshot(path='/tmp/debug_02_main.png')
            print("    Screenshot: /tmp/debug_02_main.png")

            # Try direct navigation to UsrReportesPampa list
            print("[5] Navigating to Pampa Reports section...")
            page.goto(f"{CREATIO_URL}/0/Nui/ViewModule.aspx#SectionModuleV2/UsrReportesPampaSectionV2",
                     wait_until='networkidle', timeout=60000)
            time.sleep(10)
            page.screenshot(path='/tmp/debug_03_reports_section.png')
            print("    Screenshot: /tmp/debug_03_reports_section.png")

            # Look for Commission report row
            print("[6] Looking for Commission report...")
            commission_row = page.locator('text=Commission').first
            if commission_row.count() > 0:
                print("    Found Commission, clicking...")
                commission_row.click()
                time.sleep(3)
                page.screenshot(path='/tmp/debug_04_commission_selected.png')
                print("    Screenshot: /tmp/debug_04_commission_selected.png")

                # Look for the report generation button
                print("[7] Looking for report button...")
                buttons = page.locator('button, [role="button"]').all()
                for i, btn in enumerate(buttons[:15]):
                    try:
                        text = btn.inner_text()
                        if text:
                            print(f"    Button {i}: '{text[:50]}'")
                    except:
                        pass

                # Try to find "Generar" or "Generate" or "Excel" button
                gen_btn = page.locator('text=Generar').first
                if gen_btn.count() == 0:
                    gen_btn = page.locator('text=Generate').first
                if gen_btn.count() == 0:
                    gen_btn = page.locator('text=Excel').first
                if gen_btn.count() == 0:
                    gen_btn = page.locator('[data-item-marker*="Report"]').first

                if gen_btn.count() > 0:
                    print("[8] Clicking report button...")
                    print("-" * 50)
                    gen_btn.click()

                    # Wait and capture network activity
                    time.sleep(30)
                    print("-" * 50)

                    page.screenshot(path='/tmp/debug_05_after_click.png')
                    print("    Screenshot: /tmp/debug_05_after_click.png")
                else:
                    print("    No report button found")

            # Summary
            print("\n" + "=" * 60)
            print("NETWORK SUMMARY - Report/Excel related requests:")
            print("=" * 60)

            for req in all_requests:
                if 'Excel' in req['url'] or 'Report' in req['url'] or 'Generate' in req['url']:
                    print(f"{req['method']} {req['url']}")
                    if req['post_data']:
                        print(f"    POST: {req['post_data']}")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path='/tmp/debug_error.png')
            print("Error screenshot: /tmp/debug_error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    main()
