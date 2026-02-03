#!/usr/bin/env python3
"""
Fetch page schemas from PROD to understand BGlobal's original architecture.

Targets:
- BGPage_iaptpa6 (GUID: 4c777639-49df-4569-bd4e-adb72ce0ff56) - "Rpt Excel" legacy page
- UsrPage_ebkv9e8 - Current page (ExtendParent=true)
- BGlobalLookerStudio_UsrPage_ebkv9e8 - Parent schema

Usage:
    source .env && python3 scripts/investigation/fetch_page_schemas.py
"""

import os
import sys
import json
import requests
from urllib.parse import urljoin

# Load from environment
BASE_URL = os.getenv("CREATIO_URL", "https://pampabay.creatio.com")
USERNAME = os.getenv("CREATIO_USERNAME")
PASSWORD = os.getenv("CREATIO_PASSWORD")

# Schema GUIDs to fetch
SCHEMAS = {
    "BGPage_iaptpa6": "4c777639-49df-4569-bd4e-adb72ce0ff56",
    "UsrPage_ebkv9e8": "561d9dd4-8bf2-4f63-a781-54ac48a74972",
}


def login(session: requests.Session) -> str:
    """Login and return BPMCSRF token."""
    login_url = urljoin(BASE_URL, "/ServiceModel/AuthService.svc/Login")
    payload = {"UserName": USERNAME, "UserPassword": PASSWORD}

    response = session.post(login_url, json=payload)
    response.raise_for_status()

    result = response.json()
    if result.get("Code") != 0:
        raise Exception(f"Login failed: {result.get('Message', 'Unknown error')}")

    bpmcsrf = session.cookies.get("BPMCSRF")
    if not bpmcsrf:
        raise Exception("BPMCSRF cookie not found after login")

    return bpmcsrf


def fetch_schema(session: requests.Session, bpmcsrf: str, schema_name: str, schema_uid: str) -> dict:
    """Fetch a schema by its UID."""

    # Try ClientUnitSchemaManager (Freedom UI pages)
    url = urljoin(BASE_URL, f"/0/rest/CreatioApiGateway/GetPackageSchema")

    # First, try to get schema info from SysSchema
    odata_url = urljoin(BASE_URL, f"/0/odata/SysSchema")
    params = {
        "$filter": f"UId eq {schema_uid}",
        "$select": "UId,Name,Caption,ManagerName,ExtendParent,ParentUId"
    }

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": bpmcsrf
    }

    response = session.get(odata_url, params=params, headers=headers)
    response.raise_for_status()
    result = response.json()

    schema_info = {}
    if result.get("value") and len(result["value"]) > 0:
        schema_info = result["value"][0]
        print(f"\n=== {schema_name} ===")
        print(f"UId: {schema_info.get('UId')}")
        print(f"Name: {schema_info.get('Name')}")
        print(f"Caption: {schema_info.get('Caption')}")
        print(f"ManagerName: {schema_info.get('ManagerName')}")
        print(f"ExtendParent: {schema_info.get('ExtendParent')}")
        print(f"ParentUId: {schema_info.get('ParentUId')}")
    else:
        print(f"\n=== {schema_name} ===")
        print("Not found in SysSchema via OData")

    return schema_info


def fetch_schema_source(session: requests.Session, bpmcsrf: str, schema_name: str) -> str:
    """Fetch actual schema source code."""

    # Use DataService to get schema body
    url = urljoin(BASE_URL, "/0/DataService/json/SyncReply/SelectQuery")
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": bpmcsrf
    }

    esq_body = {
        "rootSchemaName": "SysSchema",
        "operationType": 0,
        "columns": {
            "items": {
                "Name": {"expression": {"columnPath": "Name"}},
                "Caption": {"expression": {"columnPath": "Caption"}},
                "ManagerName": {"expression": {"columnPath": "ManagerName"}},
                "ExtendParent": {"expression": {"columnPath": "ExtendParent"}},
                "ParentUId": {"expression": {"columnPath": "ParentUId"}},
                "SysPackage": {"expression": {"columnPath": "SysPackage.Name"}},
            }
        },
        "filters": {
            "items": {
                "nameFilter": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "leftExpression": {"columnPath": "Name"},
                    "rightExpression": {"parameter": {"value": schema_name}}
                }
            }
        }
    }

    response = session.post(url, headers=headers, json=esq_body)
    response.raise_for_status()
    result = response.json()

    if result.get("rows") and len(result["rows"]) > 0:
        row = result["rows"][0]
        print(f"\n=== {schema_name} (from SysSchema ESQ) ===")
        print(f"Name: {row.get('Name')}")
        print(f"Caption: {row.get('Caption')}")
        print(f"ManagerName: {row.get('ManagerName')}")
        print(f"ExtendParent: {row.get('ExtendParent')}")
        print(f"ParentUId: {row.get('ParentUId')}")
        print(f"Package: {row.get('SysPackage', {}).get('displayValue', 'Unknown')}")
        return row

    return None


