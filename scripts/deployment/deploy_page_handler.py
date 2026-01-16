#!/usr/bin/env python3
"""
Deploy the updated UsrPage_ebkv9e8 handler with Year-Month and Sales Rep filter support.
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

    # Get existing schema
    print("\n=== Getting current schema ===")
    get_url = f"{CREATIO_URL}/0/rest/ClientUnitSchemaDesignerService/GetSchemaData"
    response = session.post(get_url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)

    if response.status_code != 200:
        print(f"Failed: {response.status_code}")
        print(response.text[:500])
        return False

    schema_data = response.json()
    print(f"Got schema: {schema_data.get('name', 'N/A')}")
    print(f"Schema keys: {list(schema_data.keys())}")

    # Update body
    schema_data["body"] = HANDLER_CODE

    # Save
    print("\n=== Saving updated handler code ===")
    save_url = f"{CREATIO_URL}/0/rest/ClientUnitSchemaDesignerService/SaveSchema"
    response = session.post(save_url, json=schema_data, headers=headers, timeout=60)

    if response.status_code != 200:
        print(f"Save failed: {response.status_code}")
        print(response.text[:500])
        return False

    result = response.json()
    print(f"Save result: {json.dumps(result, indent=2)[:500]}")

    if result.get("success") == False:
        print(f"Save error: {result}")
        return False

    # Compile
    print("\n=== Compiling ===")
    compile_and_test(session, headers)

def compile_and_test(session, headers):
    import time

    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"

    for attempt in range(5):
        print(f"Build attempt {attempt + 1}...")
        try:
            response = session.post(build_url, json={}, headers=headers, timeout=300)

            if response.status_code != 200:
                print(f"HTTP Error: {response.status_code}")
                time.sleep(10)
                continue

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
                    print(f"Compilation error: {error[:500]}")
                    return False
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

    return False

if __name__ == "__main__":
    main()
