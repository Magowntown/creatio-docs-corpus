#!/usr/bin/env python3
"""
Test BGIntExcelReportService2 which has proper DataContract
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

def login(session):
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    return response.status_code == 200

def test_bg_service(session, bpmcsrf):
    """Test BGIntExcelReportService2 Generate endpoint"""
    print("\n=== Testing BGIntExcelReportService2/Generate ===")
    url = f"{CREATIO_URL}/0/rest/BGIntExcelReportService2/Generate"

    esq = {"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}
    report_id = "4ba4f203-7088-41dc-b86d-130c590b3594"

    data = {
        "EsqString": json.dumps(esq),
        "ReportId": report_id,
        "RecordCollection": []
    }

    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")

    response = session.post(url, json=data, headers={
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json"
    })

    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    if response.status_code == 200:
        try:
            result = response.json()
            if result.get("success"):
                print("\nSUCCESS! BGIntExcelReportService2 works!")
                print(f"Key: {result.get('key')}")
                return True
            else:
                print(f"\nFailed: {result.get('message')}")
                # Check if ReportId was received correctly
                if "00000000-0000-0000-0000-000000000000" in str(result):
                    print("STILL HAS EMPTY GUID BUG!")
                return False
        except Exception as e:
            print(f"Parse error: {e}")
    return False

def main():
    session = requests.Session()
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")
    bpmcsrf = session.cookies.get("BPMCSRF", "")

    test_bg_service(session, bpmcsrf)

if __name__ == "__main__":
    main()
