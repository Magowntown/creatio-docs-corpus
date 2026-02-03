#!/usr/bin/env python3
"""Investigate "Items by Customer" report column mapping.

This script queries PROD Creatio OData API to discover:
1. BGSalesByItemView column schema (what IntExcelExport actually uses)
2. BGItemsByCustomerView column schema (the original view, may be empty)
3. IntExcelReport configuration for "Items by Customer"
4. Product entity columns (for description field)

Environment variables:
- CREATIO_PROD_URL, CREATIO_PROD_USERNAME, CREATIO_PROD_PASSWORD (for PROD)
- OR use CREATIO_URL, CREATIO_USERNAME, CREATIO_PASSWORD (defaults to these if PROD not set)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv
from scripts._paths import DOCS_DIR, ensure_dirs

load_dotenv()
ensure_dirs()

# Prefer PROD environment
CREATIO_URL = os.environ.get("CREATIO_PROD_URL", os.environ.get("CREATIO_URL", "")).rstrip("/")
USERNAME = os.environ.get("CREATIO_PROD_USERNAME", os.environ.get("CREATIO_USERNAME", ""))
PASSWORD = os.environ.get("CREATIO_PROD_PASSWORD", os.environ.get("CREATIO_PASSWORD", ""))

TIMEOUT_SECONDS = 120
ITEMS_BY_CUSTOMER_REPORT_ID = "d213933b-093d-47fc-8da8-422c0d9bf715"


class CreatioSession:
    """Manages Creatio API session with authentication."""

    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._authenticated = False

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "BPMCSRF": self.session.cookies.get("BPMCSRF", ""),
        }

    def login(self) -> bool:
        """Authenticate with Creatio."""
        url = f"{self.base_url}/ServiceModel/AuthService.svc/Login"
        payload = {"UserName": self.username, "UserPassword": self.password}
        resp = self.session.post(url, json=payload, timeout=TIMEOUT_SECONDS)
        if resp.status_code != 200:
            print(f"[ERROR] Login failed: {resp.status_code}")
            return False
        data = resp.json()
        if data.get("Code") != 0:
            print(f"[ERROR] Login rejected: {data}")
            return False
        self._authenticated = True
        print(f"[OK] Logged in as {self.username} to {self.base_url}")
        return True

    def odata_get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make OData GET request."""
        if not self._authenticated:
            return None
        url = f"{self.base_url}/0/odata/{endpoint}"
        resp = self.session.get(url, params=params, headers=self._headers(), timeout=TIMEOUT_SECONDS)
        if resp.status_code != 200:
            print(f"[ERROR] OData GET {endpoint} failed: {resp.status_code}")
            print(f"[ERROR] Response: {resp.text[:500]}")
            return None
        return resp.json()

    def odata_metadata(self) -> Optional[str]:
        """Get OData metadata XML."""
        if not self._authenticated:
            return None
        url = f"{self.base_url}/0/odata/$metadata"
        resp = self.session.get(url, headers=self._headers(), timeout=TIMEOUT_SECONDS)
        if resp.status_code != 200:
            print(f"[ERROR] OData metadata failed: {resp.status_code}")
            return None
        return resp.text


def get_entity_columns(session: CreatioSession, entity_name: str) -> List[Dict[str, Any]]:
    """Query SysEntitySchemaColumn for entity's columns."""
    # First get the entity schema ID
    schema_data = session.odata_get("SysSchema", {
        "$filter": f"Name eq '{entity_name}'",
        "$select": "Id,Name,Caption"
    })

    if not schema_data or not schema_data.get("value"):
        print(f"[WARN] Entity schema '{entity_name}' not found in SysSchema")
        return []

    schema_id = schema_data["value"][0]["Id"]
    schema_caption = schema_data["value"][0].get("Caption", entity_name)
    print(f"[INFO] Found {entity_name} schema ID: {schema_id} ({schema_caption})")

    # Get columns from SysEntitySchemaColumn
    # Note: This may not work for views - views might not have columns in this table
    columns_data = session.odata_get("SysEntitySchemaColumn", {
        "$filter": f"SysEntitySchemaUId eq {schema_id}",
        "$select": "Id,Name,Caption,DataValueType",
        "$orderby": "Name"
    })

    if columns_data and columns_data.get("value"):
        return columns_data["value"]
    return []


def get_sample_data(session: CreatioSession, entity_name: str, top: int = 1) -> Optional[Dict]:
    """Get sample data from entity to infer columns."""
    data = session.odata_get(entity_name, {"$top": str(top)})
    if data and data.get("value"):
        return data["value"][0] if data["value"] else None
    return None


