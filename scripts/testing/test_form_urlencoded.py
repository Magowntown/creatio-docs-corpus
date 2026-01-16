#!/usr/bin/env python3
"""
Test if form-urlencoded works with IntExcelReportService
"""

import os
import requests
import json
from urllib.parse import urlencode

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

def login(session):
    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    response = session.post(login_url, json={"UserName": USERNAME, "UserPassword": PASSWORD})
    return response.status_code == 200

def main():
    session = requests.Session()

    print("Logging in...")
    if not login(session):
        print("Login failed")
        return

    bpmcsrf = session.cookies.get("BPMCSRF", "")

    # Test report ID
    report_id = "4ba4f203-7088-41dc-b86d-130c590b3594"

    # Simple ESQ for testing
    esq_data = {
        "rootSchemaName": "BGCommissionReportDataView",
        "allColumns": True
    }

    # Test 1: Standard JSON (control - should fail with empty GUID)
    print("\n=== Test 1: Standard JSON ===")
    url = f"{CREATIO_URL}/0/rest/IntExcelReportService/Generate"
    data = {
        "EsqString": json.dumps(esq_data),
        "ReportId": report_id,
        "RecordCollection": []
    }

    response = session.post(url, json=data, headers={
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json"
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    # Test 2: Form URL-encoded
    print("\n=== Test 2: Form URL-encoded ===")
    form_data = {
        "EsqString": json.dumps(esq_data),
        "ReportId": report_id,
        "RecordCollection": json.dumps([])
    }

    response = session.post(url, data=form_data, headers={
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/x-www-form-urlencoded"
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    # Test 3: JSON with different structure (wrapped)
    print("\n=== Test 3: Wrapped JSON ===")
    wrapped_data = {
        "request": {
            "EsqString": json.dumps(esq_data),
            "ReportId": report_id,
            "RecordCollection": []
        }
    }

    response = session.post(url, json=wrapped_data, headers={
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json"
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    # Test 4: XML format
    print("\n=== Test 4: XML format ===")
    xml_data = f'''<?xml version="1.0" encoding="utf-8"?>
<IntExcelReportServiceRequest xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
    <EsqString>{json.dumps(esq_data)}</EsqString>
    <ReportId>{report_id}</ReportId>
    <RecordCollection></RecordCollection>
</IntExcelReportServiceRequest>'''

    response = session.post(url, data=xml_data, headers={
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/xml"
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    # Test 5: Use BGIntExcelReportService2 instead (which has GetReport)
    print("\n=== Test 5: BGIntExcelReportService2 endpoints ===")
    url2 = f"{CREATIO_URL}/0/rest/BGIntExcelReportService2"

    # List available methods
    response = session.options(url2, headers={"BPMCSRF": bpmcsrf})
    print(f"OPTIONS Status: {response.status_code}")
    print(f"Allow: {response.headers.get('Allow', 'N/A')}")

if __name__ == "__main__":
    main()
