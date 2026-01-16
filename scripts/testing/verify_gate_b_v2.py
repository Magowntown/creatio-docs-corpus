#!/usr/bin/env python3
"""Gate B Verification v2: Check if UsrPage_ebkv9e8 contains the hidden iframe download approach.

This version checks multiple tables where Creatio stores schema content:
- SysSchema.Body
- SysSchemaContent
- VwSysClientUnitSchemaContent

Schema details:
- Schema Name: UsrPage_ebkv9e8
- Schema UId: 1d5dfc4d-732d-48d7-af21-9e3d70794734
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv

load_dotenv()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com").rstrip("/")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
TIMEOUT_SECONDS = int(os.environ.get("CREATIO_TIMEOUT_SECONDS", "120"))

SCHEMA_NAME = "UsrPage_ebkv9e8"
SCHEMA_UID = "1d5dfc4d-732d-48d7-af21-9e3d70794734"

# Marker we're looking for - the hidden iframe ID
IFRAME_MARKER = "reportDownloadFrame"


def _headers(session: requests.Session) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", ""),
    }


def _select_query(session: requests.Session, headers: Dict[str, str], body: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    resp = session.post(url, json=body, headers=headers, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        raise RuntimeError(f"SelectQuery failed: {resp.status_code} {resp.text[:300]}")
    return resp.json()


def _odata_get(session: requests.Session, headers: Dict[str, str], endpoint: str) -> Optional[Dict[str, Any]]:
    """Execute an OData GET request."""
    url = f"{CREATIO_URL}/0/odata/{endpoint}"
    try:
        resp = session.get(url, headers=headers, timeout=TIMEOUT_SECONDS)
        if resp.status_code == 200:
            return resp.json()
        print(f"  OData {endpoint}: status {resp.status_code}")
        return None
    except Exception as e:
        print(f"  OData {endpoint}: error {e}")
        return None


def check_odata_schema_content(session: requests.Session, headers: Dict[str, str], schema_uid: str) -> Optional[str]:
    """Try to get schema content via OData."""
    # Try VwSysClientUnitSchemaContent
    endpoint = f"VwSysClientUnitSchemaContent?$filter=UId eq {schema_uid}"
    data = _odata_get(session, headers, endpoint)
    if data and data.get("value"):
        for item in data["value"]:
            content = item.get("Content") or item.get("Body") or ""
            if content:
                return content
    return None


def get_schema_via_config_endpoint(session: requests.Session, headers: Dict[str, str], schema_name: str) -> Optional[str]:
    """Try the configuration service endpoint to get schema content."""
    # Try getting the schema via the configuration API
    url = f"{CREATIO_URL}/0/ServiceModel/ClientUnitSchemaDesignerService.svc/GetSchema"
    payload = {"schemaName": schema_name}
    try:
        resp = session.post(url, json=payload, headers=headers, timeout=TIMEOUT_SECONDS)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict):
                return data.get("body") or data.get("Body") or data.get("schema") or None
    except Exception as e:
        print(f"  ClientUnitSchemaDesignerService error: {e}")
    return None


def get_compiled_content(session: requests.Session, headers: Dict[str, str], schema_name: str) -> Optional[str]:
    """Try to get the compiled/runtime content from the client app."""
    # This gets the actual runtime JS module
    url = f"{CREATIO_URL}/0/core/hash/{schema_name}.js"
    try:
        resp = session.get(url, timeout=TIMEOUT_SECONDS)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass

    # Alternative paths
    for path in [
        f"/0/ClientApp/conf/content/{schema_name}.js",
        f"/0/conf/content/{schema_name}.js",
    ]:
        try:
            resp = session.get(f"{CREATIO_URL}{path}", timeout=TIMEOUT_SECONDS)
            if resp.status_code == 200:
                return resp.text
        except Exception:
            pass

    return None


def main() -> None:
    if not USERNAME or not PASSWORD:
        raise SystemExit("Set CREATIO_USERNAME and CREATIO_PASSWORD in your environment")

    session = requests.Session()

    print("=" * 60)
    print("GATE B VERIFICATION v2: Hidden Iframe Download Approach")
    print("=" * 60)
    print(f"\nTarget: {CREATIO_URL}")
    print(f"Schema: {SCHEMA_NAME}")
    print(f"UId: {SCHEMA_UID}")
    print(f"Marker: '{IFRAME_MARKER}'")
    print()

    print("--- Step 1: Logging in ---")
    resp = session.post(
        f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
        json={"UserName": USERNAME, "UserPassword": PASSWORD},
        timeout=TIMEOUT_SECONDS,
    )
    if resp.status_code != 200:
        raise SystemExit(f"Login FAILED ({resp.status_code}): {resp.text[:200]}")
    print("Login: OK")

    headers = _headers(session)
    found_content = None
    source_name = None

    # Method 1: SysSchemaContent table
    print("\n--- Method 1: SysSchemaContent table ---")
    esq_body = {
        "rootSchemaName": "SysSchemaContent",
        "operationType": 0,
        "columns": {
            "items": {
                "Id": {"expression": {"columnPath": "Id"}},
                "SysSchema": {"expression": {"columnPath": "SysSchema.Name"}},
                "ContentType": {"expression": {"columnPath": "ContentType"}},
                "Content": {"expression": {"columnPath": "Content"}},
            }
        },
        "filters": {
            "filterType": 6,
            "items": {
                "SchemaFilter": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "leftExpression": {"expressionType": 0, "columnPath": "SysSchema.Name"},
                    "rightExpression": {
                        "expressionType": 2,
                        "parameter": {"dataValueType": 1, "value": SCHEMA_NAME},
                    },
                }
            },
        },
        "rowCount": 10,
    }
    try:
        data = _select_query(session, headers, esq_body)
        rows = data.get("rows", [])
        print(f"Found {len(rows)} SysSchemaContent records")
        for row in rows:
            content = row.get("Content") or ""
            content_type = row.get("ContentType")
            print(f"  ContentType: {content_type}, length: {len(content)}")
            if content and len(content) > len(found_content or ""):
                found_content = content
                source_name = f"SysSchemaContent (type={content_type})"
    except Exception as e:
        print(f"Error: {e}")

    # Method 2: Check compiled runtime JS
    print("\n--- Method 2: Compiled runtime JS ---")
    compiled = get_compiled_content(session, headers, SCHEMA_NAME)
    if compiled:
        print(f"Found compiled content: {len(compiled)} chars")
        if len(compiled) > len(found_content or ""):
            found_content = compiled
            source_name = "Compiled runtime JS"
    else:
        print("No compiled content found")

    # Method 3: ClientUnitSchemaDesignerService
    print("\n--- Method 3: ClientUnitSchemaDesignerService ---")
    designer_content = get_schema_via_config_endpoint(session, headers, SCHEMA_NAME)
    if designer_content:
        print(f"Found designer content: {len(designer_content)} chars")
        if len(designer_content) > len(found_content or ""):
            found_content = designer_content
            source_name = "ClientUnitSchemaDesignerService"
    else:
        print("No designer content found")

    # Method 4: Try direct DataService SelectQuery with different column names
    print("\n--- Method 4: SysSchema with various content columns ---")
    for col_name in ["Body", "ClientUnitSchemaBody", "SchemaBody"]:
        esq_body = {
            "rootSchemaName": "SysSchema",
            "operationType": 0,
            "columns": {
                "items": {
                    "Id": {"expression": {"columnPath": "Id"}},
                    "Name": {"expression": {"columnPath": "Name"}},
                    col_name: {"expression": {"columnPath": col_name}},
                }
            },
            "filters": {
                "filterType": 6,
                "items": {
                    "NameFilter": {
                        "filterType": 1,
                        "comparisonType": 3,
                        "leftExpression": {"expressionType": 0, "columnPath": "Name"},
                        "rightExpression": {
                            "expressionType": 2,
                            "parameter": {"dataValueType": 1, "value": SCHEMA_NAME},
                        },
                    }
                },
            },
            "rowCount": 1,
        }
        try:
            data = _select_query(session, headers, esq_body)
            rows = data.get("rows", [])
            if rows:
                content = rows[0].get(col_name) or ""
                print(f"  {col_name}: {len(content)} chars")
                if content and len(content) > len(found_content or ""):
                    found_content = content
                    source_name = f"SysSchema.{col_name}"
        except Exception as e:
            print(f"  {col_name}: error - {str(e)[:50]}")

    # Method 5: Try VwSysClientUnitSchema view
    print("\n--- Method 5: VwSysClientUnitSchema view ---")
    esq_body = {
        "rootSchemaName": "VwSysClientUnitSchema",
        "operationType": 0,
        "columns": {
            "items": {
                "Id": {"expression": {"columnPath": "Id"}},
                "Name": {"expression": {"columnPath": "Name"}},
                "Body": {"expression": {"columnPath": "Body"}},
            }
        },
        "filters": {
            "filterType": 6,
            "items": {
                "NameFilter": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "leftExpression": {"expressionType": 0, "columnPath": "Name"},
                    "rightExpression": {
                        "expressionType": 2,
                        "parameter": {"dataValueType": 1, "value": SCHEMA_NAME},
                    },
                }
            },
        },
        "rowCount": 1,
    }
    try:
        data = _select_query(session, headers, esq_body)
        rows = data.get("rows", [])
        if rows:
            content = rows[0].get("Body") or ""
            print(f"Found: {len(content)} chars")
            if content and len(content) > len(found_content or ""):
                found_content = content
                source_name = "VwSysClientUnitSchema.Body"
        else:
            print("No rows found")
    except Exception as e:
        print(f"Error: {e}")

    # Analyze results
    print("\n" + "=" * 60)
    print("ANALYSIS")
    print("=" * 60)

    if not found_content:
        print("\nNo schema content found in any location!")
        print("\nResult: VERIFICATION_FAILED (no content found)")
        return

    print(f"\nBest content source: {source_name}")
    print(f"Content length: {len(found_content)} chars")

    # Check for the iframe marker
    contains_iframe = IFRAME_MARKER in found_content

    print(f"\nSearching for '{IFRAME_MARKER}'...")

    if contains_iframe:
        idx = found_content.find(IFRAME_MARKER)
        start = max(0, idx - 100)
        end = min(len(found_content), idx + len(IFRAME_MARKER) + 100)
        context = found_content[start:end]

        print(f"FOUND at position {idx}")
        print(f"\nContext snippet:")
        print("-" * 40)
        print(f"...{context}...")
        print("-" * 40)
    else:
        print("NOT FOUND")

    # Check for other markers
    print("\n--- Additional markers check ---")
    markers = [
        ("window.open", "Direct browser download via window.open"),
        ("createObjectURL", "Blob URL download method"),
        ("UsrExcelReportService/Generate", "Custom generate service endpoint"),
        ("UsrExcelReportService", "Custom service reference"),
        ("IntExcelReportService/GetReport", "Report download endpoint"),
        ("IntExcelReportService", "Int report service reference"),
        ("usr.GenerateExcelReportRequest", "Handler request name"),
        ("ExportReportBtnClick", "Export button click handler"),
        ("loadIndicatorVisible", "Loading indicator"),
    ]
    for marker, desc in markers:
        if marker in found_content:
            print(f"  [FOUND] {marker}")
            print(f"          {desc}")
        else:
            print(f"  [not found] {marker}")

    # Save the content for inspection
    output_file = REPO_ROOT / "test-artifacts" / f"schema_content_{SCHEMA_NAME}.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(found_content, encoding="utf-8")
    print(f"\nContent saved to: {output_file}")

    # Final verdict
    print("\n" + "=" * 60)
    if contains_iframe:
        print("RESULT: DEPLOYED")
        print("The hidden iframe download approach (reportDownloadFrame) IS present.")
    else:
        print("RESULT: NOT_DEPLOYED")
        print("The hidden iframe download approach (reportDownloadFrame) is NOT present.")
    print("=" * 60)


if __name__ == "__main__":
    main()
