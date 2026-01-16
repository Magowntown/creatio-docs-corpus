#!/usr/bin/env python3
"""Check Order entity schema in IWQBIntegration for PaymentStatus default."""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

IWQB_PACKAGE_ID = "5af0c9b0-141b-4d3f-828e-a455a1705aed"
IWQB_ORDER_ENTITY_ID = "19fdec92-ec56-4c7d-93cb-98b97cff670c"  # From earlier query
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
            print(f"Query {entity} failed: {resp.status_code}")
            return []
        return resp.json().get("value", [])

    def get_media(self, entity, record_id, media_property):
        url = f"{self.base_url}/0/odata/{entity}({record_id})/{media_property}"
        resp = self.session.get(url)
        return resp.content if resp.status_code == 200 else None

def main():
    print("=" * 70)
    print("CHECK ORDER ENTITY SCHEMA IN IWQBINTEGRATION")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Find Order entity schema in IWQBIntegration
    print("\n1. Finding Order entity schema in IWQBIntegration...")
    schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "UId", "ManagerName", "ModifiedOn"],
        filters=f"Name eq 'Order' and SysPackageId eq {IWQB_PACKAGE_ID}",
        limit=5
    )

    if not schemas:
        print("   No Order schema found in IWQBIntegration package")
        return

    order_schema = schemas[0]
    schema_id = order_schema.get('Id')
    print(f"   Found: {order_schema.get('Name')}")
    print(f"   Schema ID: {schema_id}")
    print(f"   UId: {order_schema.get('UId')}")
    print(f"   Manager: {order_schema.get('ManagerName')}")
    print(f"   Modified: {order_schema.get('ModifiedOn')}")

    # 2. Get MetaData for entity schema
    print("\n2. Getting entity schema MetaData...")
    metadata = client.get_media("SysSchema", schema_id, "MetaData")

    if metadata:
        meta_str = metadata.decode('utf-8')
        print(f"   Got {len(meta_str)} characters")

        # Save to file
        output_file = "/home/magown/creatio-report-fix/scripts/fix/iwqb_order_entity_metadata.txt"
        with open(output_file, 'w') as f:
            f.write(meta_str)
        print(f"   Saved to: {output_file}")

        # Search for PaymentStatus
        if PLANNED_STATUS_ID in meta_str:
            print(f"\n   ⚠️  FOUND PLANNED_STATUS_ID in entity metadata!")
            idx = meta_str.find(PLANNED_STATUS_ID)
            start = max(0, idx - 300)
            end = min(len(meta_str), idx + 300)
            print(f"   Context:\n{meta_str[start:end]}")
        elif "PaymentStatus" in meta_str:
            print(f"\n   Found PaymentStatus reference")
            for line in meta_str.split('\n'):
                if "PaymentStatus" in line:
                    print(f"   {line[:200]}")
        elif "Planned" in meta_str:
            print(f"\n   Found 'Planned' reference")
            for line in meta_str.split('\n'):
                if "Planned" in line:
                    print(f"   {line[:200]}")
        else:
            print("   No PaymentStatus or Planned reference found in entity metadata")

    # 3. Check all Order-related schemas in IWQBIntegration
    print("\n3. All schemas in IWQBIntegration...")
    all_schemas = client.query(
        "SysSchema",
        columns=["Id", "Name", "ManagerName"],
        filters=f"SysPackageId eq {IWQB_PACKAGE_ID}",
        limit=100
    )

    print(f"   Found {len(all_schemas)} schemas")
    for s in all_schemas:
        name = s.get('Name', '')
        if 'Order' in name or 'Payment' in name:
            print(f"   - {name} ({s.get('ManagerName')})")

    # 4. Check all entity schemas in IWQBIntegration for PaymentStatus
    print("\n4. Searching all entity schemas for PaymentStatus...")
    entity_schemas = [s for s in all_schemas if s.get('ManagerName') == 'EntitySchemaManager']

    for es in entity_schemas:
        es_id = es.get('Id')
        es_name = es.get('Name')

        meta = client.get_media("SysSchema", es_id, "MetaData")
        if meta:
            meta_str = meta.decode('utf-8')
            if PLANNED_STATUS_ID in meta_str or "PaymentStatus" in meta_str:
                print(f"\n   ⚠️  Found in {es_name}:")
                if PLANNED_STATUS_ID in meta_str:
                    idx = meta_str.find(PLANNED_STATUS_ID)
                    print(f"   Context: {meta_str[max(0,idx-200):idx+200]}")
                else:
                    for line in meta_str.split('\n'):
                        if "PaymentStatus" in line:
                            print(f"   {line[:200]}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
