#!/usr/bin/env python3
"""
Diagnose why BGCommissionReportDataView has 0 records despite QB Download having data.
Checks the JOIN condition: Order.BGNumberInvoice = BGCommissionReportQBDownload.BGCleanInvoiceNumber
"""

import os
import sys
import requests
from datetime import datetime

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

def query(entity, select=None, filter=None, top=None, orderby=None, expand=None):
    url = f"{CREATIO_URL}/0/odata/{entity}"
    params = {}
    if select: params["$select"] = select
    if filter: params["$filter"] = filter
    if top: params["$top"] = str(top)
    if orderby: params["$orderby"] = orderby
    if expand: params["$expand"] = expand

    response = session.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.json()

def main():
    print("="*60)
    print("VIEW JOIN DIAGNOSTIC")
    print(f"Environment: {CREATIO_URL}")
    print("="*60)

    if not USERNAME or not PASSWORD:
        print("\n❌ Set CREATIO_USERNAME and CREATIO_PASSWORD")
        sys.exit(1)

    login()

    # 1. Check QB Download records for Dec 2025
    print("1. QB Download Records (Dec 2025)")
    print("-" * 50)
    result = query(
        "BGCommissionReportQBDownload",
        select="Id,BGCleanInvoiceNumber,BGTransactionDate,CreatedOn",
        filter="BGTransactionDate ge 2025-12-01T00:00:00Z and BGTransactionDate lt 2026-01-01T00:00:00Z",
        orderby="BGTransactionDate desc",
        top=20
    )

    qb_invoices = set()
    if result and result.get("value"):
        print(f"Found {len(result['value'])} records (showing up to 20)")
        for rec in result["value"]:
            inv = rec.get("BGCleanInvoiceNumber", "N/A")
            trans = rec.get("BGTransactionDate", "")[:10]
            qb_invoices.add(inv)
            print(f"  Invoice: {inv} | TransDate: {trans}")
    else:
        print("  No records found")

    # 2. Check Orders for Dec 2025 - do they have BGNumberInvoice?
    print("\n2. Orders (Dec 2025) - Invoice Numbers")
    print("-" * 50)
    result = query(
        "Order",
        select="Id,Number,BGNumberInvoice,BGInvoiceDate",
        filter="BGInvoiceDate ge 2025-12-01T00:00:00Z and BGInvoiceDate lt 2026-01-01T00:00:00Z",
        orderby="BGInvoiceDate desc",
        top=20
    )

    order_invoices = set()
    orders_without_invoice = 0
    if result and result.get("value"):
        print(f"Found {len(result['value'])} orders (showing up to 20)")
        for rec in result["value"]:
            order_num = rec.get("Number", "N/A")
            inv = rec.get("BGNumberInvoice", "")
            inv_date = rec.get("BGInvoiceDate", "")[:10] if rec.get("BGInvoiceDate") else "N/A"

            if inv:
                order_invoices.add(inv)
                match = "✓" if inv in qb_invoices else "❌ NOT IN QB"
            else:
                orders_without_invoice += 1
                match = "⚠️ NO INVOICE#"

            print(f"  {order_num}: Invoice#{inv or 'EMPTY'} | Date: {inv_date} | {match}")

        print(f"\n  Orders without BGNumberInvoice: {orders_without_invoice}")
    else:
        print("  No orders found")

    # 3. Check matching invoices
    print("\n3. Invoice Number Matching Analysis")
    print("-" * 50)

    matching = order_invoices & qb_invoices
    orders_only = order_invoices - qb_invoices
    qb_only = qb_invoices - order_invoices

    print(f"  Matching invoices (should appear in view): {len(matching)}")
    print(f"  In Orders but NOT in QB: {len(orders_only)}")
    print(f"  In QB but NOT in Orders: {len(qb_only)}")

    if matching:
        print(f"\n  Matching invoice numbers: {list(matching)[:10]}")

    if orders_only:
        print(f"\n  Orders-only invoice numbers: {list(orders_only)[:10]}")

    if qb_only:
        print(f"\n  QB-only invoice numbers: {list(qb_only)[:10]}")

    # 4. Check if Commission Earners exist for these orders
    print("\n4. Commission Earners for Dec 2025 Orders")
    print("-" * 50)
    result = query(
        "BGCommissionEarner",
        select="Id,BGName,BGOrderId",
        filter="BGOrder/BGInvoiceDate ge 2025-12-01T00:00:00Z and BGOrder/BGInvoiceDate lt 2026-01-01T00:00:00Z",
        top=20
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} earners (showing up to 20)")
        for rec in result["value"]:
            name = rec.get("BGName", "N/A")
            print(f"  {name}")
    else:
        print("  No earners found for Dec 2025 orders")

    # 5. Check the View directly for any data
    print("\n5. BGCommissionReportDataView - Sample Records")
    print("-" * 50)
    result = query(
        "BGCommissionReportDataView",
        select="Id,BGTransactionDate,BGDescription",
        orderby="BGTransactionDate desc",
        top=5
    )

    if result and result.get("value"):
        print(f"Most recent {len(result['value'])} view records:")
        for rec in result["value"]:
            trans = rec.get("BGTransactionDate", "")[:10] if rec.get("BGTransactionDate") else "N/A"
            desc = rec.get("BGDescription", "N/A")[:50]
            print(f"  {trans}: {desc}")
    else:
        print("  View has no records at all!")

    # 6. Summary and recommendations
    print("\n" + "="*60)
    print("DIAGNOSIS SUMMARY")
    print("="*60)

    if len(matching) == 0 and len(qb_invoices) > 0 and len(order_invoices) > 0:
        print("\n❌ PROBLEM: Invoice numbers don't match between Orders and QB Download")
        print("   - Orders use BGNumberInvoice")
        print("   - QB Download uses BGCleanInvoiceNumber")
        print("   - These need to match for the view JOIN to work")
        print("\n   Possible causes:")
        print("   1. Different invoice number formats (leading zeros, prefixes)")
        print("   2. QB Download has stale/old invoice numbers")
        print("   3. Orders haven't been synced to QB yet")
    elif orders_without_invoice > 0:
        print(f"\n⚠️ {orders_without_invoice} orders have no BGNumberInvoice")
        print("   These orders won't appear in the view until they're invoiced in QB")
    elif len(matching) > 0:
        print(f"\n✓ Found {len(matching)} matching invoices")
        print("   But view shows 0 records - check view definition or other filters")

if __name__ == "__main__":
    main()
