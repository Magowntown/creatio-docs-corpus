#!/usr/bin/env python3
"""
Test with proper ESQ JSON format
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

def test_with_esq_format(session, bpmcsrf, esq_json, description):
    """Test with a specific ESQ format"""
    print(f"\n=== Testing: {description} ===")
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"

    report_id = "4ba4f203-7088-41dc-b86d-130c590b3594"

    data = {
        "EsqString": json.dumps(esq_json),
        "ReportId": report_id,
        "RecordCollection": []
    }

    print(f"EsqString: {json.dumps(esq_json)[:200]}")

    response = session.post(url, json=data, headers={
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json"
    })

    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(f"✅ SUCCESS! Key: {result.get('key')}")
            return True
        else:
            msg = result.get("message", "")[:150]
            debug = result.get("debug", "")
            print(f"❌ Failed: {msg}")
            print(f"Debug: {debug}")
    else:
        print(f"HTTP Error: {response.status_code}")
    return False

def main():
    session = requests.Session()
    if not login(session):
        print("Login failed")
        return

    print("Login successful!")
    bpmcsrf = session.cookies.get("BPMCSRF", "")

    # Test 1: Original simple format
    test_with_esq_format(session, bpmcsrf, {
        "rootSchemaName": "BGCommissionReportDataView",
        "allColumns": True
    }, "Simple format")

    # Test 2: Proper Creatio ESQ format
    test_with_esq_format(session, bpmcsrf, {
        "rootSchemaName": "BGCommissionReportDataView",
        "operationType": 0,
        "columns": {"items": {}},
        "allColumns": True
    }, "Proper ESQ format")

    # Test 3: Just schema name
    test_with_esq_format(session, bpmcsrf, {
        "rootSchemaName": "BGCommissionReportDataView"
    }, "Just schema name")

    # Test 4: With empty filters
    test_with_esq_format(session, bpmcsrf, {
        "rootSchemaName": "BGCommissionReportDataView",
        "operationType": 0,
        "allColumns": True,
        "filters": None
    }, "With null filters")

    # Test 5: With empty filters object
    test_with_esq_format(session, bpmcsrf, {
        "rootSchemaName": "BGCommissionReportDataView",
        "operationType": 0,
        "allColumns": True,
        "filters": {}
    }, "With empty filters object")

if __name__ == "__main__":
    main()
