#!/usr/bin/env python3
"""Reset PaymentStatusId from 'Planned' to NULL for affected orders - V2."""

import os
import sys
import requests
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

    def query_all_pages(self, entity, columns, filters, batch_size=100, max_records=2000):
        """Query with pagination to get all matching records."""
        all_records = []
        skip = 0

        while len(all_records) < max_records:
            url = f"{self.base_url}/0/odata/{entity}"
            params = {
                "$top": str(batch_size),
                "$skip": str(skip),
                "$select": ",".join(columns),
                "$filter": filters,
                "$orderby": "CreatedOn desc"
            }

            resp = self.session.get(url, params=params)
            if resp.status_code != 200:
                print(f"Query error at skip={skip}: {resp.status_code}")
                break

            records = resp.json().get("value", [])
            if not records:
                break

            all_records.extend(records)
            skip += batch_size

            if len(records) < batch_size:
                break  # No more records

        return all_records

    def update(self, entity, record_id, data):
        url = f"{self.base_url}/0/odata/{entity}({record_id})"
        resp = self.session.patch(url, json=data)
        return resp.status_code in [200, 204], resp

def main():
    dry_run = "--dry-run" in sys.argv
    execute = "--execute" in sys.argv

    if not dry_run and not execute:
        print("Usage:")
        print("  --dry-run   Show what would be updated (no changes)")
        print("  --execute   Actually perform the updates")
        return

    print("=" * 70)
    print("RESET PAYMENTSTATUSID FROM 'PLANNED' TO NULL")
    print("=" * 70)
    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTE'}")
    print()

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Get all orders with Planned status
    print("\n1. Fetching orders with 'Planned' PaymentStatus...")

    affected_orders = client.query_all_pages(
        "Order",
        columns=["Id", "Number", "CreatedOn", "PaymentStatusId"],
        filters=f"PaymentStatusId eq {PLANNED_STATUS_ID}",
        max_records=2000
    )

    print(f"   Found {len(affected_orders)} orders with 'Planned' status")

    if not affected_orders:
        print("\n   No orders to update.")
        return

    # 2. Show breakdown
    print("\n2. Orders to be updated:")
    for order in affected_orders[:10]:
        print(f"   - {order.get('Number')} (Created: {order.get('CreatedOn', '')[:10]})")
    if len(affected_orders) > 10:
        print(f"   ... and {len(affected_orders) - 10} more")

    # 3. Dry run stops here
    if dry_run:
        print(f"\n3. DRY RUN COMPLETE")
        print(f"   Would update {len(affected_orders)} orders")
        print(f"\n   To execute, run: python3 {sys.argv[0]} --execute")
        return

    # 4. Confirm before executing
    print(f"\n3. EXECUTING updates for {len(affected_orders)} orders...")

    confirm = input(f"   Type 'yes' to confirm updating {len(affected_orders)} orders: ")
    if confirm.lower() != 'yes':
        print("   Aborted.")
        return

    # 5. Perform updates
    print("\n4. Updating orders...")
    success = 0
    errors = []

    for i, order in enumerate(affected_orders):
        order_id = order.get('Id')
        order_num = order.get('Number')

        ok, resp = client.update("Order", order_id, {
            "PaymentStatusId": EMPTY_GUID
        })

        if ok:
            success += 1
        else:
            errors.append((order_num, resp.status_code, resp.text[:100] if resp.text else "Unknown"))

        if (i + 1) % 25 == 0:
            print(f"   Progress: {i + 1}/{len(affected_orders)} (success: {success}, errors: {len(errors)})")

    # 6. Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"   Total processed: {len(affected_orders)}")
    print(f"   Successfully updated: {success}")
    print(f"   Errors: {len(errors)}")

    if errors:
        print("\n   First 10 errors:")
        for order_num, status, msg in errors[:10]:
            print(f"     Order {order_num}: HTTP {status}")

    # 7. Verify
    print("\n5. Verification...")
    remaining = client.query_all_pages(
        "Order",
        columns=["Id"],
        filters=f"PaymentStatusId eq {PLANNED_STATUS_ID}",
        max_records=100
    )
    print(f"   Orders still with 'Planned' status: {len(remaining)}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
