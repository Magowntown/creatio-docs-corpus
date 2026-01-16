#!/usr/bin/env python3
"""
Test the currently deployed UsrExcelReportService to see exact error
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

    # Test the service
    print("\n=== Testing UsrExcelReportService/Generate ===")
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"

    # Use the known ReportId
    data = {
        "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
        "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",
        "RecordCollection": []
    }

    print(f"Request: {json.dumps(data, indent=2)}")

    response = session.post(url, json=data, headers=headers, timeout=120)
    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"\nResponse:")
        print(json.dumps(result, indent=2))

        if result.get("success"):
            print("\n>>> SUCCESS!")
        else:
            print(f"\n>>> Error: {result.get('message', 'Unknown error')}")
    else:
        print(f"HTTP Error: {response.text[:500]}")

if __name__ == "__main__":
    main()
