#!/usr/bin/env python3
"""
Find all IntExcelReport entries
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

def find_reports(session):
    """Get all reports"""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    query = {
        "RootSchemaName": "IntExcelReport",
        "OperationType": 0,
        "Columns": {
            "Items": {
                "Id": {"Expression": {"ColumnPath": "Id"}},
                "IntName": {"Expression": {"ColumnPath": "IntName"}},
                "IntEntity": {"Expression": {"ColumnPath": "IntEntity"}},
                "IntFilterConfig": {"Expression": {"ColumnPath": "IntFilterConfig"}}
            }
        },
        "RowCount": 50
    }

    response = session.post(url, json=query, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("rows", [])
    else:
        print(f"Error: {response.status_code}")
        print(response.text[:500])
    return []

def main():
    session = requests.Session()
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")

    reports = find_reports(session)
    print(f"\nFound {len(reports)} reports:\n")

    for report in reports:
        report_id = report.get("Id", "N/A")
        name = report.get("IntName", "N/A")
        entity = report.get("IntEntity", "N/A")
        filter_config = report.get("IntFilterConfig", "")

        print(f"ID: {report_id}")
        print(f"Name: {name}")
        print(f"Entity: {entity}")

        if filter_config:
            print(f"FilterConfig preview: {filter_config[:200]}...")
            try:
                parsed = json.loads(filter_config)
                print(f"FilterConfig keys: {list(parsed.keys()) if isinstance(parsed, dict) else 'array'}")
            except:
                pass
        else:
            print("FilterConfig: (empty)")
        print("-" * 50)

if __name__ == "__main__":
    main()
