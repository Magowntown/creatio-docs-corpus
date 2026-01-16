#!/usr/bin/env python3
"""Check the actual column names in BGCommissionReportDataView."""

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

    # Get schema columns via OData metadata or by querying the data
    print("\n=== Getting BGCommissionReportDataView columns ===")
    
    # Try OData query to see column names
    odata_url = f"{CREATIO_URL}/0/odata/BGCommissionReportDataView?$top=1"
    response = session.get(odata_url, headers=headers, timeout=30)
    print(f"OData Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        items = data.get("value", [])
        if items:
            print(f"Columns found: {list(items[0].keys())}")
        else:
            print("No data, but checking @odata.context for schema info...")
            print(f"Context: {data.get('@odata.context', 'N/A')}")
    else:
        print(f"Error: {response.text[:300]}")

    # Also try DataService SelectQuery with allColumns
    print("\n=== Trying DataService SelectQuery ===")
    select_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    select_data = {
        "rootSchemaName": "BGCommissionReportDataView",
        "operationType": 0,
        "allColumns": True,
        "rowCount": 1
    }
    
    response = session.post(select_url, json=select_data, headers=headers, timeout=30)
    print(f"DataService Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        if rows:
            print(f"\nAll columns:\n{json.dumps(list(rows[0].keys()), indent=2)}")
            
            # Look for Year-Month and Sales Group related columns
            for col in rows[0].keys():
                if "year" in col.lower() or "month" in col.lower() or "sales" in col.lower() or "group" in col.lower():
                    print(f"  >> Potential filter column: {col} = {rows[0][col]}")
        else:
            print("No rows returned")
            # Check if there are rowsAffected or other info
            print(f"Full response: {json.dumps(result, indent=2)[:500]}")

if __name__ == "__main__":
    main()
