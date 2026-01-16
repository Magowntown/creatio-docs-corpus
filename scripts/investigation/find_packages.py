#!/usr/bin/env python3
"""
Find available packages in Creatio
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

def login(session):
    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    response = session.post(login_url, json={"UserName": USERNAME, "UserPassword": PASSWORD})
    return response.status_code == 200

def get_packages(session):
    """Get all packages"""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Simple query to get all packages
    query = {
        "RootSchemaName": "SysPackage",
        "OperationType": 0,
        "AllColumns": True,
        "RowCount": 20
    }

    response = session.post(url, json=query, headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data.get("rows"):
            print(f"\nFound {len(data['rows'])} packages:")
            for row in data["rows"][:20]:
                print(f"  - Name: {row.get('Name', 'N/A')}, UId: {row.get('UId', 'N/A')}, Maintainer: {row.get('Maintainer', 'N/A')}")
            return data["rows"]
    else:
        print(f"Error: {response.text[:500]}")
    return []

def main():
    session = requests.Session()

    print("Logging in...")
    if not login(session):
        print("Login failed")
        return

    print("Login successful!\n")
    packages = get_packages(session)

    # Filter for customer packages
    print("\nCustomer packages:")
    for pkg in packages:
        maintainer = pkg.get('Maintainer', '')
        if maintainer and 'Customer' in maintainer:
            print(f"  - {pkg.get('Name')}: {pkg.get('UId')}")

if __name__ == "__main__":
    main()
