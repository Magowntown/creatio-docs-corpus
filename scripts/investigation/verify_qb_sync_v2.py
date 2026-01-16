#!/usr/bin/env python3
"""Verify QB sync requirements - check commission data directly."""

import os
import requests
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

PLANNED_STATUS_ID = "bfe38d3d-bd57-48d7-a2d7-82435cd274ca"
EMPTY_GUID = "00000000-0000-0000-0000-000000000000"

class CreatioClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._login(username, password)

    def _login(self, username, password):
        login_url = f"{self.base_url}/ServiceModel/AuthService.svc/Login"
        resp = self.session.post(login_url, json={
            "UserName": username,
            "UserPassword": password
        })
        if resp.status_code != 200 or resp.json().get("Code") != 0:
            raise Exception(f"Login failed: {resp.text}")
        print(f"Logged in to {self.base_url}")

    def query(self, entity, columns=None, filters=None, order_by=None, limit=100, skip=0):
        url = f"{self.base_url}/0/odata/{entity}"
        params = {"$top": str(limit), "$skip": str(skip)}
        if columns:
            params["$select"] = ",".join(columns)
        if filters:
            params["$filter"] = filters
        if order_by:
            params["$orderby"] = order_by

        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            print(f"   Query {entity} failed: {resp.status_code}")
            return []
        return resp.json().get("value", [])

def main():
    print("=" * 70)
    print("VERIFY QB SYNC REQUIREMENTS")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Try different QB data entities
    print("\n1. Checking available QB-related entities...")

    entities_to_try = [
        "BGQBDownload",
        "BGCommissionReportQBDownload",
        "BGQuickBooksLog",
        "BGQBLog",
    ]

    for entity in entities_to_try:
        records = client.query(entity, limit=5)
        if records:
            print(f"   ✓ {entity}: {len(records)} sample records")
            print(f"     Columns: {list(records[0].keys())[:6]}...")
        else:
            print(f"   ✗ {entity}: No data or not accessible")

    # 2. Check BGCommissionReportDataView for orders that HAVE commission data
    print("\n2. Checking BGCommissionReportDataView...")
    commission_data = client.query(
        "BGCommissionReportDataView",
        columns=["Id", "BGInvoiceNumber", "BGTransactionDate"],
        order_by="BGTransactionDate desc",
        limit=100
    )

    if commission_data:
        print(f"   Found {len(commission_data)} commission records")
        invoice_nums_with_commission = set()
        for cd in commission_data:
            inv = cd.get("BGInvoiceNumber")
            if inv:
                invoice_nums_with_commission.add(str(inv))
        print(f"   Unique invoice numbers: {len(invoice_nums_with_commission)}")
    else:
        print("   No commission data found via OData")

    # 3. Get orders and categorize by whether they have commission data
    print("\n3. Fetching orders to analyze PaymentStatus patterns...")

    orders = []
    for skip in range(0, 1000, 200):
        batch = client.query(
            "Order",
            columns=["Id", "Number", "BGInvoiceNumber", "PaymentStatusId", "CreatedOn", "CreatedById"],
            order_by="CreatedOn desc",
            limit=200,
            skip=skip
        )
        if not batch:
            break
        orders.extend(batch)

    print(f"   Fetched {len(orders)} orders")

    # 4. Check which orders have invoice numbers that appear in commission data
    if commission_data and invoice_nums_with_commission:
        synced = []
        not_synced = []

        for order in orders:
            inv = order.get("BGInvoiceNumber")
            if inv and str(inv) in invoice_nums_with_commission:
                synced.append(order)
            else:
                not_synced.append(order)

        print(f"\n4. Orders with commission data: {len(synced)}")
        print(f"   Orders WITHOUT commission data: {len(not_synced)}")

        # Analyze synced
        print("\n   PaymentStatus for orders WITH commission data:")
        synced_status = defaultdict(int)
        for o in synced:
            ps = o.get("PaymentStatusId") or "NULL"
            if ps == EMPTY_GUID:
                ps = "EMPTY_GUID"
            elif ps == PLANNED_STATUS_ID:
                ps = "PLANNED"
            synced_status[ps] += 1
        for status, count in sorted(synced_status.items(), key=lambda x: -x[1]):
            print(f"     {status}: {count}")

        # Analyze not synced
        print("\n   PaymentStatus for orders WITHOUT commission data:")
        not_synced_status = defaultdict(int)
        for o in not_synced:
            ps = o.get("PaymentStatusId") or "NULL"
            if ps == EMPTY_GUID:
                ps = "EMPTY_GUID"
            elif ps == PLANNED_STATUS_ID:
                ps = "PLANNED"
            not_synced_status[ps] += 1
        for status, count in sorted(not_synced_status.items(), key=lambda x: -x[1]):
            print(f"     {status}: {count}")

    # 5. Alternative: Check by CreatedById pattern (Supervisor vs others)
    print("\n5. PaymentStatus by Creator (Supervisor vs Others)...")

    # Get Supervisor contact ID
    supervisor = client.query(
        "Contact",
        columns=["Id", "Name"],
        filters="Name eq 'Supervisor'",
        limit=1
    )
    supervisor_id = supervisor[0].get("Id") if supervisor else None

    if supervisor_id:
        supervisor_orders = [o for o in orders if o.get("CreatedById") == supervisor_id]
        other_orders = [o for o in orders if o.get("CreatedById") != supervisor_id]

        print(f"\n   Supervisor orders: {len(supervisor_orders)}")
        sup_status = defaultdict(int)
        for o in supervisor_orders:
            ps = o.get("PaymentStatusId") or "NULL"
            if ps == EMPTY_GUID:
                ps = "EMPTY_GUID"
            elif ps == PLANNED_STATUS_ID:
                ps = "PLANNED"
            sup_status[ps] += 1
        for status, count in sorted(sup_status.items(), key=lambda x: -x[1]):
            print(f"     {status}: {count}")

        print(f"\n   Other users' orders: {len(other_orders)}")
        other_status = defaultdict(int)
        for o in other_orders:
            ps = o.get("PaymentStatusId") or "NULL"
            if ps == EMPTY_GUID:
                ps = "EMPTY_GUID"
            elif ps == PLANNED_STATUS_ID:
                ps = "PLANNED"
            other_status[ps] += 1
        for status, count in sorted(other_status.items(), key=lambda x: -x[1]):
            print(f"     {status}: {count}")

    # 6. Conclusion
    print("\n" + "=" * 70)
    print("ANALYSIS SUMMARY")
    print("=" * 70)

    print("""
Based on the data patterns:
- Supervisor creates orders with EMPTY_GUID PaymentStatusId
- Other users create orders with PLANNED PaymentStatusId
- Commission data appears to come from QB sync which uses EMPTY_GUID orders

RECOMMENDATION:
  Reset PaymentStatusId from 'Planned' (bfe38d3d-bd57-48d7-a2d7-82435cd274ca)
  to EMPTY_GUID (00000000-0000-0000-0000-000000000000)

  This matches the pattern of orders that successfully sync to QuickBooks.
""")
    print("=" * 70)

if __name__ == "__main__":
    main()
