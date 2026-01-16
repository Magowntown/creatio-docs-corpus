#!/usr/bin/env python3
"""Test to understand where IntExcelExport stores files."""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
COMMISSION_REPORT_ID = "4ba4f203-7088-41dc-b86d-130c590b3594"

def main():
    session = requests.Session()

    # Login
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD},
                           timeout=30)
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Step 1: Generate a report
    print("\n=== Step 1: Generating report ===")
    generate_url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
    generate_data = {
        "ReportId": COMMISSION_REPORT_ID,
        "RecordCollection": []
    }
    
    response = session.post(generate_url, json=generate_data, headers=headers, timeout=300)
    print(f"Generate Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Generate Result: {json.dumps(result, indent=2)}")
        
        key = result.get("key")
        if key:
            print(f"\n=== Step 2: Diagnosing cache for key: {key} ===")
            diag_url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/DiagnoseCache/{key}"
            
            response = session.get(diag_url, headers=headers, timeout=30)
            print(f"DiagnoseCache Status: {response.status_code}")
            
            if response.status_code == 200:
                diag_result = response.json()
                print(f"DiagnoseCache Result: {json.dumps(diag_result, indent=2)}")
                
                # Parse and display diagnostics nicely
                message = diag_result.get("message", "")
                parts = message.split(" | ")
                print("\n--- Parsed Diagnostics ---")
                for part in parts:
                    print(f"  {part}")
    else:
        print(f"Error: {response.text[:500]}")

if __name__ == "__main__":
    main()
