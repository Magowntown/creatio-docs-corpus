#!/usr/bin/env python3
"""Test if there's a download handler for ExportFilterKey."""

import os
import sys
from pathlib import Path

import requests
import json
import time

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

    # Generate first
    print("\n=== Generating report ===")
    generate_url = f"{CREATIO_URL}/0/rest/IntExcelReportService/Generate"
    response = session.post(generate_url, 
                           json={"reportId": "4ba4f203-7088-41dc-b86d-130c590b3594", "recordCollection": []}, 
                           headers=headers, timeout=300)
    key = response.json().get("key", "")
    print(f"Generated key: {key}")
    
    # Confirm the working endpoint first
    report_name = "Commission"
    print("\n=== Testing working download endpoint (GetReport) ===")
    get_report_url = f"{CREATIO_URL}/0/rest/IntExcelReportService/GetReport/{key}/{report_name}"
    resp = session.get(get_report_url, headers=headers, timeout=60)
    print(f"GetReport -> {resp.status_code} ({len(resp.content)} bytes)")
    if resp.status_code == 200:
        print(f"  Signature: {resp.content[:2]!r} (expected b'PK')")

    # Then probe legacy endpoints (informational)
    print("\n=== Testing legacy download handlers (informational) ===")
    download_urls = [
        # Standard Creatio handlers
        f"{CREATIO_URL}/0/Nui/ViewModule.aspx/DownloadExportFile.ashx?key={key}",
        f"{CREATIO_URL}/0/DownloadExportFile.ashx?key={key}",
        f"{CREATIO_URL}/0/rest/DownloadExportFile?key={key}",
        
        # IntExcelExport specific
        f"{CREATIO_URL}/0/rest/IntExcelReportFileService/GetFile?key={key}",
        f"{CREATIO_URL}/0/IntExcelExport/Download?key={key}",
        f"{CREATIO_URL}/0/IntExcelExport/GetFile?key={key}",
        
        # Session-based file download
        f"{CREATIO_URL}/0/Nui/FileDownload.ashx?sessionKey={key}",
        f"{CREATIO_URL}/0/FileDownload.ashx?key={key}",
        
        # Export file handlers
        f"{CREATIO_URL}/0/ExportToExcelFile.ashx?key={key}",
        f"{CREATIO_URL}/0/Nui/ExportToExcelFile.ashx?key={key}",
    ]
    
    for url in download_urls:
        try:
            response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
            content_type = response.headers.get("Content-Type", "unknown")[:35]
            disp = response.headers.get("Content-Disposition", "")[:30]
            size = len(response.content)
            status = response.status_code
            
            # Mark if this looks like a real file
            is_file = (status == 200 and 
                      ('excel' in content_type.lower() or 
                       'octet' in content_type.lower() or
                       'xlsx' in disp.lower() or
                       size > 5000))
            
            marker = " *** FILE! ***" if is_file else ""
            print(f"{url.split('/0/')[-1][:45]:45s} -> {status:3d} ({size:>7d} bytes) [{content_type}]{marker}")
            
            if is_file:
                with open("/tmp/report_download.xlsx", "wb") as f:
                    f.write(response.content)
                print(f"    Downloaded to /tmp/report_download.xlsx")
                
        except Exception as e:
            print(f"{url.split('/0/')[-1][:45]:45s} -> Error: {str(e)[:40]}")

    # Also check POST endpoints
    print("\n=== Testing POST Download handlers ===")
    post_endpoints = [
        f"{CREATIO_URL}/0/rest/IntExcelReportService/GetExportFile",
        f"{CREATIO_URL}/0/rest/IntExcelExportService/Download",
    ]
    
    for url in post_endpoints:
        try:
            response = session.post(url, json={"key": key}, headers=headers, timeout=10)
            print(f"{url.split('/0/')[-1][:45]:45s} -> {response.status_code} ({len(response.content)} bytes)")
        except Exception as e:
            print(f"{url.split('/0/')[-1][:45]:45s} -> Error: {str(e)[:40]}")

if __name__ == "__main__":
    main()
