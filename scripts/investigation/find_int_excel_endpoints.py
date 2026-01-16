#!/usr/bin/env python3
"""Find all IntExcelExport related endpoints that exist."""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

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

    # Query SysSchema to find IntExcelExport related services
    print("\n=== Searching for IntExcelExport service schemas ===")
    search_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    search_data = {
        "rootSchemaName": "SysSchema",
        "operationType": 0,
        "columns": {
            "items": {
                "Name": {"expression": {"columnPath": "Name"}},
                "UId": {"expression": {"columnPath": "UId"}},
                "ManagerName": {"expression": {"columnPath": "ManagerName"}},
                "SysPackage": {"expression": {"columnPath": "SysPackage.Name"}}
            }
        },
        "filters": {
            "filterType": 6,
            "items": {
                "NameFilter": {
                    "filterType": 1,
                    "comparisonType": 2,  # Contains
                    "leftExpression": {"expressionType": 0, "columnPath": "Name"},
                    "rightExpression": {"expressionType": 2, "parameter": {"dataValueType": 1, "value": "IntExcel"}}
                }
            }
        }
    }
    
    response = session.post(search_url, json=search_data, headers=headers, timeout=30)
    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        print(f"Found {len(rows)} IntExcel-related schemas:")
        for row in rows:
            print(f"  - {row.get('Name')} ({row.get('ManagerName')}) in {row.get('SysPackage')}")
    else:
        print(f"Error: {response.status_code}")

    # Try to call the IntExcelReportService directly to get its methods
    print("\n=== Trying to call GetMethods on our UsrExcelReportService ===")
    response = session.get(f"{CREATIO_URL}/0/rest/UsrExcelReportService/GetMethods", headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Methods: {result.get('message', 'N/A')[:500]}")

    # Check if IntExcelReport entity has any file storage columns
    print("\n=== Checking IntExcelReport schema ===")
    search_data = {
        "rootSchemaName": "IntExcelReport",
        "operationType": 0,
        "allColumns": True,
        "rowCount": 1
    }
    
    response = session.post(search_url, json=search_data, headers=headers, timeout=30)
    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        if rows:
            print(f"IntExcelReport columns: {list(rows[0].keys())}")
        else:
            print("No IntExcelReport records found")

if __name__ == "__main__":
    main()
