#!/usr/bin/env python3
"""Investigate IWQBIntegration package for PaymentStatusId interference."""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

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
            print(f"Query error for {entity}: {resp.status_code} - {resp.text[:300]}")
            return []
        return resp.json().get("value", [])

def main():
    print("=" * 70)
    print("IWQBIntegration Package Investigation")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Get package info
    print("\n1. IWQBIntegration Package Details")
    print("-" * 50)
    packages = client.query(
        "SysPackage",
        filters=f"Id eq {IWQB_PACKAGE_ID}"
    )
    for pkg in packages:
        print(f"  Name: {pkg.get('Name')}")
        print(f"  Description: {pkg.get('Description')}")
        print(f"  ModifiedOn: {pkg.get('ModifiedOn')}")
        print(f"  IsLocked: {pkg.get('IsLocked')}")

    # 2. Get all schemas in this package
    print("\n2. Schemas in IWQBIntegration Package")
    print("-" * 50)
    schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "Caption", "ManagerName", "ModifiedOn"],
        filters=f"SysPackageId eq {IWQB_PACKAGE_ID}",
        order_by="Name"
    )
    for s in schemas:
        print(f"  {s.get('Name')} ({s.get('ManagerName')})")
        print(f"    Caption: {s.get('Caption')}")
        print(f"    Modified: {s.get('ModifiedOn')}")

    # 3. Check for Order-related schemas
    print("\n3. Order-Related Schemas in Package")
    print("-" * 50)
    order_schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "Caption", "ManagerName", "ParentId"],
        filters=f"SysPackageId eq {IWQB_PACKAGE_ID} and contains(Name, 'Order')"
    )
    for s in order_schemas:
        print(f"  {s.get('Name')}")
        print(f"    ManagerName: {s.get('ManagerName')}")
        print(f"    ParentId: {s.get('ParentId')}")

    # 4. Check for business processes in package
    print("\n4. Business Processes in IWQBIntegration")
    print("-" * 50)
    processes = client.query(
        "VwSysProcess",
        columns=["Id", "Name", "Caption", "IsActiveVersion", "SysPackageId"],
        filters=f"SysPackageId eq {IWQB_PACKAGE_ID}"
    )
    if processes:
        for p in processes:
            print(f"  {p.get('Name')}: {p.get('Caption')}")
            print(f"    Active: {p.get('IsActiveVersion')}")
    else:
        print("  No business processes found in this package")

    # 5. Check for entity event listeners
    print("\n5. Entity Event Listeners (SysEntitySchemaRecordDefValues)")
    print("-" * 50)
    # Check for default values on Order entity
    defaults = client.query(
        "SysEntitySchemaRecordDefValue",
        filters="contains(EntitySchemaColumnName, 'PaymentStatus') or contains(EntitySchemaName, 'Order')",
        limit=50
    )
    if defaults:
        for d in defaults:
            print(f"  Entity: {d.get('EntitySchemaName')}")
            print(f"    Column: {d.get('EntitySchemaColumnName')}")
            print(f"    Default: {d.get('DefValue')}")
    else:
        print("  No default value records found")

    # 6. Check SysModuleEntity for Order configuration
    print("\n6. Order Module Entity Configuration")
    print("-" * 50)
    modules = client.query(
        "SysModuleEntity",
        filters="contains(SysEntitySchemaName, 'Order') or contains(Name, 'Order')",
        limit=20
    )
    for m in modules:
        print(f"  {m.get('Name')}")
        for k, v in m.items():
            if v and not k.startswith('@') and k != 'Name':
                print(f"    {k}: {v}")

    # 7. Check all packages that extend Order
    print("\n7. All Packages Modifying Order Entity")
    print("-" * 50)
    order_extensions = client.query(
        "SysSchema",
        columns=["Id", "Name", "SysPackageId", "ModifiedOn", "ManagerName"],
        filters="Name eq 'Order'",
        limit=50
    )
    for ext in order_extensions:
        pkg_id = ext.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'unknown'
        print(f"  Package: {pkg_name}")
        print(f"    SchemaId: {ext.get('Id')}")
        print(f"    Manager: {ext.get('ManagerName')}")
        print(f"    Modified: {ext.get('ModifiedOn')}")
        print()

    # 8. Check for triggers or handlers
    print("\n8. Looking for PaymentStatus Default Value Sources")
    print("-" * 50)

    # Check PaymentStatus lookup values
    statuses = client.query(
        "PaymentStatus",
        columns=["Id", "Name", "Description"],
        limit=20
    )
    print("  Available Payment Statuses:")
    for s in statuses:
        print(f"    {s.get('Name')} -> {s.get('Id')}")

    # Find which status is "Planned"
    planned = client.query(
        "PaymentStatus",
        columns=["Id", "Name"],
        filters="Name eq 'Planned'"
    )
    if planned:
        planned_id = planned[0].get('Id')
        print(f"\n  'Planned' status ID: {planned_id}")

    print("\n" + "=" * 70)
    print("Investigation complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
