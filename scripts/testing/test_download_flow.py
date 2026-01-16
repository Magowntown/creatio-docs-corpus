#!/usr/bin/env python3
"""
Test the complete Generate -> GetReport flow in PROD.
This tests both IntExcelReportService and UsrExcelReportService endpoints.
"""

import requests
import time
import sys

# Load credentials from env
import os
from pathlib import Path

# Save command-line overrides before loading .env
cmd_url = os.environ.get('CREATIO_URL')
cmd_user = os.environ.get('CREATIO_USERNAME')
cmd_pass = os.environ.get('CREATIO_PASSWORD')

# Try to load .env file
env_file = Path(__file__).parent.parent.parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                # Only set if not already set by command line
                if key not in os.environ or not os.environ[key]:
                    os.environ[key] = val

# Command-line overrides take precedence
CREATIO_URL = cmd_url or os.environ.get('CREATIO_URL', 'https://pampabay.creatio.com')
USERNAME = cmd_user or os.environ.get('CREATIO_USERNAME', 'Supervisor')
PASSWORD = cmd_pass or os.environ.get('CREATIO_PASSWORD', '')

def main():
    print("=" * 60)
    print("PROD Download Flow Test")
    print("=" * 60)
    print(f"URL: {CREATIO_URL}")
    print()

    session = requests.Session()

    # Step 1: Login
    print("[1] Logging in...")
    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    login_resp = session.post(login_url, json={
        "UserName": USERNAME,
        "UserPassword": PASSWORD
    }, timeout=30)

    if login_resp.status_code != 200:
        print(f"    ERROR: Login failed with status {login_resp.status_code}")
        return 1

    login_data = login_resp.json()
    if login_data.get("Code") != 0:
        print(f"    ERROR: Login failed: {login_data}")
        return 1

    print("    Login successful")

    # Get CSRF token
    bpmcsrf = session.cookies.get("BPMCSRF")
    print(f"    BPMCSRF: {bpmcsrf[:20]}..." if bpmcsrf else "    BPMCSRF: not found")

    headers = {"BPMCSRF": bpmcsrf} if bpmcsrf else {}

    # Step 1.5: Look up IntExcelReport for Commission
    print()
    print("[1.5] Looking up IntExcelReport for Commission...")
    odata_url = f"{CREATIO_URL}/0/odata/IntExcelReport?$filter=contains(IntName,'Commission')"
    odata_resp = session.get(odata_url, headers=headers, timeout=30)

    if odata_resp.status_code != 200:
        print(f"    ERROR: OData lookup failed: {odata_resp.status_code}")
        return 1

    odata_result = odata_resp.json()
    if not odata_result.get("value"):
        print("    ERROR: No IntExcelReport found for Commission")
        return 1

    # Find the Commission report (not IW_Commission)
    commission_report = None
    for report in odata_result.get("value", []):
        name = report.get("IntName", "")
        if "Commission" in name and "IW_" not in name:
            commission_report = report
            break

    if not commission_report:
        # Fall back to first match
        commission_report = odata_result["value"][0]

    commission_report_id = commission_report.get("Id")
    print(f"    Found: {commission_report.get('IntName')} -> {commission_report_id}")

    # Step 2: Generate report
    print()
    print("[2] Generating report via UsrExcelReportService...")

    generate_url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
    generate_payload = {
        "ReportId": commission_report_id,
        "RecordCollection": [],
        "EsqString": ""
    }

    gen_start = time.time()
    try:
        print("    (waiting up to 5 minutes...)")
        gen_resp = session.post(generate_url, json=generate_payload, headers=headers, timeout=300)
        gen_elapsed = time.time() - gen_start
    except Exception as e:
        print(f"    ERROR: Generate request failed: {e}")
        print(f"    Elapsed: {time.time() - gen_start:.1f}s")
        return 1

    print(f"    Response status: {gen_resp.status_code}")
    print(f"    Response time: {gen_elapsed:.2f}s")

    if gen_resp.status_code != 200:
        print(f"    ERROR: Generate failed")
        print(f"    Response body: {gen_resp.text[:500]}")
        return 1

    try:
        gen_result = gen_resp.json()
    except:
        print(f"    ERROR: Response is not JSON: {gen_resp.text[:200]}")
        return 1

    print(f"    Result: {gen_result}")

    if not gen_result.get("success"):
        print(f"    ERROR: Generate failed: {gen_result.get('message')}")
        return 1

    report_key = gen_result.get("key")
    print(f"    Report key: {report_key}")

    # Step 3: Try GetReport immediately (minimal delay)
    print()
    print("[3] Downloading via IntExcelReportService/GetReport (immediate)...")

    int_download_url = f"{CREATIO_URL}/0/rest/IntExcelReportService/GetReport/{report_key}/Commission"

    dl_start = time.time()
    int_resp = session.get(int_download_url, headers=headers, timeout=60)
    dl_elapsed = time.time() - dl_start

    print(f"    Response status: {int_resp.status_code}")
    print(f"    Response time: {dl_elapsed:.2f}s")
    print(f"    Content-Type: {int_resp.headers.get('Content-Type', 'none')}")
    print(f"    Content-Length: {len(int_resp.content)} bytes")

    if int_resp.status_code == 200:
        content_type = int_resp.headers.get('Content-Type', '')
        if 'spreadsheet' in content_type or 'excel' in content_type or int_resp.content[:4] == b'PK\x03\x04':
            print("    SUCCESS: Downloaded Excel file!")
            with open('/tmp/prod_flow_int.xlsm', 'wb') as f:
                f.write(int_resp.content)
            print("    Saved to: /tmp/prod_flow_int.xlsm")
        else:
            print(f"    ERROR: Response is not Excel file")
            print(f"    Content preview: {int_resp.text[:500]}")
    else:
        print(f"    ERROR: Download failed")
        print(f"    Response: {int_resp.text[:500]}")

    # Step 4: Generate again and try UsrExcelReportService/GetReport
    print()
    print("[4] Generating new report for UsrExcelReportService test...")

    gen_resp2 = session.post(generate_url, json=generate_payload, headers=headers, timeout=120)
    if gen_resp2.status_code == 200:
        gen_result2 = gen_resp2.json()
        if gen_result2.get("success"):
            report_key2 = gen_result2.get("key")
            print(f"    New report key: {report_key2}")

            print()
            print("[5] Downloading via UsrExcelReportService/GetReport...")

            usr_download_url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/GetReport/{report_key2}/Commission"
            usr_resp = session.get(usr_download_url, headers=headers, timeout=60)

            print(f"    Response status: {usr_resp.status_code}")
            print(f"    Content-Type: {usr_resp.headers.get('Content-Type', 'none')}")
            print(f"    Content-Length: {len(usr_resp.content)} bytes")

            if usr_resp.status_code == 200:
                content_type = usr_resp.headers.get('Content-Type', '')
                if 'spreadsheet' in content_type or 'excel' in content_type or usr_resp.content[:4] == b'PK\x03\x04':
                    print("    SUCCESS: Downloaded Excel file!")
                    with open('/tmp/prod_flow_usr.xlsm', 'wb') as f:
                        f.write(usr_resp.content)
                    print("    Saved to: /tmp/prod_flow_usr.xlsm")
                else:
                    print(f"    ERROR: Response is not Excel file")
                    print(f"    Content preview: {usr_resp.text[:500]}")
            else:
                print(f"    ERROR: Download failed")
                print(f"    Response: {usr_resp.text[:500]}")

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Generate: {'OK' if gen_result.get('success') else 'FAILED'}")
    print(f"IntExcelReportService/GetReport: {int_resp.status_code}")
    print(f"UsrExcelReportService/GetReport: {usr_resp.status_code if 'usr_resp' in dir() else 'not tested'}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