def find_parent_hierarchy(session: requests.Session, bpmcsrf: str, schema_name: str):
    """Find the parent schema hierarchy."""
    url = urljoin(BASE_URL, "/0/DataService/json/SyncReply/SelectQuery")
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": bpmcsrf
    }

    # Get all schemas that could be in the hierarchy
    schemas_to_check = [schema_name]
    hierarchy = []

    while schemas_to_check:
        current = schemas_to_check.pop(0)

        esq_body = {
            "rootSchemaName": "SysSchema",
            "operationType": 0,
            "columns": {
                "items": {
                    "UId": {"expression": {"columnPath": "UId"}},
                    "Name": {"expression": {"columnPath": "Name"}},
                    "Caption": {"expression": {"columnPath": "Caption"}},
                    "ManagerName": {"expression": {"columnPath": "ManagerName"}},
                    "ExtendParent": {"expression": {"columnPath": "ExtendParent"}},
                    "Parent": {"expression": {"columnPath": "Parent.Name"}},
                    "ParentUId": {"expression": {"columnPath": "ParentUId"}},
                    "SysPackage": {"expression": {"columnPath": "SysPackage.Name"}},
                }
            },
            "filters": {
                "items": {
                    "nameFilter": {
                        "filterType": 1,
                        "comparisonType": 3,
                        "leftExpression": {"columnPath": "Name"},
                        "rightExpression": {"parameter": {"value": current}}
                    }
                }
            }
        }

        response = session.post(url, headers=headers, json=esq_body)
        response.raise_for_status()
        result = response.json()

        if result.get("rows") and len(result["rows"]) > 0:
            row = result["rows"][0]
            hierarchy.append({
                "name": row.get("Name"),
                "caption": row.get("Caption"),
                "manager": row.get("ManagerName"),
                "extend_parent": row.get("ExtendParent"),
                "parent_name": row.get("Parent", {}).get("displayValue") if row.get("Parent") else None,
                "parent_uid": row.get("ParentUId"),
                "package": row.get("SysPackage", {}).get("displayValue")
            })

            # If has parent, add to check list
            parent_name = row.get("Parent", {}).get("displayValue") if row.get("Parent") else None
            if parent_name and parent_name not in [h["name"] for h in hierarchy]:
                schemas_to_check.append(parent_name)

    return hierarchy


def main():
    if not USERNAME or not PASSWORD:
        print("Error: CREATIO_USERNAME and CREATIO_PASSWORD must be set")
        sys.exit(1)

    print(f"Connecting to {BASE_URL}...")

    session = requests.Session()

    try:
        bpmcsrf = login(session)
        print("Login successful!")

        # Fetch each schema
        for name, uid in SCHEMAS.items():
            fetch_schema(session, bpmcsrf, name, uid)
            fetch_schema_source(session, bpmcsrf, name)

        # Find hierarchy for UsrPage_ebkv9e8
        print("\n" + "=" * 60)
        print("SCHEMA HIERARCHY for UsrPage_ebkv9e8")
        print("=" * 60)

        hierarchy = find_parent_hierarchy(session, bpmcsrf, "UsrPage_ebkv9e8")
        for i, schema in enumerate(hierarchy):
            indent = "  " * i
            print(f"{indent}└── {schema['name']} ({schema['package']})")
            print(f"{indent}    Caption: {schema['caption']}")
            print(f"{indent}    ExtendParent: {schema['extend_parent']}")
            if schema['parent_name']:
                print(f"{indent}    Parent: {schema['parent_name']}")

        # Find hierarchy for BGPage_iaptpa6
        print("\n" + "=" * 60)
        print("SCHEMA HIERARCHY for BGPage_iaptpa6")
        print("=" * 60)

        hierarchy = find_parent_hierarchy(session, bpmcsrf, "BGPage_iaptpa6")
        for i, schema in enumerate(hierarchy):
            indent = "  " * i
            print(f"{indent}└── {schema['name']} ({schema['package']})")
            print(f"{indent}    Caption: {schema['caption']}")
            print(f"{indent}    ExtendParent: {schema['extend_parent']}")
            if schema['parent_name']:
                print(f"{indent}    Parent: {schema['parent_name']}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
