#!/usr/bin/env python3
"""Gate B Verification: Check if UsrPage_ebkv9e8 contains the hidden iframe download approach.

This script:
- Logs into DEV Creatio
- Queries the SysSchema table for UsrPage_ebkv9e8
- Checks if the schema body contains "reportDownloadFrame" (the hidden iframe ID)
- Reports: DEPLOYED or NOT_DEPLOYED

Schema details:
- Schema Name: UsrPage_ebkv9e8
- Schema UId: 1d5dfc4d-732d-48d7-af21-9e3d70794734
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

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


def main() -> None:
    if not USERNAME or not PASSWORD:
        raise SystemExit("Set CREATIO_USERNAME and CREATIO_PASSWORD in your environment")

    session = requests.Session()

    # Login
    print("=" * 60)
    print("GATE B VERIFICATION: Hidden Iframe Download Approach")
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

    # Query SysSchema for the schema body
    print("\n--- Step 2: Querying SysSchema ---")

    # First, try to get the schema by UId
    esq_body = {
        "rootSchemaName": "SysSchema",
        "operationType": 0,
        "columns": {
            "items": {
                "Id": {"expression": {"columnPath": "Id"}},
                "UId": {"expression": {"columnPath": "UId"}},
                "Name": {"expression": {"columnPath": "Name"}},
                "Body": {"expression": {"columnPath": "Body"}},
                "ModifiedOn": {"expression": {"columnPath": "ModifiedOn"}},
            }
        },
        "filters": {
            "filterType": 6,
            "items": {
                "UIdFilter": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "leftExpression": {"expressionType": 0, "columnPath": "UId"},
                    "rightExpression": {
                        "expressionType": 2,
                        "parameter": {"dataValueType": 0, "value": SCHEMA_UID},
                    },
                }
            },
        },
        "rowCount": 1,
    }

    data = _select_query(session, headers, esq_body)
    rows = data.get("rows", [])

    if not rows:
        # Fallback: try by name
        print(f"No schema found by UId, trying by Name={SCHEMA_NAME}...")
        esq_body["filters"] = {
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
        }
        esq_body["rowCount"] = 10  # Get multiple in case there are duplicates
        data = _select_query(session, headers, esq_body)
        rows = data.get("rows", [])

    if not rows:
        print("\nERROR: Schema not found in SysSchema table")
        print("Result: VERIFICATION_FAILED")
        return

    # If multiple rows, pick the most recent one
    if len(rows) > 1:
        print(f"Found {len(rows)} schema records, selecting most recent...")
        rows = sorted(rows, key=lambda r: r.get("ModifiedOn", ""), reverse=True)

    row = rows[0]
    schema_id = row.get("Id")
    schema_uid = row.get("UId")
    schema_name = row.get("Name")
    modified_on = row.get("ModifiedOn")
    body = row.get("Body") or ""

    print(f"Schema found:")
    print(f"  Id: {schema_id}")
    print(f"  UId: {schema_uid}")
    print(f"  Name: {schema_name}")
    print(f"  ModifiedOn: {modified_on}")
    print(f"  Body length: {len(body)} chars")

    # Check for the iframe marker
    print("\n--- Step 3: Checking for iframe marker ---")

    if not body:
        print("WARNING: Body is empty!")
        print("\nResult: NOT_DEPLOYED (empty body)")
        return

    contains_marker = IFRAME_MARKER in body

    print(f"Searching for '{IFRAME_MARKER}'...")

    if contains_marker:
        # Find the context around the marker
        idx = body.find(IFRAME_MARKER)
        start = max(0, idx - 100)
        end = min(len(body), idx + len(IFRAME_MARKER) + 100)
        context = body[start:end]

        print(f"FOUND at position {idx}")
        print(f"\nContext snippet:")
        print("-" * 40)
        print(f"...{context}...")
        print("-" * 40)

        # Also check for other key markers
        print("\n--- Additional markers check ---")
        markers = [
            ("window.open", "Alternative download method"),
            ("createObjectURL", "Blob URL download method"),
            ("UsrExcelReportService/Generate", "Custom generate service"),
            ("IntExcelReportService/GetReport", "Report download endpoint"),
            ("usr.GenerateExcelReportRequest", "Handler request name"),
        ]
        for marker, desc in markers:
            if marker in body:
                print(f"  [FOUND] {marker} - {desc}")
            else:
                print(f"  [not found] {marker} - {desc}")
    else:
        print("NOT FOUND")

        # Check what download approach is present
        print("\n--- Checking current download approach ---")
        if "window.open" in body:
            print("  [FOUND] window.open - Direct browser download")
        if "createObjectURL" in body:
            print("  [FOUND] createObjectURL - Blob URL download")
        if "UsrExcelReportService" in body:
            print("  [FOUND] UsrExcelReportService - Custom service reference")
        if "IntExcelReportService" in body:
            print("  [FOUND] IntExcelReportService - Report service reference")

    # Final verdict
    print("\n" + "=" * 60)
    if contains_marker:
        print("RESULT: DEPLOYED")
        print("The hidden iframe download approach (reportDownloadFrame) is present.")
    else:
        print("RESULT: NOT_DEPLOYED")
        print("The hidden iframe download approach (reportDownloadFrame) is NOT present.")
    print("=" * 60)

    # Save the body for inspection
    output_file = REPO_ROOT / "test-artifacts" / f"schema_body_{SCHEMA_NAME}.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(body, encoding="utf-8")
    print(f"\nSchema body saved to: {output_file}")


if __name__ == "__main__":
    main()
