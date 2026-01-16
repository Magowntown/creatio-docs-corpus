#!/usr/bin/env python3
"""
Fix the report's IntEsq configuration by removing the @P1@ placeholder filter.
The report expects a BGExecutionId filter but uses @P1@ placeholder that can't be parsed.
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

    # Get current report configuration
    print("\n=== Getting current report configuration ===")
    odata_url = f"{CREATIO_URL}/0/odata/IntExcelReport({REPORT_ID})"
    response = session.get(odata_url, headers=headers, timeout=30)

    if response.status_code != 200:
        print(f"Failed to get report: {response.status_code}")
        print(response.text[:500])
        return False

    report = response.json()
    print(f"Report Name: {report.get('IntCaption', 'N/A')}")

    current_intesq = report.get("IntEsq", "")
    print(f"\nCurrent IntEsq (first 500 chars):\n{current_intesq[:500]}")

    # Parse and fix the IntEsq
    try:
        esq_data = json.loads(current_intesq)
        print(f"\nParsed ESQ root schema: {esq_data.get('rootSchemaName')}")

        # Check if there are filters
        filters = esq_data.get("filters", {})
        items = filters.get("items", {})

        print(f"Found {len(items)} filter items")

        # Find and remove filters with @P1@ placeholder
        filters_to_remove = []
        for key, filter_item in items.items():
            right_expr = filter_item.get("rightExpression", {})
            param = right_expr.get("parameter", {})
            value = param.get("value", "")

            if value == "@P1@":
                print(f"Found @P1@ placeholder in filter: {key}")
                left_expr = filter_item.get("leftExpression", {})
                print(f"  Filter column: {left_expr.get('columnPath', 'N/A')}")
                filters_to_remove.append(key)

        if not filters_to_remove:
            print("No @P1@ placeholders found in filters")
            return False

        # Remove the problematic filters
        for key in filters_to_remove:
            del items[key]
            print(f"Removed filter: {key}")

        # If no filters left, create empty filter structure
        if not items:
            esq_data["filters"] = {
                "filterType": 6,
                "rootSchemaName": esq_data.get("rootSchemaName"),
                "items": {}
            }

        # Convert back to JSON
        fixed_intesq = json.dumps(esq_data)
        print(f"\nFixed IntEsq (first 500 chars):\n{fixed_intesq[:500]}")

    except json.JSONDecodeError as e:
        print(f"Failed to parse IntEsq: {e}")
        return False

    # Update the report
    print("\n=== Updating report IntEsq ===")
    patch_data = {
        "IntEsq": fixed_intesq
    }

    response = session.patch(odata_url, json=patch_data, headers=headers, timeout=30)
    print(f"PATCH status: {response.status_code}")

    if response.status_code in [200, 204]:
        print(">>> Report IntEsq updated successfully!")
        test_report_generation(session, headers)
        return True
    else:
        print(f"Failed to update: {response.text[:500]}")
        return False

def test_report_generation(session, headers):
    """Test the report generation after fix"""
    print("\n=== Testing Report Generation ===")

    # Test via UsrExcelReportService
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
    data = {
        "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
        "ReportId": REPORT_ID,
        "RecordCollection": []
    }

    print(f"Calling: {url}")
    response = session.post(url, json=data, headers=headers, timeout=120)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        if result.get("success"):
            print("\n>>> SUCCESS! Report generated!")
            if result.get("key"):
                print(f"Download key: {result.get('key')}")
        else:
            print(f"\nError: {result.get('message', 'Unknown error')}")
    else:
        print(f"HTTP Error: {response.text[:500]}")

if __name__ == "__main__":
    main()
