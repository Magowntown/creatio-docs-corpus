#!/usr/bin/env python3
"""
Try to update schema via package export/import or DataService
"""

import os
import requests
import json
import base64

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
    
    # Try to get the current schema content
    print("\n=== Getting current schema content ===")
    
    # Find in SysSchemaContent
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    query = {
        "RootSchemaName": "SysSchemaContent",
        "OperationType": 0,
        "Columns": {"Items": {
            "Id": {"Expression": {"ExpressionType": 0, "ColumnPath": "Id"}},
            "Content": {"Expression": {"ExpressionType": 0, "ColumnPath": "Content"}},
            "ContentType": {"Expression": {"ExpressionType": 0, "ColumnPath": "ContentType"}}
        }},
        "Filters": {
            "FilterType": 6,
            "Items": {
                "SchemaFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {"ExpressionType": 0, "ColumnPath": "SysSchema.Name"},
                    "RightExpression": {"ExpressionType": 2, "Parameter": {"DataValueType": 1, "Value": "UsrExcelReportService"}}
                }
            }
        }
    }
    
    response = session.post(url, json=query, headers=headers, timeout=30)
    print(f"SysSchemaContent query: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("rows"):
            for row in data["rows"]:
                content_type = row.get("ContentType", "")
                content_id = row.get("Id", "")
                print(f"  Found: ContentType={content_type}, Id={content_id}")
                
                # The Content might be the actual code
                content = row.get("Content", "")
                if content and len(content) > 50:
                    print(f"  Content preview: {content[:200]}...")
        else:
            print("  No schema content found")
    
    # Try the SourceCodeEditService
    print("\n=== Trying SourceCodeEditService ===")
    edit_url = f"{CREATIO_URL}/0/rest/SourceCodeEditService/GetContent"
    response = session.post(edit_url, json={
        "schemaName": "UsrExcelReportService"
    }, headers=headers, timeout=30)
    print(f"GetContent status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.text[:500]}")
    elif response.status_code == 404:
        print("Service not found")
    
    # List available services related to source code
    print("\n=== Available service endpoints ===")
    services_to_try = [
        "SourceCodeEditService/GetSchemaCode",
        "SourceCodeEditService/SaveSchemaCode", 
        "ConfigurationService/GetSchemaClientCode",
        "SchemaDesignerService/GetSchema"
    ]
    
    for service in services_to_try:
        test_url = f"{CREATIO_URL}/0/rest/{service}"
        response = session.post(test_url, json={}, headers=headers, timeout=10)
        print(f"  {service}: {response.status_code}")

if __name__ == "__main__":
    main()
