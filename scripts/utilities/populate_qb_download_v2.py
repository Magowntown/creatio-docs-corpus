#!/usr/bin/env python3
"""
Populate BGCommissionReportQBDownload with data from Commission Earners.
V2: Fixed BGCustomerId FK constraint issue
"""

import requests
import uuid
from datetime import datetime

BASE_URL = "https://pampabay.creatio.com"
USERNAME = "Supervisor"
PASSWORD = "123*Pampa?"

SALES_TRANSACTION_TYPE = "b4494f26-26c2-4aa6-951c-658d0828d0d0"

session = requests.Session()

def login():
    auth_url = f"{BASE_URL}/ServiceModel/AuthService.svc/Login"
    resp = session.post(auth_url, json={"UserName": USERNAME, "UserPassword": PASSWORD})
    if resp.status_code == 200 and resp.json().get("Code") == 0:
        csrf = resp.cookies.get("BPMCSRF")
        if csrf:
            session.headers["BPMCSRF"] = csrf
        return True
    return False

def main():
    if not login():
        print("Login failed")
        return

    print("="*70)
    print("POPULATING BGCommissionReportQBDownload (V2)")
    print("="*70)

    # 1. Get commission earners from today
    print("\n1. FETCHING COMMISSION EARNERS...")
    url = f"{BASE_URL}/0/odata/BGCommissionEarner"
    params = {
        "$filter": "CreatedOn ge 2026-01-19T00:00:00Z and BGAddedManually eq true",
        "$select": "Id,BGOrderId,BGSalesRepId,BGCommissionRate,BGName"
    }
    resp = session.get(url, params=params, timeout=120)
    if resp.status_code != 200:
        print(f"   Error: {resp.status_code}")
        return

    earners = resp.json().get("value", [])
    print(f"   Found {len(earners)} earners")

    # 2. Process each earner
    print("\n2. CREATING QB DOWNLOAD RECORDS...")
    created = 0
    skipped = 0
    errors = 0

    for i, earner in enumerate(earners):
        order_id = earner.get("BGOrderId")
        if not order_id:
            skipped += 1
            continue

        # Get order with Account
        order_url = f"{BASE_URL}/0/odata/Order({order_id})"
        params = {
            "$select": "Id,Number,BGSubTotal,BGTaxAmount,BGInvoiceDate,BGPONumber,BGNumberInvoice,AccountId",
            "$expand": "Account($select=Id,Name)"
        }
        resp = session.get(order_url, params=params, timeout=30)
        if resp.status_code != 200:
            errors += 1
            continue

        order = resp.json()
        invoice_number = order.get("BGNumberInvoice") or order.get("Number")

        if not invoice_number:
            skipped += 1
            continue

        # Check if record already exists
        check_url = f"{BASE_URL}/0/odata/BGCommissionReportQBDownload/$count"
        check_params = {"$filter": f"BGInvoiceNumber eq '{invoice_number}'"}
        resp = session.get(check_url, params=check_params, timeout=30)
        if resp.status_code == 200:
            count = int(resp.text.strip().replace('\ufeff', '').replace('ï»¿', ''))
            if count > 0:
                skipped += 1
                continue

        # Calculate amounts
        subtotal = order.get("BGSubTotal") or 0
        tax = order.get("BGTaxAmount") or 0
        amount = subtotal - tax
        rate = earner.get("BGCommissionRate") or 0
        commission = amount * (rate / 100)

        invoice_date = order.get("BGInvoiceDate")
        if not invoice_date:
            skipped += 1
            continue

        account = order.get("Account") or {}
        account_name = account.get("Name", "")

        # Create QB download record - NO BGCustomerId (has FK constraint)
        qb_data = {
            "Id": str(uuid.uuid4()),
            "BGInvoiceNumber": str(invoice_number),
            "BGCleanInvoiceNumber": int(invoice_number) if str(invoice_number).isdigit() else 0,
            "BGAmount": amount,
            "BGCommission": commission,
            "BGCommissionRatePercentage": rate,
            "BGTransactionDate": invoice_date,
            "BGDescription": account_name or earner.get("BGName", ""),
            "BGPONumber": order.get("BGPONumber") or "",
            "BGOrderId": order_id,
            "BGSalesRepId": earner.get("BGSalesRepId"),
            "BGTransactionTypeId": SALES_TRANSACTION_TYPE,
            "BGQuickBooksId": f"MANUAL-{order.get('Number', '')}-{datetime.now().strftime('%Y%m%d')}"
            # BGCustomerId OMITTED - has FK constraint
        }

        url = f"{BASE_URL}/0/odata/BGCommissionReportQBDownload"
        resp = session.post(url, json=qb_data, timeout=30)

        if resp.status_code == 201:
            created += 1
            if created % 25 == 0:
                print(f"   Progress: {created} created...")
        else:
            errors += 1
            if errors <= 3:
                print(f"   Error on {order.get('Number')}: {resp.text[:150]}")

    print(f"\n   Created: {created}")
    print(f"   Skipped: {skipped}")
    print(f"   Errors: {errors}")

    # 3. Check view
    print("\n3. CHECKING VIEW...")
    url = f"{BASE_URL}/0/odata/BGCommissionReportDataView/$count"
    resp = session.get(url, timeout=60)
    total = resp.text.strip().replace('\ufeff', '').replace('ï»¿', '') if resp.status_code == 200 else "error"
    print(f"   Total view records: {total}")

    print("\n" + "="*70)
    if created > 0:
        print(f"SUCCESS! Created {created} records.")
    print("="*70)

if __name__ == "__main__":
    main()
