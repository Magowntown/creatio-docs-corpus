#!/usr/bin/env python3
"""
Test UsrExcelReportService - the new service with proper DataContract
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

def test_usr_service(session, bpmcsrf):
    """Test UsrExcelReportService Generate endpoint"""
    print("\n=== Testing UsrExcelReportService/Generate ===")
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"

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

    print(f"\nStatus: {response.status_code}")

    if response.status_code == 200:
        try:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")

            if result.get("success"):
                print("\n✅ SUCCESS! UsrExcelReportService works!")
                print(f"Key: {result.get('key')}")
                print(f"Report Name: {result.get('reportName')}")
                return True
            else:
                print(f"\n❌ Failed: {result.get('message')}")
                if result.get("debug"):
                    print(f"Debug: {result.get('debug')}")
                return False
        except Exception as e:
            print(f"Parse error: {e}")
            print(f"Raw response: {response.text[:1000]}")
    else:
        print(f"HTTP Error: {response.text[:500]}")
    return False

def main():
    session = requests.Session()
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")
    bpmcsrf = session.cookies.get("BPMCSRF", "")

    test_usr_service(session, bpmcsrf)

if __name__ == "__main__":
    main()
