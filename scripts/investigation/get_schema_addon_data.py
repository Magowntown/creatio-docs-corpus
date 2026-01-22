#!/usr/bin/env python3
"""Get schema addon data (business rules) for UsrPage_ebkv9e8."""

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

# Known UsrPage_ebkv9e8 schema UIDs
SCHEMA_UIDS = [
    "4e6a5aa6-86b7-48c1-9147-7b09e96ee59e",  # BGlobalLookerStudio parent
    "561d9dd4-8bf2-4f63-a781-54ac48a74972",  # BGApp_eykaguu middle
    "1d5dfc4d-732d-48d7-af21-9e3d70794734",  # IWQBIntegration top (if exists)
    "873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2",  # Alternative UID
]

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
        self.bpmcsrf = self.session.cookies.get("BPMCSRF")
        self.session.headers.update({"BPMCSRF": self.bpmcsrf})
        print(f"Logged in to {self.base_url}")

    def query(self, entity, columns=None, filters=None, limit=100):
        url = f"{self.base_url}/0/odata/{entity}"
        params = {"$top": str(limit)}
        if columns:
            params["$select"] = ",".join(columns)
        if filters:
            params["$filter"] = filters

        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            print(f"Query {entity} failed: {resp.status_code}")
            return []
        return resp.json().get("value", [])

    def batch_query(self, requests_list):
        """Execute batch OData request."""
        url = f"{self.base_url}/0/odata/$batch"
        boundary = "batch_boundary"

        body_parts = []
        for req in requests_list:
            part = f"--{boundary}\r\n"
            part += "Content-Type: application/http\r\n"
            part += "Content-Transfer-Encoding: binary\r\n\r\n"
            part += f"GET {req} HTTP/1.1\r\n"
            part += "Accept: application/json\r\n\r\n"
            body_parts.append(part)

        body = "".join(body_parts) + f"--{boundary}--"

        headers = {
            "Content-Type": f"multipart/mixed; boundary={boundary}",
            "BPMCSRF": self.bpmcsrf
        }

        resp = self.session.post(url, data=body, headers=headers)
        return resp

    def get_schema_data(self, schema_uid):
        """Get schema addon data using SysPackageSchemaData."""
        # First get the SysSchema.Id for this UId
        schema = self.query(
            "SysSchema",
            columns=["Id", "UId", "Name"],
            filters=f"UId eq {schema_uid}",
            limit=1
        )

        if not schema:
            print(f"   Schema {schema_uid} not found")
            return None

        schema_id = schema[0].get("Id")
        print(f"   Found SysSchema.Id: {schema_id}")

        # Now query SysPackageSchemaData for this schema
        data = self.query(
            "SysPackageSchemaData",
            columns=["Id", "SysSchemaId", "DataId", "InstallType"],
            filters=f"SysSchemaId eq {schema_id}",
            limit=50
        )

        return data

def main():
    print("=" * 70)
    print("GET ADDON DATA FOR UsrPage_ebkv9e8 SCHEMAS")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Check available columns in SysPackageSchemaData
    print("\n1. Checking SysPackageSchemaData structure...")
    sample = client.query("SysPackageSchemaData", limit=1)
    if sample:
        print(f"   Available columns: {list(sample[0].keys())}")

    # 2. Query SysSchema to get schema IDs
    print("\n2. Finding UsrPage_ebkv9e8 schemas...")
    schemas = client.query(
        "SysSchema",
        columns=["Id", "UId", "Name", "Caption"],
        filters="Name eq 'UsrPage_ebkv9e8'",
        limit=10
    )

    if schemas:
        print(f"   Found {len(schemas)} schema(s):")
        for s in schemas:
            print(f"   - Id: {s.get('Id')}, UId: {s.get('UId')}")

    # 3. For each schema, find addon data
    print("\n3. Getting addon data for each schema...")

    for s in schemas:
        schema_id = s.get("Id")
        schema_uid = s.get("UId")
        print(f"\n   Schema UId: {schema_uid}")

        # Query addon data
        addon_data = client.query(
            "SysPackageSchemaData",
            filters=f"SysSchemaId eq {schema_id}",
            limit=50
        )

        if addon_data:
            print(f"   Found {len(addon_data)} addon data records:")
            for ad in addon_data:
                print(f"   - DataId: {ad.get('DataId')}")
                print(f"     InstallType: {ad.get('InstallType')}")

                # Check if Data column exists
                if "Data" in ad and ad["Data"]:
                    data_preview = str(ad["Data"])[:500]
                    print(f"     Data: {data_preview}...")
        else:
            print("   No addon data found")

    # 4. Try querying by specific known UIDs
    print("\n4. Direct query for known UIDs...")
    for uid in SCHEMA_UIDS:
        print(f"\n   Checking {uid}...")

        schema = client.query(
            "SysSchema",
            columns=["Id", "Name"],
            filters=f"UId eq {uid}",
            limit=1
        )

        if schema:
            schema_id = schema[0]["Id"]
            print(f"   Found schema Id: {schema_id}")

            addon = client.query(
                "SysPackageSchemaData",
                filters=f"SysSchemaId eq {schema_id}",
                limit=20
            )

            print(f"   Addon records: {len(addon) if addon else 0}")
            for a in (addon or []):
                print(f"   - {a.get('Id')}: InstallType={a.get('InstallType')}")
        else:
            print(f"   Schema not found")

    # 5. Check VwSysSchemaInPackage for more info
    print("\n5. Checking VwSysSchemaInPackage for addon types...")
    pkg_info = client.query(
        "VwSysSchemaInPackage",
        columns=["UId", "Name", "SysPackageId"],
        filters="Name eq 'UsrPage_ebkv9e8'",
        limit=10
    )

    unique_uids = set()
    for p in (pkg_info or []):
        uid = p.get("UId")
        if uid not in unique_uids:
            unique_uids.add(uid)
            print(f"   UId: {uid}, PackageId: {p.get('SysPackageId')}")

    # 6. Try to find business rules in SysSchemaContent
    print("\n6. Checking SysSchemaContent for business rules data...")
    for s in schemas[:2]:  # Check first 2 schemas
        schema_id = s.get("Id")
        content = client.query(
            "SysSchemaContent",
            filters=f"SysSchemaId eq {schema_id}",
            limit=5
        )

        if content:
            print(f"\n   Schema {s.get('UId')} has {len(content)} content records:")
            for c in content:
                print(f"   - Id: {c.get('Id')}")
                for key, val in c.items():
                    if val and key not in ["Id", "CreatedOn", "ModifiedOn"] and not key.startswith("@"):
                        val_str = str(val)[:200]
                        print(f"     {key}: {val_str}")

    print("\n" + "=" * 70)
    print("NOTES")
    print("=" * 70)
    print("""
Business rules in Freedom UI are stored differently than Classic UI:

1. WITHIN SCHEMA CODE:
   - Handler logic controls field visibility
   - Attribute bindings like "visible": "$UsrShowCommissionFilters"

2. SEPARATE ADDON DATA:
   - Business rules defined in Freedom UI Designer
   - Stored in SysPackageSchemaData table
   - May require special API access

3. TO VIEW IN UI:
   - Open: https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2
   - Look for "Business Rules" section or field-level rules

If you have access to PROD Creatio admin, the business rules can be viewed
directly in the Freedom UI Page Designer interface.
""")

if __name__ == "__main__":
    main()
