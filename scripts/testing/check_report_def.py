#!/usr/bin/env python3
"""
Check the report definition in IntExcelReport table
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

def login(session):
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    return response.status_code == 200

def get_report_config(session, report_id):
    """Get report configuration from IntExcelReport table"""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    query = {
        "RootSchemaName": "IntExcelReport",
        "OperationType": 0,
        "AllColumns": True,
        "Filters": {
            "FilterType": 1,
            "Items": {
                "IdFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {"ColumnPath": "Id"},
                    "RightExpression": {"ParameterValue": report_id, "Type": 0}
                }
            }
        }
    }

    response = session.post(url, json=query, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("rows") and len(data["rows"]) > 0:
            return data["rows"][0]
    return None

def main():
    session = requests.Session()
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")

    report_id = "4ba4f203-7088-41dc-b86d-130c590b3594"
    print(f"\nGetting report config for: {report_id}")

    config = get_report_config(session, report_id)
    if config:
        print("\n=== Report Configuration ===")
        for key, value in config.items():
            if key == "IntFile":
                print(f"{key}: [BINARY DATA - {len(str(value)) if value else 0} chars]")
            elif key == "IntFilterConfig" or key == "IntFiltersConfig":
                print(f"\n{key}:")
                if value:
                    try:
                        parsed = json.loads(value)
                        print(json.dumps(parsed, indent=2))
                    except:
                        print(f"  (raw): {value[:500]}...")
                else:
                    print("  (empty)")
            else:
                val_str = str(value)[:200] if value else "(null)"
                print(f"{key}: {val_str}")
    else:
        print("Report not found!")

if __name__ == "__main__":
    main()
