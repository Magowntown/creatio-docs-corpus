#!/usr/bin/env python3
"""
Inspect Creatio login page DOM structure to find the correct button selector
"""

import os
from playwright.sync_api import sync_playwright

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    print("Loading login page...")
    page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
    page.wait_for_load_state('networkidle', timeout=20000)

    print("\n" + "="*60)
    print("DOM INSPECTION")
    print("="*60)

    # Get all clickable elements
    print("\n1. ALL BUTTONS:")
    buttons = page.query_selector_all('button')
    for i, btn in enumerate(buttons):
        tag = btn.evaluate('el => el.tagName')
        text = btn.evaluate('el => el.innerText')
        classes = btn.evaluate('el => el.className')
        html = btn.evaluate('el => el.outerHTML')
        print(f"   [{i}] <{tag}> text='{text}' class='{classes}'")
        print(f"       HTML: {html[:200]}")

    print("\n2. ALL INPUTS (type=submit/button):")
    inputs = page.query_selector_all('input[type="submit"], input[type="button"]')
    for i, inp in enumerate(inputs):
        tag = inp.evaluate('el => el.tagName')
        value = inp.evaluate('el => el.value')
        classes = inp.evaluate('el => el.className')
        html = inp.evaluate('el => el.outerHTML')
        print(f"   [{i}] <{tag}> value='{value}' class='{classes}'")
        print(f"       HTML: {html[:200]}")

    print("\n3. ELEMENTS CONTAINING 'LOG' TEXT:")
    log_elements = page.query_selector_all('//*[contains(text(), "LOG") or contains(text(), "Log") or contains(text(), "log")]')
    for i, el in enumerate(log_elements):
        tag = el.evaluate('el => el.tagName')
        text = el.evaluate('el => el.innerText')
        classes = el.evaluate('el => el.className')
        html = el.evaluate('el => el.outerHTML')
        print(f"   [{i}] <{tag}> text='{text[:50]}' class='{classes}'")
        print(f"       HTML: {html[:300]}")

    print("\n4. ALL ANCHOR TAGS (<a>):")
    anchors = page.query_selector_all('a')
    for i, a in enumerate(anchors):
        text = a.evaluate('el => el.innerText')
        href = a.evaluate('el => el.href')
        classes = a.evaluate('el => el.className')
        if text.strip():
            print(f"   [{i}] text='{text[:30]}' href='{href[:50]}' class='{classes}'")

    print("\n5. GREEN/PRIMARY STYLED ELEMENTS:")
    styled = page.query_selector_all('[class*="btn"], [class*="button"], [class*="primary"], [class*="submit"], [class*="login"]')
    for i, el in enumerate(styled):
        tag = el.evaluate('el => el.tagName')
        text = el.evaluate('el => el.innerText')
        classes = el.evaluate('el => el.className')
        html = el.evaluate('el => el.outerHTML')
        print(f"   [{i}] <{tag}> text='{text[:30]}' class='{classes}'")
        print(f"       HTML: {html[:300]}")

    print("\n6. FORM STRUCTURE:")
    forms = page.query_selector_all('form')
    for i, form in enumerate(forms):
        html = form.evaluate('el => el.outerHTML')
        print(f"   Form [{i}]:")
        print(f"   {html[:1000]}")

    print("\n7. FULL PAGE HTML (first 5000 chars):")
    html = page.content()
    print(html[:5000])

    browser.close()
