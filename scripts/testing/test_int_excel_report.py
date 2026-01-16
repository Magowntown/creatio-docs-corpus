#!/usr/bin/env python3
"""Test IntExcelReportService directly to understand its download mechanism."""

import os
import sys
from pathlib import Path

import requests
import json

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv

load_dotenv()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
COMMISSION_REPORT_ID = "4ba4f203-7088-41dc-b86d-130c590b3594"

def main():
    if not USERNAME or not PASSWORD:
        raise SystemExit("Set CREATIO_USERNAME and CREATIO_PASSWORD in your environment")

    session = requests.Session()

    # Login
    response = session.post(
        f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
        json={"UserName": USERNAME, "UserPassword": PASSWORD},
        timeout=30,
    )
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Step 1: Check what methods IntExcelReportService has
    print("\n=== Checking IntExcelReportService endpoints ===")
    
    # Try common endpoints that might exist
    endpoints = [
        ("GetFile", f"{CREATIO_URL}/0/rest/IntExcelReportService/GetFile/test"),
        ("Download", f"{CREATIO_URL}/0/rest/IntExcelReportService/Download/test"),
        ("GetReport", f"{CREATIO_URL}/0/rest/IntExcelReportService/GetReport/test"),
        ("ExportToExcel", f"{CREATIO_URL}/0/rest/IntExcelReportService/ExportToExcel/test"),
    ]
    
    for name, url in endpoints:
        try:
            response = session.get(url, headers=headers, timeout=10)
            print(f"  {name}: {response.status_code} ({len(response.content)} bytes)")
        except Exception as e:
            print(f"  {name}: Error - {str(e)[:50]}")

    # Try the ExcelExport endpoint
    print("\n=== Checking /0/ExcelExport endpoint ===")
    export_url = f"{CREATIO_URL}/0/ExcelExport/test"
    try:
        response = session.get(export_url, headers=headers, timeout=10)
        print(f"ExcelExport: {response.status_code} ({len(response.content)} bytes)")
    except Exception as e:
        print(f"ExcelExport: Error - {str(e)[:50]}")

    # Check IntExcelExport service
    print("\n=== Checking IntExcelExport endpoints ===")
    int_endpoints = [
        ("GetFile", f"{CREATIO_URL}/0/rest/IntExcelExportService/GetFile/test"),
        ("Download", f"{CREATIO_URL}/0/rest/IntExcelExportService/Download/test"),
    ]
    
    for name, url in int_endpoints:
        try:
            response = session.get(url, headers=headers, timeout=10)
            print(f"  {name}: {response.status_code} ({len(response.content)} bytes)")
        except Exception as e:
            print(f"  {name}: Error - {str(e)[:50]}")

    # Step 2: Generate a report using the original IntExcelReportService
    print("\n=== Generate via IntExcelReportService ===")
    generate_url = f"{CREATIO_URL}/0/rest/IntExcelReportService/Generate"
    generate_data = {
        "reportId": COMMISSION_REPORT_ID,
        "recordCollection": []
    }
    
    response = session.post(generate_url, json=generate_data, headers=headers, timeout=300)
    print(f"IntExcelReportService Generate: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)}")
        
        # If we have a key, try to download it using various endpoints
        key = result.get("key") or result.get("Key")
        if key:
            print(f"\n=== Trying to download file with key: {key} ===")
            
            report_name = "Commission"
            download_urls = [
                # Verified working download endpoint
                f"{CREATIO_URL}/0/rest/IntExcelReportService/GetReport/{key}/{report_name}",

                # Legacy/unknown endpoints (kept for reference)
                f"{CREATIO_URL}/0/rest/IntExcelReportService/GetFile/{key}",
                f"{CREATIO_URL}/0/rest/IntExcelReportService/Download/{key}",
                f"{CREATIO_URL}/0/ExcelExport/{key}",
                f"{CREATIO_URL}/0/rest/ExcelExportService/GetFile/{key}",
                f"{CREATIO_URL}/0/DataService/json/exportexcel/{key}",
                f"{CREATIO_URL}/0/ServiceModel/IntExcelReportService.svc/GetFile/{key}",
            ]
            
            for url in download_urls:
                try:
                    response = session.get(url, headers=headers, timeout=30)
                    content_type = response.headers.get("Content-Type", "unknown")
                    print(f"  {url.split('/0/')[-1][:40]}: {response.status_code} ({len(response.content)} bytes) [{content_type[:30]}]")
                    
                    # If we got actual content, save it
                    if response.status_code == 200 and len(response.content) > 1000:
                        with open("/tmp/downloaded_report.xlsx", "wb") as f:
                            f.write(response.content)
                        print(f"    SUCCESS! Downloaded {len(response.content)} bytes")
                        break
                except Exception as e:
                    print(f"  Error: {str(e)[:50]}")

if __name__ == "__main__":
    main()
