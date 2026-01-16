#!/usr/bin/env python3
"""
Test original IntExcelReportService directly
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

def test_service(session, bpmcsrf, service_name):
    """Test a service"""
    print(f"\n=== Testing {service_name}/Generate ===")
    url = f"{CREATIO_URL}/0/rest/{service_name}/Generate"

    esq = {"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}
    report_id = "4ba4f203-7088-41dc-b86d-130c590b3594"

    data = {
        "EsqString": json.dumps(esq),
        "ReportId": report_id,
        "RecordCollection": []
    }

    response = session.post(url, json=data, headers={
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json"
    })

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        try:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)[:500]}")
            if result.get("success"):
                print(f"✅ SUCCESS!")
                return True
        except:
            print(f"Raw: {response.text[:300]}")
    elif response.status_code == 404:
        print("Service not found (404)")
    else:
        print(f"Error: {response.text[:200]}")
    return False

def main():
    session = requests.Session()
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")
    bpmcsrf = session.cookies.get("BPMCSRF", "")

    # Test various service names
    services = [
        "IntExcelReportService",
        "IntExcelExport.Services.IntExcelReportService",
        "BGIntExcelReportService",
        "BGIntExcelReportService2",
        "UsrExcelReportService"
    ]

    for service in services:
        test_service(session, bpmcsrf, service)

if __name__ == "__main__":
    main()