def get_entity_count(session: CreatioSession, entity_name: str) -> int:
    """Get total count of records in entity."""
    data = session.odata_get(entity_name, {"$count": "true", "$top": "0"})
    if data:
        return data.get("@odata.count", 0)
    return -1


def get_int_excel_report_config(session: CreatioSession, report_id: str) -> Optional[Dict]:
    """Get IntExcelReport configuration by ID."""
    data = session.odata_get("IntExcelReport", {
        "$filter": f"Id eq {report_id}",
        "$expand": "IntExcelReportLookup"
    })
    if data and data.get("value"):
        return data["value"][0]
    return None


def get_all_items_reports(session: CreatioSession) -> List[Dict]:
    """Find all IntExcelReport entries related to Items/Customer."""
    data = session.odata_get("IntExcelReport", {
        "$filter": "contains(IntName, 'Item') or contains(IntName, 'Customer')",
        "$select": "Id,IntName,IntObjectName,IntQueryConfig",
        "$orderby": "IntName"
    })
    if data and data.get("value"):
        return data["value"]
    return []


def get_product_columns(session: CreatioSession) -> Optional[Dict]:
    """Get sample Product entity data to see available columns."""
    data = session.odata_get("Product", {"$top": "1"})
    if data and data.get("value"):
        return data["value"][0]
    return None


def infer_columns_from_sample(sample_data: Dict) -> List[str]:
    """Extract column names from a sample record."""
    if not sample_data:
        return []
    # Filter out OData metadata keys
    return [k for k in sample_data.keys() if not k.startswith("@odata") and not k.startswith("odata")]


