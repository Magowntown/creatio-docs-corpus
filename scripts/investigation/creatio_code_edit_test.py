#!/usr/bin/env python3
"""
Creatio Code Editor Test
Tests ability to open and view code within Creatio Configuration
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

def screenshot(page, name):
    path = f"{SCREENSHOT_DIR}/{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"📸 Screenshot: {path}")
    return path

with sync_playwright() as p:
    print("🚀 Launching browser...")
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    # Login
    print("\n1️⃣ Logging in...")
    page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
    page.wait_for_load_state('networkidle')
    page.fill('input[type="text"]:first-of-type', USERNAME)
    page.fill('input[type="password"]', PASSWORD)
    page.click('[data-item-marker="btnLogin"]')
    page.wait_for_timeout(5000)
    page.wait_for_load_state('networkidle')
    print(f"   ✅ Logged in. URL: {page.url}")

    # Navigate to WorkspaceExplorer
    print("\n2️⃣ Opening WorkspaceExplorer...")
    page.goto(f"{CREATIO_URL}/0/ClientApp/#/WorkspaceExplorer", timeout=30000)
    page.wait_for_timeout(3000)
    page.wait_for_load_state('networkidle')
    screenshot(page, "10_workspace_ready")

    # Look for a schema to open
    print("\n3️⃣ Finding a schema to open...")

    # Click on an object in the list (look for Product or similar)
    schema_selectors = [
        'text=Product *',
        'text=OrderProduct',
        '[title*="Product"]',
        'tr:has-text("Product")',
        'td:has-text("Product")'
    ]

    for sel in schema_selectors:
        try:
            locator = page.locator(sel)
            if locator.count() > 0:
                print(f"   Found schema with: {sel}")
                # Double-click to open
                locator.first.dblclick()
                print(f"   Double-clicked to open schema")
                page.wait_for_timeout(3000)
                screenshot(page, "11_schema_opened")
                break
        except Exception as e:
            print(f"   Failed {sel}: {e}")

    # Wait and inspect what opened
    page.wait_for_load_state('networkidle')
    screenshot(page, "12_after_schema_open")

    # Look for code editor elements
    print("\n4️⃣ Looking for code editor...")
    code_indicators = [
        'textarea',
        '[class*="editor"]',
        '[class*="code"]',
        '[class*="monaco"]',
        '[class*="ace"]',
        '[class*="codemirror"]',
        'pre',
        '[contenteditable="true"]'
    ]

    for ind in code_indicators:
        try:
            count = page.locator(ind).count()
            if count > 0:
                print(f"   ✅ Found code element: {ind} (count: {count})")
        except:
            pass

    # Try to find source code viewer
    print("\n5️⃣ Looking for Source Code option...")
    source_selectors = [
        'text=Source code',
        'text=View source',
        'text=Edit code',
        '[title*="source" i]',
        '[title*="code" i]',
        'button:has-text("Source")',
    ]

    for sel in source_selectors:
        try:
            locator = page.locator(sel)
            if locator.count() > 0:
                print(f"   Found: {sel}")
                locator.first.click()
                page.wait_for_timeout(2000)
                screenshot(page, "13_source_code_view")
                break
        except:
            pass

    # Check current page structure
    print("\n6️⃣ Documenting current page...")
    buttons = page.locator('button').all()
    print(f"   Buttons found: {len(buttons)}")
    for btn in buttons[:15]:
        try:
            text = btn.inner_text()[:30] if btn.inner_text() else "(no text)"
            print(f"      - {text}")
        except:
            pass

    # Final screenshot
    screenshot(page, "14_final_state")
    print(f"\n🔗 Final URL: {page.url}")

    browser.close()
    print("\n✅ Test complete!")
