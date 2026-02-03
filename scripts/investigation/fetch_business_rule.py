#!/usr/bin/env python3
"""
Fetch BGUsrPage_ebkv9e8BusinessRule content from Creatio PROD.
Investigate if Custom package version conflicts with v19 handler.
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

class CreatioClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.bpmcsrf = None

    def login(self):
        """Authenticate with Creatio"""
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
        """Execute OData query"""
        url = f"{self.base_url}/0/odata/{entity}"
        if params:
            url += f"?{params}"

        headers = {"Content-Type": "application/json"}
        if self.bpmcsrf:
            headers["BPMCSRF"] = self.bpmcsrf

        resp = self.session.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        print(f"  Error: {resp.status_code} - {resp.text[:200]}")
        return None


def main():
    # Get credentials
    prod_url = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
    prod_user = os.getenv("CREATIO_PROD_USERNAME")
    prod_pass = os.getenv("CREATIO_PROD_PASSWORD")

    if not all([prod_url, prod_user, prod_pass]):
        print("Missing PROD credentials in .env")
        sys.exit(1)

    print(f"Connecting to PROD: {prod_url}")
    client = CreatioClient(prod_url, prod_user, prod_pass)

    if not client.login():
        print("Login failed!")
        sys.exit(1)
    print("Login successful\n")

    # Query 1: Find all BGUsrPage_ebkv9e8BusinessRule schemas
    print("=" * 70)
    print("SEARCHING FOR BGUsrPage_ebkv9e8BusinessRule SCHEMAS")
    print("=" * 70)

    query = "$filter=contains(Name,'BGUsrPage_ebkv9e8')&$select=Id,UId,Name,Caption,SysPackageId,ManagerName,ModifiedOn&$orderby=ModifiedOn desc"
    data = client.odata_query("SysSchema", query)

    if not data or not data.get("value"):
        print("No business rules found!")
        return

    schemas = data["value"]
    print(f"Found {len(schemas)} schema(s):\n")

    results = []

    for s in schemas:
        schema_id = s.get("Id")
        uid = s.get("UId")
        name = s.get("Name")
        caption = s.get("Caption")
        pkg_id = s.get("SysPackageId")
        manager = s.get("ManagerName")
        modified = s.get("ModifiedOn", "")[:19]

        # Get package name
        pkg_name = "Unknown"
        if pkg_id:
            pkg_query = f"$filter=Id eq {pkg_id}&$select=Name"
            pkg_data = client.odata_query("SysPackage", pkg_query)
            if pkg_data and pkg_data.get("value"):
                pkg_name = pkg_data["value"][0].get("Name", "Unknown")

        print(f"Schema: {name}")
        print(f"  UId:      {uid}")
        print(f"  Package:  {pkg_name}")
        print(f"  Manager:  {manager}")
        print(f"  Modified: {modified}")
        print()

        results.append({
            "id": schema_id,
            "uid": uid,
            "name": name,
            "package": pkg_name,
            "manager": manager,
            "modified": modified
        })

    # Query 2: Try to get business rule content via SysSchemaContent
    print("=" * 70)
    print("FETCHING BUSINESS RULE CONTENT")
    print("=" * 70)

    for r in results:
        if "BusinessRule" in r["name"]:
            print(f"\nFetching content for: {r['name']} ({r['package']})")
            print(f"UId: {r['uid']}")

            # Try SysSchemaContent
            content_query = f"$filter=SysSchemaId eq {r['id']}&$select=Id,Content,ContentType"
            content_data = client.odata_query("SysSchemaContent", content_query)

            if content_data and content_data.get("value"):
                for c in content_data["value"]:
                    content = c.get("Content", "")
                    content_type = c.get("ContentType", "")
                    print(f"  ContentType: {content_type}")
                    if content:
                        print(f"  Content length: {len(content)} chars")
                        print("-" * 50)
                        # Print first 2000 chars
                        print(content[:2000])
                        if len(content) > 2000:
                            print(f"\n... (truncated, total {len(content)} chars)")
                        print("-" * 50)

                        # Save full content to file
                        filename = f"/home/magown/creatio-report-fix/test-artifacts/business-rules/{r['package']}_{r['name']}.json"
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                        with open(filename, "w") as f:
                            f.write(content)
                        print(f"  Saved to: {filename}")
            else:
                print("  No content found in SysSchemaContent")

                # Try SysSchemaExtensionData (alternative storage)
                ext_query = f"$filter=SysSchemaId eq {r['id']}"
                ext_data = client.odata_query("SysSchemaExtensionData", ext_query)
                if ext_data and ext_data.get("value"):
                    print(f"  Found {len(ext_data['value'])} extension data records")
                    for e in ext_data["value"]:
                        print(f"    Data: {json.dumps(e, indent=2)[:500]}")

    print("\n" + "=" * 70)
    print("INVESTIGATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
