#!/usr/bin/env python3
"""Get BGIntExcelreportMixin code via DataService."""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "a589d29b-9da7-4f66-836b-8e39fe0ca376"

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

    # Try different endpoints
    endpoints = [
        f"/0/rest/CreatioApiGateway/GetSchemaMetaData",
        f"/0/ServiceModel/SchemaDesignerService.svc/GetSchema",
        f"/0/rest/SchemaDesignerService/GetSchema",
    ]
    
    for endpoint in endpoints:
        url = f"{CREATIO_URL}{endpoint}"
        print(f"\nTrying: {endpoint}")
        response = session.post(url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Keys: {list(data.keys())[:10]}")
            except:
                print(f"Response: {response.text[:200]}")

    # Try OData for SysSchema
    print("\n=== Trying OData for SysClientUnitSchema ===")
    odata_url = f"{CREATIO_URL}/0/odata/SysClientUnitSchema"
    params = {"$filter": f"UId eq {SCHEMA_UID}"}
    response = session.get(odata_url, headers=headers, params=params, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        items = data.get("value", [])
        if items:
            print(f"Found {len(items)} items")
            print(f"Keys: {list(items[0].keys())}")
            # Look for Body or similar
            for key in ["Body", "body", "Source", "source"]:
                if key in items[0]:
                    val = items[0][key]
                    print(f"{key}: {str(val)[:500]}...")

    # Try direct SysSchema query
    print("\n=== Trying DataService SelectQuery ===")
    select_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    select_data = {
        "rootSchemaName": "SysClientUnitSchema",
        "operationType": 0,
        "allColumns": True,
        "filters": {
            "filterType": 6,
            "items": {
                "UId": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "isEnabled": True,
                    "leftExpression": {"expressionType": 0, "columnPath": "UId"},
                    "rightExpression": {
                        "expressionType": 2,
                        "parameter": {"dataValueType": 0, "value": SCHEMA_UID}
                    }
                }
            }
        }
    }
    response = session.post(select_url, json=select_data, headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        if rows:
            print(f"Columns: {list(rows[0].keys())}")
            # Check for body
            body = rows[0].get("Body", "")
            if body:
                print(f"\nBody length: {len(body)}")
                print(f"Body preview:\n{body[:2000]}")

if __name__ == "__main__":
    main()
