#!/usr/bin/env python3
"""
Test the ORIGINAL IntExcelReportService directly after fixing the IntEsq.
This bypasses our wrapper to see if the underlying service now works.
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

REPORT_ID = "4ba4f203-7088-41dc-b86d-130c590b3594"

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

    # Test original IntExcelReportService directly
    print("\n=== Testing ORIGINAL IntExcelReportService/Generate ===")
    url = f"{CREATIO_URL}/0/rest/IntExcelReportService/Generate"

    data = {
        "ReportId": REPORT_ID,
        "filtersConfig": None,
        "recordCollection": []
    }

    print(f"URL: {url}")
    print(f"Request: {json.dumps(data, indent=2)}")

    response = session.post(url, json=data, headers=headers, timeout=120)
    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"Response:\n{json.dumps(result, indent=2)}")

        if result.get("success"):
            print("\n>>> SUCCESS! Original service works now!")
            key = result.get("key")
            if key:
                print(f"Download key: {key}")
                # Try to download
                download_url = f"{CREATIO_URL}/0/rest/IntExcelReportService/GetReportFile/{key}"
                print(f"\nDownload URL: {download_url}")
        else:
            print(f"\n>>> Error from original service: {result.get('message', 'Unknown')}")
    else:
        print(f"HTTP Error: {response.text[:1000]}")

    # Also try with FiltersConfig as empty JSON
    print("\n=== Testing with empty filtersConfig JSON ===")
    data2 = {
        "ReportId": REPORT_ID,
        "filtersConfig": json.dumps({"filterType": 6, "items": {}}),
        "recordCollection": []
    }

    response = session.post(url, json=data2, headers=headers, timeout=120)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"Response:\n{json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
