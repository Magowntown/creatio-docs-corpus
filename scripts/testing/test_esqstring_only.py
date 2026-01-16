#!/usr/bin/env python3
"""
Test what the current service does - check if it's the ESQ setting that causes issues
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

def main():
    session = requests.Session()
    
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    print("Login:", "OK" if response.status_code == 200 else "FAILED")
        
    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }
    
    # First, let's test the ORIGINAL service to confirm it has the WCF bug
    print("\n=== Test 1: Original IntExcelReportService ===")
    url1 = f"{CREATIO_URL}/0/rest/IntExcelReportService/Generate"
    data1 = {
        "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
        "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",
        "RecordCollection": []
    }
    response = session.post(url1, json=data1, headers=headers, timeout=60)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        # The original service should fail with "template with Id 00000000..." 
        # because ReportId is being deserialized as empty Guid
        msg = result.get("errorInfo", {}).get("message", result.get("message", ""))
        print(f"Error: {msg[:150]}")
        
        if "00000000-0000-0000-0000-000000000000" in msg:
            print("✅ CONFIRMED: WCF bug - ReportId received as empty GUID")
        elif result.get("success"):
            print("✅ SUCCESS (unexpected!)")
            print(f"Key: {result.get('key')}")
    
    # Test our service
    print("\n=== Test 2: UsrExcelReportService (current version) ===")
    url2 = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
    response = session.post(url2, json=data1, headers=headers, timeout=60)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Message: {result.get('message', '')[:200]}")
        print(f"Debug: {result.get('debug', '')}")
        
        if result.get("success"):
            print(f"\n✅ SUCCESS!")
            print(f"Key: {result.get('key')}")
        else:
            # Check error details
            error_info = result.get("errorInfo", {})
            if error_info:
                print(f"\nError code: {error_info.get('errorCode')}")
                print(f"Error msg: {error_info.get('message', '')[:200]}")
                stack = error_info.get("stackTrace", "")
                if stack:
                    print(f"Stack: ...{stack[-300:]}")

if __name__ == "__main__":
    main()
