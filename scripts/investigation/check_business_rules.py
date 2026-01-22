#!/usr/bin/env python3
"""Check business rules addon data for UsrPage_ebkv9e8 schemas."""

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

# Known UsrPage_ebkv9e8 schema UIDs
SCHEMA_UIDS = {
    "BGlobalLookerStudio": "4e6a5aa6-86b7-48c1-9147-7b09e96ee59e",
    "BGApp_eykaguu": "873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2",  # 561d9dd4-8bf2-4f63-a781-54ac48a74972 in some contexts
}

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
            print(f"Query {entity} failed: {resp.status_code} - {resp.text[:200]}")
            return []
        return resp.json().get("value", [])

    def query_dataservice(self, root_name, columns, filters=None):
        """Use DataService for more complex queries."""
        url = f"{self.base_url}/0/DataService/json/SyncReply/SelectQuery"
        payload = {
            "RootSchemaName": root_name,
            "OperationType": 0,
            "Columns": {"Items": {col: {"Expression": {"ColumnPath": col}} for col in columns}},
            "AllColumns": False,
            "Filters": filters or {}
        }
        resp = self.session.post(url, json=payload)
        if resp.status_code != 200:
            return {"error": resp.text[:500]}
        return resp.json()

def main():
    print("=" * 70)
    print("CHECK BUSINESS RULES FOR UsrPage_ebkv9e8 SCHEMAS")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Find all UsrPage_ebkv9e8 schemas
    print("\n1. Finding UsrPage_ebkv9e8 schemas...")
    schemas = client.query(
        "SysSchema",
        columns=["Id", "UId", "Name", "Caption", "ManagerName", "PackageId"],
        filters="Name eq 'UsrPage_ebkv9e8'"
    )

    if schemas:
        print(f"   Found {len(schemas)} schema(s):")
        for s in schemas:
            print(f"   - UId: {s.get('UId')}, PackageId: {s.get('PackageId')}")
    else:
        print("   No schemas found with OData, trying alternative...")

    # 2. Check VwSysSchemaInPackage for schema locations
    print("\n2. Checking VwSysSchemaInPackage...")
    pkg_schemas = client.query(
        "VwSysSchemaInPackage",
        columns=["Id", "UId", "Name", "SysPackage", "SysPackageId"],
        filters="Name eq 'UsrPage_ebkv9e8'",
        limit=10
    )

    if pkg_schemas:
        for ps in pkg_schemas:
            print(f"   - UId: {ps.get('UId')}, Package: {ps.get('SysPackage')}")

    # 3. Check for business rules tables
    print("\n3. Checking business rules tables...")

    # Common business rules related tables in Creatio
    rule_tables = [
        "SysEntitySchemaBusinessRule",
        "SysModuleBusinessRule",
        "SysFreedomUIPageSchemaBusinessRule",
        "VwSysPageSchemaBusinessRule",
        "SysSchemaContent",
        "SysPackageSchemaData",
        "SysSchemaAddon",
    ]

    for table in rule_tables:
        try:
            records = client.query(table, limit=1)
            if records:
                print(f"   ✓ {table}: accessible - columns: {list(records[0].keys())[:6]}...")
            else:
                print(f"   ? {table}: accessible but empty")
        except Exception as e:
            print(f"   ✗ {table}: {str(e)[:50]}")

    # 4. Try to find business rules by schema name
    print("\n4. Looking for business rules linked to UsrPage_ebkv9e8...")

    # Check SysPackageSchemaData for addon data
    addon_data = client.query(
        "SysPackageSchemaData",
        columns=["Id", "SysSchemaId", "DataId", "Data"],
        filters="contains(Data, 'UsrPage_ebkv9e8') or contains(Data, 'visible')",
        limit=20
    )

    if addon_data:
        print(f"   Found {len(addon_data)} addon data records")
        for ad in addon_data:
            data_preview = str(ad.get("Data", ""))[:200]
            print(f"   - SchemaId: {ad.get('SysSchemaId')}, Data: {data_preview}...")
    else:
        print("   No addon data found via OData")

    # 5. Check SysPackageSchemaData via DataService
    print("\n5. Querying SysPackageSchemaData via DataService...")
    ds_result = client.query_dataservice(
        "SysPackageSchemaData",
        columns=["Id", "SysSchemaId", "DataId", "Data"],
    )

    if "error" not in ds_result:
        rows = ds_result.get("rows", [])
        print(f"   Found {len(rows)} total addon records")
        # Look for UsrPage or business rule related data
        for row in rows[:50]:
            data = str(row.get("Data", ""))
            if "UsrPage" in data or "business" in data.lower() or "visible" in data.lower():
                print(f"   - SchemaId: {row.get('SysSchemaId')}")
                print(f"     Data preview: {data[:300]}...")
    else:
        print(f"   DataService error: {ds_result['error'][:200]}")

    # 6. Query VwSysSchemaInfo for complete schema details
    print("\n6. Getting complete schema info for known UIDs...")
    for name, uid in SCHEMA_UIDS.items():
        info = client.query(
            "VwSysSchemaInfo",
            filters=f"UId eq {uid}",
            limit=1
        )
        if info:
            print(f"\n   {name} ({uid}):")
            for key, val in info[0].items():
                if val and not key.startswith("@"):
                    val_str = str(val)
                    if len(val_str) > 100:
                        val_str = val_str[:100] + "..."
                    print(f"     {key}: {val_str}")

    # 7. Look for Freedom UI specific business rules
    print("\n7. Checking SysFreedomUIPageSchemaBusinessRule (if exists)...")
    freedom_rules = client.query(
        "SysFreedomUIPageSchemaBusinessRule",
        limit=50
    )
    if freedom_rules:
        print(f"   Found {len(freedom_rules)} Freedom UI business rules")
        for rule in freedom_rules:
            print(f"   - {rule}")

    # 8. Alternative: check SysModuleEntity for page associations
    print("\n8. Checking page module associations...")
    modules = client.query(
        "SysModuleEntity",
        columns=["Id", "SysEntitySchemaUId", "CardSchemaUId", "SectionSchemaUId"],
        limit=10
    )
    if modules:
        print(f"   Found module entity associations (showing first 5)")
        for m in modules[:5]:
            print(f"   - CardSchema: {m.get('CardSchemaUId')}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
Business rules in Freedom UI are typically managed through:
1. Schema handlers (crt.HandleViewModelAttributeChangeRequest)
2. Attribute bindings in viewConfigDiff ("visible": "$SomeAttribute")
3. Business rules section in Freedom UI Page Designer

To see business rules for UsrPage_ebkv9e8:
1. Open PROD: https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2
2. Click on "Business Rules" tab in the designer
3. Or check the "Rules" section of each field in the designer

The business rules for field visibility (Year-Month, Sales Group) are likely
controlled through handlers in the schema code itself, not separate addon data.
""")

if __name__ == "__main__":
    main()
