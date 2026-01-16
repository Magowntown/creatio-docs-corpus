#!/usr/bin/env python3
"""Check QuickBooks sync process filters and IWQBIntegration Order defaults."""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

PLANNED_STATUS_ID = "bfe38d3d-bd57-48d7-a2d7-82435cd274ca"
IWQB_PACKAGE_ID = "5af0c9b0-141b-4d3f-828e-a455a1705aed"

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
    print("=" * 70)
    print("QuickBooks Sync Process & Order Default Investigation")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Check the QB Customer Order Integration process
    print("\n1. QuickBooks Integration Processes")
    print("-" * 50)
    qb_processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId"],
        filters="contains(Name, 'QB') or contains(Name, 'QuickBooks')",
        limit=30
    )
    for p in qb_processes:
        pkg_id = p.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        print(f"  {p.get('Name')}")
        print(f"    Caption: {p.get('Caption')}")
        print(f"    Package: {pkg_name}")
        print()

    # 2. Check the BGCommissionReportQBDownload entity
    print("\n2. BGCommissionReportQBDownload - Sample Data")
    print("-" * 50)
    qb_downloads = client.query(
        "BGQBDownload",
        columns=["Id", "BGTransactionDate", "BGTransactionType", "BGRep", "BGCleanInvoiceNumber"],
        order_by="BGTransactionDate desc",
        limit=10
    )
    for qb in qb_downloads:
        print(f"  Invoice: {qb.get('BGCleanInvoiceNumber')} - {qb.get('BGTransactionDate', '')[:10]}")
        print(f"    Type: {qb.get('BGTransactionType')} | Rep: {qb.get('BGRep')}")

    # 3. Check if there's a PaymentStatus filter in GetQuickBooks
    print("\n3. Orders with Planned Status - Check if they have QBDownload records")
    print("-" * 50)

    # Get some orders with Planned status
    planned_orders = client.query(
        "Order",
        columns=["Id", "Number", "BGInvoiceNumber", "BGInvoiceDate", "PaymentStatusId"],
        filters=f"PaymentStatusId eq {PLANNED_STATUS_ID}",
        order_by="CreatedOn desc",
        limit=10
    )

    for o in planned_orders:
        invoice_num = o.get('BGInvoiceNumber')
        print(f"  Order {o.get('Number')} (Invoice: {invoice_num})")

        if invoice_num:
            # Check if this invoice exists in QBDownload
            qb_records = client.query(
                "BGQBDownload",
                filters=f"BGCleanInvoiceNumber eq {invoice_num}",
                limit=5
            )
            if qb_records:
                print(f"    -> Found in QBDownload: YES ({len(qb_records)} records)")
            else:
                print(f"    -> Found in QBDownload: NO")
        else:
            print(f"    -> No invoice number assigned")

    # 4. Check orders with NULL PaymentStatus and their QBDownload records
    print("\n4. Orders with NULL/Empty PaymentStatus - Check QBDownload records")
    print("-" * 50)

    null_orders = client.query(
        "Order",
        columns=["Id", "Number", "BGInvoiceNumber", "BGInvoiceDate", "PaymentStatusId"],
        filters="PaymentStatusId eq 00000000-0000-0000-0000-000000000000",
        order_by="CreatedOn desc",
        limit=10
    )

    for o in null_orders:
        invoice_num = o.get('BGInvoiceNumber')
        print(f"  Order {o.get('Number')} (Invoice: {invoice_num})")

        if invoice_num:
            qb_records = client.query(
                "BGQBDownload",
                filters=f"BGCleanInvoiceNumber eq {invoice_num}",
                limit=5
            )
            if qb_records:
                print(f"    -> Found in QBDownload: YES ({len(qb_records)} records)")
            else:
                print(f"    -> Found in QBDownload: NO")
        else:
            print(f"    -> No invoice number assigned")

    # 5. Check BGGetQBCommissions process
    print("\n5. GetQuickBooksCommissions Process Details")
    print("-" * 50)
    commission_procs = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId", "Description"],
        filters="contains(Name, 'Commission') and contains(Name, 'QB')",
        limit=10
    )
    for p in commission_procs:
        print(f"  {p.get('Name')}")
        print(f"    Caption: {p.get('Caption')}")
        if p.get('Description'):
            print(f"    Description: {p.get('Description')[:200]}")

    # 6. Check IWQBIntegration Order schema columns
    print("\n6. IWQBIntegration Order Schema - Added Columns")
    print("-" * 50)

    # Get schema ID for Order in IWQBIntegration
    iwqb_order = client.query(
        "SysSchema",
        columns=["Id", "Name", "ManagerName"],
        filters=f"Name eq 'Order' and SysPackageId eq {IWQB_PACKAGE_ID}"
    )
    if iwqb_order:
        schema_id = iwqb_order[0].get('Id')
        print(f"  IWQBIntegration Order Schema ID: {schema_id}")

        # Check for columns added by this schema
        # (This may not work if SysSchemaColumn isn't exposed)
        # Instead, check for IW-prefixed columns on Order entity
        orders = client.query("Order", limit=1)
        if orders:
            all_columns = list(orders[0].keys())
            iw_columns = [c for c in all_columns if c.startswith('IW') or 'Payment' in c]
            print(f"  IW-related columns on Order: {iw_columns}")
    else:
        print("  No Order schema found in IWQBIntegration")

    # 7. Check default PaymentStatus by examining Order section page
    print("\n7. Order Section Page Configuration")
    print("-" * 50)
    order_pages = client.query(
        "SysSchema",
        columns=["Id", "Name", "ManagerName", "SysPackageId"],
        filters="contains(Name, 'OrderPage') or contains(Name, 'Order1Page')",
        limit=10
    )
    for p in order_pages:
        pkg_id = p.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        print(f"  {p.get('Name')} ({p.get('ManagerName')}) - {pkg_name}")

    print("\n" + "=" * 70)
    print("Investigation complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
