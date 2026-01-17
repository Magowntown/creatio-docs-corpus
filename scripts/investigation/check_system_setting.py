#!/usr/bin/env python3
"""
Check OrderPaymentStatusDef system setting value.
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


def main():
    print("=" * 60)
    print("CHECKING OrderPaymentStatusDef SYSTEM SETTING")
    print("=" * 60)

    with sync_playwright() as p:
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

            # Query system setting
            print("\n2. Querying OrderPaymentStatusDef...")

            result = page.evaluate('''async () => {
                const getCookie = (name) => {
                    const value = `; ${document.cookie}`;
                    const parts = value.split(`; ${name}=`);
                    if (parts.length === 2) return parts.pop().split(';').shift();
                    return "";
                };
                const bpmcsrf = getCookie("BPMCSRF");

                let findings = {};

                // Query 1: Get system setting definition
                const settingDefUrl = "/0/odata/SysSettings?$filter=Code eq 'OrderPaymentStatusDef'&$select=Id,Code,Name,ValueTypeName,ReferenceSchemaUId";
                try {
                    const defResp = await fetch(settingDefUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (defResp.ok) {
                        const defData = await defResp.json();
                        findings.settingDef = defData.value && defData.value[0];
                    }
                } catch(e) {
                    findings.defError = e.message;
                }

                // Query 2: Get current value from SysSettingsValue
                if (findings.settingDef && findings.settingDef.Id) {
                    const valueUrl = `/0/odata/SysSettingsValue?$filter=SysSettingsId eq ${findings.settingDef.Id}&$select=GuidValue,TextValue`;
                    try {
                        const valResp = await fetch(valueUrl, { headers: { "BPMCSRF": bpmcsrf } });
                        if (valResp.ok) {
                            const valData = await valResp.json();
                            findings.settingValue = valData.value && valData.value[0];
                        }
                    } catch(e) {
                        findings.valueError = e.message;
                    }
                }

                // Query 3: If we have a GUID, look up what it maps to in OrderPaymentStatus
                if (findings.settingValue && findings.settingValue.GuidValue) {
                    const guid = findings.settingValue.GuidValue;
                    const statusUrl = `/0/odata/OrderPaymentStatus(${guid})?$select=Id,Name`;
                    try {
                        const statusResp = await fetch(statusUrl, { headers: { "BPMCSRF": bpmcsrf } });
                        if (statusResp.ok) {
                            const statusData = await statusResp.json();
                            findings.paymentStatusName = statusData.Name;
                            findings.paymentStatusId = statusData.Id;
                        }
                    } catch(e) {
                        findings.statusError = e.message;
                    }
                }

                // Query 4: Get all payment statuses for reference
                const allStatusUrl = "/0/odata/OrderPaymentStatus?$select=Id,Name&$orderby=Name";
                try {
                    const allResp = await fetch(allStatusUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (allResp.ok) {
                        const allData = await allResp.json();
                        findings.allStatuses = allData.value;
                    }
                } catch(e) {}

                return findings;
            }''')

            print("\n3. Results:")
            print("-" * 40)

            if result.get('settingDef'):
                sd = result['settingDef']
                print(f"   System Setting: {sd.get('Code')}")
                print(f"   Name: {sd.get('Name')}")
                print(f"   ID: {sd.get('Id')}")
                print(f"   Value Type: {sd.get('ValueTypeName')}")

            if result.get('settingValue'):
                sv = result['settingValue']
                guid_val = sv.get('GuidValue', 'none')
                print(f"\n   Current GUID Value: {guid_val}")

            if result.get('paymentStatusName'):
                print(f"\n   *** CURRENT DEFAULT: {result.get('paymentStatusName')} ***")
                print(f"   *** Status ID: {result.get('paymentStatusId')} ***")

                if "planned" in result.get('paymentStatusName', '').lower():
                    print("\n   !!! THIS IS THE PROBLEM !!!")
                    print("   The system setting is configured to default to 'Planned'")
                    print("   which blocks orders from QB sync.")

            print("\n   All Payment Statuses:")
            if result.get('allStatuses'):
                for status in result['allStatuses']:
                    marker = " <-- CURRENT DEFAULT" if status.get('Id') == result.get('paymentStatusId') else ""
                    print(f"   - {status.get('Name')} | ID: {status.get('Id')}{marker}")

            print("\n" + "=" * 60)
            print("FIX OPTIONS")
            print("=" * 60)
            print("""
Option A: Change System Setting Value
  - Go to: System Designer > System Settings
  - Find: OrderPaymentStatusDef
  - Change to: NULL (no default) or another status like "Unpaid"

Option B: Remove Default from Entity
  - Go to: Advanced Settings > Order entity
  - Find: PaymentStatus column
  - Remove the system setting default

Option C: Keep Default, Update QB Sync
  - Modify QB sync process to include "Planned" orders
  - This may have business implications
""")

        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()

        browser.close()


if __name__ == "__main__":
    main()
