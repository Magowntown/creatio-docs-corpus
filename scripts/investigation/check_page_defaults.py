#!/usr/bin/env python3
"""Check OrderPageV2 schemas for default values."""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

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
    print("ORDER PAGE SCHEMA ANALYSIS")
    print("=" * 80)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Get all OrderPageV2 schemas
    print("\n" + "=" * 80)
    print("1. ALL ORDER PAGE SCHEMAS")
    print("=" * 80)

    order_pages = client.query(
        "SysSchema",
        columns=["Id", "Name", "Caption", "SysPackageId", "ModifiedOn", "ManagerName"],
        filters="contains(Name, 'OrderPage')",
        order_by="ModifiedOn desc",
        limit=50
    )

    for page in order_pages:
        pkg_id = page.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        print(f"\n  {page.get('Name')} [{pkg_name}]")
        print(f"    Manager: {page.get('ManagerName')}")
        print(f"    Modified: {page.get('ModifiedOn')}")
        print(f"    Schema ID: {page.get('Id')}")

    # 2. Look for BaseOrderPage schemas
    print("\n" + "=" * 80)
    print("2. BASE ORDER PAGE SCHEMAS")
    print("=" * 80)

    base_pages = client.query(
        "SysSchema",
        columns=["Id", "Name", "SysPackageId", "ModifiedOn"],
        filters="contains(Name, 'BaseOrderPage')",
        limit=20
    )

    for page in base_pages:
        pkg_id = page.get('SysPackageId')
        pkg = client.query("SysPackage", columns=["Name"], filters=f"Id eq {pkg_id}")
        pkg_name = pkg[0].get('Name') if pkg else 'Unknown'
        print(f"  {page.get('Name')} [{pkg_name}]")
        print(f"    Modified: {page.get('ModifiedOn')}")

    # 3. Check for SysEntitySchemaDefValue or similar
    print("\n" + "=" * 80)
    print("3. LOOKING FOR DEFAULT VALUE CONFIGURATIONS")
    print("=" * 80)

    # Try different approaches to find default values
    entities_to_try = [
        "SysEntitySchemaDefValue",
        "SysEntitySchemaRecordDefValue",
        "SysLookupColumnValue",
        "SysModuleEntityInStage",
    ]

    for entity in entities_to_try:
        result = client.query(entity, limit=5)
        if result:
            print(f"\n  {entity}: Found data")
            print(f"    Columns: {list(result[0].keys())[:8]}...")
        else:
            print(f"\n  {entity}: Not accessible or empty")

    # 4. Check SysModuleLookup for default values
    print("\n" + "=" * 80)
    print("4. SysModuleLookup - ORDER RELATED")
    print("=" * 80)

    lookups = client.query(
        "SysModuleLookup",
        limit=50
    )

    if lookups:
        for lookup in lookups:
            name = str(lookup.get('Name', ''))
            if 'Order' in name or 'Payment' in name:
                print(f"  {name}")
                for k, v in lookup.items():
                    if v and not k.startswith('@'):
                        print(f"    {k}: {v}")

    # 5. Check SysLookup for PaymentStatus
    print("\n" + "=" * 80)
    print("5. SysLookup - PAYMENT STATUS")
    print("=" * 80)

    sys_lookups = client.query(
        "SysLookup",
        filters="contains(Name, 'Payment') or contains(Name, 'Order')",
        limit=30
    )

    for lookup in sys_lookups:
        print(f"  {lookup.get('Name')}")
        for k, v in lookup.items():
            if v and not k.startswith('@') and k != 'Name':
                print(f"    {k}: {v}")

    # 6. Check for entity default value schemas in IWQBIntegration
    print("\n" + "=" * 80)
    print("6. IWQBIntegration SCHEMAS (Client/Entity)")
    print("=" * 80)

    iwqb_pkg_id = "5af0c9b0-141b-4d3f-828e-a455a1705aed"
    iwqb_schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "Caption", "ManagerName", "ModifiedOn"],
        filters=f"SysPackageId eq {iwqb_pkg_id}",
        order_by="Name",
        limit=100
    )

    # Group by manager
    by_manager = {}
    for s in iwqb_schemas:
        manager = s.get('ManagerName', 'Unknown')
        if manager not in by_manager:
            by_manager[manager] = []
        by_manager[manager].append(s)

    for manager, schemas in sorted(by_manager.items()):
        print(f"\n  {manager} ({len(schemas)} schemas):")
        for s in schemas[:15]:
            print(f"    - {s.get('Name')}: {s.get('Caption', '')}")
        if len(schemas) > 15:
            print(f"    ... and {len(schemas) - 15} more")

    # 7. Compare with PampaBayQuickBooks schemas
    print("\n" + "=" * 80)
    print("7. PampaBayQuickBooks SCHEMAS (Client/Entity)")
    print("=" * 80)

    pbqb_pkg_id = "f63b797a-cff7-4fdc-9c73-000676e1d209"
    pbqb_schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "Caption", "ManagerName"],
        filters=f"SysPackageId eq {pbqb_pkg_id}",
        order_by="Name",
        limit=100
    )

    by_manager = {}
    for s in pbqb_schemas:
        manager = s.get('ManagerName', 'Unknown')
        if manager not in by_manager:
            by_manager[manager] = []
        by_manager[manager].append(s)

    for manager, schemas in sorted(by_manager.items()):
        print(f"\n  {manager} ({len(schemas)} schemas):")
        for s in schemas[:15]:
            print(f"    - {s.get('Name')}: {s.get('Caption', '')}")
        if len(schemas) > 15:
            print(f"    ... and {len(schemas) - 15} more")

    # 8. Check Custom package for any Order defaults
    print("\n" + "=" * 80)
    print("8. CUSTOM PACKAGE ORDER SCHEMAS")
    print("=" * 80)

    custom_pkg_id = "af2b71ef-e323-410f-9017-8059bfda38c8"
    custom_schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "Caption", "ManagerName"],
        filters=f"SysPackageId eq {custom_pkg_id} and contains(Name, 'Order')",
        limit=50
    )

    for s in custom_schemas:
        print(f"  {s.get('Name')} ({s.get('ManagerName')})")
        print(f"    Caption: {s.get('Caption', 'N/A')}")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
