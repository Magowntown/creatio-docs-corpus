#!/usr/bin/env python3
import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

def main():
    session = requests.Session()
    
    print("Logging in...")
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    if response.status_code != 200:
        print("Login failed")
        return
        
    print("Login successful!")
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }
    
    # Find schema
    print("\nFinding schema...")
    find_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    query = {
        "RootSchemaName": "SysSchema",
        "OperationType": 0,
        "Columns": {"Items": {
            "Id": {"Expression": {"ColumnPath": "Id"}},
            "UId": {"Expression": {"ColumnPath": "UId"}},
            "Name": {"Expression": {"ColumnPath": "Name"}}
        }},
        "Filters": {
            "FilterType": 1,
            "Items": {
                "NameFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {"ColumnPath": "Name"},
                    "RightExpression": {"ParameterValue": "UsrExcelReportService", "Type": 0}
                }
            }
        }
    }
    
    try:
        response = session.post(find_url, json=query, headers=headers, timeout=30)
        print(f"FindSchema status: {response.status_code}")
        print(f"FindSchema response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("rows"):
                schema = data["rows"][0]
                schema_uid = schema.get("UId")
                print(f"\nFound schema UId: {schema_uid}")
                
                # Try to get schema
                print("\nGetting schema...")
                get_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/GetSchema"
                get_response = session.post(get_url, json={"schemaUId": schema_uid}, headers=headers, timeout=30)
                print(f"GetSchema status: {get_response.status_code}")
                print(f"GetSchema response: {get_response.text[:800]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
