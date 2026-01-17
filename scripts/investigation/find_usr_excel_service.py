#!/usr/bin/env python3
"""Find UsrExcelReportService and check what package it's in."""

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
    print("=" * 60)
    print("FINDING UsrExcelReportService")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = browser.new_page()

        # Login
        print("\n1. Logging in...")
        page.goto(f"{PROD_URL}/Login/NuiLogin.aspx", timeout=60000)
        page.wait_for_timeout(2000)
        page.fill('input[type="text"]:first-of-type', USERNAME)
        page.fill('input[type="password"]', PASSWORD)
        page.click('[data-item-marker="btnLogin"]')
        page.wait_for_timeout(8000)
        print("   Logged in")

        print("\n2. Searching for schemas...")

        result = page.evaluate('''async () => {
            const getCookie = (name) => {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${name}=`);
                if (parts.length === 2) return parts.pop().split(';').shift();
                return "";
            };
            const bpmcsrf = getCookie("BPMCSRF");

            let findings = { schemas: [], packages: {} };

            // Search for UsrExcelReport schemas
            const url1 = "/0/odata/SysSchema?$filter=contains(Name,'UsrExcel') or contains(Name,'ExcelReport')&$select=UId,Name,ManagerName,SysPackageId,ModifiedOn&$orderby=ModifiedOn desc";
            try {
                const resp = await fetch(url1, { headers: { "BPMCSRF": bpmcsrf } });
                if (resp.ok) {
                    const data = await resp.json();
                    findings.schemas = data.value || [];
                }
            } catch(e) { findings.error = e.message; }

            // Get package names
            const pkgIds = [...new Set(findings.schemas.map(s => s.SysPackageId))];
            for (const pkgId of pkgIds) {
                try {
                    const resp = await fetch(`/0/odata/SysPackage(${pkgId})?$select=Name`, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) { findings.packages[pkgId] = (await resp.json()).Name; }
                } catch(e) {}
            }

            // Also search for "Int" excel report (the underlying service)
            const url2 = "/0/odata/SysSchema?$filter=contains(Name,'IntExcel')&$select=UId,Name,ManagerName,SysPackageId,ModifiedOn&$orderby=ModifiedOn desc";
            try {
                const resp = await fetch(url2, { headers: { "BPMCSRF": bpmcsrf } });
                if (resp.ok) {
                    const data = await resp.json();
                    findings.intSchemas = data.value || [];
                    // Get those package names too
                    for (const s of findings.intSchemas) {
                        if (!findings.packages[s.SysPackageId]) {
                            try {
                                const resp2 = await fetch(`/0/odata/SysPackage(${s.SysPackageId})?$select=Name`, { headers: { "BPMCSRF": bpmcsrf } });
                                if (resp2.ok) { findings.packages[s.SysPackageId] = (await resp2.json()).Name; }
                            } catch(e) {}
                        }
                    }
                }
            } catch(e) {}

            return findings;
        }''')

        print("\n3. Results:")
        print("-" * 40)

        if result.get('schemas'):
            print("\nUsrExcel/ExcelReport Schemas:")
            for s in result['schemas']:
                pkg = result.get('packages', {}).get(s.get('SysPackageId'), 'unknown')
                mod = str(s.get('ModifiedOn', ''))[:19]
                mgr = s.get('ManagerName', 'unknown')
                print(f"  - {s.get('Name')}")
                print(f"    Type: {mgr}")
                print(f"    Package: {pkg}")
                print(f"    Modified: {mod}")
                print(f"    UId: {s.get('UId')}")
                print()
        else:
            print("\nNo UsrExcel/ExcelReport schemas found")

        if result.get('intSchemas'):
            print("\nIntExcel Schemas (underlying service):")
            for s in result['intSchemas']:
                pkg = result.get('packages', {}).get(s.get('SysPackageId'), 'unknown')
                mod = str(s.get('ModifiedOn', ''))[:19]
                mgr = s.get('ManagerName', 'unknown')
                print(f"  - {s.get('Name')}")
                print(f"    Type: {mgr}")
                print(f"    Package: {pkg}")
                print(f"    Modified: {mod}")
                print()

        browser.close()


if __name__ == "__main__":
    main()
