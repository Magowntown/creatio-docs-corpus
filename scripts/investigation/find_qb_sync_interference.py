#!/usr/bin/env python3
"""
Find business processes, business rules, and event handlers in IWQBIntegration
that might interfere with QB sync.
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


def wait_for_stable(page, timeout=5000):
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    page.wait_for_timeout(1000)


def main():
    print("=" * 60)
    print("FINDING QB SYNC INTERFERENCE IN IWQBIntegration")
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

            # Comprehensive queries
            print("\n2. Querying IWQBIntegration package contents...")

            result = page.evaluate('''async () => {
                const getCookie = (name) => {
                    const value = `; ${document.cookie}`;
                    const parts = value.split(`; ${name}=`);
                    if (parts.length === 2) return parts.pop().split(';').shift();
                    return "";
                };
                const bpmcsrf = getCookie("BPMCSRF");
                const iwqbPkgId = "21e7eb4b-a41b-42f1-913a-41046da1cb86";

                let findings = {
                    businessProcesses: [],
                    sourceCodeSchemas: [],
                    entitySchemas: [],
                    allSchemas: [],
                    qbRelatedProcesses: [],
                    orderRelatedProcesses: []
                };

                // Query 1: ALL schemas in IWQBIntegration package
                console.log("Getting all schemas in package...");
                const allSchemaUrl = `/0/odata/SysSchema?$filter=SysPackageId eq ${iwqbPkgId}&$select=UId,Name,ManagerName,ModifiedOn&$orderby=ManagerName,Name`;
                try {
                    const resp = await fetch(allSchemaUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) {
                        const data = await resp.json();
                        findings.allSchemas = data.value || [];
                    }
                } catch(e) {
                    findings.allSchemasError = e.message;
                }

                // Query 2: Business Processes (SysProcessSchemaManager)
                console.log("Getting business processes...");
                const processUrl = `/0/odata/SysSchema?$filter=SysPackageId eq ${iwqbPkgId} and ManagerName eq 'ProcessSchemaManager'&$select=UId,Name,Caption,ModifiedOn`;
                try {
                    const resp = await fetch(processUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) {
                        const data = await resp.json();
                        findings.businessProcesses = data.value || [];
                    }
                } catch(e) {}

                // Query 3: Source Code Schemas (C# code)
                console.log("Getting source code schemas...");
                const srcUrl = `/0/odata/SysSchema?$filter=SysPackageId eq ${iwqbPkgId} and ManagerName eq 'SourceCodeSchemaManager'&$select=UId,Name,Caption,ModifiedOn`;
                try {
                    const resp = await fetch(srcUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) {
                        const data = await resp.json();
                        findings.sourceCodeSchemas = data.value || [];
                    }
                } catch(e) {}

                // Query 4: Entity Schemas
                console.log("Getting entity schemas...");
                const entityUrl = `/0/odata/SysSchema?$filter=SysPackageId eq ${iwqbPkgId} and ManagerName eq 'EntitySchemaManager'&$select=UId,Name,Caption,ModifiedOn`;
                try {
                    const resp = await fetch(entityUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) {
                        const data = await resp.json();
                        findings.entitySchemas = data.value || [];
                    }
                } catch(e) {}

                // Query 5: Find ALL processes mentioning "QB" or "QuickBooks" across all packages
                console.log("Finding QB-related processes...");
                const qbProcessUrl = "/0/odata/SysSchema?$filter=ManagerName eq 'ProcessSchemaManager' and (contains(Name,'QB') or contains(Name,'QuickBooks') or contains(Name,'Sync'))&$select=UId,Name,Caption,SysPackageId,ModifiedOn&$orderby=ModifiedOn desc&$top=50";
                try {
                    const resp = await fetch(qbProcessUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) {
                        const data = await resp.json();
                        findings.qbRelatedProcesses = data.value || [];
                    }
                } catch(e) {}

                // Query 6: Find processes mentioning "Order"
                console.log("Finding Order-related processes...");
                const orderProcessUrl = "/0/odata/SysSchema?$filter=ManagerName eq 'ProcessSchemaManager' and contains(Name,'Order')&$select=UId,Name,Caption,SysPackageId,ModifiedOn&$orderby=ModifiedOn desc&$top=30";
                try {
                    const resp = await fetch(orderProcessUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) {
                        const data = await resp.json();
                        findings.orderRelatedProcesses = data.value || [];
                    }
                } catch(e) {}

                // Query 7: Find running/active process instances
                console.log("Checking active process instances...");
                const activeUrl = "/0/odata/SysProcessLog?$filter=Status eq 1&$select=Id,Name,StartDate,Status&$orderby=StartDate desc&$top=20";
                try {
                    const resp = await fetch(activeUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) {
                        const data = await resp.json();
                        findings.activeProcesses = data.value || [];
                    }
                } catch(e) {}

                // Query 8: Find failed/error process instances recently
                console.log("Checking failed processes...");
                const failedUrl = "/0/odata/SysProcessLog?$filter=Status eq 3&$select=Id,Name,StartDate,Status,ErrorDescription&$orderby=StartDate desc&$top=20";
                try {
                    const resp = await fetch(failedUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) {
                        const data = await resp.json();
                        findings.failedProcesses = data.value || [];
                    }
                } catch(e) {}

                // Query 9: Get package names for reference
                console.log("Getting package names...");
                const pkgIds = [...new Set([
                    ...findings.qbRelatedProcesses.map(p => p.SysPackageId),
                    ...findings.orderRelatedProcesses.map(p => p.SysPackageId)
                ])].filter(id => id);

                findings.packageNames = {};
                for (const pkgId of pkgIds.slice(0, 10)) {
                    try {
                        const pkgUrl = `/0/odata/SysPackage(${pkgId})?$select=Name`;
                        const resp = await fetch(pkgUrl, { headers: { "BPMCSRF": bpmcsrf } });
                        if (resp.ok) {
                            const pkg = await resp.json();
                            findings.packageNames[pkgId] = pkg.Name;
                        }
                    } catch(e) {}
                }

                return findings;
            }''')

            # Print results
            print("\n3. Results:")
            print("=" * 60)

            # All schemas by type
            print("\n=== ALL SCHEMAS IN IWQBIntegration ===")
            if result.get('allSchemas'):
                by_manager = {}
                for s in result['allSchemas']:
                    mgr = s.get('ManagerName', 'Unknown')
                    if mgr not in by_manager:
                        by_manager[mgr] = []
                    by_manager[mgr].append(s)

                for mgr, schemas in sorted(by_manager.items()):
                    print(f"\n{mgr} ({len(schemas)} schemas):")
                    for s in schemas:
                        mod = str(s.get('ModifiedOn', ''))[:10]
                        print(f"   - {s.get('Name')} | Modified: {mod}")

            # Business processes in IWQB
            print("\n\n=== BUSINESS PROCESSES IN IWQBIntegration ===")
            if result.get('businessProcesses'):
                for bp in result['businessProcesses']:
                    mod = str(bp.get('ModifiedOn', ''))[:10]
                    print(f"   - {bp.get('Name')} | Modified: {mod}")
                    print(f"     UId: {bp.get('UId')}")
            else:
                print("   (none found)")

            # Source code schemas
            print("\n=== SOURCE CODE (C#) IN IWQBIntegration ===")
            if result.get('sourceCodeSchemas'):
                for src in result['sourceCodeSchemas']:
                    mod = str(src.get('ModifiedOn', ''))[:10]
                    marker = " <-- INVESTIGATE" if any(kw in src.get('Name', '').lower() for kw in ['order', 'sync', 'event', 'handler']) else ""
                    print(f"   - {src.get('Name')}{marker}")
                    print(f"     UId: {src.get('UId')} | Modified: {mod}")
            else:
                print("   (none found)")

            # Entity schemas
            print("\n=== ENTITY SCHEMAS IN IWQBIntegration ===")
            if result.get('entitySchemas'):
                for ent in result['entitySchemas']:
                    print(f"   - {ent.get('Name')}")
            else:
                print("   (none found)")

            # QB-related processes across all packages
            print("\n=== QB/SYNC RELATED PROCESSES (ALL PACKAGES) ===")
            if result.get('qbRelatedProcesses'):
                pkgNames = result.get('packageNames', {})
                for bp in result['qbRelatedProcesses']:
                    pkg = pkgNames.get(bp.get('SysPackageId'), bp.get('SysPackageId', 'unknown')[:8])
                    mod = str(bp.get('ModifiedOn', ''))[:10]
                    print(f"   - {bp.get('Name')} | Package: {pkg} | Modified: {mod}")
            else:
                print("   (none found)")

            # Order-related processes
            print("\n=== ORDER RELATED PROCESSES (ALL PACKAGES) ===")
            if result.get('orderRelatedProcesses'):
                pkgNames = result.get('packageNames', {})
                for bp in result['orderRelatedProcesses']:
                    pkg = pkgNames.get(bp.get('SysPackageId'), bp.get('SysPackageId', 'unknown')[:8])
                    mod = str(bp.get('ModifiedOn', ''))[:10]
                    print(f"   - {bp.get('Name')} | Package: {pkg} | Modified: {mod}")
            else:
                print("   (none found)")

            # Active processes
            print("\n=== CURRENTLY RUNNING PROCESSES ===")
            if result.get('activeProcesses'):
                for p in result['activeProcesses']:
                    start = str(p.get('StartDate', ''))[:19]
                    print(f"   - {p.get('Name')} | Started: {start}")
            else:
                print("   (none currently running)")

            # Failed processes
            print("\n=== RECENTLY FAILED PROCESSES ===")
            if result.get('failedProcesses'):
                for p in result['failedProcesses']:
                    start = str(p.get('StartDate', ''))[:19]
                    err = (p.get('ErrorDescription') or '')[:80]
                    print(f"   - {p.get('Name')} | At: {start}")
                    if err:
                        print(f"     Error: {err}...")
            else:
                print("   (none recently failed)")

            # Save results
            output_file = REPO_ROOT / "scripts" / "investigation" / "qb_sync_interference_search.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\n\nFull results saved to: {output_file.name}")

            print("\n" + "=" * 60)
            print("ANALYSIS")
            print("=" * 60)
            print("""
Things to check:
1. Source code schemas with 'Order', 'Sync', 'Event', 'Handler' in name
   - These might contain C# event handlers that fire on Order operations
   - Could be setting PaymentStatus or blocking sync

2. Business processes that trigger on Order entity
   - Look for signal starts or entity events

3. Any process that recently failed with QB-related errors
   - Could indicate sync interference
""")

        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()

        browser.close()


if __name__ == "__main__":
    main()
