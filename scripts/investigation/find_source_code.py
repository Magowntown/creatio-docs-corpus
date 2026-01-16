#!/usr/bin/env python3
"""
Find where source code is stored and how to update it.
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"

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

    # First get the schema Id (not UId)
    print("\n=== Getting SysSchema Id ===")
    select_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    select_data = {
        "rootSchemaName": "SysSchema",
        "operationType": 0,
        "columnValues": {
            "items": {
                "Id": {"expressionType": 0, "columnPath": "Id"},
                "Name": {"expressionType": 0, "columnPath": "Name"},
                "UId": {"expressionType": 0, "columnPath": "UId"},
            }
        },
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

    if response.status_code != 200:
        print(f"Error: {response.text[:500]}")
        return

    result = response.json()
    rows = result.get("rows", [])
    if not rows:
        print("Schema not found")
        return

    schema_id = rows[0].get("Id")
    schema_name = rows[0].get("Name")
    print(f"Schema: {schema_name}, Id: {schema_id}")

    # Try to get SysSchemaSource
    print("\n=== Trying SysSchemaSource ===")
    select_data = {
        "rootSchemaName": "SysSchemaSource",
        "operationType": 0,
        "allColumns": True,
        "filters": {
            "filterType": 6,
            "items": {
                "Schema": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "isEnabled": True,
                    "leftExpression": {"expressionType": 0, "columnPath": "Schema"},
                    "rightExpression": {
                        "expressionType": 2,
                        "parameter": {"dataValueType": 0, "value": schema_id}
                    }
                }
            }
        }
    }

    response = session.post(select_url, json=select_data, headers=headers, timeout=30)
    print(f"SysSchemaSource query: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        print(f"Found {len(rows)} source records")
        if rows:
            print(f"Columns: {list(rows[0].keys())}")

    # Try SysSchemaSourceCode
    print("\n=== Trying SysSchemaSourceCode ===")
    select_data["rootSchemaName"] = "SysSchemaSourceCode"
    response = session.post(select_url, json=select_data, headers=headers, timeout=30)
    print(f"SysSchemaSourceCode query: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        print(f"Found {len(rows)} source code records")
        if rows:
            print(f"Columns: {list(rows[0].keys())}")

    # Try to get available services
    print("\n=== Finding available designer services ===")
    test_urls = [
        "/0/rest/SourceCodeSchemaDesignerService",
        "/0/ServiceModel/SourceCodeSchemaDesignerService.svc",
        "/0/rest/ConfigurationBuilderService",
        "/0/ServiceModel/ConfigurationBuilderService.svc",
        "/0/rest/SourceCodeService",
        "/0/rest/PackageService",
    ]

    for url in test_urls:
        full_url = f"{CREATIO_URL}{url}"
        response = session.get(full_url, headers=headers, timeout=10)
        print(f"{url}: {response.status_code}")

    # Check if there's a metadata endpoint
    print("\n=== Checking MetaData column ===")
    select_data = {
        "rootSchemaName": "SysSchema",
        "operationType": 0,
        "columnValues": {
            "items": {
                "MetaData": {"expressionType": 0, "columnPath": "MetaData"},
            }
        },
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
    print(f"MetaData query: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        if rows and rows[0].get("MetaData"):
            metadata = rows[0]["MetaData"]
            print(f"MetaData length: {len(metadata)}")
            print(f"MetaData preview: {metadata[:500]}")

if __name__ == "__main__":
    main()
