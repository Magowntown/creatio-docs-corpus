#!/usr/bin/env python3
"""Try to update schema via WorkspaceExplorer or SysPackageSchemaData."""

import os
import requests
import json
import base64
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import SOURCE_CODE_DIR
from scripts._env import load_dotenv

load_dotenv()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"

# Read the new code from file
with open(SOURCE_CODE_DIR / "UsrExcelReportService_Updated.cs", "r", encoding="utf-8") as f:
    NEW_CODE = f.read()

def main():
    session = requests.Session()

    # Login
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD},
                           timeout=30)
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Try various endpoints for updating schema source
    endpoints = [
        # WorkspaceExplorer APIs
        (f"{CREATIO_URL}/0/rest/WorkspaceExplorerService/SaveSchemaSource", {"schemaUId": SCHEMA_UID, "source": NEW_CODE}),
        (f"{CREATIO_URL}/0/rest/WorkspaceExplorerService/UpdateSchemaSource", {"schemaUId": SCHEMA_UID, "source": NEW_CODE}),
        (f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/SaveSchemaSource", {"schemaUId": SCHEMA_UID, "source": NEW_CODE}),
        
        # SysPackageService APIs
        (f"{CREATIO_URL}/0/rest/SysPackageService/SaveSchemaSource", {"schemaUId": SCHEMA_UID, "source": NEW_CODE}),
        
        # SchemaDesigner APIs  
        (f"{CREATIO_URL}/0/rest/SchemaDesignerService/SaveSchema", {"schemaUId": SCHEMA_UID, "source": NEW_CODE}),
        
        # ServiceDesigner APIs
        (f"{CREATIO_URL}/0/rest/ServiceDesignerService/SaveSchemaSource", {"schemaUId": SCHEMA_UID, "source": NEW_CODE}),
        
        # SchemaManagerItem API
        (f"{CREATIO_URL}/0/rest/SchemaManagerItem/SaveSchema", {"schemaUId": SCHEMA_UID, "body": NEW_CODE}),
    ]
    
    print("\n=== Trying various update endpoints ===")
    for url, data in endpoints:
        try:
            response = session.post(url, json=data, headers=headers, timeout=30)
            endpoint_name = url.split("/0/")[-1][:50]
            print(f"{endpoint_name:50s} -> {response.status_code}")
            
            if response.status_code == 200:
                result = response.text[:200]
                print(f"  Response: {result}")
                
                # If successful, try to compile
                if "success" in result.lower() or "true" in result.lower():
                    print("  Attempting to compile...")
                    compile_url = f"{CREATIO_URL}/0/rest/WorkspaceExplorerService/Build"
                    compile_response = session.post(compile_url, headers=headers, timeout=120)
                    print(f"  Compile: {compile_response.status_code}")
                    
        except Exception as e:
            print(f"{url.split('/0/')[-1][:50]:50s} -> Error: {str(e)[:40]}")

    # Also try SysSchemaContent update
    print("\n=== Trying SysSchemaContent update via DataService ===")
    content_id = "7e46118c-7961-4f26-b051-7972e84d3d64"  # From previous query
    
    update_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/UpdateQuery"
    update_data = {
        "rootSchemaName": "SysSchemaContent",
        "operationType": 2,  # Update
        "columnValues": {
            "items": {
                "Content": {
                    "expressionType": 2,
                    "parameter": {
                        "dataValueType": 1,
                        "value": base64.b64encode(NEW_CODE.encode()).decode()
                    }
                }
            }
        },
        "filters": {
            "filterType": 6,
            "items": {
                "IdFilter": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "leftExpression": {"expressionType": 0, "columnPath": "Id"},
                    "rightExpression": {"expressionType": 2, "parameter": {"dataValueType": 0, "value": content_id}}
                }
            }
        }
    }
    
    response = session.post(update_url, json=update_data, headers=headers, timeout=60)
    print(f"DataService Update Status: {response.status_code}")
    print(f"Response: {response.text[:300]}")

if __name__ == "__main__":
    main()
