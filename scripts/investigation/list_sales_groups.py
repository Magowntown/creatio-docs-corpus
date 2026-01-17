#!/usr/bin/env python3
"""List all Sales Groups to find the RDGZ one."""

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


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = browser.new_page()

        page.goto(f"{PROD_URL}/Login/NuiLogin.aspx", timeout=90000)
        page.wait_for_timeout(2000)
        page.fill('input[type="text"]:first-of-type', USERNAME)
        page.fill('input[type="password"]', PASSWORD)
        page.click('[data-item-marker="btnLogin"]')
        page.wait_for_timeout(8000)

        result = page.evaluate('''async () => {
            const getCookie = (name) => {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${name}=`);
                if (parts.length === 2) return parts.pop().split(';').shift();
                return "";
            };
            const bpmcsrf = getCookie("BPMCSRF");

            // Get ALL Sales Groups
            const resp = await fetch("/0/odata/BGSalesGroup?$select=Id,BGName&$orderby=BGName",
                { headers: { "BPMCSRF": bpmcsrf } });
            if (resp.ok) {
                return await resp.json();
            }
            return { error: "failed" };
        }''')

        print("ALL SALES GROUPS:")
        print("-" * 50)
        if result.get('value'):
            for sg in result['value']:
                name = sg.get('BGName', 'unknown')
                marker = ' <-- RDGZ?' if 'rdgz' in name.lower() or 'consulting' in name.lower() else ''
                print(f"  {name}{marker}")
                print(f"    ID: {sg.get('Id')}")

        browser.close()


if __name__ == "__main__":
    main()
