#!/usr/bin/env python3
"""Check Commission report data availability in PROD."""

import os
import requests
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

class CreatioClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._login(username, password)

    def _login(self, username, password):
        login_url = f"{self.base_url}/ServiceModel/AuthService.svc/Login"
        resp = self.session.post(login_url, json={
            "UserName": username,
            "UserPassword": password
        })
        if resp.status_code != 200 or resp.json().get("Code") != 0:
            raise Exception(f"Login failed: {resp.text}")
        print(f"✓ Logged in to {self.base_url}")

    def query(self, entity, columns=None, filters=None, order_by=None, limit=100):
        url = f"{self.base_url}/0/odata/{entity}"
        params = {"$top": str(limit)}
        if columns:
            params["$select"] = ",".join(columns)
        if filters:
            params["$filter"] = filters
        if order_by:
            params["$orderby"] = order_by

        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            print(f"Query error: {resp.status_code} - {resp.text[:300]}")
            return []
        return resp.json().get("value", [])

    def count(self, entity, filters=None):
        url = f"{self.base_url}/0/odata/{entity}/$count"
        params = {}
        if filters:
            params["$filter"] = filters
        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            return -1
        try:
            return int(resp.text)
        except:
            return -1

def main():
    print("=" * 70)
    print("PROD Commission Data Investigation")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Check available Year-Months
    print("\n1. Available Year-Months (recent)")
    print("-" * 50)
    year_months = client.query(
        "BGYearMonth",
        columns=["Id", "Name"],
        order_by="Name desc",
        limit=15
    )
    for ym in year_months:
        print(f"  {ym.get('Name')} -> {ym.get('Id')}")

    # 2. Check Faire sales group
    print("\n2. Faire Sales Group")
    print("-" * 50)
    faire = client.query(
        "BGSalesGroup",
        columns=["Id", "BGSalesGroupName"],
        filters="contains(BGSalesGroupName, 'Faire')"
    )
    faire_id = None
    for sg in faire:
        print(f"  {sg.get('BGSalesGroupName')} -> {sg.get('Id')}")
        faire_id = sg.get('Id')

    # 3. Check recent BGReportExecution records for Commission
    print("\n3. Recent Commission Executions")
    print("-" * 50)
    executions = client.query(
        "BGReportExecution",
        columns=["Id", "BGReportName", "BGYearMonthId", "BGSalesGroupId", "CreatedOn"],
        filters="contains(BGReportName, 'Commission')",
        order_by="CreatedOn desc",
        limit=5
    )
    recent_exec_ids = []
    for ex in executions:
        exec_id = ex.get('Id')
        recent_exec_ids.append(exec_id)
        print(f"  Execution: {exec_id}")
        print(f"    YearMonthId: {ex.get('BGYearMonthId')}")
        print(f"    SalesGroupId: {ex.get('BGSalesGroupId')}")
        print(f"    Created: {ex.get('CreatedOn')}")
        print()

    # 4. Try to query BGCommissionReportDataView directly
    print("\n4. BGCommissionReportDataView - Check Data Availability")
    print("-" * 50)

    # First check if the view exists and has data at all
    try:
        total_count = client.count("BGCommissionReportDataView")
        print(f"  Total records in view (no filter): {total_count}")
    except Exception as e:
        print(f"  Error counting view: {e}")

    # Check with recent execution IDs
    for exec_id in recent_exec_ids[:3]:
        count = client.count("BGCommissionReportDataView", f"BGExecutionId eq {exec_id}")
        print(f"  Records for ExecutionId {exec_id}: {count}")

    # 5. Check base data - BGQBDownload (source table for commission)
    print("\n5. BGQBDownload - Base Commission Data")
    print("-" * 50)

    # Count all records
    qb_total = client.count("BGQBDownload")
    print(f"  Total BGQBDownload records: {qb_total}")

    # Check for recent transaction dates
    recent_months = ["2025-12", "2026-01", "2025-11"]
    for month in recent_months:
        year, mo = month.split("-")
        start_date = f"{year}-{mo}-01T00:00:00Z"
        if mo == "12":
            end_date = f"{int(year)+1}-01-01T00:00:00Z"
        else:
            end_date = f"{year}-{int(mo)+1:02d}-01T00:00:00Z"

        # Try filtering by BGTransactionDate
        count = client.count(
            "BGQBDownload",
            f"BGTransactionDate ge {start_date} and BGTransactionDate lt {end_date}"
        )
        print(f"  Records for {month} (by BGTransactionDate): {count}")

    # 6. Check Sales Orders with Invoice Date (used by view)
    print("\n6. SalesOrder - Invoice Dates")
    print("-" * 50)
    for month in recent_months:
        year, mo = month.split("-")
        start_date = f"{year}-{mo}-01T00:00:00Z"
        if mo == "12":
            end_date = f"{int(year)+1}-01-01T00:00:00Z"
        else:
            end_date = f"{year}-{int(mo)+1:02d}-01T00:00:00Z"

        count = client.count(
            "SalesOrder",
            f"BGInvoiceDate ge {start_date} and BGInvoiceDate lt {end_date}"
        )
        print(f"  Orders invoiced in {month}: {count}")

    # 7. Check if Faire has any commission data
    if faire_id:
        print(f"\n7. Commission Data for Faire ({faire_id})")
        print("-" * 50)

        # Check BGQBDownload for Faire sales group via SalesRep
        # This requires knowing the relationship chain
        print("  Checking via execution records...")

        for ex in executions:
            if ex.get('BGSalesGroupId') == faire_id:
                exec_id = ex.get('Id')
                ym_id = ex.get('BGYearMonthId')

                # Look up year-month name
                ym = client.query("BGYearMonth", columns=["Name"], filters=f"Id eq {ym_id}")
                ym_name = ym[0].get('Name') if ym else 'unknown'

                count = client.count("BGCommissionReportDataView", f"BGExecutionId eq {exec_id}")
                print(f"    Execution {exec_id[:8]}... (YM: {ym_name}): {count} records")

    print("\n" + "=" * 70)
    print("Investigation complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
