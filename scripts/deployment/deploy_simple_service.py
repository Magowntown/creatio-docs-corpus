#!/usr/bin/env python3
"""Deploy UsrExcelReportService_Simple.cs to Creatio DEV via API.

This script:
1. Reads the C# source file from the repo
2. Updates the SysSchemaContent record via DataService
3. Triggers compilation via WorkspaceExplorerService
4. Tests the deployed service

Usage:
    source .env
    python3 scripts/deployment/deploy_simple_service.py
"""

import json
import os
import sys
import time
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv

load_dotenv()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com").rstrip("/")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
TIMEOUT = int(os.environ.get("CREATIO_TIMEOUT_SECONDS", "120"))

# UsrExcelReportService schema content ID (from schema designer URL)
CONTENT_ID = "ad87ec24-9520-4178-b0a8-2ea17e47b460"

# Source file path
SOURCE_FILE = REPO_ROOT / "source-code" / "UsrExcelReportService_Simple.cs"


def login(session):
    """Login to Creatio and return headers with CSRF token."""
    resp = session.post(
        f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
        json={"UserName": USERNAME, "UserPassword": PASSWORD},
        timeout=TIMEOUT,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Login failed: {resp.status_code}")
    return {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", ""),
    }


def update_schema_content(session, headers, content_id, new_code):
    """Update schema content via DataService UpdateQuery."""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/UpdateQuery"
    query = {
        "RootSchemaName": "SysSchemaContent",
        "OperationType": 1,  # Update
        "ColumnValues": {
            "Items": {
                "Content": {
                    "ExpressionType": 2,
                    "Parameter": {
                        "DataValueType": 1,
                        "Value": new_code
                    }
                }
            }
        },
        "Filters": {
            "FilterType": 6,
            "Items": {
                "IdFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {"ExpressionType": 0, "ColumnPath": "Id"},
                    "RightExpression": {
                        "ExpressionType": 2,
                        "Parameter": {"DataValueType": 0, "Value": content_id}
                    }
                }
            }
        }
    }

    resp = session.post(url, json=query, headers=headers, timeout=TIMEOUT)
    return resp.json()


def trigger_build(session, headers, max_attempts=5):
    """Trigger compilation and wait for completion."""
    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"

    for attempt in range(1, max_attempts + 1):
        print(f"  Build attempt {attempt}/{max_attempts}...")
        time.sleep(5)

        resp = session.post(build_url, json={}, headers=headers, timeout=120)
        result = resp.json()

        if result.get("success"):
            return True, "Compilation successful"

        error = result.get("errorInfo", {}).get("message", "")
        if "another compilation" in error.lower():
            print(f"  Waiting for other compilation to finish...")
            time.sleep(15)
            continue

        # Check for compilation errors
        errors = result.get("errors", [])
        if errors:
            return False, f"Compilation failed: {errors[:5]}"

        return False, f"Build failed: {error}"

    return False, "Build timed out after max attempts"


def test_service(session, headers):
    """Test the deployed service."""
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
    data = {
        "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",  # Commission report
        "YearMonthId": "00000000-0000-0000-0000-000000000000",
        "SalesRepId": "00000000-0000-0000-0000-000000000000",
        "ExecutionId": "00000000-0000-0000-0000-000000000000",
        "RecordCollection": []
    }

    try:
        resp = session.post(url, json=data, headers=headers, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        return {"success": False, "message": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def main():
    if not USERNAME or not PASSWORD:
        print("ERROR: Set CREATIO_USERNAME and CREATIO_PASSWORD")
        sys.exit(1)

    if not SOURCE_FILE.exists():
        print(f"ERROR: Source file not found: {SOURCE_FILE}")
        sys.exit(1)

    print(f"=== Deploying UsrExcelReportService to {CREATIO_URL} ===")
    print(f"Source: {SOURCE_FILE}")

    # Read source code
    code = SOURCE_FILE.read_text(encoding="utf-8")
    print(f"Code length: {len(code)} chars")

    session = requests.Session()

    # Login
    print("\n=== Login ===")
    headers = login(session)
    print("Login: OK")

    # Update schema content
    print("\n=== Updating schema content ===")
    result = update_schema_content(session, headers, CONTENT_ID, code)

    if not result.get("success"):
        print(f"ERROR: Update failed: {result}")
        sys.exit(1)

    print("Schema content updated")

    # Trigger build
    print("\n=== Compiling ===")
    success, msg = trigger_build(session, headers)

    if not success:
        print(f"ERROR: {msg}")
        sys.exit(1)

    print(f"Build: {msg}")

    # Test service
    print("\n=== Testing service ===")
    result = test_service(session, headers)
    print(f"Test result: {json.dumps(result, indent=2)}")

    if result.get("success"):
        print("\n✅ Deployment successful!")
        print(f"Message: {result.get('message')}")
        print(f"Cache key: {result.get('key')}")
    else:
        print(f"\n⚠️ Service responded but with error: {result.get('message')}")


if __name__ == "__main__":
    main()
