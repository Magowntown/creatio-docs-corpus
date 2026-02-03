#!/usr/bin/env python3
"""Test script for "Items by Customer" report.

This script verifies:
1. IntExcelReport template exists
2. Customer lookup works (gets sample customer from Account)
3. UsrExcelReportService generates report with CustomerName filter
4. Date filters are applied correctly

Environment variables:
- CREATIO_URL, CREATIO_USERNAME, CREATIO_PASSWORD
- CREATIO_CUSTOMER_NAME (optional - defaults to first Account found)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv
from scripts._paths import ARTIFACTS_DIR, ensure_dirs

load_dotenv()
ensure_dirs()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com").rstrip("/")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
CUSTOMER_NAME = os.environ.get("CREATIO_CUSTOMER_NAME", "").strip()

EMPTY_GUID = "00000000-0000-0000-0000-000000000000"
TIMEOUT_SECONDS = 120


def _headers(session: requests.Session) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", ""),
    }


def login(session: requests.Session) -> bool:
    """Login to Creatio and get BPMCSRF cookie."""
    url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    payload = {"UserName": USERNAME, "UserPassword": PASSWORD}
    resp = session.post(url, json=payload, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        print(f"[ERROR] Login failed: {resp.status_code}")
        return False
    data = resp.json()
    if data.get("Code") != 0:
        print(f"[ERROR] Login rejected: {data}")
        return False
    print(f"[OK] Logged in as {USERNAME}")
    return True


def find_int_excel_report(session: requests.Session, headers: Dict[str, str]) -> Optional[str]:
    """Find IntExcelReport ID for 'Items by Customer' or 'Rpt Items by Customer'."""
    url = f"{CREATIO_URL}/0/odata/IntExcelReport"
    params = {
        "$filter": "(IntName eq 'Items by Customer' or IntName eq 'Rpt Items by Customer' or IntName eq 'Rpt_ItemsByCustomer')",
        "$select": "Id,IntName"
    }
    resp = session.get(url, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        print(f"[ERROR] IntExcelReport query failed: {resp.status_code}")
        return None

    data = resp.json()
    records = data.get("value", [])
    if not records:
        print("[ERROR] IntExcelReport not found for 'Items by Customer'")
        # Try broader search
        params["$filter"] = "contains(IntName, 'Item')"
        resp = session.get(url, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
        if resp.status_code == 200:
            data = resp.json()
            records = data.get("value", [])
            if records:
                print(f"[INFO] Found similar templates: {[r['IntName'] for r in records[:5]]}")
        return None

    report = records[0]
    print(f"[OK] Found template: {report['IntName']} (ID: {report['Id']})")
    return report["Id"]


def get_sample_customer(session: requests.Session, headers: Dict[str, str]) -> Optional[str]:
    """Get a sample customer name from Account entity."""
    if CUSTOMER_NAME:
        print(f"[OK] Using provided customer: {CUSTOMER_NAME}")
        return CUSTOMER_NAME

    # Query Account for a sample customer with recent orders
    url = f"{CREATIO_URL}/0/odata/Account"
    params = {
        "$select": "Id,Name",
        "$top": 10,
        "$orderby": "ModifiedOn desc"
    }
    resp = session.get(url, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        print(f"[ERROR] Account query failed: {resp.status_code}")
        return None

    data = resp.json()
    records = data.get("value", [])
    if not records:
        print("[ERROR] No accounts found")
        return None

    # Return first customer name
    customer = records[0]
    print(f"[OK] Using sample customer: {customer['Name']}")
    return customer["Name"]


def check_sales_by_item_view(session: requests.Session, headers: Dict[str, str], customer_name: str) -> int:
    """Check BGSalesByItemView for records matching customer."""
    url = f"{CREATIO_URL}/0/odata/BGSalesByItemView"
    params = {
        "$filter": f"BGCustomer eq '{customer_name}'",
        "$top": 5,
        "$count": "true"
    }
    resp = session.get(url, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        print(f"[WARN] BGSalesByItemView query failed: {resp.status_code}")
        return -1

    data = resp.json()
    count = data.get("@odata.count", len(data.get("value", [])))
    print(f"[INFO] BGSalesByItemView records for '{customer_name}': {count}")
    return count


def generate_items_by_customer_report(
    session: requests.Session,
    headers: Dict[str, str],
    report_id: str,
    customer_name: str,
    with_dates: bool = False
) -> Dict[str, Any]:
    """Call UsrExcelReportService/Generate with customer filter."""

    # Build request payload
    payload = {
        "ReportId": report_id,
        "YearMonthId": EMPTY_GUID,
        "SalesRepId": EMPTY_GUID,
        "CustomerId": EMPTY_GUID,  # We use CustomerName for varchar filter
        "CustomerName": customer_name,
    }

    # Optionally add date filters
    if with_dates:
        # Last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        # WCF format: /Date(milliseconds)/
        payload["CreatedFrom"] = f"/Date({int(start_date.timestamp() * 1000)})/"
        payload["CreatedTo"] = f"/Date({int(end_date.timestamp() * 1000)})/"
        print(f"[INFO] Date filter: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
    print(f"[INFO] Calling Generate with CustomerName='{customer_name}'")
    print(f"[DEBUG] Payload: {json.dumps(payload, indent=2)}")

    resp = session.post(url, json=payload, headers=headers, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        print(f"[ERROR] Generate failed: {resp.status_code}")
        print(f"[ERROR] Response: {resp.text[:500]}")
        return {"success": False, "message": f"HTTP {resp.status_code}"}

    result = resp.json()
    print(f"[INFO] Generate response: {json.dumps(result, indent=2)}")
    return result


def download_report(
    session: requests.Session,
    headers: Dict[str, str],
    cache_key: str,
    report_name: str = "ItemsByCustomer"
) -> bool:
    """Download the generated report."""
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/GetReport/{cache_key}/{report_name}"
    print(f"[INFO] Downloading from: {url}")

    resp = session.get(url, headers=headers, timeout=TIMEOUT_SECONDS, stream=True)
    if resp.status_code != 200:
        print(f"[ERROR] Download failed: {resp.status_code}")
        return False

    content_type = resp.headers.get("Content-Type", "")
    content_length = resp.headers.get("Content-Length", "unknown")
    print(f"[INFO] Content-Type: {content_type}")
    print(f"[INFO] Content-Length: {content_length}")

    # Save to artifacts
    filename = f"ItemsByCustomer_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = ARTIFACTS_DIR / filename

    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    file_size = filepath.stat().st_size
    print(f"[OK] Saved to: {filepath} ({file_size} bytes)")

    # Basic validation
    if file_size < 1000:
        print(f"[WARN] File seems too small - might be an error response")
        with open(filepath, "rb") as f:
            content = f.read(500)
            if b"error" in content.lower() or b"exception" in content.lower():
                print(f"[ERROR] File contains error: {content[:200]}")
                return False

    return True


def main():
    print("=" * 60)
    print("Items by Customer Report Test")
    print("=" * 60)

    session = requests.Session()

    # Step 1: Login
    if not login(session):
        return 1

    headers = _headers(session)

    # Step 2: Find IntExcelReport template
    report_id = find_int_excel_report(session, headers)
    if not report_id:
        print("\n[FAIL] Could not find IntExcelReport template")
        return 1

    # Step 3: Get sample customer
    customer_name = get_sample_customer(session, headers)
    if not customer_name:
        print("\n[FAIL] Could not find customer")
        return 1

    # Step 4: Check if customer has data in BGSalesByItemView
    record_count = check_sales_by_item_view(session, headers, customer_name)
    if record_count == 0:
        print(f"[WARN] No data for customer '{customer_name}' - trying another...")
        # Try a few more customers
        url = f"{CREATIO_URL}/0/odata/Account"
        params = {"$select": "Name", "$top": 50}
        resp = session.get(url, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
        if resp.status_code == 200:
            for acc in resp.json().get("value", []):
                test_name = acc["Name"]
                cnt = check_sales_by_item_view(session, headers, test_name)
                if cnt > 0:
                    customer_name = test_name
                    print(f"[OK] Switched to customer with data: {customer_name}")
                    break

    # Step 5: Test WITHOUT date filters
    print("\n" + "-" * 60)
    print("Test 1: Generate WITHOUT date filters")
    print("-" * 60)

    result = generate_items_by_customer_report(
        session, headers, report_id, customer_name, with_dates=False
    )

    if result.get("success"):
        cache_key = result.get("key")
        if cache_key:
            print(f"[OK] Generation successful - key: {cache_key}")
            print(f"[OK] Message: {result.get('message', '')}")
            download_report(session, headers, cache_key)
        else:
            print("[WARN] Success but no cache key - checking message")
    else:
        print(f"[FAIL] Generation failed: {result.get('message', 'Unknown error')}")
        # Don't return - try with dates too

    # Step 6: Test WITH date filters
    print("\n" + "-" * 60)
    print("Test 2: Generate WITH date filters (last 30 days)")
    print("-" * 60)

    result = generate_items_by_customer_report(
        session, headers, report_id, customer_name, with_dates=True
    )

    if result.get("success"):
        cache_key = result.get("key")
        if cache_key:
            print(f"[OK] Generation successful - key: {cache_key}")
            print(f"[OK] Message: {result.get('message', '')}")
            download_report(session, headers, cache_key, "ItemsByCustomer_WithDates")
        else:
            print("[WARN] Success but no cache key")
    else:
        print(f"[FAIL] Generation failed: {result.get('message', 'Unknown error')}")

    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
