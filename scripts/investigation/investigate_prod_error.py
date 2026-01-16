#!/usr/bin/env python3
"""Investigate PROD GUID parsing error for Commission report."""

import os
import sys
import json
import requests

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
        """Run OData query."""
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

def main():
    print("=" * 60)
    print("PROD Investigation - Commission Report & Faire")
    print("=" * 60)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Find Commission report specifically
    print("\n1. Find Commission Report in IntExcelReport")
    print("-" * 40)
    reports = client.query(
        "IntExcelReport",
        columns=["Id", "IntName", "IntEntitySchemaNameId", "IntEntitySchemaId", "IntSheetName"],
        filters="contains(IntName, 'Commission')",
        limit=10
    )
    for r in reports:
        print(f"  Report: {r.get('IntName')}")
        print(f"    Id: {r.get('Id')}")
        print(f"    IntEntitySchemaNameId: {r.get('IntEntitySchemaNameId')}")
        print(f"    IntEntitySchemaId: {r.get('IntEntitySchemaId')}")
        print(f"    SheetName: {r.get('IntSheetName')}")

        # Check if IntEntitySchemaNameId is valid
        schema_id = r.get('IntEntitySchemaNameId')
        if schema_id:
            if schema_id == '00000000-0000-0000-0000-000000000000':
                print(f"    ⚠️ IntEntitySchemaNameId is EMPTY GUID!")
            else:
                print(f"    ✓ IntEntitySchemaNameId is set")
        print()

    # 2. Find Faire in BGSalesGroup
    print("\n2. Find 'Faire' in BGSalesGroup")
    print("-" * 40)
    sales_groups = client.query(
        "BGSalesGroup",
        columns=["Id", "BGSalesGroupName", "BGIsActive"],
        filters="contains(BGSalesGroupName, 'Faire')",
        limit=10
    )
    if sales_groups:
        for sg in sales_groups:
            print(f"  Found: {sg.get('BGSalesGroupName')}")
            print(f"    Id: {sg.get('Id')}")
            print(f"    Active: {sg.get('BGIsActive')}")
    else:
        print("  ⚠️ No 'Faire' sales group found!")
        print("\n  Let me search all active sales groups...")
        all_active = client.query(
            "BGSalesGroup",
            columns=["Id", "BGSalesGroupName"],
            filters="BGIsActive eq true",
            limit=50
        )
        for sg in all_active:
            print(f"    - {sg.get('BGSalesGroupName')}")

    # 3. Check recent Commission executions
    print("\n3. Recent Commission Report Executions")
    print("-" * 40)
    executions = client.query(
        "BGReportExecution",
        columns=["Id", "BGReportName", "BGYearMonthId", "BGSalesGroupId", "CreatedOn"],
        filters="contains(BGReportName, 'Commission')",
        order_by="CreatedOn desc",
        limit=5
    )
    for ex in executions:
        print(f"  Report: {ex.get('BGReportName')}")
        print(f"    ExecutionId: {ex.get('Id')}")
        print(f"    YearMonthId: {ex.get('BGYearMonthId')}")
        print(f"    SalesGroupId: {ex.get('BGSalesGroupId')}")
        print(f"    Created: {ex.get('CreatedOn')}")

        # Check if the SalesGroupId is valid
        sg_id = ex.get('BGSalesGroupId')
        if sg_id and sg_id != '00000000-0000-0000-0000-000000000000':
            # Look up the sales group name
            sg = client.query(
                "BGSalesGroup",
                columns=["BGSalesGroupName"],
                filters=f"Id eq {sg_id}"
            )
            if sg:
                print(f"    SalesGroup Name: {sg[0].get('BGSalesGroupName')}")
        print()

    # 4. Check if there's an IntExcelReportCode or similar field
    print("\n4. IntExcelReport - Looking for Code Field")
    print("-" * 40)
    # Get all fields by querying metadata
    all_reports = client.query("IntExcelReport", limit=20)
    if all_reports:
        print(f"  All columns: {list(all_reports[0].keys())}")

        # Search for Commission by name
        for r in all_reports:
            name = r.get('IntName', '')
            if 'Commission' in name:
                print(f"\n  ** FOUND Commission Report **")
                for k, v in r.items():
                    if v is not None and v != "" and not k.startswith('@'):
                        print(f"    {k}: {v}")

    print("\n" + "=" * 60)
    print("Investigation complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
