#!/usr/bin/env python3
import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

def main():
    session = requests.Session()
    
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    print("Login:", "OK" if response.status_code == 200 else "FAILED")
        
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }
    
    # Proper filter structure
    find_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    query = {
        "RootSchemaName": "SysSchema",
        "OperationType": 0,
        "Columns": {"Items": {
            "Id": {"Expression": {"ExpressionType": 0, "ColumnPath": "Id"}},
            "UId": {"Expression": {"ExpressionType": 0, "ColumnPath": "UId"}},
            "Name": {"Expression": {"ExpressionType": 0, "ColumnPath": "Name"}}
        }},
        "Filters": {
            "FilterType": 6,
            "RootSchemaName": "SysSchema",
            "Items": {
                "NameFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {
                        "ExpressionType": 0,
                        "ColumnPath": "Name"
                    },
                    "RightExpression": {
                        "ExpressionType": 2,
                        "Parameter": {
                            "DataValueType": 1,
                            "Value": "UsrExcelReportService"
                        }
                    }
                }
            }
        }
    }
    
    response = session.post(find_url, json=query, headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:800]}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("rows"):
            schema = data["rows"][0]
            print(f"\nFound: {schema}")
            schema_uid = schema.get("UId")
            
            # Get schema content
            get_url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeSchemaDesignerService.svc/GetSchema"
            get_response = session.post(get_url, json={"schemaUId": schema_uid}, headers=headers, timeout=30)
            print(f"\nGetSchema: {get_response.status_code}")
            if get_response.status_code == 200:
                result = get_response.json()
                print(f"Success: {result.get('success')}")
                if result.get("body"):
                    print(f"Body preview: {result.get('body')[:200]}...")

if __name__ == "__main__":
    main()
