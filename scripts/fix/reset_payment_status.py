#!/usr/bin/env python3
"""Reset PaymentStatusId from 'Planned' to NULL for affected orders."""

import os
import requests
from datetime import datetime
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

    def query(self, entity, columns=None, filters=None, order_by=None, limit=100):
        url = f"{self.base_url}/0/odata/{entity}"
        params = {"$top": str(limit)}
        if columns:
            params["$select"] = ",".join(columns)
        if filters:
            params["$filter"] = filters
        if order_by:
            params["$orderby"] = order_by

        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            print(f"Query error: {resp.status_code} - {resp.text[:200]}")
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

    def update(self, entity, record_id, data):
        url = f"{self.base_url}/0/odata/{entity}({record_id})"
        resp = self.session.patch(url, json=data)
        return resp.status_code == 204 or resp.status_code == 200, resp

def main():
    import sys

    dry_run = "--dry-run" in sys.argv
    limit_arg = None
    for arg in sys.argv:
        if arg.startswith("--limit="):
            limit_arg = int(arg.split("=")[1])

    print("=" * 70)
    print("RESET PAYMENTSTATUSID FROM 'PLANNED' TO NULL")
    print("=" * 70)
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE UPDATE'}")
    print(f"Target: Orders with PaymentStatusId = {PLANNED_STATUS_ID}")
    print()

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Count affected orders
    print("\n1. Counting affected orders...")
    total_affected = client.count("Order", f"PaymentStatusId eq {PLANNED_STATUS_ID}")
    print(f"   Total orders with 'Planned' status: {total_affected}")

    if total_affected <= 0:
        print("\n   No orders to update. Exiting.")
        return

    # 2. Get affected orders
    print("\n2. Fetching affected orders...")
    fetch_limit = limit_arg or min(total_affected, 500)

    affected_orders = client.query(
        "Order",
        columns=["Id", "Number", "CreatedOn", "CreatedById"],
        filters=f"PaymentStatusId eq {PLANNED_STATUS_ID}",
        order_by="CreatedOn desc",
        limit=fetch_limit
    )

    print(f"   Fetched {len(affected_orders)} orders to process")

    # 3. Show sample before update
    print("\n3. Sample of orders to be updated:")
    for order in affected_orders[:5]:
        print(f"   - Order {order.get('Number')} (Created: {order.get('CreatedOn', '')[:10]})")

    if len(affected_orders) > 5:
        print(f"   ... and {len(affected_orders) - 5} more")

    # 4. Perform updates
    if dry_run:
        print("\n4. DRY RUN - No updates performed")
        print(f"   Would have updated {len(affected_orders)} orders")
        print("\n   To perform actual updates, run without --dry-run flag")
        return

    print(f"\n4. Updating {len(affected_orders)} orders...")
    success_count = 0
    error_count = 0
    errors = []

    for i, order in enumerate(affected_orders):
        order_id = order.get('Id')
        order_num = order.get('Number')

        success, resp = client.update("Order", order_id, {
            "PaymentStatusId": EMPTY_GUID
        })

        if success:
            success_count += 1
            if (i + 1) % 50 == 0:
                print(f"   Progress: {i + 1}/{len(affected_orders)} updated")
        else:
            error_count += 1
            errors.append((order_num, resp.status_code, resp.text[:100]))
            print(f"   ERROR updating Order {order_num}: {resp.status_code}")

    # 5. Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"   Total processed: {len(affected_orders)}")
    print(f"   Successfully updated: {success_count}")
    print(f"   Errors: {error_count}")

    if errors:
        print("\n   Errors:")
        for order_num, status, msg in errors[:10]:
            print(f"     Order {order_num}: {status} - {msg}")

    # 6. Verify
    print("\n6. Verification...")
    remaining = client.count("Order", f"PaymentStatusId eq {PLANNED_STATUS_ID}")
    print(f"   Orders still with 'Planned' status: {remaining}")

    print("\n" + "=" * 70)
    print("RESET COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
