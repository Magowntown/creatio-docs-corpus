#!/usr/bin/env python3
"""Reset PaymentStatusId using DataService API."""

import os
import sys
import json
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

    def select_query(self, root_schema, columns, filters=None, row_count=100):
        """Use DataService SelectQuery."""
        url = f"{self.base_url}/0/DataService/json/SyncReply/SelectQuery"

        query = {
            "RootSchemaName": root_schema,
            "OperationType": 0,
            "Columns": {
                "Items": {col: {"Expression": {"ColumnPath": col}} for col in columns}
            },
            "AllColumns": False,
            "RowCount": row_count
        }

        if filters:
            query["Filters"] = filters

        resp = self.session.post(url, json=query)
        if resp.status_code != 200:
            print(f"SelectQuery error: {resp.status_code} - {resp.text[:200]}")
            return []

        result = resp.json()
        rows = result.get("rows", [])
        return rows

    def update_query(self, root_schema, column_values, filters):
        """Use DataService UpdateQuery."""
        url = f"{self.base_url}/0/DataService/json/SyncReply/UpdateQuery"

        query = {
            "RootSchemaName": root_schema,
            "OperationType": 2,
            "ColumnValues": {
                "Items": column_values
            },
            "Filters": filters
        }

        resp = self.session.post(url, json=query)
        if resp.status_code != 200:
            print(f"UpdateQuery error: {resp.status_code} - {resp.text[:200]}")
            return False, resp

        return True, resp

def build_guid_filter(column, guid_value):
    """Build a filter for GUID comparison."""
    return {
        "FilterType": 1,
        "ComparisonType": 3,  # Equal
        "LeftExpression": {
            "ExpressionType": 0,
            "ColumnPath": column
        },
        "RightExpression": {
            "ExpressionType": 2,
            "Parameter": {
                "DataValueType": 0,  # GUID
                "Value": guid_value
            }
        }
    }

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

    # 1. Count affected orders using SelectQuery
    print("\n1. Fetching orders with 'Planned' PaymentStatus...")

    filters = {
        "FilterType": 6,  # FilterGroup
        "Items": {
            "PaymentStatusFilter": build_guid_filter("PaymentStatusId", PLANNED_STATUS_ID)
        }
    }

    affected_orders = client.select_query(
        "Order",
        columns=["Id", "Number", "CreatedOn"],
        filters=filters,
        row_count=2000
    )

    print(f"   Found {len(affected_orders)} orders with 'Planned' status")

    if not affected_orders:
        print("\n   No orders to update.")
        return

    # 2. Show sample
    print("\n2. Sample orders to be updated:")
    for order in affected_orders[:10]:
        print(f"   - {order.get('Number')} (Created: {str(order.get('CreatedOn', ''))[:10]})")
    if len(affected_orders) > 10:
        print(f"   ... and {len(affected_orders) - 10} more")

    # 3. Dry run stops here
    if dry_run:
        print(f"\n3. DRY RUN COMPLETE")
        print(f"   Would update {len(affected_orders)} orders")
        print(f"\n   To execute, run: python3 {sys.argv[0]} --execute")
        return

    # 4. Execute bulk update
    print(f"\n3. EXECUTING bulk update...")

    confirm = input(f"   Type 'yes' to confirm updating {len(affected_orders)} orders: ")
    if confirm.lower() != 'yes':
        print("   Aborted.")
        return

    # Use UpdateQuery to update all matching records at once
    column_values = {
        "PaymentStatusId": {
            "Expression": {
                "ExpressionType": 2,
                "Parameter": {
                    "DataValueType": 0,
                    "Value": EMPTY_GUID
                }
            }
        }
    }

    success, resp = client.update_query("Order", column_values, filters)

    if success:
        result = resp.json()
        rows_affected = result.get("rowsAffected", "unknown")
        print(f"\n   SUCCESS! Rows affected: {rows_affected}")
    else:
        print(f"\n   FAILED: {resp.text[:300]}")

    # 5. Verify
    print("\n4. Verification...")
    remaining = client.select_query(
        "Order",
        columns=["Id"],
        filters=filters,
        row_count=100
    )
    print(f"   Orders still with 'Planned' status: {len(remaining)}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
