#!/usr/bin/env python3
"""
Compare UsrPage_ebkv9e8 between PROD and local version.
Fetch the PROD schema and identify differences.
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from difflib import unified_diff

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
load_dotenv(REPO_ROOT / ".env")

PROD_URL = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.environ.get("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.environ.get("CREATIO_PROD_PASSWORD", "")

LOCAL_FILE = REPO_ROOT / "client-module" / "UsrPage_ebkv9e8_Updated.js"
TARGET_SCHEMA = "UsrPage_ebkv9e8"


def get_session(base_url: str, username: str, password: str) -> requests.Session:
    """Authenticate and return session."""
    session = requests.Session()
    session.verify = True

    # Login
    login_url = f"{base_url}/ServiceModel/AuthService.svc/Login"
    login_data = {"UserName": username, "UserPassword": password}

    resp = session.post(login_url, json=login_data, timeout=30)
    resp.raise_for_status()

    result = resp.json()
    if result.get("Code") != 0:
        raise Exception(f"Login failed: {result}")

    # Get CSRF token
    cookies = session.cookies.get_dict()
    if "BPMCSRF" in cookies:
        session.headers["BPMCSRF"] = cookies["BPMCSRF"]

    print(f"✅ Authenticated to {base_url}")
    return session


def find_schema_uid(session: requests.Session, base_url: str, schema_name: str) -> str:
    """Find the schema UID by name."""
    url = f"{base_url}/0/odata/SysSchema"
    params = {
        "$filter": f"Name eq '{schema_name}'",
        "$select": "UId,Name,ManagerName,PackageUId"
    }

    resp = session.get(url, params=params, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    if data.get("value"):
        schema = data["value"][0]
        print(f"   Found: {schema['Name']} (UID: {schema['UId']})")
        return schema["UId"]

    raise Exception(f"Schema '{schema_name}' not found")


def get_schema_source(session: requests.Session, base_url: str, schema_uid: str) -> str:
    """Get the source code of a client schema."""
    # Method 1: Try SysClientUnitSchema
    url = f"{base_url}/0/odata/SysClientUnitSchema"
    params = {
        "$filter": f"UId eq {schema_uid}",
        "$select": "UId,Name,Body"
    }

    resp = session.get(url, params=params, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("value") and data["value"][0].get("Body"):
            return data["value"][0]["Body"]

    # Method 2: Try DataService
    url = f"{base_url}/0/DataService/json/SyncReply/SelectQuery"
    query = {
        "RootSchemaName": "VwSysClientUnitSchema",
        "OperationType": 0,
        "Columns": {
            "Items": {
                "UId": {"Expression": {"ColumnPath": "UId"}},
                "Name": {"Expression": {"ColumnPath": "Name"}},
                "Body": {"Expression": {"ColumnPath": "Body"}}
            }
        },
        "Filters": {
            "FilterType": 6,
            "LogicalOperation": 0,
            "Items": {
                "UIdFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {
                        "ExpressionType": 0,
                        "ColumnPath": "UId"
                    },
                    "RightExpression": {
                        "ExpressionType": 2,
                        "Parameter": {
                            "DataValueType": 0,
                            "Value": schema_uid
                        }
                    }
                }
            }
        }
    }

    resp = session.post(url, json=query, timeout=60)
    if resp.status_code == 200:
        data = resp.json()
        rows = data.get("rows", [])
        if rows and rows[0].get("Body"):
            return rows[0]["Body"]

    # Method 3: Try client schema body directly
    url = f"{base_url}/0/odata/VwSysClientUnitSchema({schema_uid})?$select=Body"
    resp = session.get(url, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("Body"):
            return data["Body"]

    return None


def main():
    print("=" * 60)
    print(f"COMPARING UsrPage_ebkv9e8: PROD vs LOCAL")
    print("=" * 60)

    # Read local file
    print(f"\n1️⃣ Reading local file: {LOCAL_FILE}")
    if not LOCAL_FILE.exists():
        print(f"   ❌ Local file not found!")
        return

    local_content = LOCAL_FILE.read_text(encoding="utf-8")
    print(f"   ✅ Local: {len(local_content)} chars")

    # Connect to PROD
    print(f"\n2️⃣ Connecting to PROD: {PROD_URL}")
    try:
        session = get_session(PROD_URL, PROD_USER, PROD_PASS)
    except Exception as e:
        print(f"   ❌ Failed to connect: {e}")
        return

    # Find schema
    print(f"\n3️⃣ Finding schema: {TARGET_SCHEMA}")
    try:
        schema_uid = find_schema_uid(session, PROD_URL, TARGET_SCHEMA)
    except Exception as e:
        print(f"   ❌ Schema not found: {e}")
        return

    # Get PROD source
    print(f"\n4️⃣ Fetching PROD source...")
    prod_content = get_schema_source(session, PROD_URL, schema_uid)

    if not prod_content:
        print("   ❌ Could not fetch PROD source")
        print("   Trying alternative method...")

        # Try listing all schemas to see what we can access
        url = f"{PROD_URL}/0/odata/SysClientUnitSchema?$filter=startswith(Name,'UsrPage')&$select=UId,Name&$top=10"
        resp = session.get(url, timeout=30)
        if resp.status_code == 200:
            print(f"   Available UsrPage schemas: {resp.json()}")
        return

    print(f"   ✅ PROD: {len(prod_content)} chars")

    # Save PROD version
    prod_file = REPO_ROOT / "client-module" / "UsrPage_ebkv9e8_PROD.js"
    prod_file.write_text(prod_content, encoding="utf-8")
    print(f"   📄 Saved PROD version to: {prod_file}")

    # Compare
    print(f"\n5️⃣ Comparing versions...")

    # Normalize for comparison
    local_lines = local_content.strip().split("\n")
    prod_lines = prod_content.strip().split("\n")

    if local_content.strip() == prod_content.strip():
        print("   ✅ IDENTICAL - No differences found")
    else:
        print("   ⚠️  DIFFERENCES FOUND:")
        print(f"      Local: {len(local_lines)} lines, {len(local_content)} chars")
        print(f"      PROD:  {len(prod_lines)} lines, {len(prod_content)} chars")

        # Generate diff
        diff = list(unified_diff(
            local_lines, prod_lines,
            fromfile="LOCAL",
            tofile="PROD",
            lineterm=""
        ))

        if diff:
            print("\n   DIFF (first 100 lines):")
            print("   " + "-" * 50)
            for line in diff[:100]:
                print(f"   {line}")
            if len(diff) > 100:
                print(f"   ... ({len(diff) - 100} more lines)")

            # Save full diff
            diff_file = REPO_ROOT / "client-module" / "UsrPage_ebkv9e8_DIFF.txt"
            diff_file.write_text("\n".join(diff), encoding="utf-8")
            print(f"\n   📄 Full diff saved to: {diff_file}")

    # Analyze PROD code for QB-related patterns
    print(f"\n6️⃣ Analyzing PROD code for QB sync patterns...")

    patterns = [
        ("QuickBooks", "QB reference"),
        ("Sync", "Sync reference"),
        ("BGQuickBooks", "BGQuickBooks reference"),
        ("Order", "Order entity reference"),
        ("IWPayments", "IWPayments query"),
        ("PaymentStatus", "PaymentStatus reference"),
        ("HandleViewModelAttributeChangeRequest", "Attribute change handler"),
        ("LoadDataRequest", "Data load interceptor"),
        ("crt.SaveRecordRequest", "Save record handler"),
        ("crt.CreateRecordRequest", "Create record handler"),
    ]

    print(f"   Pattern scan:")
    for pattern, desc in patterns:
        count = prod_content.count(pattern)
        if count > 0:
            print(f"      ⚠️  {desc}: {count} occurrence(s)")
        else:
            print(f"      ✅ {desc}: Not found")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
