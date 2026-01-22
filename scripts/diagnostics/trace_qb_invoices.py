#!/usr/bin/env python3
"""
Trace QB Download invoice numbers back to their original Orders.
Check if December 2025 QB payments are for older invoices.
"""

import os
import sys
import requests

CREATIO_URL = os.environ.get("CREATIO_URL", "https://pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

session = requests.Session()

def login():
    session.get(f"{CREATIO_URL}/0/", allow_redirects=True)
    response = session.post(
        f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
        json={"UserName": USERNAME, "UserPassword": PASSWORD}
    )
    if response.status_code != 200 or response.json().get("Code") != 0:
        print(f"Login failed: {response.text}")
        sys.exit(1)

    session.get(f"{CREATIO_URL}/0/odata/", allow_redirects=True)
    bpmcsrf = session.cookies.get("BPMCSRF", "")
    session.headers.update({
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json;odata=verbose",
        "Accept": "application/json"
    })
    print(f"✓ Logged in to {CREATIO_URL}\n")

def query(entity, select=None, filter=None, top=None, orderby=None):
    url = f"{CREATIO_URL}/0/odata/{entity}"
    params = {}
    if select: params["$select"] = select
    if filter: params["$filter"] = filter
    if top: params["$top"] = str(top)
    if orderby: params["$orderby"] = orderby

    response = session.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.json()

def main():
    print("="*70)
    print("TRACE QB DOWNLOAD INVOICES TO ORIGINAL ORDERS")
    print(f"Environment: {CREATIO_URL}")
    print("="*70)

    if not USERNAME or not PASSWORD:
        print("\n❌ Set CREATIO_USERNAME and CREATIO_PASSWORD")
        sys.exit(1)

    login()

    # Get December 2025 QB Download records
    print("1. December 2025 QB Download Records (TransactionDate in Dec)")
    print("-" * 70)
    result = query(
        "BGCommissionReportQBDownload",
        select="Id,BGCleanInvoiceNumber,BGTransactionDate",
        filter="BGTransactionDate ge 2025-12-01T00:00:00Z and BGTransactionDate lt 2026-01-01T00:00:00Z",
        orderby="BGTransactionDate desc",
        top=30
    )

    if not result or not result.get("value"):
        print("  No QB Download records found for December 2025")
        return

    qb_records = result["value"]
    print(f"  Found {len(qb_records)} QB Download records")

    # For each QB Download, find the matching Order
    print("\n2. Tracing Invoices to Orders")
    print("-" * 70)
    print(f"{'Invoice#':<12} {'QB TransDate':<12} {'Order#':<15} {'Order InvDate':<12} {'Match?':<10}")
    print("-" * 70)

    matches_found = 0
    for rec in qb_records[:20]:  # Check first 20
        inv_num = rec.get("BGCleanInvoiceNumber", "")
        trans_date = rec.get("BGTransactionDate", "")[:10]

        if not inv_num:
            print(f"{'EMPTY':<12} {trans_date:<12} {'N/A':<15} {'N/A':<12} {'⚠️':<10}")
            continue

        # Find order with this invoice number
        order_result = query(
            "Order",
            select="Id,Number,BGNumberInvoice,BGInvoiceDate",
            filter=f"BGNumberInvoice eq '{inv_num}'",
            top=1
        )

        if order_result and order_result.get("value"):
            order = order_result["value"][0]
            order_num = order.get("Number", "N/A")
            order_inv_date = order.get("BGInvoiceDate", "")[:10] if order.get("BGInvoiceDate") else "N/A"

            # Check if order is from December
            is_dec = order_inv_date.startswith("2025-12") if order_inv_date else False
            status = "✓ DEC" if is_dec else f"← {order_inv_date[:7]}"
            matches_found += 1
            print(f"{inv_num:<12} {trans_date:<12} {order_num:<15} {order_inv_date:<12} {status:<10}")
        else:
            print(f"{inv_num:<12} {trans_date:<12} {'NOT FOUND':<15} {'N/A':<12} {'❌':<10}")

    print("-" * 70)
    print(f"Orders found: {matches_found}/{len(qb_records[:20])}")

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("""
The December 2025 QB Download records show payments that happened in December.
These payments can be for invoices from ANY month (not just December).

Commission Flow:
  Order Created (Oct) → Invoice #52386 → Paid in December → QB Download (Dec)

The VIEW joins on invoice number, so:
  - December PAYMENTS appear in the view under the ORIGINAL order's month
  - NOT under December (unless the order was also from December)

This is CORRECT behavior - payments are attributed to when the order was made,
not when payment was received.

If December 2025 orders are missing:
1. They may not be invoiced yet (no BGNumberInvoice)
2. The invoices may not be paid yet (no QB ReceivePayment)
3. The QB sync may not have run recently
""")

if __name__ == "__main__":
    main()
