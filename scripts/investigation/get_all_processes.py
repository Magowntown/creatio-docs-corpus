#!/usr/bin/env python3
"""Get all processes without filters to understand schema."""

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

    def query_raw(self, entity, params=None):
        url = f"{self.base_url}/0/odata/{entity}"
        resp = self.session.get(url, params=params or {})
        print(f"  Query {entity}: {resp.status_code}")
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"    Error: {resp.text[:200]}")
            return None

def main():
    print("=" * 70)
    print("Process Schema Investigation")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Try VwSysProcess without filters
    print("\n1. VwSysProcess (no filters, top 5)")
    result = client.query_raw("VwSysProcess", {"$top": "5"})
    if result and result.get("value"):
        print(f"  Found {len(result.get('value'))} records")
        for proc in result.get("value", []):
            print(f"    Keys: {list(proc.keys())[:10]}...")
            break
    else:
        print("  No data or error")

    # 2. Try SysProcessLog for recent activity
    print("\n2. SysProcessLog (recent, top 20)")
    result = client.query_raw("SysProcessLog", {
        "$top": "20",
        "$orderby": "StartDate desc",
        "$select": "Id,Name,StartDate,Status"
    })
    if result and result.get("value"):
        print(f"  Found {len(result.get('value'))} records")
        for log in result.get("value", []):
            print(f"    {log.get('Name')} - {log.get('StartDate', '')[:19]}")

    # 3. Try SysSchema for process schemas
    print("\n3. SysSchema (ProcessSchemaManager)")
    result = client.query_raw("SysSchema", {
        "$top": "50",
        "$filter": "ManagerName eq 'ProcessSchemaManager'",
        "$select": "Id,Name,Caption,SysPackageId",
        "$orderby": "Name"
    })
    if result and result.get("value"):
        print(f"  Found {len(result.get('value'))} process schemas")

        # Group by package
        by_package = {}
        for schema in result.get("value", []):
            pkg_id = schema.get("SysPackageId")
            if pkg_id not in by_package:
                by_package[pkg_id] = []
            by_package[pkg_id].append(schema)

        # Look up package names and display
        for pkg_id, schemas in by_package.items():
            pkg_result = client.query_raw("SysPackage", {
                "$filter": f"Id eq {pkg_id}",
                "$select": "Name"
            })
            pkg_name = "Unknown"
            if pkg_result and pkg_result.get("value"):
                pkg_name = pkg_result["value"][0].get("Name", "Unknown")

            print(f"\n  [{pkg_name}] - {len(schemas)} processes")
            for s in schemas[:10]:  # Show first 10
                print(f"    - {s.get('Name')}: {s.get('Caption', '')}")
            if len(schemas) > 10:
                print(f"    ... and {len(schemas) - 10} more")

    # 4. Specifically look for IW and QB processes
    print("\n4. Process Schemas containing 'IW' or 'QB'")
    result = client.query_raw("SysSchema", {
        "$top": "100",
        "$filter": "ManagerName eq 'ProcessSchemaManager' and (contains(Name, 'IW') or contains(Name, 'QB') or contains(Name, 'QuickBooks'))",
        "$select": "Id,Name,Caption,SysPackageId"
    })
    if result and result.get("value"):
        for schema in result.get("value", []):
            pkg_id = schema.get("SysPackageId")
            pkg_result = client.query_raw("SysPackage", {
                "$filter": f"Id eq {pkg_id}",
                "$select": "Name"
            })
            pkg_name = pkg_result["value"][0].get("Name") if pkg_result and pkg_result.get("value") else "Unknown"
            print(f"    {schema.get('Name')} [{pkg_name}]")
            print(f"      Caption: {schema.get('Caption', 'N/A')}")

    # 5. Look for Commission and Payment processes
    print("\n5. Process Schemas containing 'Commission' or 'Payment'")
    result = client.query_raw("SysSchema", {
        "$top": "100",
        "$filter": "ManagerName eq 'ProcessSchemaManager' and (contains(Name, 'Commission') or contains(Name, 'Payment'))",
        "$select": "Id,Name,Caption,SysPackageId"
    })
    if result and result.get("value"):
        for schema in result.get("value", []):
            pkg_id = schema.get("SysPackageId")
            pkg_result = client.query_raw("SysPackage", {
                "$filter": f"Id eq {pkg_id}",
                "$select": "Name"
            })
            pkg_name = pkg_result["value"][0].get("Name") if pkg_result and pkg_result.get("value") else "Unknown"
            print(f"    {schema.get('Name')} [{pkg_name}]")
            print(f"      Caption: {schema.get('Caption', 'N/A')}")

    # 6. Look for Order-related processes
    print("\n6. Process Schemas containing 'Order'")
    result = client.query_raw("SysSchema", {
        "$top": "100",
        "$filter": "ManagerName eq 'ProcessSchemaManager' and contains(Name, 'Order')",
        "$select": "Id,Name,Caption,SysPackageId"
    })
    if result and result.get("value"):
        for schema in result.get("value", []):
            pkg_id = schema.get("SysPackageId")
            pkg_result = client.query_raw("SysPackage", {
                "$filter": f"Id eq {pkg_id}",
                "$select": "Name"
            })
            pkg_name = pkg_result["value"][0].get("Name") if pkg_result and pkg_result.get("value") else "Unknown"
            print(f"    {schema.get('Name')} [{pkg_name}]")

    print("\n" + "=" * 70)
    print("Investigation complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
