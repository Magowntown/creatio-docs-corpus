#!/usr/bin/env python3
"""
Deploy the updated UsrPage_ebkv9e8 handler to Creatio using the correct FreedomUI API.
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

    # Try multiple endpoint patterns for FreedomUI schema
    endpoints_to_try = [
        "/0/ServiceModel/ClientUnitSchemaDesignerService.svc/GetSchemaData",
        "/0/rest/ClientUnitSchemaDesignerService/GetSchemaData",
        "/0/ServiceModel/SchemaDesignerService.svc/GetSchema",
        "/0/rest/SchemaDesignerService/GetSchema",
    ]

    schema_data = None
    working_endpoint = None

    print("\n=== Finding working endpoint ===")
    for endpoint in endpoints_to_try:
        url = f"{CREATIO_URL}{endpoint}"
        print(f"Trying: {endpoint}")
        try:
            response = session.post(url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data and not data.get("errorInfo"):
                    schema_data = data
                    working_endpoint = endpoint
                    print(f"  SUCCESS! Got schema: {data.get('name', 'N/A')}")
                    break
                else:
                    print(f"  Got response but with error: {data.get('errorInfo', {}).get('message', str(data)[:200])}")
            else:
                print(f"  Status: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

    if not schema_data:
        print("\nCould not find working endpoint. Trying OData approach...")

        # Try OData to get schema info
        odata_url = f"{CREATIO_URL}/0/odata/SysClientUnitSchema?$filter=UId eq {SCHEMA_UID}"
        response = session.get(odata_url, headers=headers, timeout=30)
        print(f"OData response: {response.status_code}")
        if response.status_code == 200:
            print(response.json())

        # Try the schema manager API
        print("\n=== Trying Schema Manager API ===")
        schema_manager_url = f"{CREATIO_URL}/0/ServiceModel/SchemaManagerService.svc/GetSchema"
        response = session.post(schema_manager_url,
                               json={"schemaUId": SCHEMA_UID, "schemaType": "ClientUnitSchema"},
                               headers=headers, timeout=30)
        print(f"Schema Manager response: {response.status_code}")
        if response.status_code == 200:
            print(response.text[:500])

        # Try the workspace explorer
        print("\n=== Trying Workspace Explorer API ===")
        workspace_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/GetSchemaData"
        response = session.post(workspace_url,
                               json={"schemaUId": SCHEMA_UID},
                               headers=headers, timeout=30)
        print(f"Workspace Explorer response: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data and not data.get("errorInfo"):
                schema_data = data
                working_endpoint = "/0/ServiceModel/WorkspaceExplorerService.svc/GetSchemaData"
                print(f"SUCCESS via Workspace Explorer!")
            else:
                print(response.text[:500])

    if not schema_data:
        print("\nFailed to get schema data. Trying direct update approach...")

        # Try direct schema update without getting first
        print("\n=== Trying Direct Schema Update ===")
        update_endpoints = [
            "/0/ServiceModel/ClientUnitSchemaDesignerService.svc/SaveSchema",
            "/0/rest/ClientUnitSchemaDesignerService/SaveSchema",
            "/0/ServiceModel/SchemaDesignerService.svc/SaveSchema",
        ]

        for endpoint in update_endpoints:
            url = f"{CREATIO_URL}{endpoint}"
            print(f"Trying save: {endpoint}")

            # Construct minimal schema update
            update_data = {
                "uId": SCHEMA_UID,
                "body": HANDLER_CODE
            }

            try:
                response = session.post(url, json=update_data, headers=headers, timeout=60)
                print(f"  Status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"  Result: {json.dumps(result, indent=2)[:500]}")
                    if result.get("success") != False:
                        print("  Might have worked!")
                        break
            except Exception as e:
                print(f"  Error: {e}")

        return

    # If we got schema data, update and save
    print(f"\n=== Updating schema body ===")
    schema_data["body"] = HANDLER_CODE

    # Determine save endpoint
    if "ClientUnitSchemaDesignerService" in working_endpoint:
        save_endpoint = working_endpoint.replace("GetSchemaData", "SaveSchema")
    elif "WorkspaceExplorerService" in working_endpoint:
        save_endpoint = working_endpoint.replace("GetSchemaData", "SaveSchema")
    else:
        save_endpoint = working_endpoint.replace("GetSchema", "SaveSchema")

    save_url = f"{CREATIO_URL}{save_endpoint}"
    print(f"Saving to: {save_endpoint}")

    response = session.post(save_url, json=schema_data, headers=headers, timeout=60)
    print(f"Save status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"Save result: {json.dumps(result, indent=2)[:500]}")

        if result.get("success") != False:
            compile_schema(session, headers)
    else:
        print(f"Save error: {response.text[:500]}")

def compile_schema(session, headers):
    """Compile the workspace after saving"""
    import time

    print("\n=== Compiling ===")
    compile_endpoints = [
        "/0/ServiceModel/WorkspaceExplorerService.svc/Build",
        "/0/rest/WorkspaceExplorerService/Build",
    ]

    for endpoint in compile_endpoints:
        build_url = f"{CREATIO_URL}{endpoint}"
        print(f"Trying compile: {endpoint}")

        for attempt in range(3):
            print(f"  Build attempt {attempt + 1}...")
            try:
                response = session.post(build_url, json={}, headers=headers, timeout=300)

                if response.status_code != 200:
                    print(f"  HTTP Error: {response.status_code}")
                    continue

                result = response.json()

                if result.get("success"):
                    print("  >>> Compilation successful!")
                    return True
                else:
                    error = result.get("errorInfo", {}).get("message", str(result))
                    if "another compilation" in error.lower():
                        print("  Waiting for other compilation...")
                        time.sleep(30)
                    else:
                        print(f"  Compilation error: {error[:300]}")
                        break
            except Exception as e:
                print(f"  Error: {e}")
                time.sleep(10)

        # If this endpoint worked (even with errors), don't try others
        if response.status_code == 200:
            break

    return False

if __name__ == "__main__":
    main()
