#!/usr/bin/env python3
"""Get the full BGIntExcelreportMixin code to understand filter handling."""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "a589d29b-9da7-4f66-836b-8e39fe0ca376"  # BGIntExcelreportMixin

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

    # Get schema data
    get_url = f"{CREATIO_URL}/0/rest/ClientUnitSchemaDesignerService/GetSchemaData"
    response = session.post(get_url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        body = data.get("body", "")
        print(f"\n=== BGIntExcelreportMixin Code ({len(body)} chars) ===\n")
        print(body)
    else:
        print(f"Failed: {response.status_code}")
        print(response.text[:500])

if __name__ == "__main__":
    main()
