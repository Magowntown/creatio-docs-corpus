#!/usr/bin/env python3
"""
Fetch process schema metadata from Creatio via DataService API.

Usage:
    source .env && python3 scripts/investigation/fetch_process_schema.py <process_uid>

Example:
    source .env && python3 scripts/investigation/fetch_process_schema.py 8cdd4845-4b27-45cd-9907-e9cc478bc3c5
"""

import os
import sys
import json
import requests
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv

load_dotenv()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")


def login(session):
    """Authenticate with Creatio"""
    response = session.post(
        f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
        json={"UserName": USERNAME, "UserPassword": PASSWORD}
    )
    if response.status_code == 200:
        result = response.json()
        return result.get("Code", -1) == 0
    return False


def query_entity(session, root_schema, filters, columns=None):
    """Execute SelectQuery against DataService"""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    query = {
        "RootSchemaName": root_schema,
        "OperationType": 0,
        "AllColumns": columns is None,
        "Filters": filters
    }

    if columns:
        query["Columns"] = {"Items": {col: {"Expression": {"ColumnPath": col}} for col in columns}}

    response = session.post(url, json=query, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Query failed: {response.status_code}")
        print(response.text[:500])
        return None


def get_process_schema(session, process_uid):
    """Get process schema from SysSchema table"""
    filters = {
        "FilterType": 1,
        "ComparisonType": 3,  # Equal
        "LeftExpression": {"ExpressionType": 0, "ColumnPath": "UId"},
        "RightExpression": {"ExpressionType": 2, "Parameter": {"DataValueType": 0, "Value": process_uid}}
    }

    return query_entity(session, "SysSchema", filters)


def get_process_schema_by_name(session, process_name):
    """Get process schema by Name"""
    filters = {
        "FilterType": 1,
        "ComparisonType": 3,  # Equal
        "LeftExpression": {"ExpressionType": 0, "ColumnPath": "Name"},
        "RightExpression": {"ExpressionType": 2, "Parameter": {"DataValueType": 1, "Value": process_name}}
    }

    return query_entity(session, "SysSchema", filters)


def get_process_enabled_status(session, process_name):
    """Check if process is enabled via VwSysSchemaInWorkspace"""
    filters = {
        "FilterType": 1,
        "Items": {
            "NameFilter": {
                "FilterType": 1,
                "ComparisonType": 3,
                "LeftExpression": {"ColumnPath": "Name"},
                "RightExpression": {"ParameterValue": process_name, "Type": 1}
            }
        }
    }

    # Try VwSysSchemaInWorkspace which has Enabled column
    result = query_entity(session, "VwSysSchemaInWorkspace", filters)
    return result


def list_commission_processes(session):
    """List all commission-related processes"""
    # Query each process individually since StartsWith filter syntax is complex
    process_names = [
        "IWCalculateCommissiononPayment",
        "IWCalculateCommissiononPaymentV2",
        "IWCalculateCommissiononPaymentIWQBIntegrationV3",
        "IWCalculateCommissiononPaymentCustomV4"
    ]

    results = []
    for name in process_names:
        filters = {
            "FilterType": 1,
            "ComparisonType": 3,
            "LeftExpression": {"ExpressionType": 0, "ColumnPath": "Name"},
            "RightExpression": {"ExpressionType": 2, "Parameter": {"DataValueType": 1, "Value": name}}
        }
        result = query_entity(session, "SysSchema", filters)
        if result and result.get("rows"):
            results.extend(result["rows"])

    return {"rows": results}


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_process_schema.py <process_uid_or_name>")
        print("       python fetch_process_schema.py --list-commission")
        sys.exit(1)

    session = requests.Session()

    print(f"Connecting to: {CREATIO_URL}")
    if not login(session):
        print("Login failed! Check CREATIO_USERNAME and CREATIO_PASSWORD in .env")
        sys.exit(1)

    print("Login successful!\n")

    arg = sys.argv[1]

    if arg == "--list-commission":
        print("=== Commission Processes ===\n")
        result = list_commission_processes(session)
        if result and result.get("rows"):
            for row in result["rows"]:
                enabled = row.get("Enabled", "?")
                enabled_str = "✅ ENABLED" if enabled else "❌ DISABLED"
                print(f"{row.get('Name', '?')}")
                print(f"  UId: {row.get('UId', '?')}")
                print(f"  Status: {enabled_str}")
                print(f"  Caption: {row.get('Caption', '?')}")
                print(f"  Modified: {row.get('ModifiedOn', '?')}")
                print()
        else:
            print("No processes found or query failed")
        return

    # Check if arg looks like a GUID
    is_guid = len(arg) == 36 and arg.count('-') == 4

    if is_guid:
        print(f"Fetching process by UId: {arg}\n")
        result = get_process_schema(session, arg)
    else:
        print(f"Fetching process by Name: {arg}\n")
        result = get_process_schema_by_name(session, arg)

    if result and result.get("rows"):
        row = result["rows"][0]
        print("=== Process Schema ===\n")

        # Display key fields
        important_fields = ["Id", "UId", "Name", "Caption", "ManagerName", "Enabled",
                          "ModifiedOn", "CreatedOn", "SysPackage", "Parent"]

        for field in important_fields:
            if field in row:
                value = row[field]
                if isinstance(value, dict):
                    value = value.get("displayValue", value.get("value", str(value)))
                print(f"{field}: {value}")

        print("\n=== All Fields ===\n")
        for key, value in sorted(row.items()):
            if key in ["MetaData", "MetaDataModifiedOn"]:
                print(f"{key}: [BINARY/LARGE DATA]")
            elif isinstance(value, dict):
                print(f"{key}: {json.dumps(value, indent=2)}")
            else:
                val_str = str(value)[:200] if value else "(null)"
                print(f"{key}: {val_str}")
    else:
        print("Process not found or query failed")
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
