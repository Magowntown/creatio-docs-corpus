#!/usr/bin/env python3
"""Deploy with alternative endpoints."""

import os
import requests
import json
import time

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "ed794ab8-8a59-4c7e-983c-cc039449d178"

def main():
    session = requests.Session()

    # Login
    print("=== Logging in ===")
    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    response = session.post(login_url,
                           json={"UserName": USERNAME, "UserPassword": PASSWORD},
                           timeout=30)
    
    if response.status_code != 200:
        print(f"Login failed: {response.status_code}")
        return
    
    login_result = response.json()
    print(f"Login result: {login_result}")
    
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }
    
    print(f"BPMCSRF: {headers['BPMCSRF'][:20]}...")

    # Try multiple endpoints
    endpoints = [
        "/0/rest/SourceCodeSchemaDesignerService/GetSchemaData",
        "/0/ServiceModel/SourceCodeSchemaDesignerService.svc/GetSchemaData",
    ]
    
    for endpoint in endpoints:
        url = f"{CREATIO_URL}{endpoint}"
        print(f"\nTrying: {endpoint}")
        response = session.post(url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Keys: {list(data.keys())}")
            if "name" in data:
                print(f"Schema name: {data.get('name')}")
            return data
        else:
            print(f"Response: {response.text[:300]}")

if __name__ == "__main__":
    main()
