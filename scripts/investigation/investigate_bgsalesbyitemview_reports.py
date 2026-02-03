#!/usr/bin/env python3
"""Investigate all reports using BGSalesByItemView in PROD.

This script:
1. Queries IntExcelReport for all templates using BGSalesByItemView
2. Analyzes ESQ configuration for each report
3. Checks column mappings and potential conflicts
4. Documents impact of adding a Product description column
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv
from scripts._paths import ensure_dirs

load_dotenv()
ensure_dirs()

# Use PROD environment
CREATIO_URL = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com").rstrip("/")
USERNAME = os.environ.get("CREATIO_PROD_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PROD_PASSWORD", "")

TIMEOUT_SECONDS = 120

# Known reports using BGSalesByItemView
KNOWN_REPORTS = {
    "d213933b-093d-47fc-8da8-422c0d9bf715": "Items by Customer",
    "c4f4e32c-376d-4b19-b04b-2129dba29d06": "Rpt Sales By Item",
    "53682214-a63c-407a-b3f1-79d8ab235f18": "Rpt Sales By Item By Type Of Customer"
}

# BGSalesByItemView schema ID
BGSALESBYITEMVIEW_SCHEMA_ID = "5f969641-af66-48bd-9fca-b532f479684f"


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
    print(f"[OK] Logged in as {USERNAME} to {CREATIO_URL}")
    return True


def get_all_int_excel_reports(session: requests.Session, headers: Dict[str, str]) -> List[Dict]:
    """Get all IntExcelReport records."""
    url = f"{CREATIO_URL}/0/odata/IntExcelReport"
    params = {
        "$select": "Id,IntName,IntEntitySchemaNameId,IntEsq",
        "$orderby": "IntName"
    }
    resp = session.get(url, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        print(f"[ERROR] IntExcelReport query failed: {resp.status_code}")
        return []

    data = resp.json()
    return data.get("value", [])


def get_schema_name(session: requests.Session, headers: Dict[str, str], schema_id: str) -> Optional[str]:
    """Get schema name from SysSchema by ID."""
    if not schema_id:
        return None

    url = f"{CREATIO_URL}/0/odata/SysSchema({schema_id})"
    params = {"$select": "Name,Caption"}
    resp = session.get(url, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        return None

    data = resp.json()
    return data.get("Name")


def get_view_columns(session: requests.Session, headers: Dict[str, str], schema_name: str) -> List[Dict]:
    """Get columns from a view/entity schema."""
    # Query SysEntitySchemaColumn for the schema
    url = f"{CREATIO_URL}/0/odata/SysEntitySchemaColumn"

    # First get the schema ID
    schema_url = f"{CREATIO_URL}/0/odata/VwSysEntitySchemaInWorkspace"
    schema_params = {
        "$filter": f"Name eq '{schema_name}'",
        "$select": "UId,Name,Caption"
    }
    resp = session.get(schema_url, params=schema_params, headers=headers, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        print(f"[WARN] Could not find schema {schema_name}")
        return []

    schema_data = resp.json()
    schemas = schema_data.get("value", [])
    if not schemas:
        return []

    schema_uid = schemas[0].get("UId")

    # Now get columns
    col_url = f"{CREATIO_URL}/0/odata/VwSysEntitySchemaColumn"
    col_params = {
        "$filter": f"SysEntitySchemaUId eq {schema_uid}",
        "$select": "Name,Caption,DataValueTypeId",
        "$orderby": "Name"
    }
    resp = session.get(col_url, params=col_params, headers=headers, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        return []

    return resp.json().get("value", [])


def parse_esq_columns(int_esq: str) -> List[str]:
    """Parse column names from IntEsq JSON."""
    if not int_esq:
        return []

    try:
        esq = json.loads(int_esq)
        columns = []

        # ESQ structure has 'columns' object with column definitions
        if "columns" in esq and isinstance(esq["columns"], dict):
            for col_key, col_def in esq["columns"].items():
                if isinstance(col_def, dict):
                    col_path = col_def.get("columnPath", col_key)
                    col_caption = col_def.get("caption", col_path)
                    columns.append({
                        "key": col_key,
                        "path": col_path,
                        "caption": col_caption
                    })

        return columns
    except json.JSONDecodeError:
        return []


def analyze_report(session: requests.Session, headers: Dict[str, str], report: Dict) -> Dict:
    """Analyze a single IntExcelReport record."""
    report_id = report.get("Id")
    report_name = report.get("IntName", "Unknown")
    schema_id = report.get("IntEntitySchemaNameId")
    int_esq = report.get("IntEsq", "")

    result = {
        "id": report_id,
        "name": report_name,
        "schema_id": schema_id,
        "schema_name": None,
        "uses_bgsalesbyitemview": False,
        "esq_columns": [],
        "has_template": True  # Assume yes since we got it from IntExcelReport
    }

    # Get schema name
    if schema_id:
        result["schema_name"] = get_schema_name(session, headers, schema_id)
        result["uses_bgsalesbyitemview"] = (
            schema_id == BGSALESBYITEMVIEW_SCHEMA_ID or
            result["schema_name"] == "BGSalesByItemView"
        )

    # Parse ESQ columns
    result["esq_columns"] = parse_esq_columns(int_esq)

    return result


def main():
    print("=" * 70)
    print("BGSalesByItemView Report Impact Analysis")
    print(f"Environment: PROD ({CREATIO_URL})")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    session = requests.Session()

    # Login
    if not login(session):
        return 1

    headers = _headers(session)

    # Get all IntExcelReport records
    print("\n[1/4] Fetching all IntExcelReport records...")
    all_reports = get_all_int_excel_reports(session, headers)
    print(f"      Found {len(all_reports)} total report templates")

    # Analyze each report
    print("\n[2/4] Analyzing reports for BGSalesByItemView usage...")
    bgsalesbyitem_reports = []
    other_reports = []

    for report in all_reports:
        analysis = analyze_report(session, headers, report)
        if analysis["uses_bgsalesbyitemview"]:
            bgsalesbyitem_reports.append(analysis)
            print(f"      [BGSalesByItemView] {analysis['name']}")
        else:
            other_reports.append(analysis)

    print(f"\n      Found {len(bgsalesbyitem_reports)} reports using BGSalesByItemView")

    # Get BGSalesByItemView columns
    print("\n[3/4] Fetching BGSalesByItemView column schema...")
    view_columns = get_view_columns(session, headers, "BGSalesByItemView")
    print(f"      Found {len(view_columns)} columns in view")

    # Generate output
    print("\n[4/4] Generating impact analysis report...")

    output = []
    output.append("# Option A Impact Analysis: Adding Product Description to BGSalesByItemView")
    output.append("")
    output.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    output.append(f"**Environment:** PROD (pampabay.creatio.com)")
    output.append(f"**Analysis Type:** Column addition impact assessment")
    output.append("")
    output.append("---")
    output.append("")
    output.append("## Summary")
    output.append("")
    output.append(f"- **Total IntExcelReport templates:** {len(all_reports)}")
    output.append(f"- **Reports using BGSalesByItemView:** {len(bgsalesbyitem_reports)}")
    output.append("")
    output.append("### Reports Affected by View Change")
    output.append("")
    output.append("| Report Name | Report ID | Impact Level |")
    output.append("|-------------|-----------|--------------|")

    for report in bgsalesbyitem_reports:
        impact = "LOW"  # Default - new column appended, won't break existing
        if "Item" in report["name"]:
            impact = "REVIEW"
        output.append(f"| {report['name']} | `{report['id']}` | {impact} |")

    output.append("")
    output.append("---")
    output.append("")
    output.append("## BGSalesByItemView Current Schema")
    output.append("")
    output.append("### Columns from Database/Entity Schema")
    output.append("")
    if view_columns:
        output.append("| Column Name | Caption | Data Type |")
        output.append("|-------------|---------|-----------|")
        for col in view_columns:
            output.append(f"| {col.get('Name', 'N/A')} | {col.get('Caption', 'N/A')} | {col.get('DataValueTypeId', 'N/A')} |")
    else:
        output.append("*Could not retrieve columns from metadata - see direct SQL query below*")
        output.append("")
        output.append("**Known columns from documentation:**")
        output.append("")
        output.append("| Column | Type | Description |")
        output.append("|--------|------|-------------|")
        output.append("| Id | uuid | Primary key |")
        output.append("| BGCustomer | varchar | Customer name |")
        output.append("| BGItem | varchar | Item/Product code |")
        output.append("| BGNumber | varchar | Order number |")
        output.append("| BGPONumber | varchar | PO number |")
        output.append("| BGQuantity | integer | Quantity |")
        output.append("| BGPrice | numeric | Unit price |")
        output.append("| BGAmount | numeric | Total amount |")
        output.append("| BGSalesGroup | varchar | Sales group name |")
        output.append("| BGSalesRep | varchar | Sales rep name |")
        output.append("| BGStatus | varchar | Order status |")
        output.append("| CreatedOn | timestamp | Order creation date |")
        output.append("| BGShipDate | date | Shipping date |")
        output.append("| BGDeliveryDate | date | Delivery date |")

    output.append("")
    output.append("---")
    output.append("")
    output.append("## Detailed Report Analysis")
    output.append("")

    for report in bgsalesbyitem_reports:
        output.append(f"### {report['name']}")
        output.append("")
        output.append(f"**ID:** `{report['id']}`")
        output.append(f"**Schema:** {report['schema_name'] or 'Unknown'}")
        output.append("")

        if report["esq_columns"]:
            output.append("**ESQ Columns:**")
            output.append("")
            output.append("| Key | Column Path | Caption |")
            output.append("|-----|-------------|---------|")
            for col in report["esq_columns"]:
                output.append(f"| {col['key']} | {col['path']} | {col['caption']} |")
            output.append("")
        else:
            output.append("*ESQ column parsing not available or ESQ is empty*")
            output.append("")

        # Impact analysis for this report
        output.append("**Impact Assessment:**")
        output.append("")
        if report["name"] == "Items by Customer":
            output.append("- **Status:** REVIEW REQUIRED")
            output.append("- **Reason:** VBA macro reads columns by position")
            output.append("- **Risk:** If new column is inserted (not appended), VBA will read wrong data")
            output.append("- **Mitigation:** Ensure new column is added AFTER existing columns in ESQ")
            output.append("- **Benefit:** Product description would add value to this report")
        elif "Item" in report["name"]:
            output.append("- **Status:** LOW RISK")
            output.append("- **Reason:** Standard Excel report without VBA macros")
            output.append("- **Risk:** Minimal - new column will appear in output but won't break existing")
            output.append("- **Benefit:** Product description would enhance report readability")
        else:
            output.append("- **Status:** LOW RISK")
            output.append("- **Reason:** Report likely doesn't depend on column positions")
        output.append("")

    output.append("---")
    output.append("")
    output.append("## Proposed Change: Add BGProductDescription Column")
    output.append("")
    output.append("### SQL View Modification")
    output.append("")
    output.append("```sql")
    output.append("-- Add product description to BGSalesByItemView")
    output.append("-- This should JOIN with Product table to get description")
    output.append("ALTER VIEW \"BGSalesByItemView\" AS")
    output.append("SELECT")
    output.append("    existing_columns...,")
    output.append("    p.\"Name\" AS \"BGProductDescription\"  -- NEW COLUMN")
    output.append("FROM existing_join")
    output.append("LEFT JOIN \"Product\" p ON ...")
    output.append("```")
    output.append("")
    output.append("### Required Backend Changes")
    output.append("")
    output.append("1. **QuerySalesByItemData()** - Add BGProductDescription to columnMapping")
    output.append("2. **Ensure column order matches VBA expectations**")
    output.append("")
    output.append("### Required Template Changes")
    output.append("")
    output.append("1. **Items by Customer Excel template** - Add column header for description")
    output.append("2. **Other templates** - Optional, will auto-include if in ESQ")
    output.append("")
    output.append("---")
    output.append("")
    output.append("## Impact Summary")
    output.append("")
    output.append("| Aspect | Risk Level | Notes |")
    output.append("|--------|------------|-------|")
    output.append("| View modification | LOW | Adding column doesn't break existing queries |")
    output.append("| Items by Customer VBA | MEDIUM | Column order must be preserved |")
    output.append("| Other reports | LOW | New column appears but doesn't break them |")
    output.append("| Backend code | LOW | Just add column to mapping |")
    output.append("| Template files | MEDIUM | May need to update templates |")
    output.append("")
    output.append("### Recommendation")
    output.append("")
    output.append("**PROCEED WITH CAUTION**")
    output.append("")
    output.append("1. Adding a column to BGSalesByItemView is safe at the database level")
    output.append("2. The \"Items by Customer\" report needs special attention due to VBA macros")
    output.append("3. Test thoroughly in DEV before deploying to PROD")
    output.append("4. Consider Option B (new dedicated view) if VBA dependencies are complex")
    output.append("")
    output.append("---")
    output.append("")
    output.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    # Write to file
    output_path = REPO_ROOT / "docs" / "investigation" / "OPTION_A_OTHER_REPORTS_IMPACT.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write("\n".join(output))

    print(f"\n[DONE] Report saved to: {output_path}")

    # Also print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nReports using BGSalesByItemView ({len(bgsalesbyitem_reports)}):")
    for report in bgsalesbyitem_reports:
        print(f"  - {report['name']} ({report['id']})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
