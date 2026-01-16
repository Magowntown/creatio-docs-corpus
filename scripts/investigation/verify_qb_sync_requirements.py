#!/usr/bin/env python3
"""Verify what PaymentStatusId values allow QB sync."""

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
            return []
        return resp.json().get("value", [])

def main():
    print("=" * 70)
    print("VERIFY QB SYNC PAYMENTSTATUS REQUIREMENTS")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Get orders that HAVE been synced to QB (have BGQBDownload records)
    print("\n1. Checking orders that HAVE been synced to QuickBooks...")

    # Get recent BGQBDownload records with invoice numbers
    qb_records = client.query(
        "BGQBDownload",
        columns=["Id", "BGCleanInvoiceNumber", "BGTransactionDate"],
        order_by="BGTransactionDate desc",
        limit=200
    )

    print(f"   Found {len(qb_records)} recent QB download records")

    # Get the invoice numbers
    synced_invoice_nums = set()
    for qb in qb_records:
        inv_num = qb.get("BGCleanInvoiceNumber")
        if inv_num:
            synced_invoice_nums.add(inv_num)

    print(f"   Unique invoice numbers: {len(synced_invoice_nums)}")

    # 2. Get orders and check their PaymentStatusId
    print("\n2. Fetching orders to compare synced vs non-synced...")

    # Fetch recent orders
    orders = []
    for skip in range(0, 1000, 200):
        batch = client.query(
            "Order",
            columns=["Id", "Number", "BGInvoiceNumber", "PaymentStatusId", "CreatedOn"],
            order_by="CreatedOn desc",
            limit=200,
            skip=skip
        )
        if not batch:
            break
        orders.extend(batch)

    print(f"   Fetched {len(orders)} orders")

    # 3. Categorize orders
    synced_orders = []
    not_synced_orders = []

    for order in orders:
        inv_num = order.get("BGInvoiceNumber")
        if inv_num and inv_num in synced_invoice_nums:
            synced_orders.append(order)
        else:
            not_synced_orders.append(order)

    print(f"\n3. Order categorization:")
    print(f"   Orders synced to QB: {len(synced_orders)}")
    print(f"   Orders NOT synced to QB: {len(not_synced_orders)}")

    # 4. Analyze PaymentStatusId for synced orders
    print("\n4. PaymentStatusId distribution for SYNCED orders:")
    synced_status_counts = defaultdict(int)
    for order in synced_orders:
        status = order.get("PaymentStatusId") or "NULL"
        if status == EMPTY_GUID:
            status = "EMPTY_GUID"
        elif status == PLANNED_STATUS_ID:
            status = "PLANNED"
        synced_status_counts[status] += 1

    for status, count in sorted(synced_status_counts.items(), key=lambda x: -x[1]):
        print(f"     {status}: {count}")

    # 5. Analyze PaymentStatusId for NOT synced orders
    print("\n5. PaymentStatusId distribution for NOT SYNCED orders:")
    not_synced_status_counts = defaultdict(int)
    for order in not_synced_orders:
        status = order.get("PaymentStatusId") or "NULL"
        if status == EMPTY_GUID:
            status = "EMPTY_GUID"
        elif status == PLANNED_STATUS_ID:
            status = "PLANNED"
        not_synced_status_counts[status] += 1

    for status, count in sorted(not_synced_status_counts.items(), key=lambda x: -x[1]):
        print(f"     {status}: {count}")

    # 6. Look up all PaymentStatus values
    print("\n6. All PaymentStatus lookup values:")
    statuses = client.query(
        "OrderPaymentStatus",
        columns=["Id", "Name"],
        limit=20
    )
    status_names = {s.get("Id"): s.get("Name") for s in statuses}
    for s in statuses:
        print(f"     {s.get('Name')}: {s.get('Id')}")

    # 7. Summary with names
    print("\n7. SUMMARY - PaymentStatus that allows QB sync:")
    print("   " + "-" * 50)

    if synced_status_counts:
        for status_id, count in synced_status_counts.items():
            if status_id in ["NULL", "EMPTY_GUID", "PLANNED"]:
                name = status_id
            else:
                name = status_names.get(status_id, status_id)
            print(f"   SYNCED with '{name}': {count} orders")

    print("\n   PaymentStatus that BLOCKS QB sync:")
    print("   " + "-" * 50)
    if not_synced_status_counts:
        for status_id, count in not_synced_status_counts.items():
            if status_id in ["NULL", "EMPTY_GUID", "PLANNED"]:
                name = status_id
            else:
                name = status_names.get(status_id, status_id)
            print(f"   NOT SYNCED with '{name}': {count} orders")

    # 8. Conclusion
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)

    if "EMPTY_GUID" in synced_status_counts or "NULL" in synced_status_counts:
        print("   ✓ Orders with NULL/EMPTY PaymentStatusId ARE being synced to QB")

    if "PLANNED" in not_synced_status_counts and "PLANNED" not in synced_status_counts:
        print("   ✗ Orders with 'Planned' PaymentStatusId are NOT being synced to QB")
        print("\n   RECOMMENDATION: Reset PaymentStatusId from 'Planned' to NULL")
    elif "PLANNED" in synced_status_counts:
        print("   ? Some 'Planned' orders ARE synced - need more investigation")

    print("=" * 70)

if __name__ == "__main__":
    main()
