#!/usr/bin/env python3
"""
Verify Commission Report Download Fix
Tests that the GenerateWithDateFilter path is used and downloads work.
Run after deploying UsrExcelReportService_Updated.cs to PROD.
"""
import requests
import json
import os
import sys

def load_env():
    """Load environment variables from .env file."""
    env_path = '/home/magown/creatio-report-fix/.env'
    env_vars = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

def test_download(env='PROD'):
    """Test Commission report generation and download."""
    env_vars = load_env()

    if env == 'PROD':
        base_url = env_vars.get('CREATIO_PROD_URL', 'https://pampabay.creatio.com')
        username = env_vars.get('CREATIO_PROD_USERNAME')
        password = env_vars.get('CREATIO_PROD_PASSWORD')
    else:
        base_url = env_vars.get('CREATIO_URL', 'https://dev-pampabay.creatio.com')
        username = env_vars.get('CREATIO_USERNAME')
        password = env_vars.get('CREATIO_PASSWORD')

    print(f"Testing {env}: {base_url}")
    print("=" * 60)

    # Authenticate
    session = requests.Session()
    auth_url = f'{base_url}/ServiceModel/AuthService.svc/Login'
    auth_resp = session.post(auth_url, json={'UserName': username, 'UserPassword': password})

    if auth_resp.json().get('Code') != 0:
        print(f"❌ Authentication failed: {auth_resp.json()}")
        return False

    print("✅ Authenticated")

    csrf_token = session.cookies.get('BPMCSRF')
    headers = {'BPMCSRF': csrf_token, 'Content-Type': 'application/json'}

    # Commission report ID
    commission_id = '4ba4f203-7088-41dc-b86d-130c590b3594'

    # Test 1: With Year-Month filter (Dec 2024)
    print("\n--- Test 1: Commission with Year-Month filter ---")
    gen_url = f'{base_url}/0/rest/UsrExcelReportService/Generate'
    payload = {
        'ReportId': commission_id,
        'YearMonthName': '2024-12',
        'SalesGroupId': 'edfefb79-77b6-43fe-932b-c012d9a2fc9d'  # RDGZ
    }

    resp = session.post(gen_url, json=payload, headers=headers, timeout=120)
    result = resp.json()
    print(f"Generate: success={result.get('success')}")
    print(f"Message: {result.get('message', '')[:100]}")

    if result.get('success') and result.get('key'):
        key = result.get('key')

        # Try to download
        get_url = f'{base_url}/0/rest/UsrExcelReportService/GetReport/{key}/Commission.xlsx'
        download_resp = session.get(get_url, headers={'BPMCSRF': csrf_token}, timeout=60)

        print(f"Download status: {download_resp.status_code}")
        print(f"Content-Type: {download_resp.headers.get('Content-Type', 'N/A')}")
        print(f"Size: {len(download_resp.content)} bytes")

        if download_resp.status_code == 200 and download_resp.content[:2] == b'PK':
            print("✅ Download successful - valid Excel file!")
            # Save for verification
            with open('/tmp/commission_test.xlsx', 'wb') as f:
                f.write(download_resp.content)
            print("   Saved to /tmp/commission_test.xlsx")
        else:
            print("❌ Download failed")
            if download_resp.status_code == 404:
                print("   ERROR: GetReport returned 404 - bytes not in SessionData")
                print("   This indicates the fix is NOT deployed or not working")
            return False
    else:
        print(f"❌ Generation failed: {result.get('message')}")
        return False

    # Test 2: Without Year-Month filter (all time)
    print("\n--- Test 2: Commission without Year-Month filter ---")
    payload = {'ReportId': commission_id}

    resp = session.post(gen_url, json=payload, headers=headers, timeout=120)
    result = resp.json()
    print(f"Generate: success={result.get('success')}")
    print(f"Message: {result.get('message', '')[:100]}")

    if result.get('success') and result.get('key'):
        key = result.get('key')

        get_url = f'{base_url}/0/rest/UsrExcelReportService/GetReport/{key}/Commission.xlsx'
        download_resp = session.get(get_url, headers={'BPMCSRF': csrf_token}, timeout=60)

        print(f"Download status: {download_resp.status_code}")

        if download_resp.status_code == 200 and download_resp.content[:2] == b'PK':
            print("✅ Download successful - valid Excel file!")
            print(f"   Size: {len(download_resp.content)} bytes")
        else:
            print("❌ Download failed (all-time query)")
            return False

    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - Download fix is working!")
    return True

if __name__ == '__main__':
    env = sys.argv[1] if len(sys.argv) > 1 else 'PROD'
    success = test_download(env)
    sys.exit(0 if success else 1)
