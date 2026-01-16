#!/usr/bin/env python3
"""
Update BGIntExcelReportService2 via Creatio API to add 'public' keyword
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
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    print("Login:", "OK" if response.status_code == 200 else "FAILED")
    
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }
    
    schema_uid = "ff5499a9-4aec-4403-9511-3394370035d3"
    
    # Try SourceCodeDesignerService
    print("\n=== Trying SourceCodeDesignerService ===")
    
    # Get current schema data
    url = f"{CREATIO_URL}/0/ServiceModel/SourceCodeDesignerService.svc/GetSchemaData"
    response = session.post(url, json={"schemaUId": schema_uid}, headers=headers, timeout=30)
    print(f"GetSchemaData: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") != False:
            print(f"Response keys: {list(data.keys())[:10]}")
            
            # Check if we can get the source code
            if "sourceCode" in data or "body" in data or "metaData" in data:
                print("Found source code field!")
                source = data.get("sourceCode") or data.get("body") or ""
                if source:
                    print(f"Source preview: {source[:200]}...")
        else:
            print(f"Error: {data}")
    
    # Try alternative endpoints
    endpoints = [
        "SourceCodeDesignerService.svc/GetSchema",
        "SourceCodeSchemaDesignerService.svc/GetSchemaData",
        "SchemaDesignerService.svc/GetSchema",
        "ConfigurationService.svc/GetSchemaCode"
    ]
    
    for endpoint in endpoints:
        url = f"{CREATIO_URL}/0/ServiceModel/{endpoint}"
        try:
            response = session.post(url, json={"schemaUId": schema_uid}, headers=headers, timeout=10)
            print(f"{endpoint}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                keys = list(data.keys()) if isinstance(data, dict) else ['array']
                print(f"  Keys: {keys[:5]}")
        except Exception as e:
            print(f"{endpoint}: Error - {str(e)[:50]}")

if __name__ == "__main__":
    main()
