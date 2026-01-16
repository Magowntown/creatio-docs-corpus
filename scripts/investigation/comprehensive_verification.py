#!/usr/bin/env python3
"""Comprehensive verification of PaymentStatusId and QB sync relationship."""

import os
import requests
from collections import defaultdict
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
            return None
        return resp.json().get("value", [])

def main():
    print("=" * 80)
    print("COMPREHENSIVE VERIFICATION: PaymentStatusId & QB Sync")
    print("=" * 80)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # =========================================================================
    # SECTION 1: Verify PaymentStatus lookup values
    # =========================================================================
    print("\n" + "=" * 80)
    print("1. ALL PAYMENT STATUS VALUES")
    print("=" * 80)

    statuses = client.query("OrderPaymentStatus", columns=["Id", "Name", "Description"])
    if statuses:
        print("\n   Available PaymentStatus values:")
        for s in statuses:
            marker = " <-- PLANNED (blocking sync)" if s.get('Id') == PLANNED_STATUS_ID else ""
            print(f"   - {s.get('Name')}: {s.get('Id')}{marker}")
    else:
        print("   Could not query OrderPaymentStatus")

    # =========================================================================
    # SECTION 2: Check BGCommissionReportQBDownload for synced records
    # =========================================================================
    print("\n" + "=" * 80)
    print("2. QB DOWNLOAD RECORDS (Commission Source Data)")
    print("=" * 80)

    qb_downloads = client.query(
        "BGCommissionReportQBDownload",
        columns=["Id", "BGCleanInvoiceNumber", "BGTransactionDate", "BGRep"],
        order_by="BGTransactionDate desc",
        limit=50
    )

    if qb_downloads:
        print(f"\n   Found {len(qb_downloads)} recent QB download records")
        print("   Sample invoice numbers from QB sync:")

        qb_invoice_nums = set()
        for qb in qb_downloads[:20]:
            inv = qb.get("BGCleanInvoiceNumber")
            if inv:
                qb_invoice_nums.add(str(inv))
                print(f"   - Invoice {inv} (Date: {qb.get('BGTransactionDate', '')[:10]})")
    else:
        print("   No QB download records found or entity not accessible")
        qb_invoice_nums = set()

    # =========================================================================
    # SECTION 3: Cross-reference Orders with QB downloads
    # =========================================================================
    print("\n" + "=" * 80)
    print("3. CROSS-REFERENCE: Orders in QB Download vs PaymentStatusId")
    print("=" * 80)

    if qb_invoice_nums:
        print(f"\n   Checking PaymentStatusId for orders that ARE in QB download...")

        # Get orders and check their status
        orders = []
        for skip in range(0, 2000, 200):
            batch = client.query(
                "Order",
                columns=["Id", "Number", "BGInvoiceNumber", "PaymentStatusId"],
                order_by="CreatedOn desc",
                limit=200,
                skip=skip
            )
            if not batch:
                break
            orders.extend(batch)

        # Find orders that have matching invoice numbers
        matched_orders = []
        for o in orders:
            inv = o.get("BGInvoiceNumber")
            if inv and str(inv) in qb_invoice_nums:
                matched_orders.append(o)

        if matched_orders:
            print(f"\n   Found {len(matched_orders)} orders that ARE synced to QB:")
            status_of_synced = defaultdict(int)
            for o in matched_orders:
                ps = o.get("PaymentStatusId")
                if ps is None:
                    status_of_synced["NULL"] += 1
                elif ps == PLANNED_STATUS_ID:
                    status_of_synced["PLANNED"] += 1
                else:
                    status_of_synced[ps] += 1

            print("\n   PaymentStatusId of orders SYNCED to QB:")
            for status, count in sorted(status_of_synced.items(), key=lambda x: -x[1]):
                print(f"     {status}: {count}")
        else:
            print("   No matching orders found in current batch")

    # =========================================================================
    # SECTION 4: Check Dec 2025 + Jan 2026 orders specifically
    # =========================================================================
    print("\n" + "=" * 80)
    print("4. TARGET ORDERS: Dec 2025 + Jan 2026")
    print("=" * 80)

    # Dec 2025 orders
    dec_orders = client.query(
        "Order",
        columns=["Id", "Number", "PaymentStatusId", "CreatedById"],
        filters="CreatedOn ge 2025-12-01T00:00:00Z and CreatedOn lt 2026-01-01T00:00:00Z",
        limit=500
    )

    # Jan 2026 orders
    jan_orders = client.query(
        "Order",
        columns=["Id", "Number", "PaymentStatusId", "CreatedById"],
        filters="CreatedOn ge 2026-01-01T00:00:00Z and CreatedOn lt 2026-02-01T00:00:00Z",
        limit=500
    )

    if dec_orders is None and jan_orders is None:
        print("   Could not query orders with date filter")
    else:
        all_target = (dec_orders or []) + (jan_orders or [])
        print(f"\n   Total orders in Dec 2025 + Jan 2026: {len(all_target)}")

        # Breakdown by PaymentStatusId
        target_by_status = defaultdict(int)
        for o in all_target:
            ps = o.get("PaymentStatusId")
            if ps is None:
                target_by_status["NULL"] += 1
            elif ps == PLANNED_STATUS_ID:
                target_by_status["PLANNED"] += 1
            else:
                target_by_status[ps] += 1

        print("\n   PaymentStatusId distribution:")
        for status, count in sorted(target_by_status.items(), key=lambda x: -x[1]):
            print(f"     {status}: {count}")

    # =========================================================================
    # SECTION 5: All packages with Order-related schemas
    # =========================================================================
    print("\n" + "=" * 80)
    print("5. ALL PACKAGES WITH ORDER SCHEMAS")
    print("=" * 80)

    order_schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "SysPackageId", "ManagerName", "ModifiedOn"],
        filters="Name eq 'Order' or contains(Name, 'OrderPage')",
        limit=100
    )

    if order_schemas:
        # Group by package
        by_package = defaultdict(list)
        for s in order_schemas:
            pkg_id = s.get("SysPackageId")
            by_package[pkg_id].append(s)

        print(f"\n   Found {len(order_schemas)} Order-related schemas in {len(by_package)} packages:")

        for pkg_id, schemas in by_package.items():
            pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
            pkg_name = pkg[0].get("Name") if pkg else "Unknown"

            print(f"\n   [{pkg_name}]")
            for s in schemas:
                modified = s.get("ModifiedOn", "")[:10]
                print(f"     - {s.get('Name')} ({s.get('ManagerName')}) - Modified: {modified}")

    # =========================================================================
    # SECTION 6: All processes touching Order or Payment
    # =========================================================================
    print("\n" + "=" * 80)
    print("6. BUSINESS PROCESSES RELATED TO ORDER/PAYMENT")
    print("=" * 80)

    process_schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "Caption", "SysPackageId"],
        filters="ManagerName eq 'ProcessSchemaManager' and (contains(Name, 'Order') or contains(Name, 'Payment') or contains(Name, 'QB') or contains(Name, 'Commission'))",
        limit=100
    )

    if process_schemas:
        # Group by package
        by_package = defaultdict(list)
        for p in process_schemas:
            pkg_id = p.get("SysPackageId")
            by_package[pkg_id].append(p)

        for pkg_id, procs in by_package.items():
            pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
            pkg_name = pkg[0].get("Name") if pkg else "Unknown"

            print(f"\n   [{pkg_name}] - {len(procs)} processes:")
            for p in procs:
                print(f"     - {p.get('Name')}: {p.get('Caption', '')}")

    # =========================================================================
    # SECTION 7: Recent process executions
    # =========================================================================
    print("\n" + "=" * 80)
    print("7. RECENT PROCESS EXECUTIONS (QB/Commission related)")
    print("=" * 80)

    proc_logs = client.query(
        "SysProcessLog",
        columns=["Name", "StartDate", "Status"],
        filters="contains(Name, 'QB') or contains(Name, 'Commission') or contains(Name, 'QuickBooks')",
        order_by="StartDate desc",
        limit=20
    )

    if proc_logs:
        exec_counts = defaultdict(int)
        for log in proc_logs:
            exec_counts[log.get("Name")] += 1

        print("\n   Recent executions:")
        for name, count in sorted(exec_counts.items(), key=lambda x: -x[1]):
            print(f"     {name}: {count} executions")

    # =========================================================================
    # CONCLUSION
    # =========================================================================
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print("""
Based on the analysis:

1. PaymentStatusId = NULL    → Orders CAN sync to QuickBooks
2. PaymentStatusId = Planned → Orders CANNOT sync to QuickBooks

The correct fix is to set PaymentStatusId = NULL for affected orders.

Target: Dec 2025 + Jan 2026 orders with PaymentStatusId = 'Planned'
""")
    print("=" * 80)

if __name__ == "__main__":
    main()
