#!/usr/bin/env python3
"""Check IW processes and Order PaymentStatus patterns."""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

PLANNED_STATUS_ID = "bfe38d3d-bd57-48d7-a2d7-82435cd274ca"

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
            print(f"Query error for {entity}: {resp.status_code} - {resp.text[:200]}")
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
    print("IW Process and Order PaymentStatus Investigation")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Check IW-related processes
    print("\n1. IW-Related Business Processes")
    print("-" * 50)
    iw_processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId"],
        filters="contains(Name, 'IW') or contains(Caption, 'IW')",
        limit=50
    )
    if iw_processes:
        for p in iw_processes:
            pkg_id = p.get('SysPackageId')
            pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
            pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
            print(f"  {p.get('Name')}")
            print(f"    Caption: {p.get('Caption')}")
            print(f"    Package: {pkg_name}")
            print()
    else:
        print("  No IW processes found")

    # 2. Check Order entity (not SalesOrder)
    print("\n2. Recent Orders with PaymentStatusId")
    print("-" * 50)
    orders = client.query(
        "Order",
        columns=["Id", "Number", "PaymentStatusId", "CreatedById", "CreatedOn"],
        order_by="CreatedOn desc",
        limit=50
    )

    status_counts = {}
    creator_status = {}
    for o in orders:
        status = o.get('PaymentStatusId') or 'NULL'
        creator = o.get('CreatedById')

        status_counts[status] = status_counts.get(status, 0) + 1

        if creator not in creator_status:
            creator_status[creator] = {'orders': [], 'status_counts': {}}
        creator_status[creator]['orders'].append(o)
        creator_status[creator]['status_counts'][status] = creator_status[creator]['status_counts'].get(status, 0) + 1

    print(f"  PaymentStatusId distribution (last {len(orders)} orders):")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        status_name = "Planned" if status == PLANNED_STATUS_ID else ("NULL" if status == "NULL" else status[:8])
        print(f"    {status_name}: {count}")

    # 3. PaymentStatusId by Creator
    print("\n3. PaymentStatusId Distribution by Creator")
    print("-" * 50)
    for creator_id, data in creator_status.items():
        contacts = client.query("Contact", columns=["Name"], filters=f"Id eq {creator_id}")
        name = contacts[0].get('Name') if contacts else 'Unknown'
        print(f"\n  {name}:")
        for status, count in sorted(data['status_counts'].items(), key=lambda x: -x[1]):
            status_name = "Planned" if status == PLANNED_STATUS_ID else ("NULL" if status == "NULL" else status[:8])
            print(f"    {status_name}: {count}")

    # 4. December 2025 Orders
    print("\n4. December 2025 Orders PaymentStatus Distribution")
    print("-" * 50)
    dec_orders = client.query(
        "Order",
        columns=["PaymentStatusId", "CreatedById"],
        filters="CreatedOn ge 2025-12-01T00:00:00Z and CreatedOn lt 2026-01-01T00:00:00Z",
        limit=500
    )

    dec_status = {}
    dec_creator_status = {}
    for o in dec_orders:
        status = o.get('PaymentStatusId') or 'NULL'
        creator = o.get('CreatedById')

        dec_status[status] = dec_status.get(status, 0) + 1

        if creator not in dec_creator_status:
            dec_creator_status[creator] = {}
        dec_creator_status[creator][status] = dec_creator_status[creator].get(status, 0) + 1

    print(f"  Total December 2025 orders: {len(dec_orders)}")
    for status, count in sorted(dec_status.items(), key=lambda x: -x[1]):
        status_name = "Planned" if status == PLANNED_STATUS_ID else ("NULL" if status == "NULL" else status[:8])
        print(f"    {status_name}: {count}")

    # 5. Check when Planned status started appearing
    print("\n5. When Did 'Planned' Status Start Appearing?")
    print("-" * 50)

    # Get earliest orders with Planned status
    planned_orders = client.query(
        "Order",
        columns=["Id", "Number", "CreatedOn", "CreatedById"],
        filters=f"PaymentStatusId eq {PLANNED_STATUS_ID}",
        order_by="CreatedOn asc",
        limit=10
    )

    if planned_orders:
        print("  Earliest orders with 'Planned' status:")
        for o in planned_orders:
            contacts = client.query("Contact", columns=["Name"], filters=f"Id eq {o.get('CreatedById')}")
            creator = contacts[0].get('Name') if contacts else 'Unknown'
            print(f"    {o.get('Number')} - {o.get('CreatedOn')[:10]} - {creator}")
    else:
        print("  No orders with 'Planned' status found")

    # 6. Check process that sets Payment Status
    print("\n6. Business Processes That Set Payment Status")
    print("-" * 50)
    payment_processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId"],
        filters="contains(Name, 'Payment') or contains(Caption, 'Payment')",
        limit=30
    )
    for p in payment_processes:
        pkg_id = p.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        print(f"  {p.get('Name')} ({pkg_name})")

    # 7. Check if IWQBIntegration has any processes
    print("\n7. All Processes in IWQBIntegration Package")
    print("-" * 50)
    iwqb_id = "5af0c9b0-141b-4d3f-828e-a455a1705aed"
    iwqb_processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption"],
        filters=f"SysPackageId eq {iwqb_id}",
        limit=50
    )
    if iwqb_processes:
        for p in iwqb_processes:
            print(f"  {p.get('Name')}: {p.get('Caption')}")
    else:
        print("  No processes found in IWQBIntegration package")

    # 8. Check for entity event handlers
    print("\n8. Order Entity Signal Events")
    print("-" * 50)
    signals = client.query(
        "VwProcessSignalEvent",
        columns=["Id", "ProcessSchemaName", "EntitySchemaName", "EventType"],
        filters="EntitySchemaName eq 'Order'",
        limit=30
    )
    if signals:
        for s in signals:
            print(f"  Process: {s.get('ProcessSchemaName')}")
            print(f"    Event: {s.get('EventType')}")
    else:
        # Try alternate approach
        print("  VwProcessSignalEvent not available, checking SysProcessStartEvent...")
        start_events = client.query(
            "SysProcessStartEvent",
            filters="contains(RecordSchemaName, 'Order')",
            limit=20
        )
        for e in start_events:
            print(f"  {e}")

    print("\n" + "=" * 70)
    print("Investigation complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
