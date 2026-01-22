#!/usr/bin/env python3
"""Check if BGCommissionReportDataView has data"""

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
        print(f"Login failed")
        sys.exit(1)
    session.get(f"{CREATIO_URL}/0/odata/", allow_redirects=True)
    session.headers.update({
        "BPMCSRF": session.cookies.get("BPMCSRF", ""),
        "Accept": "application/json"
    })
    print(f"Logged in to {CREATIO_URL}\n")

def query(entity, params):
    url = f"{CREATIO_URL}/0/odata/{entity}"
    response = session.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.json()

def main():
    if not USERNAME or not PASSWORD:
        print("Set CREATIO_USERNAME and CREATIO_PASSWORD")
        sys.exit(1)

    login()

    print("=== VIEW DATA CHECK ===\n")

    # Check view total
    result = query("BGCommissionReportDataView", {"$select": "Id", "$top": "1", "$count": "true"})
    print(f"Total view records: {result.get('@odata.count', 'unknown') if result else 'error'}")

    # Check view for December 2025
    result = query("BGCommissionReportDataView", {
        "$filter": "BGTransactionDate ge 2025-12-01T00:00:00Z and BGTransactionDate lt 2026-01-01T00:00:00Z",
        "$select": "Id",
        "$top": "1",
        "$count": "true"
    })
    print(f"December 2025 view records: {result.get('@odata.count', 'unknown') if result else 'error'}")

    # Check view for January 2026
    result = query("BGCommissionReportDataView", {
        "$filter": "BGTransactionDate ge 2026-01-01T00:00:00Z and BGTransactionDate lt 2026-02-01T00:00:00Z",
        "$select": "Id",
        "$top": "1",
        "$count": "true"
    })
    print(f"January 2026 view records: {result.get('@odata.count', 'unknown') if result else 'error'}")

    # Get most recent view records
    print("\nMost recent view records:")
    result = query("BGCommissionReportDataView", {
        "$select": "BGTransactionDate,BGDescription",
        "$orderby": "BGTransactionDate desc",
        "$top": "10"
    })
    if result and result.get("value"):
        for r in result["value"]:
            trans = r.get("BGTransactionDate", "")[:10] if r.get("BGTransactionDate") else "N/A"
            desc = r.get("BGDescription", "N/A")[:50]
            print(f"  {trans}: {desc}")

    # Test specific invoice 61451
    print("\n=== SPECIFIC INVOICE TEST (61451) ===")

    # QB Download
    result = query("BGCommissionReportQBDownload", {
        "$filter": "BGCleanInvoiceNumber eq 61451",
        "$select": "Id,BGTransactionDate",
        "$top": "1"
    })
    if result and result.get("value"):
        trans = result["value"][0].get("BGTransactionDate", "")[:10]
        print(f"QB Download: FOUND (TransDate: {trans})")
    else:
        print("QB Download: NOT FOUND")

    # Order
    result = query("Order", {
        "$filter": "BGNumberInvoice eq '61451'",
        "$select": "Number,BGInvoiceDate",
        "$top": "1"
    })
    if result and result.get("value"):
        order = result["value"][0]
        print(f"Order: FOUND ({order.get('Number')}, InvoiceDate: {order.get('BGInvoiceDate', '')[:10]})")
    else:
        print("Order: NOT FOUND")

    # Check view for Dec 22 (the TransDate of invoice 61451)
    result = query("BGCommissionReportDataView", {
        "$filter": "BGTransactionDate ge 2025-12-22T00:00:00Z and BGTransactionDate lt 2025-12-23T00:00:00Z",
        "$select": "Id,BGDescription",
        "$top": "1",
        "$count": "true"
    })
    count = result.get("@odata.count", 0) if result else 0
    print(f"View records for Dec 22, 2025: {count}")

if __name__ == "__main__":
    main()