def main():
    print("=" * 70)
    print("Items by Customer - Column Investigation")
    print("=" * 70)
    print(f"Target: {CREATIO_URL}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Initialize session
    session = CreatioSession(CREATIO_URL, USERNAME, PASSWORD)
    if not session.login():
        print("[FATAL] Authentication failed")
        return 1

    results = {
        "timestamp": datetime.now().isoformat(),
        "environment": CREATIO_URL,
        "findings": {}
    }

    # ===================================================================
    # 1. BGSalesByItemView - The view we're actually using
    # ===================================================================
    print("\n" + "-" * 70)
    print("1. BGSalesByItemView (Current Data Source)")
    print("-" * 70)

    # Get record count
    count = get_entity_count(session, "BGSalesByItemView")
    print(f"   Record count: {count}")
    results["findings"]["BGSalesByItemView"] = {"record_count": count}

    # Get sample data to infer columns
    sample = get_sample_data(session, "BGSalesByItemView")
    if sample:
        columns = infer_columns_from_sample(sample)
        print(f"   Columns ({len(columns)}):")
        for col in sorted(columns):
            val = sample.get(col)
            val_type = type(val).__name__
            val_preview = str(val)[:50] + "..." if len(str(val)) > 50 else str(val)
            print(f"      - {col} ({val_type}): {val_preview}")
        results["findings"]["BGSalesByItemView"]["columns"] = columns
        results["findings"]["BGSalesByItemView"]["sample"] = {k: str(v) for k, v in sample.items() if not k.startswith("@")}
    else:
        print("   [WARN] No sample data available")

    # ===================================================================
    # 2. BGItemsByCustomerView - The original view
    # ===================================================================
    print("\n" + "-" * 70)
    print("2. BGItemsByCustomerView (Original View)")
    print("-" * 70)

    count = get_entity_count(session, "BGItemsByCustomerView")
    print(f"   Record count: {count}")
    results["findings"]["BGItemsByCustomerView"] = {"record_count": count}

    sample = get_sample_data(session, "BGItemsByCustomerView")
    if sample:
        columns = infer_columns_from_sample(sample)
        print(f"   Columns ({len(columns)}):")
        for col in sorted(columns):
            val = sample.get(col)
            val_type = type(val).__name__
            val_preview = str(val)[:50] + "..." if len(str(val)) > 50 else str(val)
            print(f"      - {col} ({val_type}): {val_preview}")
        results["findings"]["BGItemsByCustomerView"]["columns"] = columns
        results["findings"]["BGItemsByCustomerView"]["sample"] = {k: str(v) for k, v in sample.items() if not k.startswith("@")}
    else:
        print("   [INFO] View appears to be empty or doesn't exist")

    # ===================================================================
    # 3. IntExcelReport Configuration
    # ===================================================================
    print("\n" + "-" * 70)
    print("3. IntExcelReport Configuration")
    print("-" * 70)

    # Get specific report config
    report_config = get_int_excel_report_config(session, ITEMS_BY_CUSTOMER_REPORT_ID)
    if report_config:
        print(f"   Report ID: {report_config.get('Id')}")
        print(f"   Name: {report_config.get('IntName')}")
        print(f"   Object Name: {report_config.get('IntObjectName')}")
        print(f"   Sheet Name: {report_config.get('IntSheetName')}")

        query_config = report_config.get("IntQueryConfig")
        if query_config:
            print(f"   Query Config (raw):")
            try:
                qc_parsed = json.loads(query_config)
                print(f"      {json.dumps(qc_parsed, indent=6)}")
            except:
                print(f"      {query_config[:200]}...")

        results["findings"]["IntExcelReport"] = {
            "Id": report_config.get("Id"),
            "IntName": report_config.get("IntName"),
            "IntObjectName": report_config.get("IntObjectName"),
            "IntSheetName": report_config.get("IntSheetName"),
            "IntQueryConfig": query_config
        }
    else:
        print(f"   [ERROR] Report {ITEMS_BY_CUSTOMER_REPORT_ID} not found")

    # Get all related reports
    print("\n   All Items/Customer related reports:")
    related_reports = get_all_items_reports(session)
    for rpt in related_reports:
        print(f"      - {rpt.get('IntName')} (Object: {rpt.get('IntObjectName')})")
    results["findings"]["related_reports"] = related_reports

    # ===================================================================
    # 4. Product Entity
    # ===================================================================
    print("\n" + "-" * 70)
    print("4. Product Entity (for Description column)")
    print("-" * 70)

    product_sample = get_product_columns(session)
    if product_sample:
        columns = infer_columns_from_sample(product_sample)
        print(f"   Columns ({len(columns)}):")

        # Highlight description-like columns
        desc_columns = [c for c in columns if 'desc' in c.lower() or 'name' in c.lower() or 'title' in c.lower()]
        for col in desc_columns:
            val = product_sample.get(col)
            val_preview = str(val)[:80] + "..." if len(str(val)) > 80 else str(val)
            print(f"      * {col}: {val_preview}")  # Star for description-like

        print("   All columns:")
        for col in sorted(columns):
            if col not in desc_columns:
                print(f"      - {col}")

        results["findings"]["Product"] = {
            "columns": columns,
            "description_columns": desc_columns,
            "sample": {k: str(v)[:100] for k, v in product_sample.items() if not k.startswith("@")}
        }
    else:
        print("   [ERROR] Could not get Product sample")

    # ===================================================================
    # 5. OrderProduct Entity (line items)
    # ===================================================================
    print("\n" + "-" * 70)
    print("5. OrderProduct Entity (Order Line Items)")
    print("-" * 70)

    order_product_sample = get_sample_data(session, "OrderProduct")
    if order_product_sample:
        columns = infer_columns_from_sample(order_product_sample)
        print(f"   Columns ({len(columns)}):")

        # Highlight important columns
        important = ['ProductId', 'Product', 'Name', 'Quantity', 'Price', 'Amount', 'OrderId']
        for col in columns:
            if any(imp.lower() in col.lower() for imp in important):
                val = order_product_sample.get(col)
                val_preview = str(val)[:60] + "..." if len(str(val)) > 60 else str(val)
                print(f"      * {col}: {val_preview}")

        results["findings"]["OrderProduct"] = {
            "columns": columns,
            "sample": {k: str(v)[:100] for k, v in order_product_sample.items() if not k.startswith("@")}
        }
    else:
        print("   [WARN] Could not get OrderProduct sample")

    # ===================================================================
    # 6. Check if BGItem links to Product.Name
    # ===================================================================
    print("\n" + "-" * 70)
    print("6. BGItem Column Analysis")
    print("-" * 70)

    # Query a few distinct BGItem values
    items_data = session.odata_get("BGSalesByItemView", {
        "$select": "BGItem,BGNumber",
        "$top": "10",
        "$orderby": "BGItem"
    })
    if items_data and items_data.get("value"):
        print("   Sample BGItem values (first 10):")
        for item in items_data["value"]:
            print(f"      BGItem: {item.get('BGItem', 'NULL')} | BGNumber: {item.get('BGNumber', 'NULL')}")
        results["findings"]["BGItem_samples"] = items_data["value"]
    else:
        print("   [WARN] Could not get BGItem samples")

    # ===================================================================
    # Summary
    # ===================================================================
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print("""
Key Findings:
- BGSalesByItemView.BGItem contains: Check sample data above
- BGSalesByItemView.BGNumber contains: Check sample data above
- Product entity has description column: Check 'description_columns' above
- IntExcelReport configured for: Check IntObjectName above
    """)

    # Save results to JSON for reference
    results_file = REPO_ROOT / "test-artifacts" / f"column_investigation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nDetailed results saved to: {results_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
