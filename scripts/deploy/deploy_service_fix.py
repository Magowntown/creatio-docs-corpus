#!/usr/bin/env python3
"""
Deploy the DL-003B fix for UsrExcelReportService.

This fixes the FormatException when IntEntitySchemaName is a lookup instead of text.
"""

import os
import sys
import requests
import json

# Add parent to path for _env
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"  # UsrExcelReportService

def read_service_code():
    """Read the updated service code from file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    code_path = os.path.join(script_dir, "..", "..", "source-code", "UsrExcelReportService_Updated.cs")
    with open(code_path, "r") as f:
        return f.read()

def login(session):
    """Login to Creatio and return success status."""
    response = session.post(
        f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
        json={"UserName": USERNAME, "UserPassword": PASSWORD}
    )
    if response.status_code == 200:
        result = response.json()
        return result.get("Code") == 0
    return False

def get_schema_metadata(session):
    """Get current schema metadata."""
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Try OData first
    url = f"{CREATIO_URL}/0/odata/SysSchema?$filter=UId eq {SCHEMA_UID}&$select=Id,Name,UId"
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("value"):
            return data["value"][0]

    return None

def update_schema_body(session, new_code):
    """Update schema body using DataService."""
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Method 1: Try SourceCodeSchemaManager.SaveSchema
    save_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SourceCodeSchemaManagerRequest"
    payload = {
        "schemaUId": SCHEMA_UID,
        "methodName": "SaveSchema",
        "body": new_code
    }

    response = session.post(save_url, json=payload, headers=headers)
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get("success"):
                return True, "SaveSchema succeeded"
        except:
            pass

    # Method 2: Try direct SysSchema update via OData
    update_url = f"{CREATIO_URL}/0/odata/SysSchema"

    # First get the schema ID
    schema_meta = get_schema_metadata(session)
    if not schema_meta:
        return False, "Could not find schema metadata"

    schema_id = schema_meta.get("Id")

    # Try PATCH to update Body
    patch_url = f"{CREATIO_URL}/0/odata/SysSchema({schema_id})"
    patch_data = {
        "Body": new_code
    }

    response = session.patch(patch_url, json=patch_data, headers=headers)
    if response.status_code in [200, 204]:
        return True, "OData PATCH succeeded"

    # Method 3: Try WorkspaceExplorerService
    ws_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/SaveSchema"
    ws_payload = {
        "UId": SCHEMA_UID,
        "SchemaManagerName": "SourceCodeSchemaManager",
        "Body": new_code
    }

    response = session.post(ws_url, json=ws_payload, headers=headers)
    if response.status_code == 200:
        return True, "WorkspaceExplorerService succeeded"

    return False, f"All methods failed. Last status: {response.status_code}, response: {response.text[:500]}"

def compile_workspace(session):
    """Trigger workspace compilation."""
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    compile_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"
    response = session.post(compile_url, json={}, headers=headers)

    if response.status_code == 200:
        return True, response.text
    return False, f"Compile failed: {response.status_code}"

def main():
    print("=== DL-003B Fix Deployment ===")
    print(f"Target: {CREATIO_URL}")
    print(f"Schema: UsrExcelReportService ({SCHEMA_UID})")
    print()

    if not USERNAME or not PASSWORD:
        print("ERROR: Set CREATIO_USERNAME and CREATIO_PASSWORD environment variables")
        sys.exit(1)

    # Read updated code
    print("Reading updated service code...")
    try:
        new_code = read_service_code()
        print(f"  Code size: {len(new_code)} bytes")
    except Exception as e:
        print(f"ERROR: Could not read service code: {e}")
        sys.exit(1)

    # Login
    session = requests.Session()
    print("Logging in...")
    if not login(session):
        print("ERROR: Login failed")
        sys.exit(1)
    print("  Login: OK")

    # Update schema
    print("Updating schema body...")
    success, message = update_schema_body(session, new_code)
    if success:
        print(f"  Update: OK ({message})")
    else:
        print(f"  Update: FAILED ({message})")
        print()
        print("=== MANUAL DEPLOYMENT REQUIRED ===")
        print("1. Open: https://dev-pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178")
        print("2. Ctrl+A to select all")
        print("3. Paste contents of source-code/UsrExcelReportService_Updated.cs")
        print("4. Ctrl+S to save")
        print("5. Actions menu -> Publish")
        sys.exit(1)

    # Compile
    print("Triggering compilation...")
    success, message = compile_workspace(session)
    if success:
        print(f"  Compile: Started")
    else:
        print(f"  Compile: {message}")

    print()
    print("=== Deployment initiated ===")
    print("Wait 30-60 seconds for compilation, then verify with:")
    print("  python3 scripts/testing/test_report_service.py")

if __name__ == "__main__":
    main()
