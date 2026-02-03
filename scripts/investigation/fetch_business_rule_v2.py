#!/usr/bin/env python3
"""
Deep search for BGUsrPage_ebkv9e8BusinessRule - check by UId and Custom package.
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class CreatioClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.bpmcsrf = None

    def login(self):
        login_url = f"{self.base_url}/ServiceModel/AuthService.svc/Login"
        payload = {"UserName": self.username, "UserPassword": self.password}
        resp = self.session.post(login_url, json=payload)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("Code") == 0:
                self.bpmcsrf = self.session.cookies.get("BPMCSRF")
                return True
        return False

    def odata_query(self, entity, params=""):
        url = f"{self.base_url}/0/odata/{entity}"
        if params:
            url += f"?{params}"
        headers = {"Content-Type": "application/json"}
        if self.bpmcsrf:
            headers["BPMCSRF"] = self.bpmcsrf
        resp = self.session.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        return None


def main():
    prod_url = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
    prod_user = os.getenv("CREATIO_PROD_USERNAME")
    prod_pass = os.getenv("CREATIO_PROD_PASSWORD")

    client = CreatioClient(prod_url, prod_user, prod_pass)
    if not client.login():
        print("Login failed!")
        sys.exit(1)
    print(f"Connected to: {prod_url}\n")

    # Search 1: By specific UIds
    print("=" * 70)
    print("SEARCH 1: By Specific UIds")
    print("=" * 70)

    uids = [
        ("60ed3410-ca3e-4423-9cf5-8cc0ccc616b2", "BGApp_eykaguu (Original - documented)"),
        ("e42d1bec-59a1-46d1-968b-8efd41a0afe6", "Custom (Duplicate - documented)"),
    ]

    for uid, description in uids:
        print(f"\nSearching for UId: {uid}")
        print(f"  Expected: {description}")
        query = f"$filter=UId eq {uid}&$select=Id,UId,Name,SysPackageId,ManagerName,ModifiedOn"
        data = client.odata_query("SysSchema", query)
        if data and data.get("value"):
            for s in data["value"]:
                pkg_id = s.get("SysPackageId")
                pkg_name = "Unknown"
                if pkg_id:
                    pkg_query = f"$filter=Id eq {pkg_id}&$select=Name"
                    pkg_data = client.odata_query("SysPackage", pkg_query)
                    if pkg_data and pkg_data.get("value"):
                        pkg_name = pkg_data["value"][0].get("Name")
                print(f"  ✅ FOUND: {s.get('Name')} in {pkg_name}")
                print(f"     Modified: {s.get('ModifiedOn', '')[:19]}")
        else:
            print(f"  ❌ NOT FOUND")

    # Search 2: All AddonSchemaManager schemas (business rules)
    print("\n" + "=" * 70)
    print("SEARCH 2: All AddonSchemaManager Schemas (Business Rules)")
    print("=" * 70)

    query = "$filter=ManagerName eq 'AddonSchemaManager'&$select=Id,UId,Name,SysPackageId,ModifiedOn&$orderby=ModifiedOn desc&$top=20"
    data = client.odata_query("SysSchema", query)

    if data and data.get("value"):
        print(f"Found {len(data['value'])} business rule(s):\n")
        for s in data["value"]:
            pkg_id = s.get("SysPackageId")
            pkg_name = "Unknown"
            if pkg_id:
                pkg_query = f"$filter=Id eq {pkg_id}&$select=Name"
                pkg_data = client.odata_query("SysPackage", pkg_query)
                if pkg_data and pkg_data.get("value"):
                    pkg_name = pkg_data["value"][0].get("Name")
            name = s.get("Name", "")
            modified = s.get("ModifiedOn", "")[:19]
            highlight = " 🔴 REPORTS PAGE" if "ebkv9e8" in name else ""
            print(f"  {name:<50} | {pkg_name:<20} | {modified}{highlight}")

    # Search 3: Find Custom package and list all its schemas
    print("\n" + "=" * 70)
    print("SEARCH 3: All Schemas in Custom Package")
    print("=" * 70)

    pkg_query = "$filter=Name eq 'Custom'&$select=Id,Name,UId"
    pkg_data = client.odata_query("SysPackage", pkg_query)

    if pkg_data and pkg_data.get("value"):
        custom_pkg = pkg_data["value"][0]
        custom_pkg_id = custom_pkg.get("Id")
        print(f"Custom Package ID: {custom_pkg_id}\n")

        # Get all schemas in Custom package
        schema_query = f"$filter=SysPackageId eq {custom_pkg_id}&$select=Id,UId,Name,ManagerName,ModifiedOn&$orderby=ModifiedOn desc"
        schema_data = client.odata_query("SysSchema", schema_query)

        if schema_data and schema_data.get("value"):
            print(f"Found {len(schema_data['value'])} schema(s) in Custom package:\n")
            for s in schema_data["value"]:
                name = s.get("Name", "")
                manager = s.get("ManagerName", "")
                modified = s.get("ModifiedOn", "")[:19]
                uid = s.get("UId", "")
                highlight = " 🔴 BUSINESS RULE" if "BusinessRule" in name else ""
                highlight = highlight or (" 🔴 ADDON" if "Addon" in manager else "")
                print(f"  {name:<40} | {manager:<25} | {modified}{highlight}")
        else:
            print("No schemas found in Custom package")
    else:
        print("Custom package not found!")

    # Search 4: Search for UsrPage_ebkv9e8 related schemas
    print("\n" + "=" * 70)
    print("SEARCH 4: All UsrPage_ebkv9e8 Related Schemas")
    print("=" * 70)

    query = "$filter=contains(Name,'UsrPage_ebkv9e8') or contains(Name,'ebkv9e8')&$select=Id,UId,Name,SysPackageId,ManagerName,ModifiedOn&$orderby=ModifiedOn desc"
    data = client.odata_query("SysSchema", query)

    if data and data.get("value"):
        print(f"Found {len(data['value'])} schema(s):\n")
        for s in data["value"]:
            pkg_id = s.get("SysPackageId")
            pkg_name = "Unknown"
            if pkg_id:
                pkg_query = f"$filter=Id eq {pkg_id}&$select=Name"
                pkg_data = client.odata_query("SysPackage", pkg_query)
                if pkg_data and pkg_data.get("value"):
                    pkg_name = pkg_data["value"][0].get("Name")
            name = s.get("Name", "")
            manager = s.get("ManagerName", "")
            modified = s.get("ModifiedOn", "")[:19]
            uid = s.get("UId", "")[:8] + "..."
            print(f"  {name:<45} | {pkg_name:<20} | {manager:<20} | {modified}")

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)


if __name__ == "__main__":
    main()
