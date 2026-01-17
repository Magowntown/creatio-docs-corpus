#!/usr/bin/env python3
"""
Find where PaymentStatusId default is set - check entity, processes, and backend code.
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

IWQB_PACKAGE_UID = "21e7eb4b-a41b-42f1-913a-41046da1cb86"
PLANNED_STATUS_ID = "bfe38d3d-bd57-48d7-a2d7-82435cd274ca"


def wait_for_stable(page, timeout=5000):
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    page.wait_for_timeout(1000)


def main():
    print("=" * 60)
    print("FINDING PaymentStatusId DEFAULT SOURCE")
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

            # Run comprehensive queries
            print("\n2. Querying for PaymentStatusId default source...")

            result = page.evaluate('''async () => {
                const getCookie = (name) => {
                    const value = `; ${document.cookie}`;
                    const parts = value.split(`; ${name}=`);
                    if (parts.length === 2) return parts.pop().split(';').shift();
                    return "";
                };
                const bpmcsrf = getCookie("BPMCSRF");

                let findings = {
                    entityColumns: [],
                    businessProcesses: [],
                    sourceCodeSchemas: [],
                    recentOrdersWithPlanned: [],
                    orderEventHandlers: []
                };

                // Query 1: Get Order entity schema first
                console.log("Finding Order entity schema...");
                const orderEntityUrl = "/0/odata/SysSchema?$filter=Name eq 'Order' and ManagerName eq 'EntitySchemaManager'&$select=UId,Name";
                try {
                    const orderResp = await fetch(orderEntityUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (orderResp.ok) {
                        const orderData = await orderResp.json();
                        if (orderData.value && orderData.value.length > 0) {
                            const orderSchemaUId = orderData.value[0].UId;
                            findings.orderSchemaUId = orderSchemaUId;

                            // Query columns for this entity
                            const columnsUrl = `/0/odata/SysEntitySchemaColumn?$filter=SysEntitySchemaUId eq ${orderSchemaUId} and (contains(Name,'Payment') or contains(Name,'Status'))&$select=UId,Name,DefValue,ReferenceSchemaUId,Caption`;
                            const colResp = await fetch(columnsUrl, { headers: { "BPMCSRF": bpmcsrf } });
                            if (colResp.ok) {
                                const colData = await colResp.json();
                                findings.entityColumns = colData.value || [];
                            }
                        }
                    }
                } catch(e) {
                    findings.entityColumnError = e.message;
                }

                // Query 2: Business processes in IWQBIntegration
                console.log("Finding business processes...");
                const processUrl = "/0/odata/SysProcessSchema?$filter=SysPackageId eq 21e7eb4b-a41b-42f1-913a-41046da1cb86&$select=UId,Name,Caption";
                try {
                    const procResp = await fetch(processUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (procResp.ok) {
                        const procData = await procResp.json();
                        findings.businessProcesses = procData.value || [];
                    }
                } catch(e) {
                    // Try alternative query
                    const processUrl2 = "/0/odata/VwSysProcess?$filter=contains(Caption,'Order') or contains(Name,'Order')&$select=Id,Name,Caption,SysPackageId&$top=20";
                    try {
                        const procResp2 = await fetch(processUrl2, { headers: { "BPMCSRF": bpmcsrf } });
                        if (procResp2.ok) {
                            const procData2 = await procResp2.json();
                            findings.businessProcesses = procData2.value || [];
                        }
                    } catch(e2) {
                        findings.processError = e.message;
                    }
                }

                // Query 3: Source code schemas in IWQBIntegration
                console.log("Finding source code schemas...");
                const sourceUrl = "/0/odata/SysSchema?$filter=SysPackageId eq 21e7eb4b-a41b-42f1-913a-41046da1cb86 and ManagerName eq 'SourceCodeSchemaManager'&$select=UId,Name,Caption";
                try {
                    const srcResp = await fetch(sourceUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (srcResp.ok) {
                        const srcData = await srcResp.json();
                        findings.sourceCodeSchemas = srcData.value || [];
                    }
                } catch(e) {
                    findings.sourceCodeError = e.message;
                }

                // Query 4: Recent orders with Planned status (to see pattern)
                console.log("Finding recent orders with Planned status...");
                const ordersUrl = "/0/odata/Order?$filter=PaymentStatus/Id eq bfe38d3d-bd57-48d7-a2d7-82435cd274ca&$select=Id,Number,CreatedOn,CreatedBy&$expand=CreatedBy($select=Name)&$orderby=CreatedOn desc&$top=10";
                try {
                    const ordResp = await fetch(ordersUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (ordResp.ok) {
                        const ordData = await ordResp.json();
                        findings.recentOrdersWithPlanned = ordData.value || [];
                    }
                } catch(e) {
                    findings.ordersError = e.message;
                }

                // Query 5: Order entity event handlers (EventSubProcess)
                console.log("Finding Order event handlers...");
                const eventUrl = "/0/odata/SysSchema?$filter=contains(Name,'Order') and ManagerName eq 'EntitySchemaManager'&$select=UId,Name,SysPackageId";
                try {
                    const evtResp = await fetch(eventUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (evtResp.ok) {
                        const evtData = await evtResp.json();
                        findings.orderEventHandlers = evtData.value || [];
                    }
                } catch(e) {
                    findings.eventError = e.message;
                }

                // Query 6: Check for entity event listeners (SysEntityEventListener)
                console.log("Finding entity event listeners...");
                try {
                    const listenerUrl = "/0/odata/SysEntityEventListener?$filter=contains(EntitySchemaName,'Order')&$select=SourceCodeSchemaName,EventName,EntitySchemaName";
                    const listResp = await fetch(listenerUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (listResp.ok) {
                        const listData = await listResp.json();
                        findings.eventListeners = listData.value || [];
                    }
                } catch(e) {
                    // Table might not exist
                }

                // Query 7: Direct query for Order.PaymentStatus column
                console.log("Direct query for PaymentStatus column...");
                try {
                    const directUrl = "/0/odata/SysEntitySchemaColumn?$filter=Name eq 'PaymentStatus' or Name eq 'PaymentStatusId'&$select=UId,Name,DefValue,SysEntitySchemaUId&$top=10";
                    const directResp = await fetch(directUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (directResp.ok) {
                        const directData = await directResp.json();
                        findings.paymentStatusColumns = directData.value || [];
                    }
                } catch(e) {}

                return findings;
            }''')

            # Print results
            print("\n3. Results:")

            # Entity columns
            print("\n   === ENTITY COLUMNS (Order.PaymentStatus*) ===")
            if result.get('entityColumns'):
                for col in result['entityColumns']:
                    def_val = col.get('DefValue', 'none')
                    print(f"   - {col.get('Name')}")
                    print(f"     DefValue: {def_val}")
                    print(f"     UId: {col.get('UId')}")
            else:
                print("   (no columns found)")

            # Direct PaymentStatus column query
            print("\n   === DIRECT PaymentStatus COLUMN QUERY ===")
            if result.get('paymentStatusColumns'):
                for col in result['paymentStatusColumns']:
                    def_val = col.get('DefValue', 'none')
                    schema_id = col.get('SysEntitySchemaUId', 'unknown')
                    print(f"   - {col.get('Name')} | Schema: {schema_id}")
                    print(f"     DefValue: {def_val}")
                    if def_val and "bfe38d3d" in str(def_val).lower():
                        print("     *** FOUND PLANNED DEFAULT! ***")
            else:
                print("   (no columns found)")

            # Business processes
            print("\n   === BUSINESS PROCESSES (IWQBIntegration) ===")
            if result.get('businessProcesses'):
                for proc in result['businessProcesses']:
                    print(f"   - {proc.get('Name', proc.get('Caption', 'unknown'))}")
            else:
                print("   (no processes found or error)")

            # Source code schemas
            print("\n   === SOURCE CODE SCHEMAS (IWQBIntegration C#) ===")
            if result.get('sourceCodeSchemas'):
                for src in result['sourceCodeSchemas']:
                    name = src.get('Name', 'unknown')
                    # Highlight order-related schemas
                    marker = " <-- CHECK THIS" if "order" in name.lower() else ""
                    print(f"   - {name}{marker}")
            else:
                print("   (no source schemas found)")

            # Event listeners
            print("\n   === ENTITY EVENT LISTENERS (Order) ===")
            if result.get('eventListeners'):
                for lst in result['eventListeners']:
                    print(f"   - {lst.get('SourceCodeSchemaName')} -> {lst.get('EventName')}")
            else:
                print("   (no event listeners found)")

            # Recent orders with Planned status
            print("\n   === RECENT ORDERS WITH PLANNED STATUS ===")
            if result.get('recentOrdersWithPlanned'):
                for ord in result['recentOrdersWithPlanned']:
                    created_by = ord.get('CreatedBy', {}).get('Name', 'unknown')
                    created_on = str(ord.get('CreatedOn', ''))[:19]
                    print(f"   - {ord.get('Number')} | By: {created_by} | On: {created_on}")
            else:
                print("   (no orders found)")

            # Save full results
            output_file = REPO_ROOT / "scripts" / "investigation" / "paymentstatus_default_search.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\n   Full results saved to: {output_file.name}")

            # Analysis
            print("\n" + "=" * 60)
            print("ANALYSIS")
            print("=" * 60)

            if result.get('sourceCodeSchemas'):
                print("\nC# schemas to investigate:")
                for src in result['sourceCodeSchemas']:
                    name = src.get('Name', '')
                    if any(kw in name.lower() for kw in ['order', 'event', 'listener', 'handler']):
                        print(f"  - {name} (UId: {src.get('UId')})")

            print("\nTo find the default, check:")
            print("1. Entity Schema Designer for Order entity column defaults")
            print("2. Source code schemas listed above for C# event handlers")
            print("3. Business processes that trigger on Order creation")

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
