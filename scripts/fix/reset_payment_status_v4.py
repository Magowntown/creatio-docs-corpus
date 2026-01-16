#!/usr/bin/env python3
"""Reset PaymentStatusId - fetch all orders and filter locally."""

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

    def query_batch(self, entity, columns, skip=0, top=100, order_by=None):
        """Query a batch of records."""
        url = f"{self.base_url}/0/odata/{entity}"
        params = {
            "$top": str(top),
            "$skip": str(skip),
            "$select": ",".join(columns)
        }
        if order_by:
            params["$orderby"] = order_by

        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            return None, resp.status_code
        return resp.json().get("value", []), 200

    def update(self, entity, record_id, data):
        """Update a single record."""
        url = f"{self.base_url}/0/odata/{entity}({record_id})"
        resp = self.session.patch(url, json=data)
        return resp.status_code in [200, 204], resp

def main():
    dry_run = "--dry-run" in sys.argv
    execute = "--execute" in sys.argv
    limit = 500

    for arg in sys.argv:
        if arg.startswith("--limit="):
            limit = int(arg.split("=")[1])

    if not dry_run and not execute:
        print("Usage:")
        print("  --dry-run         Show what would be updated (no changes)")
        print("  --execute         Actually perform the updates")
        print("  --limit=N         Process max N orders (default 500)")
        return

    print("=" * 70)
    print("RESET PAYMENTSTATUSID FROM 'PLANNED' TO NULL")
    print("=" * 70)
    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTE'}")
    print(f"Max orders to process: {limit}")
    print()

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Fetch orders in batches and filter locally
    print("\n1. Fetching orders and filtering for 'Planned' status...")

    affected_orders = []
    skip = 0
    batch_size = 200
    total_scanned = 0

    while len(affected_orders) < limit:
        records, status = client.query_batch(
            "Order",
            columns=["Id", "Number", "CreatedOn", "PaymentStatusId"],
            skip=skip,
            top=batch_size,
            order_by="CreatedOn desc"
        )

        if status != 200 or records is None:
            print(f"   Query failed at skip={skip}")
            break

        if not records:
            print(f"   No more records at skip={skip}")
            break

        # Filter locally
        for order in records:
            if order.get("PaymentStatusId") == PLANNED_STATUS_ID:
                affected_orders.append(order)
                if len(affected_orders) >= limit:
                    break

        total_scanned += len(records)
        skip += batch_size

        print(f"   Scanned {total_scanned} orders, found {len(affected_orders)} with 'Planned' status...")

        if len(records) < batch_size:
            break

    print(f"\n   Total scanned: {total_scanned}")
    print(f"   Orders with 'Planned' status: {len(affected_orders)}")

    if not affected_orders:
        print("\n   No orders to update.")
        return

    # 2. Show sample
    print("\n2. Orders to be updated:")
    for order in affected_orders[:15]:
        print(f"   - {order.get('Number')} (Created: {order.get('CreatedOn', '')[:10]})")
    if len(affected_orders) > 15:
        print(f"   ... and {len(affected_orders) - 15} more")

    # 3. Dry run stops here
    if dry_run:
        print(f"\n3. DRY RUN COMPLETE")
        print(f"   Would update {len(affected_orders)} orders")
        print(f"\n   To execute, run: python3 {sys.argv[0]} --execute")
        return

    # 4. Confirm before executing
    print(f"\n3. Ready to update {len(affected_orders)} orders")
    confirm = input("   Type 'yes' to confirm: ")
    if confirm.lower() != 'yes':
        print("   Aborted.")
        return

    # 5. Execute updates
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
            errors.append((order_num, resp.status_code))

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
        print("\n   Errors:")
        for order_num, status in errors[:10]:
            print(f"     Order {order_num}: HTTP {status}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
