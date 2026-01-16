#!/usr/bin/env python3
"""
Investigate the relationship between UsrReportesPampa and IntExcelReport tables.
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

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

    # Step 1: Get ALL columns from UsrReportesPampa
    print("\n" + "="*60)
    print("=== Querying UsrReportesPampa with allColumns ===")
    print("="*60)

    esq_url = f"{CREATIO_URL}/0/dataservice/json/SyncReply/SelectQuery"
    esq_body = {
        "rootSchemaName": "UsrReportesPampa",
        "operationType": 0,
        "allColumns": True,
        "rowCount": 5
    }
    response = session.post(esq_url, json=esq_body, headers=headers, timeout=30)

    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        if rows:
            print(f"\nFound {len(rows)} records. Columns in UsrReportesPampa:")
            for col in sorted(rows[0].keys()):
                print(f"  - {col}: {rows[0][col]}")

            # Look for foreign key columns
            print("\n=== Looking for IntExcelReport foreign key columns ===")
            for col in rows[0].keys():
                col_lower = col.lower()
                if "excel" in col_lower or "report" in col_lower or "int" in col_lower:
                    print(f"  >> Potential FK: {col} = {rows[0][col]}")
        else:
            print("No rows found in UsrReportesPampa")
            print(f"Response: {json.dumps(data, indent=2)[:500]}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text[:500])

    # Step 2: Try OData metadata for schema info
    print("\n" + "="*60)
    print("=== Querying via OData ===")
    print("="*60)

    odata_url = f"{CREATIO_URL}/0/odata/UsrReportesPampa?$top=5"
    response = session.get(odata_url, headers=headers, timeout=30)

    if response.status_code == 200:
        data = response.json()
        items = data.get("value", [])
        if items:
            print(f"\nOData columns in UsrReportesPampa:")
            for col in sorted(items[0].keys()):
                print(f"  - {col}: {items[0][col]}")
        else:
            print("No OData rows returned")
    else:
        print(f"OData Error: {response.status_code}")
        print(response.text[:300])

    # Step 3: Get IntExcelReport entries
    print("\n" + "="*60)
    print("=== Querying IntExcelReport for Commission ===")
    print("="*60)

    esq_body = {
        "rootSchemaName": "IntExcelReport",
        "operationType": 0,
        "allColumns": True,
        "rowCount": 50
    }
    response = session.post(esq_url, json=esq_body, headers=headers, timeout=30)

    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        print(f"\nFound {len(rows)} IntExcelReport records")

        if rows:
            # Show columns
            print("\nColumns in IntExcelReport:")
            for col in sorted(rows[0].keys()):
                print(f"  - {col}")

            # Find Commission report
            print("\n=== Looking for Commission report ===")
            for row in rows:
                name = row.get("IntName", row.get("Name", ""))
                if "commission" in str(name).lower():
                    print(f"\nCommission Report found:")
                    for k, v in row.items():
                        print(f"  {k}: {v}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text[:500])

    # Step 4: Try to find direct FK relationship
    print("\n" + "="*60)
    print("=== Comparing IDs ===")
    print("="*60)

    # Get Commission from UsrReportesPampa
    esq_body = {
        "rootSchemaName": "UsrReportesPampa",
        "operationType": 0,
        "allColumns": True,
        "filters": {
            "filterType": 6,
            "items": {
                "CommissionFilter": {
                    "filterType": 1,
                    "comparisonType": 2,  # Contains
                    "leftExpression": {"columnPath": "Name"},
                    "rightExpression": {"parameter": {"dataValueType": 1, "value": "Commission"}}
                }
            }
        }
    }
    response = session.post(esq_url, json=esq_body, headers=headers, timeout=30)

    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        if rows:
            print(f"\nUsrReportesPampa 'Commission' entry:")
            for k, v in rows[0].items():
                print(f"  {k}: {v}")
        else:
            print("Commission not found with Contains filter, trying exact match...")
            # Try without filter to see all records
            esq_body = {
                "rootSchemaName": "UsrReportesPampa",
                "operationType": 0,
                "allColumns": True,
                "rowCount": 10
            }
            response = session.post(esq_url, json=esq_body, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                rows = data.get("rows", [])
                print(f"\nAll UsrReportesPampa entries ({len(rows)} records):")
                for row in rows:
                    print(f"\n  Name: {row.get('Name', 'N/A')}")
                    print(f"  Id: {row.get('Id', 'N/A')}")
                    # Print any potential FK columns
                    for k, v in row.items():
                        if k not in ['Name', 'Id', 'CreatedOn', 'ModifiedOn', 'CreatedById', 'ModifiedById']:
                            print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
