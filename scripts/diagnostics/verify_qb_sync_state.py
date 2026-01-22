#!/usr/bin/env python3
"""
Diagnostic script to verify QB sync state in Creatio.
Checks if QB payments have been synced and identifies any gaps.
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# Load environment
CREATIO_URL = os.environ.get("CREATIO_URL", "https://pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

session = requests.Session()

def login():
    """Authenticate to Creatio"""
    # First, hit a page to get initial cookies
    session.get(f"{CREATIO_URL}/0/", allow_redirects=True)

    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    response = session.post(login_url, json={
        "UserName": USERNAME,
        "UserPassword": PASSWORD
    })

    if response.status_code != 200:
        print(f"Login failed: {response.status_code}")
        sys.exit(1)

    result = response.json()
    if result.get("Code") != 0:
        print(f"Login error: {result}")
        sys.exit(1)

    # Get BPMCSRF token by hitting OData endpoint
    odata_url = f"{CREATIO_URL}/0/odata/"
    session.get(odata_url, allow_redirects=True)

    bpmcsrf = session.cookies.get("BPMCSRF", "")
    if not bpmcsrf:
        # Try alternate cookie name
        for cookie in session.cookies:
            if "CSRF" in cookie.name.upper():
                bpmcsrf = cookie.value
                break

    session.headers.update({
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json;odata=verbose",
        "Accept": "application/json"
    })
    print(f"✓ Logged in to {CREATIO_URL}")

def odata_query(entity, select=None, filter=None, top=None, orderby=None, count=False):
    """Execute OData query"""
    url = f"{CREATIO_URL}/0/odata/{entity}"
    params = {}
    if select:
        params["$select"] = select
    if filter:
        params["$filter"] = filter
    if top:
        params["$top"] = str(top)
    if orderby:
        params["$orderby"] = orderby
    if count:
        params["$count"] = "true"

    response = session.get(url, params=params)
    if response.status_code != 200:
        print(f"Query error: {response.status_code} - {response.text[:200]}")
        return None
    return response.json()

def check_qb_download_stats():
    """Check BGCommissionReportQBDownload statistics"""
    print("\n" + "="*60)
    print("1. BGCommissionReportQBDownload Statistics")
    print("="*60)

    # Get total count
    result = odata_query("BGCommissionReportQBDownload", select="Id", top=1, count=True)
    if result:
        total = result.get("@odata.count", "unknown")
        print(f"Total records: {total}")

    # Get most recent records
    result = odata_query(
        "BGCommissionReportQBDownload",
        select="Id,CreatedOn,BGTransactionDate,BGCleanInvoiceNumber,BGSalesAmount",
        orderby="CreatedOn desc",
        top=10
    )

    if result and result.get("value"):
        print("\nMost recent 10 records (by CreatedOn):")
        print("-" * 80)
        for rec in result["value"]:
            created = rec.get("CreatedOn", "")[:10]
            trans_date = rec.get("BGTransactionDate", "")[:10] if rec.get("BGTransactionDate") else "N/A"
            invoice = rec.get("BGCleanInvoiceNumber", "N/A")
            amount = rec.get("BGSalesAmount", 0)
            print(f"  Created: {created} | TransDate: {trans_date} | Invoice: {invoice} | Amount: ${amount:,.2f}")

    # Get records by month (last 6 months)
    print("\nRecords by Transaction Date (last 6 months):")
    print("-" * 50)

    months_data = {}
    for i in range(6):
        date = datetime.now() - timedelta(days=30*i)
        year = date.year
        month = date.month

        start = f"{year}-{month:02d}-01T00:00:00Z"
        if month == 12:
            end = f"{year+1}-01-01T00:00:00Z"
        else:
            end = f"{year}-{month+1:02d}-01T00:00:00Z"

        filter_str = f"BGTransactionDate ge {start} and BGTransactionDate lt {end}"
        result = odata_query("BGCommissionReportQBDownload", select="Id", filter=filter_str, top=1, count=True)

        count = result.get("@odata.count", 0) if result else 0
        month_key = f"{year}-{month:02d}"
        months_data[month_key] = count
        print(f"  {month_key}: {count:,} records")

    return months_data

def check_commission_earners():
    """Check BGCommissionEarner statistics"""
    print("\n" + "="*60)
    print("2. BGCommissionEarner Statistics")
    print("="*60)

    # Get total count
    result = odata_query("BGCommissionEarner", select="Id", top=1, count=True)
    if result:
        total = result.get("@odata.count", "unknown")
        print(f"Total records: {total}")

    # Get most recent records
    result = odata_query(
        "BGCommissionEarner",
        select="Id,CreatedOn,BGName,BGCommissionRate",
        orderby="CreatedOn desc",
        top=5
    )

    if result and result.get("value"):
        print("\nMost recent 5 earners:")
        for rec in result["value"]:
            created = rec.get("CreatedOn", "")[:10]
            name = rec.get("BGName", "N/A")
            rate = rec.get("BGCommissionRate", 0)
            print(f"  {created}: {name} ({rate}%)")

def check_sync_logs():
    """Check QB sync process logs"""
    print("\n" + "="*60)
    print("3. QB Sync Process Logs (BGQuickBooksIntegrationLogDetail)")
    print("="*60)

    # Get total by status
    statuses = {
        "c97db3bc-634d-4c90-8432-ec7141c87640": "Pending",
        "e7428193-4cf1-4d1b-abae-00e93ab5e1c5": "Processed",
        "bdfc60c7-55fd-4cbd-9a2c-dca2def46d80": "Error",
        "fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef": "Processing",
        "ff92e20c-da27-4255-96bc-57e32f0944f4": "Re-Process"
    }

    print("\nRecords by status:")
    print("-" * 40)
    for status_id, status_name in statuses.items():
        result = odata_query(
            "BGQuickBooksIntegrationLogDetail",
            select="Id",
            filter=f"BGStatusId eq {status_id}",
            top=1,
            count=True
        )
        count = result.get("@odata.count", 0) if result else 0
        print(f"  {status_name}: {count:,}")

    # Get most recent processed records
    result = odata_query(
        "BGQuickBooksIntegrationLogDetail",
        select="Id,CreatedOn,ModifiedOn,BGTypeName,BGActionName",
        filter=f"BGStatusId eq e7428193-4cf1-4d1b-abae-00e93ab5e1c5",  # Processed
        orderby="ModifiedOn desc",
        top=5
    )

    if result and result.get("value"):
        print("\nMost recent 5 PROCESSED entries:")
        for rec in result["value"]:
            modified = rec.get("ModifiedOn", "")[:16].replace("T", " ")
            type_name = rec.get("BGTypeName", "N/A")
            action = rec.get("BGActionName", "N/A")
            print(f"  {modified}: {type_name} - {action}")

    # Check for Commission-specific sync
    result = odata_query(
        "BGQuickBooksIntegrationLogDetail",
        select="Id,CreatedOn,ModifiedOn,BGTypeName",
        filter="contains(BGTypeName,'Commission') or contains(BGTypeName,'Payment')",
        orderby="ModifiedOn desc",
        top=10
    )

    if result and result.get("value"):
        print("\nRecent Commission/Payment sync entries:")
        for rec in result["value"]:
            modified = rec.get("ModifiedOn", "")[:16].replace("T", " ")
            type_name = rec.get("BGTypeName", "N/A")
            print(f"  {modified}: {type_name}")
    else:
        print("\n⚠️  No Commission/Payment sync entries found!")

def check_view_data():
    """Check BGCommissionReportDataView"""
    print("\n" + "="*60)
    print("4. BGCommissionReportDataView Statistics")
    print("="*60)

    # Get total count
    result = odata_query("BGCommissionReportDataView", select="Id", top=1, count=True)
    if result:
        total = result.get("@odata.count", "unknown")
        print(f"Total records: {total}")

    # Get sample records with dates
    result = odata_query(
        "BGCommissionReportDataView",
        select="Id,BGTransactionDate,BGInvoiceDate,BGSalesAmount,BGIsNote",
        orderby="BGTransactionDate desc",
        top=10
    )

    if result and result.get("value"):
        print("\nMost recent 10 records (by BGTransactionDate):")
        print("-" * 70)
        for rec in result["value"]:
            trans = rec.get("BGTransactionDate", "")[:10] if rec.get("BGTransactionDate") else "N/A"
            inv = rec.get("BGInvoiceDate", "")[:10] if rec.get("BGInvoiceDate") else "N/A"
            amount = rec.get("BGSalesAmount", 0)
            is_note = rec.get("BGIsNote", False)
            print(f"  Trans: {trans} | Invoice: {inv} | Amount: ${amount:,.2f} | Note: {is_note}")

def check_december_gap():
    """Specifically check December 2025 data gap"""
    print("\n" + "="*60)
    print("5. December 2025 Data Gap Analysis")
    print("="*60)

    # QB Download records for Dec 2025
    result = odata_query(
        "BGCommissionReportQBDownload",
        select="Id",
        filter="BGTransactionDate ge 2025-12-01T00:00:00Z and BGTransactionDate lt 2026-01-01T00:00:00Z",
        top=1,
        count=True
    )
    dec_qb = result.get("@odata.count", 0) if result else 0
    print(f"QB Download records (Dec 2025): {dec_qb}")

    # View records for Dec 2025
    result = odata_query(
        "BGCommissionReportDataView",
        select="Id",
        filter="BGTransactionDate ge 2025-12-01T00:00:00Z and BGTransactionDate lt 2026-01-01T00:00:00Z",
        top=1,
        count=True
    )
    dec_view = result.get("@odata.count", 0) if result else 0
    print(f"View records (Dec 2025): {dec_view}")

    # Orders with Dec 2025 invoice dates
    result = odata_query(
        "Order",
        select="Id",
        filter="BGInvoiceDate ge 2025-12-01T00:00:00Z and BGInvoiceDate lt 2026-01-01T00:00:00Z",
        top=1,
        count=True
    )
    dec_orders = result.get("@odata.count", 0) if result else 0
    print(f"Orders with Dec 2025 invoice date: {dec_orders}")

    # Commission earners for Dec 2025 orders
    result = odata_query(
        "BGCommissionEarner",
        select="Id",
        filter="BGOrder/BGInvoiceDate ge 2025-12-01T00:00:00Z and BGOrder/BGInvoiceDate lt 2026-01-01T00:00:00Z",
        top=1,
        count=True
    )
    dec_earners = result.get("@odata.count", 0) if result else 0
    print(f"Commission earners for Dec 2025 orders: {dec_earners}")

    print("\n--- Gap Analysis ---")
    if dec_orders > 0:
        qb_coverage = (dec_qb / dec_orders * 100) if dec_orders > 0 else 0
        print(f"QB Download coverage: {qb_coverage:.1f}% ({dec_qb}/{dec_orders} orders)")

    if dec_qb == 0:
        print("\n⚠️  NO December 2025 QB Download records!")
        print("   This means QB payments haven't been synced for December.")
        print("   Action: Run 'Get QuickBooks Commissions' process")

def check_last_sync_run():
    """Check when QB Commission sync last ran"""
    print("\n" + "="*60)
    print("6. Last QB Commission Sync Run")
    print("="*60)

    # Check BGReportExecution for recent runs
    result = odata_query(
        "BGReportExecution",
        select="Id,CreatedOn,BGReportName,BGYearMonthId",
        orderby="CreatedOn desc",
        top=10
    )

    if result and result.get("value"):
        print("Recent report executions:")
        for rec in result["value"]:
            created = rec.get("CreatedOn", "")[:16].replace("T", " ")
            name = rec.get("BGReportName", "N/A")
            print(f"  {created}: {name}")

    # Check process log for QB sync
    result = odata_query(
        "SysProcessLog",
        select="Id,CreatedOn,Name,Status",
        filter="contains(Name,'QuickBooks') or contains(Name,'Commission')",
        orderby="CreatedOn desc",
        top=10
    )

    if result and result.get("value"):
        print("\nRecent QB/Commission process runs:")
        for rec in result["value"]:
            created = rec.get("CreatedOn", "")[:16].replace("T", " ")
            name = rec.get("Name", "N/A")[:50]
            status = rec.get("Status", "N/A")
            print(f"  {created}: {name} [{status}]")
    else:
        print("\n⚠️  No QB sync process logs found (SysProcessLog)")

def main():
    print("="*60)
    print("QB SYNC STATE DIAGNOSTIC")
    print(f"Environment: {CREATIO_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    if not USERNAME or not PASSWORD:
        print("\n❌ Error: Set CREATIO_USERNAME and CREATIO_PASSWORD")
        print("   source .env && python3 scripts/diagnostics/verify_qb_sync_state.py")
        sys.exit(1)

    login()

    check_qb_download_stats()
    check_commission_earners()
    check_sync_logs()
    check_view_data()
    check_december_gap()
    check_last_sync_run()

    print("\n" + "="*60)
    print("DIAGNOSTIC COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
