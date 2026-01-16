#!/usr/bin/env python3
"""
Run this after manually applying the fix in Creatio Configuration
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
    
    print("\n=== Verifying UsrExcelReportService Fix ===")
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
    
    data = {
        "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
        "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",
        "RecordCollection": []
    }
    
    print(f"Testing with ReportId: {data['ReportId']}")
    
    response = session.post(url, json=data, headers=headers, timeout=60)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        
        if result.get("success"):
            print("\n✅ SUCCESS! Report generated!")
            print(f"Key: {result.get('key')}")
            print(f"Report Name: {result.get('reportName')}")
        else:
            msg = result.get("message", "")
            print(f"\n❌ Failed: {msg[:200]}")
            
            # Check if it's the old reflection error
            if "EsqBuilder.CreateFilter" in msg or "EsqBuilder" in str(result):
                print("\n⚠️ Still seeing EsqBuilder error - the fix wasn't applied correctly")
                print("Make sure you replaced ALL the code and compiled successfully")
            
            # Check if ReportId is now working
            if "00000000-0000-0000-0000-000000000000" in msg:
                print("\n⚠️ Still seeing empty GUID - DataContract isn't working")
            elif "4ba4f203" in msg:
                print("\n✅ Good: ReportId is being received correctly!")

if __name__ == "__main__":
    main()
