#!/usr/bin/env python3
"""Check what error messages the download handlers return."""

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

    # Generate first
    print("\n=== Generating report ===")
    generate_url = f"{CREATIO_URL}/0/rest/IntExcelReportService/Generate"
    response = session.post(generate_url, 
                           json={"reportId": "4ba4f203-7088-41dc-b86d-130c590b3594", "recordCollection": []}, 
                           headers=headers, timeout=300)
    key = response.json().get("key", "")
    print(f"Generated key: {key}")
    
    # First: confirm the currently working download endpoint
    report_name = "Commission"
    ok_url = f"{CREATIO_URL}/0/rest/IntExcelReportService/GetReport/{key}/{report_name}"
    ok_resp = session.get(ok_url, headers=headers, timeout=60)
    print("\n=== Confirming GetReport download works ===")
    print(f"{ok_url.split('/0/')[-1]}")
    print(f"  Status: {ok_resp.status_code}")
    print(f"  Content-Length: {ok_resp.headers.get('Content-Length', 'N/A')}")
    if ok_resp.status_code == 200:
        print(f"  Signature: {ok_resp.content[:2]!r} (expected b'PK')")

    # Check error messages from legacy handlers that often return 404/500
    print("\n=== Checking legacy handler error messages (informational) ===")
    error_urls = [
        f"{CREATIO_URL}/0/DownloadExportFile.ashx?key={key}",
        f"{CREATIO_URL}/0/FileDownload.ashx?key={key}",
        f"{CREATIO_URL}/0/ExportToExcelFile.ashx?key={key}",
        f"{CREATIO_URL}/0/Nui/ExportToExcelFile.ashx?key={key}",
    ]
    
    for url in error_urls:
        try:
            response = session.get(url, headers=headers, timeout=10)
            print(f"\n{url.split('/0/')[-1]}")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
        except Exception as e:
            print(f"  Error: {str(e)[:100]}")

if __name__ == "__main__":
    main()
