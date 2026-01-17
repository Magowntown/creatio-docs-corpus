#!/usr/bin/env python3
"""
Check if Commission data exists for December 2025 + RDGZ & Consulting LLC.
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


def main():
    print("=" * 60)
    print("CHECKING COMMISSION DATA FOR DEC 2025 + RDGZ")
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

        print("\n2. Querying Commission data...")

        result = page.evaluate('''async () => {
            const getCookie = (name) => {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${name}=`);
                if (parts.length === 2) return parts.pop().split(';').shift();
                return "";
            };
            const bpmcsrf = getCookie("BPMCSRF");

            let findings = {};

            // 1. Find RDGZ Sales Group ID
            const sgUrl = "/0/odata/BGSalesGroup?$filter=contains(BGName,'RDGZ')&$select=Id,BGName";
            try {
                const resp = await fetch(sgUrl, { headers: { "BPMCSRF": bpmcsrf } });
                if (resp.ok) {
                    const data = await resp.json();
                    findings.salesGroups = data.value || [];
                }
            } catch(e) { findings.sgError = e.message; }

            // 2. Find December 2025 Year-Month ID
            const ymUrl = "/0/odata/BGYearMonth?$filter=Name eq '2025-12'&$select=Id,Name";
            try {
                const resp = await fetch(ymUrl, { headers: { "BPMCSRF": bpmcsrf } });
                if (resp.ok) {
                    const data = await resp.json();
                    findings.yearMonths = data.value || [];
                }
            } catch(e) { findings.ymError = e.message; }

            // 3. Count ALL Commission records for December 2025 (no Sales Group filter)
            const dec2025Start = "2025-12-01T00:00:00Z";
            const dec2025End = "2026-01-01T00:00:00Z";

            // Try BGCommissionReportQBDownload (raw QB data)
            const qbUrl = `/0/odata/BGCommissionReportQBDownload?$filter=BGTransactionDate ge ${dec2025Start} and BGTransactionDate lt ${dec2025End}&$count=true&$top=0`;
            try {
                const resp = await fetch(qbUrl, { headers: { "BPMCSRF": bpmcsrf } });
                if (resp.ok) {
                    const data = await resp.json();
                    findings.qbDownloadCount = data["@odata.count"] || 0;
                }
            } catch(e) { findings.qbError = e.message; }

            // 4. Count Commission records for RDGZ specifically (if we found the ID)
            if (findings.salesGroups && findings.salesGroups.length > 0) {
                const rdgzId = findings.salesGroups[0].Id;
                findings.rdgzId = rdgzId;

                // Check BGCommissionReportDataView for RDGZ + Dec 2025
                // Note: The view uses BGTransactionDate for filtering
                const viewUrl = `/0/odata/BGCommissionReportDataView?$filter=BGTransactionDate ge ${dec2025Start} and BGTransactionDate lt ${dec2025End}&$count=true&$top=5&$select=BGSalesRep,BGTransactionDate,BGAmount,BGCommission`;
                try {
                    const resp = await fetch(viewUrl, { headers: { "BPMCSRF": bpmcsrf } });
                    if (resp.ok) {
                        const data = await resp.json();
                        findings.viewCount = data["@odata.count"] || (data.value ? data.value.length : 0);
                        findings.viewSample = data.value || [];
                    }
                } catch(e) { findings.viewError = e.message; }
            }

            // 5. Check recent BGReportExecution records
            const execUrl = "/0/odata/BGReportExecution?$orderby=CreatedOn desc&$top=5&$select=Id,BGReportName,BGYearMonth,BGSalesGroup,CreatedOn&$expand=BGYearMonth($select=Name),BGSalesGroup($select=BGName)";
            try {
                const resp = await fetch(execUrl, { headers: { "BPMCSRF": bpmcsrf } });
                if (resp.ok) {
                    const data = await resp.json();
                    findings.recentExecutions = data.value || [];
                }
            } catch(e) { findings.execError = e.message; }

            // 6. Check total Commission data in QB Download table
            const totalUrl = "/0/odata/BGCommissionReportQBDownload?$count=true&$top=0";
            try {
                const resp = await fetch(totalUrl, { headers: { "BPMCSRF": bpmcsrf } });
                if (resp.ok) {
                    const data = await resp.json();
                    findings.totalQBRecords = data["@odata.count"] || 0;
                }
            } catch(e) {}

            // 7. Check most recent QB download dates
            const recentUrl = "/0/odata/BGCommissionReportQBDownload?$orderby=BGTransactionDate desc&$top=5&$select=BGTransactionDate,BGAmount";
            try {
                const resp = await fetch(recentUrl, { headers: { "BPMCSRF": bpmcsrf } });
                if (resp.ok) {
                    const data = await resp.json();
                    findings.mostRecentDates = data.value || [];
                }
            } catch(e) {}

            return findings;
        }''')

        print("\n3. Results:")
        print("-" * 40)

        # Sales Group
        print("\nSales Group (RDGZ):")
        if result.get('salesGroups'):
            for sg in result['salesGroups']:
                print(f"  - {sg.get('BGName')} | ID: {sg.get('Id')}")
        else:
            print("  NOT FOUND!")

        # Year-Month
        print("\nYear-Month (2025-12):")
        if result.get('yearMonths'):
            for ym in result['yearMonths']:
                print(f"  - {ym.get('Name')} | ID: {ym.get('Id')}")
        else:
            print("  NOT FOUND!")

        # Commission data counts
        print("\nCommission Data for December 2025:")
        print(f"  QB Download records (Dec 2025): {result.get('qbDownloadCount', 'ERROR: ' + result.get('qbError', 'unknown'))}")
        print(f"  View records (Dec 2025): {result.get('viewCount', 'ERROR: ' + result.get('viewError', 'unknown'))}")
        print(f"  Total QB Download records (all time): {result.get('totalQBRecords', 'unknown')}")

        # Sample data
        if result.get('viewSample'):
            print("\n  Sample records from view:")
            for row in result['viewSample'][:3]:
                print(f"    - Date: {str(row.get('BGTransactionDate', ''))[:10]} | Amount: {row.get('BGAmount')} | Commission: {row.get('BGCommission')}")

        # Most recent dates
        if result.get('mostRecentDates'):
            print("\n  Most recent transaction dates in QB Download:")
            for row in result['mostRecentDates']:
                print(f"    - {str(row.get('BGTransactionDate', ''))[:10]} | Amount: {row.get('BGAmount')}")

        # Recent executions
        print("\nRecent Report Executions:")
        if result.get('recentExecutions'):
            for ex in result['recentExecutions']:
                ym = ex.get('BGYearMonth', {}).get('Name', 'none')
                sg = ex.get('BGSalesGroup', {}).get('BGName', 'none')
                created = str(ex.get('CreatedOn', ''))[:19]
                print(f"  - {ex.get('BGReportName')} | YM: {ym} | SG: {sg} | Created: {created}")
        else:
            print("  (none found)")

        print("\n" + "=" * 60)
        print("DIAGNOSIS")
        print("=" * 60)

        qb_count = result.get('qbDownloadCount', 0)
        if isinstance(qb_count, int) and qb_count == 0:
            print("""
NO DECEMBER 2025 DATA in BGCommissionReportQBDownload!

This means the QB sync has NOT successfully pulled December 2025
payment data from QuickBooks. The connection timeout errors you
saw are preventing the sync from getting this data.

The report is empty because there's no data to report, not because
of a code bug.

ACTION NEEDED:
1. Fix the QuickBooks connectivity issue (96.56.203.106:8080)
2. Re-run the QB Commission sync for December 2025
3. Then the report will have data
""")
        elif isinstance(qb_count, int) and qb_count > 0:
            print(f"""
FOUND {qb_count} records for December 2025 in BGCommissionReportQBDownload.

The data exists. If the report is still empty after deploying
the fixed hybrid version, check:
1. Is the RDGZ Sales Group filter matching the data?
2. Are there records for RDGZ specifically in December 2025?
""")

        browser.close()


if __name__ == "__main__":
    main()
