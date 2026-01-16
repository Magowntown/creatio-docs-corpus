#!/usr/bin/env python3
"""Check Order entity default values and payment status configuration."""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

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

    def query(self, entity, columns=None, filters=None, order_by=None, limit=100, expand=None):
        url = f"{self.base_url}/0/odata/{entity}"
        params = {"$top": str(limit)}
        if columns:
            params["$select"] = ",".join(columns)
        if filters:
            params["$filter"] = filters
        if order_by:
            params["$orderby"] = order_by
        if expand:
            params["$expand"] = expand

        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            print(f"Query error for {entity}: {resp.status_code}")
            return []
        return resp.json().get("value", [])

    def count(self, entity, filters=None):
        url = f"{self.base_url}/0/odata/{entity}/$count"
        params = {}
        if filters:
            params["$filter"] = filters
        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            return -1
        try:
            return int(resp.text)
        except:
            return -1

def main():
    print("=" * 70)
    print("Order Payment Status Investigation")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Get distinct PaymentStatusId values from SalesOrder
    print("\n1. Distinct PaymentStatusId Values in Orders")
    print("-" * 50)

    # Sample recent orders to see PaymentStatusId distribution
    orders = client.query(
        "SalesOrder",
        columns=["Id", "Number", "PaymentStatusId", "CreatedById", "CreatedOn"],
        order_by="CreatedOn desc",
        limit=100
    )

    status_counts = {}
    creator_status = {}
    for o in orders:
        status = o.get('PaymentStatusId') or 'NULL'
        creator = o.get('CreatedById')

        status_counts[status] = status_counts.get(status, 0) + 1

        if creator not in creator_status:
            creator_status[creator] = {}
        creator_status[creator][status] = creator_status[creator].get(status, 0) + 1

    print("  PaymentStatusId distribution (last 100 orders):")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        print(f"    {status}: {count}")

    # 2. Look up creator names
    print("\n2. PaymentStatusId by Creator")
    print("-" * 50)
    for creator_id, statuses in creator_status.items():
        # Look up contact name
        contacts = client.query(
            "Contact",
            columns=["Name"],
            filters=f"Id eq {creator_id}"
        )
        name = contacts[0].get('Name') if contacts else 'Unknown'
        print(f"\n  {name}:")
        for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
            print(f"    {status}: {count}")

    # 3. Get the "Planned" status ID and other statuses
    print("\n3. Looking Up Payment Status Names via Order Expansion")
    print("-" * 50)

    # Try to expand PaymentStatus on Order
    order_with_status = client.query(
        "SalesOrder",
        columns=["Number", "PaymentStatusId"],
        filters="PaymentStatusId ne null",
        expand="PaymentStatus($select=Name)",
        limit=10
    )

    status_names = {}
    for o in order_with_status:
        status_id = o.get('PaymentStatusId')
        status_obj = o.get('PaymentStatus', {})
        status_name = status_obj.get('Name') if status_obj else 'Unknown'
        if status_id not in status_names:
            status_names[status_id] = status_name
            print(f"  {status_id} = '{status_name}'")

    # 4. Check for OrderPaymentStatus or similar lookup
    print("\n4. Checking OrderPaymentStatus Lookup")
    print("-" * 50)
    lookups = client.query(
        "OrderPaymentStatus",
        columns=["Id", "Name", "Description"],
        limit=20
    )
    if lookups:
        for l in lookups:
            print(f"  {l.get('Name')}: {l.get('Id')}")
    else:
        print("  OrderPaymentStatus entity not accessible via OData")

    # 5. Check which orders have Planned status and when they were created
    print("\n5. Recent Orders with 'Planned' Status (if any)")
    print("-" * 50)

    # First find an order with Planned status to get the ID
    planned_orders = client.query(
        "SalesOrder",
        columns=["Id", "Number", "CreatedOn", "CreatedById", "PaymentStatusId"],
        filters="PaymentStatusId ne null",
        order_by="CreatedOn desc",
        limit=20
    )

    for o in planned_orders:
        contacts = client.query("Contact", columns=["Name"], filters=f"Id eq {o.get('CreatedById')}")
        creator_name = contacts[0].get('Name') if contacts else 'Unknown'
        print(f"  {o.get('Number')} - Created: {o.get('CreatedOn')[:10]} by {creator_name}")
        print(f"    PaymentStatusId: {o.get('PaymentStatusId')}")

    # 6. Check business process logs for Order creation
    print("\n6. Recent Process Logs Related to Order/Payment")
    print("-" * 50)
    logs = client.query(
        "SysProcessLog",
        columns=["Id", "Name", "StartDate", "Status", "OwnerId"],
        filters="contains(Name, 'Order') or contains(Name, 'Payment')",
        order_by="StartDate desc",
        limit=10
    )
    if logs:
        for log in logs:
            print(f"  {log.get('Name')}")
            print(f"    Started: {log.get('StartDate')}")
            print(f"    Status: {log.get('Status')}")
    else:
        print("  No matching process logs found")

    # 7. Count orders by PaymentStatus for December 2025
    print("\n7. December 2025 Orders by PaymentStatus")
    print("-" * 50)

    dec_orders = client.query(
        "SalesOrder",
        columns=["PaymentStatusId"],
        filters="CreatedOn ge 2025-12-01T00:00:00Z and CreatedOn lt 2026-01-01T00:00:00Z",
        limit=500
    )

    dec_status_counts = {}
    for o in dec_orders:
        status = o.get('PaymentStatusId') or 'NULL'
        dec_status_counts[status] = dec_status_counts.get(status, 0) + 1

    print(f"  Total December 2025 orders checked: {len(dec_orders)}")
    for status, count in sorted(dec_status_counts.items(), key=lambda x: -x[1]):
        print(f"    {status}: {count}")

    print("\n" + "=" * 70)
    print("Investigation complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
