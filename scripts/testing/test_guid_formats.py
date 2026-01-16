#!/usr/bin/env python3
"""
Test different GUID formats with IntExcelReportService
DataContractJsonSerializer has specific requirements for Guid serialization
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

def test_format(session, bpmcsrf, name, report_id_value, manual_json=None):
    print(f"\n=== {name} ===")
    url = f"{CREATIO_URL}/0/rest/IntExcelReportService/Generate"

    esq = {"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}

    if manual_json:
        # Send raw JSON string
        response = session.post(url, data=manual_json, headers={
            "BPMCSRF": bpmcsrf,
            "Content-Type": "application/json"
        })
    else:
        data = {
            "EsqString": json.dumps(esq),
            "ReportId": report_id_value,
            "RecordCollection": []
        }
        response = session.post(url, json=data, headers={
            "BPMCSRF": bpmcsrf,
            "Content-Type": "application/json"
        })

    result = response.text[:300]
    success = "key" in result.lower() and "success" in result.lower() and '"success":true' in result.lower()
    status = "SUCCESS" if success else ("EMPTY_GUID" if "00000000-0000-0000-0000-000000000000" in result else "OTHER_ERROR")
    print(f"Status: {response.status_code} - {status}")
    print(f"Response: {result}")
    return success

def main():
    session = requests.Session()
    if not login(session):
        print("Login failed")
        return

    bpmcsrf = session.cookies.get("BPMCSRF", "")
    report_id = "4ba4f203-7088-41dc-b86d-130c590b3594"

    esq = {"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}

    # Test different GUID formats

    # 1. Standard GUID with dashes
    test_format(session, bpmcsrf, "1. Standard GUID (with dashes)", report_id)

    # 2. GUID without dashes
    test_format(session, bpmcsrf, "2. GUID without dashes", report_id.replace("-", ""))

    # 3. GUID in uppercase
    test_format(session, bpmcsrf, "3. GUID uppercase", report_id.upper())

    # 4. GUID with braces
    test_format(session, bpmcsrf, "4. GUID with braces", f"{{{report_id}}}")

    # 5. DataContractJsonSerializer escaped format (\/Date\/ style doesn't apply to Guid)
    # But let's try double-escaped
    manual_json = json.dumps({
        "EsqString": json.dumps(esq),
        "ReportId": report_id,
        "RecordCollection": []
    })
    test_format(session, bpmcsrf, "5. Double-serialized JSON", None, manual_json)

    # 6. ReportId as object with value property
    test_format(session, bpmcsrf, "6. ReportId as object", {"value": report_id})

    # 7. Try with __type hint (DataContractJsonSerializer uses this for type info)
    manual_json = '{"EsqString":"{\\"rootSchemaName\\":\\"BGCommissionReportDataView\\",\\"allColumns\\":true}","ReportId":"4ba4f203-7088-41dc-b86d-130c590b3594","RecordCollection":[],"__type":"IntExcelReportServiceRequest:#IntExcelExport.Models"}'
    test_format(session, bpmcsrf, "7. With __type hint", None, manual_json)

    # 8. Try lowercase property names (WCF may use camelCase)
    manual_json = '{"esqString":"{\\"rootSchemaName\\":\\"BGCommissionReportDataView\\",\\"allColumns\\":true}","reportId":"4ba4f203-7088-41dc-b86d-130c590b3594","recordCollection":[]}'
    test_format(session, bpmcsrf, "8. camelCase properties", None, manual_json)

    # 9. Check if it's a namespace issue - try Terrasoft namespace
    manual_json = '{"EsqString":"{\\"rootSchemaName\\":\\"BGCommissionReportDataView\\",\\"allColumns\\":true}","ReportId":"4ba4f203-7088-41dc-b86d-130c590b3594","RecordCollection":[],"__type":"IntExcelReportServiceRequest:#Terrasoft.Configuration"}'
    test_format(session, bpmcsrf, "9. With Terrasoft namespace type", None, manual_json)

if __name__ == "__main__":
    main()
