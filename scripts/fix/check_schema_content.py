#!/usr/bin/env python3
"""Check and potentially modify OrderPageV2 schema content."""

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

IWQB_ORDER_PAGE_SCHEMA_ID = "6c9e5e8b-9d0b-41b4-b24d-bec395eb68bf"
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

    def query(self, entity, columns=None, filters=None, limit=100):
        url = f"{self.base_url}/0/odata/{entity}"
        params = {"$top": str(limit)}
        if columns:
            params["$select"] = ",".join(columns)
        if filters:
            params["$filter"] = filters

        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            print(f"Query {entity} failed: {resp.status_code} - {resp.text[:200]}")
            return []
        return resp.json().get("value", [])

def main():
    print("=" * 70)
    print("CHECK IWQBINTEGRATION ORDERPAGEV2 SCHEMA")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Get the schema record
    print("\n1. Fetching OrderPageV2 schema info...")
    schema = client.query(
        "SysSchema",
        filters=f"Id eq {IWQB_ORDER_PAGE_SCHEMA_ID}"
    )

    if schema:
        print(f"   Found schema:")
        for key, val in schema[0].items():
            if val and not key.startswith("@"):
                if isinstance(val, str) and len(val) > 100:
                    print(f"   {key}: {val[:100]}...")
                else:
                    print(f"   {key}: {val}")

    # 2. Try to get schema content
    print("\n2. Checking for schema content tables...")

    content_tables = [
        "SysSchemaContent",
        "SysSchemaData",
        "VwSysSchemaInfo",
        "SysSchemaSource",
    ]

    for table in content_tables:
        records = client.query(table, limit=1)
        if records:
            print(f"   ✓ {table}: accessible")
            print(f"     Columns: {list(records[0].keys())[:8]}...")
        else:
            print(f"   ✗ {table}: not accessible")

    # 3. Try to get the actual schema source
    print("\n3. Attempting to get schema source...")

    # Try VwSysSchemaInfo which often has more details
    schema_info = client.query(
        "VwSysSchemaInfo",
        filters=f"UId eq {IWQB_ORDER_PAGE_SCHEMA_ID}",
        limit=1
    )

    if schema_info:
        print("   Found VwSysSchemaInfo record:")
        for key, val in schema_info[0].items():
            if val and not key.startswith("@"):
                print(f"   {key}: {val}")

    # 4. Check SysSchemaProperty for default values
    print("\n4. Checking SysSchemaProperty for defaults...")
    props = client.query(
        "SysSchemaProperty",
        filters=f"contains(Name, 'Payment')",
        limit=20
    )
    if props:
        for p in props:
            print(f"   {p}")
    else:
        print("   SysSchemaProperty not accessible or empty")

    print("\n" + "=" * 70)
    print("SCHEMA MODIFICATION OPTIONS")
    print("=" * 70)
    print("""
The OrderPageV2 schema content is stored in Creatio's internal format
and cannot be easily modified via API.

OPTIONS:

1. MANUAL (Recommended):
   Open in Configuration UI:
   https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/6c9e5e8b-9d0b-41b4-b24d-bec395eb68bf

   Find and remove the PaymentStatus default value.

2. DATABASE (Advanced):
   Connect to PostgreSQL and update SysSchema.Body or related tables.
   Requires knowledge of Creatio's internal schema format.

For now, I recommend:
1. Execute the reset script to fix existing orders (immediate fix)
2. Update the schema in Configuration UI to prevent future issues
""")
    print("=" * 70)

if __name__ == "__main__":
    main()
