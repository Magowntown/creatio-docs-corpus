#!/usr/bin/env python3
"""Analyze process triggers and Order entity columns."""

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
            print(f"Query error for {entity}: {resp.status_code}")
            return []
        return resp.json().get("value", [])

def main():
    print("=" * 80)
    print("PROCESS TRIGGER & ORDER COLUMN ANALYSIS")
    print("=" * 80)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Get recent process logs for IW processes
    print("\n" + "=" * 80)
    print("1. RECENT IW PROCESS EXECUTIONS")
    print("=" * 80)

    iw_logs = client.query(
        "SysProcessLog",
        columns=["Id", "Name", "StartDate", "CompleteDate", "Status", "ErrorDescription"],
        filters="contains(Name, 'IW')",
        order_by="StartDate desc",
        limit=30
    )

    process_counts = {}
    for log in iw_logs:
        name = log.get('Name')
        process_counts[name] = process_counts.get(name, 0) + 1

    print("\n  IW Process execution counts (last 30 logs):")
    for name, count in sorted(process_counts.items(), key=lambda x: -x[1]):
        print(f"    {name}: {count}")

    print("\n  Recent IW executions with details:")
    for log in iw_logs[:10]:
        print(f"\n    {log.get('Name')}")
        print(f"      Started: {log.get('StartDate', '')[:19]}")
        print(f"      Status: {log.get('Status')}")
        if log.get('ErrorDescription'):
            print(f"      Error: {log.get('ErrorDescription')[:100]}")

    # 2. Check recent QB sync process logs
    print("\n" + "=" * 80)
    print("2. RECENT QB SYNC PROCESS EXECUTIONS")
    print("=" * 80)

    qb_logs = client.query(
        "SysProcessLog",
        columns=["Id", "Name", "StartDate", "CompleteDate", "Status", "ErrorDescription"],
        filters="contains(Name, 'QB') or contains(Name, 'QuickBooks')",
        order_by="StartDate desc",
        limit=30
    )

    qb_counts = {}
    for log in qb_logs:
        name = log.get('Name')
        qb_counts[name] = qb_counts.get(name, 0) + 1

    print("\n  QB Process execution counts (last 30 logs):")
    for name, count in sorted(qb_counts.items(), key=lambda x: -x[1]):
        print(f"    {name}: {count}")

    # 3. Get ALL columns on Order entity
    print("\n" + "=" * 80)
    print("3. ORDER ENTITY COLUMNS (Looking for IW/Payment fields)")
    print("=" * 80)

    orders = client.query("Order", limit=1)
    if orders:
        all_columns = sorted(orders[0].keys())

        # Filter for interesting columns
        iw_columns = [c for c in all_columns if c.startswith('IW')]
        payment_columns = [c for c in all_columns if 'Payment' in c]
        status_columns = [c for c in all_columns if 'Status' in c]
        tax_columns = [c for c in all_columns if 'Tax' in c]

        print(f"\n  Total columns: {len(all_columns)}")

        print(f"\n  IW-prefixed columns ({len(iw_columns)}):")
        for c in iw_columns:
            print(f"    - {c}")

        print(f"\n  Payment-related columns ({len(payment_columns)}):")
        for c in payment_columns:
            print(f"    - {c}")

        print(f"\n  Status-related columns ({len(status_columns)}):")
        for c in status_columns:
            print(f"    - {c}")

        print(f"\n  Tax-related columns ({len(tax_columns)}):")
        for c in tax_columns:
            print(f"    - {c}")

    # 4. Check if IW processes run on Order creation
    print("\n" + "=" * 80)
    print("4. ORDER CREATION TIMELINE vs PROCESS EXECUTION")
    print("=" * 80)

    # Get recent orders with Planned status
    recent_planned = client.query(
        "Order",
        columns=["Id", "Number", "CreatedOn", "CreatedById", "PaymentStatusId"],
        filters=f"PaymentStatusId eq {PLANNED_STATUS_ID}",
        order_by="CreatedOn desc",
        limit=5
    )

    print("\n  Recent orders with Planned status and corresponding process logs:")
    for order in recent_planned:
        created_on = order.get('CreatedOn', '')
        print(f"\n  Order {order.get('Number')} created at {created_on[:19]}")

        # Look for process logs around that time
        if created_on:
            # Get process logs within 1 minute of order creation
            start_time = created_on[:19] + "Z"
            logs_around = client.query(
                "SysProcessLog",
                columns=["Name", "StartDate"],
                filters=f"StartDate ge {start_time}",
                order_by="StartDate asc",
                limit=10
            )

            if logs_around:
                print("    Processes that ran shortly after:")
                for log in logs_around[:5]:
                    print(f"      {log.get('StartDate', '')[:19]} - {log.get('Name')}")

    # 5. Compare Order creators and their IW process triggering
    print("\n" + "=" * 80)
    print("5. IW ORDER-TAX PROCESS TRIGGER ANALYSIS")
    print("=" * 80)

    # Check if IWSetOrderandProductTaxStatusByOrderSalesTaxV2 ran recently
    tax_logs = client.query(
        "SysProcessLog",
        columns=["Id", "Name", "StartDate", "Status"],
        filters="contains(Name, 'TaxStatus')",
        order_by="StartDate desc",
        limit=20
    )

    print(f"\n  IW Tax Status process executions: {len(tax_logs)}")
    for log in tax_logs[:10]:
        print(f"    {log.get('StartDate', '')[:19]} - {log.get('Name')} - {log.get('Status')}")

    # 6. Check BGSetOrderProductTaxStatusByOrderSalesTax specifically
    print("\n" + "=" * 80)
    print("6. BGSetOrderProductTaxStatusByOrderSalesTax PROCESS")
    print("=" * 80)

    bg_tax_logs = client.query(
        "SysProcessLog",
        columns=["Id", "Name", "StartDate", "Status", "ErrorDescription"],
        filters="Name eq 'BGSetOrderProductTaxStatusByOrderSalesTax'",
        order_by="StartDate desc",
        limit=10
    )

    print(f"\n  BGSetOrderProductTaxStatusByOrderSalesTax executions: {len(bg_tax_logs)}")
    for log in bg_tax_logs:
        print(f"    {log.get('StartDate', '')[:19]} - Status: {log.get('Status')}")

    # 7. Check Order-related processes from PampaBay package
    print("\n" + "=" * 80)
    print("7. PAMPABAY ORDER PROCESSES")
    print("=" * 80)

    pampabay_order_procs = [
        "BGAddCommissionEarners",
        "BGAddCommissionEarnersManager",
        "BGBPOrderCalculateFieldsV2",
        "BGOrdersStockInventory",
        "BGBPOrdersSetTotalInnerAndMaster",
    ]

    for proc_name in pampabay_order_procs:
        logs = client.query(
            "SysProcessLog",
            columns=["StartDate", "Status"],
            filters=f"Name eq '{proc_name}'",
            order_by="StartDate desc",
            limit=5
        )
        print(f"\n  {proc_name}: {len(logs)} recent executions")
        for log in logs[:3]:
            print(f"    {log.get('StartDate', '')[:19]} - {log.get('Status')}")

    # 8. Look for any process that might set PaymentStatus
    print("\n" + "=" * 80)
    print("8. SEARCHING FOR PAYMENTSTATUS SETTER")
    print("=" * 80)

    # Get orders where PaymentStatus was set to Planned and check what ran
    print("\n  Looking at orders with Planned status created TODAY...")

    today_planned = client.query(
        "Order",
        columns=["Id", "Number", "CreatedOn", "ModifiedOn", "PaymentStatusId"],
        filters=f"PaymentStatusId eq {PLANNED_STATUS_ID} and CreatedOn ge 2026-01-15T00:00:00Z",
        order_by="CreatedOn desc",
        limit=10
    )

    print(f"  Found {len(today_planned)} orders with Planned status created today")
    for order in today_planned:
        print(f"    Order {order.get('Number')}: Created {order.get('CreatedOn', '')[:19]}, Modified {order.get('ModifiedOn', '')[:19]}")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
