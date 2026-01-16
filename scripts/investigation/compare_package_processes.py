#!/usr/bin/env python3
"""Compare automation processes across all packages that extend Order entity."""

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

# Known package IDs from previous investigation
PACKAGES = {
    "IWQBIntegration": "5af0c9b0-141b-4d3f-828e-a455a1705aed",
    "PampaBayQuickBooks": None,  # Will discover
    "PampaBay": None,
    "Custom": None,
    "IWInterWeavePaymentApp": None,
}

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
            return []
        return resp.json().get("value", [])

def main():
    print("=" * 80)
    print("PACKAGE PROCESS COMPARISON - Order Entity Automation")
    print("=" * 80)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Get all packages that have Order schema
    print("\n" + "=" * 80)
    print("1. PACKAGES EXTENDING ORDER ENTITY")
    print("=" * 80)

    order_schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "SysPackageId", "ModifiedOn", "ManagerName"],
        filters="Name eq 'Order'",
        limit=50
    )

    package_ids = {}
    for schema in order_schemas:
        pkg_id = schema.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name", "Description"], filters=f"Id eq {pkg_id}")
        if pkg:
            pkg_name = pkg[0].get('Name')
            package_ids[pkg_name] = pkg_id
            print(f"\n  [{pkg_name}]")
            print(f"    Package ID: {pkg_id}")
            print(f"    Schema Modified: {schema.get('ModifiedOn')}")
            print(f"    Manager: {schema.get('ManagerName')}")

    # 2. Get ALL business processes and group by package
    print("\n" + "=" * 80)
    print("2. ALL BUSINESS PROCESSES BY PACKAGE")
    print("=" * 80)

    all_processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId", "Enabled"],
        limit=500
    )

    # Group by package
    processes_by_package = {}
    for proc in all_processes:
        pkg_id = proc.get('SysPackageId')
        if pkg_id not in processes_by_package:
            processes_by_package[pkg_id] = []
        processes_by_package[pkg_id].append(proc)

    # Show processes for packages that extend Order
    for pkg_name, pkg_id in package_ids.items():
        procs = processes_by_package.get(pkg_id, [])
        if procs:
            print(f"\n  [{pkg_name}] - {len(procs)} processes")
            print("-" * 60)
            for p in sorted(procs, key=lambda x: x.get('Name', '')):
                enabled = "✓" if p.get('Enabled', True) else "✗"
                print(f"    {enabled} {p.get('Name')}")
                if p.get('Caption'):
                    print(f"        Caption: {p.get('Caption')}")

    # 3. Focus on QuickBooks-related processes
    print("\n" + "=" * 80)
    print("3. QUICKBOOKS INTEGRATION PROCESSES (All Packages)")
    print("=" * 80)

    qb_processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId", "Enabled"],
        filters="contains(Name, 'QB') or contains(Name, 'QuickBooks') or contains(Caption, 'QuickBooks')",
        limit=100
    )

    for proc in sorted(qb_processes, key=lambda x: x.get('Name', '')):
        pkg_id = proc.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        enabled = "✓ ENABLED" if proc.get('Enabled', True) else "✗ DISABLED"
        print(f"\n  {proc.get('Name')} [{pkg_name}]")
        print(f"    Caption: {proc.get('Caption')}")
        print(f"    Status: {enabled}")

    # 4. Focus on Commission-related processes
    print("\n" + "=" * 80)
    print("4. COMMISSION PROCESSES (All Packages)")
    print("=" * 80)

    commission_processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId", "Enabled"],
        filters="contains(Name, 'Commission') or contains(Caption, 'Commission')",
        limit=100
    )

    for proc in sorted(commission_processes, key=lambda x: x.get('Name', '')):
        pkg_id = proc.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        enabled = "✓ ENABLED" if proc.get('Enabled', True) else "✗ DISABLED"
        print(f"\n  {proc.get('Name')} [{pkg_name}]")
        print(f"    Caption: {proc.get('Caption')}")
        print(f"    Status: {enabled}")

    # 5. Focus on Order-triggered processes
    print("\n" + "=" * 80)
    print("5. ORDER-RELATED PROCESSES (All Packages)")
    print("=" * 80)

    order_processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId", "Enabled"],
        filters="contains(Name, 'Order') or contains(Caption, 'Order')",
        limit=100
    )

    for proc in sorted(order_processes, key=lambda x: x.get('Name', '')):
        pkg_id = proc.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        enabled = "✓ ENABLED" if proc.get('Enabled', True) else "✗ DISABLED"
        print(f"\n  {proc.get('Name')} [{pkg_name}]")
        print(f"    Caption: {proc.get('Caption')}")
        print(f"    Status: {enabled}")

    # 6. Focus on Payment-related processes
    print("\n" + "=" * 80)
    print("6. PAYMENT STATUS PROCESSES (All Packages)")
    print("=" * 80)

    payment_processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId", "Enabled"],
        filters="contains(Name, 'Payment') or contains(Caption, 'Payment')",
        limit=100
    )

    for proc in sorted(payment_processes, key=lambda x: x.get('Name', '')):
        pkg_id = proc.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        enabled = "✓ ENABLED" if proc.get('Enabled', True) else "✗ DISABLED"
        print(f"\n  {proc.get('Name')} [{pkg_name}]")
        print(f"    Caption: {proc.get('Caption')}")
        print(f"    Status: {enabled}")

    # 7. Check for entity event handlers / signal processes
    print("\n" + "=" * 80)
    print("7. PROCESS START SIGNALS (Triggers)")
    print("=" * 80)

    # Try to find process start events
    try:
        start_signals = client.query(
            "VwSysProcessStartEvent",
            columns=["ProcessSchemaName", "RecordSchemaName", "SignalType"],
            filters="RecordSchemaName eq 'Order'",
            limit=50
        )
        if start_signals:
            print("\n  Processes triggered by Order events:")
            for sig in start_signals:
                print(f"    {sig.get('ProcessSchemaName')} - Signal: {sig.get('SignalType')}")
        else:
            print("  No Order signal events found (or view not accessible)")
    except:
        print("  VwSysProcessStartEvent not accessible")

    # 8. Compare IWQBIntegration vs PampaBayQuickBooks
    print("\n" + "=" * 80)
    print("8. DIRECT COMPARISON: IWQBIntegration vs PampaBayQuickBooks")
    print("=" * 80)

    iwqb_id = package_ids.get("IWQBIntegration")
    pbqb_id = package_ids.get("PampaBayQuickBooks")

    if iwqb_id:
        iwqb_procs = processes_by_package.get(iwqb_id, [])
        print(f"\n  IWQBIntegration ({len(iwqb_procs)} processes):")
        for p in sorted(iwqb_procs, key=lambda x: x.get('Name', '')):
            print(f"    - {p.get('Name')}: {p.get('Caption')}")

    if pbqb_id:
        pbqb_procs = processes_by_package.get(pbqb_id, [])
        print(f"\n  PampaBayQuickBooks ({len(pbqb_procs)} processes):")
        for p in sorted(pbqb_procs, key=lambda x: x.get('Name', '')):
            print(f"    - {p.get('Name')}: {p.get('Caption')}")

    # 9. Look for potential conflicts
    print("\n" + "=" * 80)
    print("9. POTENTIAL CONFLICTS ANALYSIS")
    print("=" * 80)

    # Find processes with similar names across packages
    all_names = {}
    for proc in all_processes:
        name = proc.get('Name', '')
        pkg_id = proc.get('SysPackageId')
        if name not in all_names:
            all_names[name] = []
        all_names[name].append(pkg_id)

    # Check for duplicate/similar process names
    print("\n  Checking for duplicate process names across packages...")
    duplicates_found = False
    for name, pkg_ids in all_names.items():
        if len(pkg_ids) > 1:
            duplicates_found = True
            print(f"\n  DUPLICATE: {name}")
            for pid in pkg_ids:
                pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pid}")
                pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
                print(f"    - Found in: {pkg_name}")

    if not duplicates_found:
        print("  No duplicate process names found across packages")

    # 10. Check for IW processes that might set PaymentStatus
    print("\n" + "=" * 80)
    print("10. IW PROCESSES THAT MIGHT SET PAYMENTSTATUS")
    print("=" * 80)

    iw_all = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "SysPackageId", "Enabled"],
        filters="contains(Name, 'IW') or startswith(Name, 'IW')",
        limit=100
    )

    for proc in sorted(iw_all, key=lambda x: x.get('Name', '')):
        pkg_id = proc.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        enabled = "✓" if proc.get('Enabled', True) else "✗"
        print(f"\n  {enabled} {proc.get('Name')} [{pkg_name}]")
        print(f"      {proc.get('Caption')}")

    print("\n" + "=" * 80)
    print("COMPARISON COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
