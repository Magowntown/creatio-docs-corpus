#!/usr/bin/env python3
"""
Investigate Commission Data Gap
Checks what data exists in Creatio for Dec 2025 / Jan 2026 commissions
"""

import os
import sys
import requests
from datetime import datetime
from collections import defaultdict

# Load environment
from dotenv import load_dotenv
load_dotenv()

CREATIO_URL = os.getenv("CREATIO_URL", "https://pampabay.creatio.com")
USERNAME = os.getenv("CREATIO_USERNAME")
PASSWORD = os.getenv("CREATIO_PASSWORD")

session = requests.Session()

def authenticate():
    """Authenticate to Creatio"""
    auth_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    payload = {"UserName": USERNAME, "UserPassword": PASSWORD}

    resp = session.post(auth_url, json=payload)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("Code") == 0:
            print("✅ Authenticated successfully")
            # Get BPMCSRF token
            csrf = session.cookies.get("BPMCSRF")
            if csrf:
                session.headers.update({"BPMCSRF": csrf})
            return True
    print(f"❌ Authentication failed: {resp.text}")
    return False

def query_odata(entity, select=None, filter=None, top=None, orderby=None, count=False):
    """Query Creatio OData endpoint"""
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

    resp = session.get(url, params=params)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"❌ Query failed for {entity}: {resp.status_code} - {resp.text[:200]}")
        return None

def main():
    print("=" * 60)
    print("COMMISSION DATA GAP INVESTIGATION")
    print(f"Environment: {CREATIO_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    if not authenticate():
        sys.exit(1)

    print("\n" + "=" * 60)
    print("1. BGCommissionReportQBDownload - Records by Month")
    print("=" * 60)

    # Check QB Download records by month
    qb_download = query_odata(
        "BGCommissionReportQBDownload",
        select="Id,BGTransactionDate,BGCleanInvoiceNumber,BGAmount",
        top=5000,
        orderby="BGTransactionDate desc"
    )

    if qb_download and qb_download.get("value"):
        records = qb_download["value"]
        print(f"Total records retrieved: {len(records)}")

        # Group by month
        by_month = defaultdict(int)
        by_month_amount = defaultdict(float)
        for r in records:
            txn_date = r.get("BGTransactionDate")
            if txn_date:
                month = txn_date[:7]  # YYYY-MM
                by_month[month] += 1
                by_month_amount[month] += r.get("BGAmount", 0) or 0

        print("\nRecords by Month (most recent first):")
        print("-" * 50)
        for month in sorted(by_month.keys(), reverse=True)[:12]:
            print(f"  {month}: {by_month[month]:>5} records  ${by_month_amount[month]:>12,.2f}")
    else:
        print("No records found or query failed")

    print("\n" + "=" * 60)
    print("2. Orders - Dec 2025 / Jan 2026 with Invoice Numbers")
    print("=" * 60)

    # Check orders for Dec 2025 and Jan 2026
    for month_name, date_filter in [
        ("December 2025", "BGInvoiceDate ge 2025-12-01 and BGInvoiceDate lt 2026-01-01"),
        ("January 2026", "BGInvoiceDate ge 2026-01-01 and BGInvoiceDate lt 2026-02-01"),
    ]:
        orders = query_odata(
            "Order",
            select="Id,Number,BGInvoiceDate,BGNumberInvoice,Amount,BGQuickBooksId",
            filter=date_filter,
            top=1000,
            orderby="BGInvoiceDate desc"
        )

        if orders and orders.get("value"):
            records = orders["value"]
            with_invoice = [r for r in records if r.get("BGNumberInvoice")]
            with_qb_id = [r for r in records if r.get("BGQuickBooksId")]
            total_amount = sum(r.get("Amount", 0) or 0 for r in records)

            print(f"\n{month_name}:")
            print(f"  Total orders: {len(records)}")
            print(f"  With invoice number: {len(with_invoice)}")
            print(f"  With QuickBooks ID: {len(with_qb_id)}")
            print(f"  Total amount: ${total_amount:,.2f}")
        else:
            print(f"\n{month_name}: No orders found or query failed")

    print("\n" + "=" * 60)
    print("3. BGCommissionEarner - Dec 2025 / Jan 2026")
    print("=" * 60)

    # Check commission earners
    # Need to join with Order to filter by date - use expand
    earners = query_odata(
        "BGCommissionEarner",
        select="Id,BGName,BGCommissionRate,BGOrderId,CreatedOn",
        filter="CreatedOn ge 2025-12-01",
        top=2000,
        orderby="CreatedOn desc"
    )

    if earners and earners.get("value"):
        records = earners["value"]

        # Group by month
        by_month = defaultdict(int)
        for r in records:
            created = r.get("CreatedOn")
            if created:
                month = created[:7]
                by_month[month] += 1

        print(f"Total earner records (since Dec 2025): {len(records)}")
        print("\nBy Month:")
        for month in sorted(by_month.keys(), reverse=True):
            print(f"  {month}: {by_month[month]} earners")
    else:
        print("No earner records found or query failed")

    print("\n" + "=" * 60)
    print("4. Gap Analysis")
    print("=" * 60)

    # Compare: Do orders with invoice numbers exist in QB Download?
    print("\nChecking if Dec 2025 invoices are in QB Download...")

    dec_orders = query_odata(
        "Order",
        select="Id,Number,BGNumberInvoice",
        filter="BGInvoiceDate ge 2025-12-01 and BGInvoiceDate lt 2026-01-01 and BGNumberInvoice ne null",
        top=500
    )

    if dec_orders and dec_orders.get("value"):
        dec_invoices = [r.get("BGNumberInvoice") for r in dec_orders["value"] if r.get("BGNumberInvoice")]
        print(f"December 2025 orders with invoices: {len(dec_invoices)}")

        # Sample check - look for first 10 invoices in QB Download
        found_count = 0
        not_found = []
        for inv in dec_invoices[:20]:
            check = query_odata(
                "BGCommissionReportQBDownload",
                select="Id,BGCleanInvoiceNumber",
                filter=f"BGCleanInvoiceNumber eq '{inv}'",
                top=1
            )
            if check and check.get("value") and len(check["value"]) > 0:
                found_count += 1
            else:
                not_found.append(inv)

        print(f"\nSample check (first 20 Dec 2025 invoices):")
        print(f"  Found in QB Download: {found_count}")
        print(f"  NOT found in QB Download: {len(not_found)}")
        if not_found[:5]:
            print(f"  Missing invoice examples: {not_found[:5]}")

    print("\n" + "=" * 60)
    print("5. SUMMARY")
    print("=" * 60)

    print("""
Based on the data above:

IF QB Download has Dec 2025 / Jan 2026 records:
  → The sync worked! Report should show data now.
  → Re-run Commission report to verify.

IF QB Download is MISSING Dec 2025 / Jan 2026:
  → QuickBooks hasn't processed payments for those invoices
  → Options:
     A. Wait for QB accounting to process payments
     B. Build commission from Orders + Earners directly
     C. Manually populate QB Download table
""")

if __name__ == "__main__":
    main()
