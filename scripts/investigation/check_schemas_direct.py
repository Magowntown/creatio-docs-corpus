#!/usr/bin/env python3
"""
Direct API check for UsrPage_ebkv9e8 schemas
"""

import os
import requests

def check_environment(name, url, username, password):
    print(f"\n{'='*60}")
    print(f"CHECKING: {name}")
    print(f"{'='*60}")

    session = requests.Session()

    # Login
    login_url = f"{url}/ServiceModel/AuthService.svc/Login"
    payload = {"UserName": username, "UserPassword": password}

    try:
        resp = session.post(login_url, json=payload, timeout=30)
        print(f"Login response: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Login code: {data.get('Code')}")
            if data.get("Code") != 0:
                print(f"Login failed: {data.get('Message')}")
                return
        else:
            print(f"Login HTTP error: {resp.text[:200]}")
            return
    except Exception as e:
        print(f"Login exception: {e}")
        return

    bpmcsrf = session.cookies.get("BPMCSRF")
    headers = {"Content-Type": "application/json", "BPMCSRF": bpmcsrf}

    # Query schemas with Name containing 'UsrPage'
    print("\nQuerying schemas...")
    query_url = f"{url}/0/odata/SysSchema?$filter=contains(Name,'UsrPage_ebkv9e8')&$select=Id,UId,Name,SysPackageId,ExtendParent,ManagerName,ModifiedOn&$orderby=ModifiedOn desc"

    try:
        resp = session.get(query_url, headers=headers, timeout=60)
        print(f"Query response: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            schemas = data.get("value", [])
            print(f"Found {len(schemas)} schemas")

            for s in schemas:
                print(f"\n  Name: {s.get('Name')}")
                print(f"  UId: {s.get('UId')}")
                print(f"  PackageId: {s.get('SysPackageId')}")
                print(f"  ExtendParent: {s.get('ExtendParent')}")
                print(f"  Manager: {s.get('ManagerName')}")
                print(f"  Modified: {s.get('ModifiedOn')}")

                # Get package name
                pkg_id = s.get('SysPackageId')
                if pkg_id:
                    pkg_url = f"{url}/0/odata/SysPackage({pkg_id})?$select=Name"
                    pkg_resp = session.get(pkg_url, headers=headers, timeout=30)
                    if pkg_resp.status_code == 200:
                        pkg_data = pkg_resp.json()
                        print(f"  Package: {pkg_data.get('Name')}")
        else:
            print(f"Query failed: {resp.text[:500]}")
    except Exception as e:
        print(f"Query exception: {e}")

    # Query business rules
    print("\nQuerying business rules...")
    br_url = f"{url}/0/odata/SysSchema?$filter=contains(Name,'BGUsrPage')&$select=Id,UId,Name,SysPackageId,ManagerName,ModifiedOn"

    try:
        resp = session.get(br_url, headers=headers, timeout=60)
        print(f"BR query response: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            rules = data.get("value", [])
            print(f"Found {len(rules)} business rules")

            for r in rules:
                print(f"\n  Name: {r.get('Name')}")
                print(f"  UId: {r.get('UId')}")
                print(f"  Modified: {r.get('ModifiedOn')}")

                pkg_id = r.get('SysPackageId')
                if pkg_id:
                    pkg_url = f"{url}/0/odata/SysPackage({pkg_id})?$select=Name"
                    pkg_resp = session.get(pkg_url, headers=headers, timeout=30)
                    if pkg_resp.status_code == 200:
                        pkg_data = pkg_resp.json()
                        print(f"  Package: {pkg_data.get('Name')}")
        else:
            print(f"BR query failed: {resp.text[:500]}")
    except Exception as e:
        print(f"BR query exception: {e}")


# Run checks
print("=" * 70)
print("UsrPage_ebkv9e8 SCHEMA INVESTIGATION")
print("=" * 70)

check_environment(
    "DEV",
    "https://dev-pampabay.creatio.com",
    "Supervisor",
    "BayPampa3002!"
)

check_environment(
    "PROD",
    "https://pampabay.creatio.com",
    "Supervisor",
    "123*Pampa?"
)
