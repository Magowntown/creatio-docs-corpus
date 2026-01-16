#!/usr/bin/env python3
"""
Deploy handler using correct Creatio 8.x FreedomUI API.
"""

import os
import requests
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import CLIENT_MODULE_DIR

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "1d5dfc4d-732d-48d7-af21-9e3d70794734"  # UsrPage_ebkv9e8
SCHEMA_NAME = "UsrPage_ebkv9e8"

# Read the updated handler code
with open(CLIENT_MODULE_DIR / "UsrPage_ebkv9e8_Updated.js", "r", encoding="utf-8") as f:
    HANDLER_CODE = f.read()

def main():
    session = requests.Session()

    # Login
    print("=== Logging in ===")
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD},
                           timeout=30)
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Step 1: Get schema via DataService
    print("\n=== Getting schema via DataService ===")
    esq_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    esq_body = {
        "rootSchemaName": "SysClientUnitSchema",
        "operationType": 0,
        "allColumns": True,
        "filters": {
            "filterType": 1,
            "comparisonType": 3,
            "leftExpression": {"columnPath": "UId"},
            "rightExpression": {"parameter": {"dataValueType": 0, "value": SCHEMA_UID}}
        }
    }
    response = session.post(esq_url, json=esq_body, headers=headers, timeout=30)
    print(f"DataService response: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        if rows:
            schema_record = rows[0]
            print(f"Found schema: {schema_record.get('Name', 'N/A')}")
            print(f"Schema ID in DB: {schema_record.get('Id', 'N/A')}")
            print(f"Available columns: {list(schema_record.keys())}")
        else:
            print("Schema not found in SysClientUnitSchema")

    # Step 2: Try VwSysClientUnitSchema (view with body)
    print("\n=== Getting schema body via VwSysClientUnitSchema ===")
    esq_body = {
        "rootSchemaName": "VwSysClientUnitSchema",
        "operationType": 0,
        "allColumns": True,
        "filters": {
            "filterType": 1,
            "comparisonType": 3,
            "leftExpression": {"columnPath": "UId"},
            "rightExpression": {"parameter": {"dataValueType": 0, "value": SCHEMA_UID}}
        }
    }
    response = session.post(esq_url, json=esq_body, headers=headers, timeout=30)
    print(f"VwSysClientUnitSchema response: {response.status_code}")

    schema_id = None
    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        if rows:
            schema_record = rows[0]
            schema_id = schema_record.get("Id")
            print(f"Found schema view: {schema_record.get('Name', 'N/A')}")
            print(f"Schema record Id: {schema_id}")
            if schema_record.get("Body"):
                print(f"Current body preview: {str(schema_record.get('Body', ''))[:200]}...")

    # Step 3: Try updating via SysPackageSchemaData
    print("\n=== Trying SysPackageSchemaData update ===")
    esq_body = {
        "rootSchemaName": "SysPackageSchemaData",
        "operationType": 0,
        "allColumns": True,
        "filters": {
            "filterType": 1,
            "comparisonType": 3,
            "leftExpression": {"columnPath": "UId"},
            "rightExpression": {"parameter": {"dataValueType": 0, "value": SCHEMA_UID}}
        }
    }
    response = session.post(esq_url, json=esq_body, headers=headers, timeout=30)
    print(f"SysPackageSchemaData response: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        if rows:
            print(f"Found {len(rows)} schema data records")
            for row in rows:
                print(f"  - Package: {row.get('SysPackage', {}).get('displayValue', 'N/A')}")
                print(f"    Id: {row.get('Id')}")

    # Step 4: Use the REST API for schema content
    print("\n=== Trying REST API for schema content ===")

    # Get schema content
    content_url = f"{CREATIO_URL}/0/ServiceModel/ClientUnitSchemaDesignerService.svc/GetSchemaContent"
    response = session.post(content_url,
                           json={"schemaUId": SCHEMA_UID},
                           headers=headers, timeout=30)
    print(f"GetSchemaContent response: {response.status_code}")
    if response.status_code == 200:
        print(response.text[:500])

    # Try the schema designer manifest
    print("\n=== Trying Schema Designer Manifest ===")
    manifest_url = f"{CREATIO_URL}/0/ServiceModel/ClientUnitSchemaDesignerService.svc/GetSchemaManifest"
    response = session.post(manifest_url,
                           json={"schemaUId": SCHEMA_UID},
                           headers=headers, timeout=30)
    print(f"GetSchemaManifest response: {response.status_code}")
    if response.status_code == 200:
        try:
            manifest = response.json()
            print(f"Manifest: {json.dumps(manifest, indent=2)[:800]}")
        except:
            print(response.text[:500])

    # Step 5: Try full SaveSchema with proper structure
    print("\n=== Trying full SaveSchema ===")
    save_url = f"{CREATIO_URL}/0/ServiceModel/ClientUnitSchemaDesignerService.svc/SaveSchema"

    # Build full schema structure
    full_schema = {
        "uId": SCHEMA_UID,
        "name": SCHEMA_NAME,
        "body": HANDLER_CODE,
        "extendParent": False,
        "schemaManagerName": "ClientUnitSchemaManager"
    }

    response = session.post(save_url, json=full_schema, headers=headers, timeout=60)
    print(f"SaveSchema response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)[:500]}")

        if result.get("success"):
            print("\n>>> Schema saved successfully!")
            compile_schema(session, headers)
        else:
            print(f"Error: {result.get('errorInfo', {}).get('message', 'Unknown')}")

def compile_schema(session, headers):
    """Compile the workspace"""
    import time

    print("\n=== Compiling ===")
    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"

    for attempt in range(3):
        print(f"Build attempt {attempt + 1}...")
        try:
            response = session.post(build_url, json={}, headers=headers, timeout=300)
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(">>> Compilation successful!")
                    return True
                else:
                    error = result.get("errorInfo", {}).get("message", str(result))
                    if "another compilation" in error.lower():
                        print("Waiting for other compilation...")
                        time.sleep(30)
                    else:
                        print(f"Error: {error[:300]}")
                        break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
    return False

if __name__ == "__main__":
    main()
