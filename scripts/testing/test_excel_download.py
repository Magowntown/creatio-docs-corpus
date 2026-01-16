#!/usr/bin/env python3
"""Test various Excel download endpoints in Creatio."""

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

    # Check FileService endpoints - this is a common Creatio file handler
    print("\n=== Checking FileService and common file endpoints ===")
    
    # Generate a key first
    generate_url = f"{CREATIO_URL}/0/rest/IntExcelReportService/Generate"
    response = session.post(generate_url, 
                           json={"reportId": "4ba4f203-7088-41dc-b86d-130c590b3594", "recordCollection": []}, 
                           headers=headers, timeout=300)
    key = response.json().get("key", "")
    print(f"Generated key: {key}")
    
    # Try FileService endpoints
    report_name = "Commission"
    file_endpoints = [
        # Verified working endpoint for IntExcelReport keys
        f"{CREATIO_URL}/0/rest/IntExcelReportService/GetReport/{key}/{report_name}",

        # Other/legacy endpoints (informational)
        f"{CREATIO_URL}/0/rest/FileService/GetFile/{key}",
        f"{CREATIO_URL}/0/rest/FileService/GetFile?key={key}",
        f"{CREATIO_URL}/0/ServiceModel/FileService.svc/GetFile/{key}",
        f"{CREATIO_URL}/0/Nui/FileDownload.ashx?key={key}",
        f"{CREATIO_URL}/0/Nui/ViewModule.aspx/FileDownload/{key}",
        f"{CREATIO_URL}/0/rest/ExportToExcelService/GetExportFile?key={key}",
        f"{CREATIO_URL}/0/rest/ExportToExcelFileService/GetFile?key={key}",
        f"{CREATIO_URL}/0/rest/ExportToExcelModule/GetExportFile?key={key}",
    ]
    
    for url in file_endpoints:
        try:
            response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
            content_type = response.headers.get("Content-Type", "unknown")
            print(f"{url.split('/0/')[-1][:50]:50s} -> {response.status_code} ({len(response.content):>6d} bytes)")
        except Exception as e:
            print(f"{url.split('/0/')[-1][:50]:50s} -> Error: {str(e)[:30]}")

    # Check the FileApiService (newer Creatio versions)
    print("\n=== Checking FileApiService ===")
    file_api_endpoints = [
        f"{CREATIO_URL}/0/FileApiService/Export/{key}",
        f"{CREATIO_URL}/0/rest/FileApiService/GetFile/{key}",
        f"{CREATIO_URL}/0/odata/SysFile(guid'{key}')/Data",
    ]
    
    for url in file_api_endpoints:
        try:
            response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
            print(f"{url.split('/0/')[-1][:50]:50s} -> {response.status_code} ({len(response.content):>6d} bytes)")
        except Exception as e:
            print(f"{url.split('/0/')[-1][:50]:50s} -> Error: {str(e)[:30]}")

    # Test the built-in Excel export for a section (to understand the pattern)
    print("\n=== Testing built-in Excel export for Orders section ===")
    
    # This is how standard Creatio Excel export works
    export_url = f"{CREATIO_URL}/0/rest/ExportToExcelService/ExportToExcel"
    export_data = {
        "rootSchemaName": "Order",
        "filters": "",
        "columns": [],
        "recordCount": 10
    }
    
    try:
        response = session.post(export_url, json=export_data, headers=headers, timeout=30)
        print(f"ExportToExcel: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Result: {json.dumps(result, indent=2)[:500]}")
    except Exception as e:
        print(f"Error: {str(e)[:100]}")

if __name__ == "__main__":
    main()
