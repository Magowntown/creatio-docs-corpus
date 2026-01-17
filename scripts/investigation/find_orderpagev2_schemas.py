#!/usr/bin/env python3
"""
Find ALL OrderPageV2 schemas in PROD via browser automation.
"""

from playwright.sync_api import sync_playwright
import os
import sys
import json
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


def main():
    print("=" * 60)
    print("FINDING ALL OrderPageV2 SCHEMAS IN PROD")
    print("=" * 60)

    with sync_playwright() as p:
        print("\nLaunching browser...")
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        try:
            # Login
            print("\n1. Logging into PROD...")
            page.goto(f"{PROD_URL}/Login/NuiLogin.aspx", timeout=60000)
            wait_for_stable(page)
            page.fill('input[type="text"]:first-of-type', USERNAME)
            page.fill('input[type="password"]', PASSWORD)
            page.click('[data-item-marker="btnLogin"]')
            page.wait_for_timeout(8000)
            wait_for_stable(page)
            print("   Logged in")

            # Query for OrderPageV2 schemas via JavaScript fetch
            print("\n2. Querying for OrderPageV2 schemas...")

            result = page.evaluate('''async () => {
                const getCookie = (name) => {
                    const value = `; ${document.cookie}`;
                    const parts = value.split(`; ${name}=`);
                    if (parts.length === 2) return parts.pop().split(';').shift();
                    return "";
                };
                const bpmcsrf = getCookie("BPMCSRF");

                // Query 1: Find all OrderPageV2 client schemas
                const url1 = "/0/odata/VwSysClientUnitSchema?$filter=contains(Name,'OrderPage')&$select=UId,Name,PackageUId,ModifiedOn&$orderby=ModifiedOn desc";
                const resp1 = await fetch(url1, {
                    headers: { "BPMCSRF": bpmcsrf }
                });
                const data1 = await resp1.json();

                // Query 2: Get package names
                const packageIds = [...new Set(data1.value.map(s => s.PackageUId))];
                let packages = {};
                for (const pkgId of packageIds) {
                    try {
                        const pkgUrl = `/0/odata/SysPackage(${pkgId})?$select=Name,Caption`;
                        const pkgResp = await fetch(pkgUrl, { headers: { "BPMCSRF": bpmcsrf } });
                        if (pkgResp.ok) {
                            const pkg = await pkgResp.json();
                            packages[pkgId] = pkg.Name || pkg.Caption || pkgId;
                        }
                    } catch(e) {
                        packages[pkgId] = pkgId;
                    }
                }

                // Query 3: Check Order entity for PaymentStatus default
                const url3 = "/0/odata/SysEntitySchemaColumn?$filter=SysEntitySchema/Name eq 'Order'&$select=Name,DefValue,ReferenceSchemaName&$expand=SysEntitySchema($select=Name)";
                let orderColumns = [];
                try {
                    const resp3 = await fetch(url3, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp3.ok) {
                        const data3 = await resp3.json();
                        orderColumns = data3.value.filter(c =>
                            c.Name.toLowerCase().includes('payment') ||
                            c.Name.toLowerCase().includes('status')
                        );
                    }
                } catch(e) {}

                // Query 4: Get PaymentStatus lookup values
                const url4 = "/0/odata/OrderPaymentStatus?$select=Id,Name&$orderby=Name";
                let paymentStatuses = [];
                try {
                    const resp4 = await fetch(url4, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp4.ok) {
                        const data4 = await resp4.json();
                        paymentStatuses = data4.value;
                    }
                } catch(e) {}

                // Query 5: Find IWQBIntegration package
                const url5 = "/0/odata/SysPackage?$filter=contains(Name,'IWQB') or contains(Name,'IWQBIntegration')&$select=UId,Name,ModifiedOn";
                let iwqbPackage = null;
                try {
                    const resp5 = await fetch(url5, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp5.ok) {
                        const data5 = await resp5.json();
                        if (data5.value && data5.value.length > 0) {
                            iwqbPackage = data5.value[0];
                        }
                    }
                } catch(e) {}

                // Query 6: Find ALL schemas in IWQBIntegration that mention Order
                let iwqbSchemas = [];
                if (iwqbPackage) {
                    const url6 = `/0/odata/VwSysClientUnitSchema?$filter=PackageUId eq ${iwqbPackage.UId}&$select=UId,Name,ModifiedOn`;
                    try {
                        const resp6 = await fetch(url6, { headers: { "BPMCSRF": bpmcsrf } });
                        if (resp6.ok) {
                            const data6 = await resp6.json();
                            iwqbSchemas = data6.value;
                        }
                    } catch(e) {}
                }

                return {
                    orderPageSchemas: data1.value,
                    packages: packages,
                    orderColumns: orderColumns,
                    paymentStatuses: paymentStatuses,
                    iwqbPackage: iwqbPackage,
                    iwqbSchemas: iwqbSchemas
                };
            }''')

            print("\n3. Results:")

            # OrderPageV2 schemas
            print("\n   OrderPage* schemas found:")
            if result.get('orderPageSchemas'):
                for schema in result['orderPageSchemas']:
                    pkg_id = schema.get('PackageUId', 'unknown')
                    pkg_name = result.get('packages', {}).get(pkg_id, pkg_id[:8])
                    mod = schema.get('ModifiedOn', 'unknown')[:19]
                    uid = schema.get('UId', 'unknown')
                    name = schema.get('Name', 'unknown')
                    print(f"   - {name}")
                    print(f"     UID: {uid}")
                    print(f"     Package: {pkg_name}")
                    print(f"     Modified: {mod}")
                    print()

            # IWQBIntegration package
            print("\n   IWQBIntegration Package:")
            if result.get('iwqbPackage'):
                pkg = result['iwqbPackage']
                print(f"   - Name: {pkg.get('Name')}")
                print(f"   - UId: {pkg.get('UId')}")
                print(f"   - Modified: {pkg.get('ModifiedOn', '')[:19]}")

            # Schemas in IWQBIntegration
            print("\n   ALL Client Schemas in IWQBIntegration:")
            if result.get('iwqbSchemas'):
                for schema in result['iwqbSchemas']:
                    print(f"   - {schema.get('Name')} | UID: {schema.get('UId')} | Modified: {schema.get('ModifiedOn', '')[:19]}")
            else:
                print("   (none found or package not found)")

            # Payment statuses
            print("\n   OrderPaymentStatus lookup values:")
            if result.get('paymentStatuses'):
                for status in result['paymentStatuses']:
                    marker = " <-- PROBLEMATIC?" if "Planned" in status.get('Name', '') else ""
                    print(f"   - {status.get('Name')} | ID: {status.get('Id')}{marker}")

            # Save full results
            output_file = REPO_ROOT / "scripts" / "investigation" / "orderpagev2_search_results.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\n   Full results saved to: {output_file.name}")

        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()

        browser.close()

    print("\n" + "=" * 60)
    print("SEARCH COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
