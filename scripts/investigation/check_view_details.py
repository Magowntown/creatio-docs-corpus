#!/usr/bin/env python3
"""
Deep investigation of BGSalesByItemView - SQL definition and all dependencies.
"""

import os
import sys
import json
import requests
from datetime import datetime

CREATIO_URL = os.getenv('CREATIO_PROD_URL', 'https://pampabay.creatio.com')
CREATIO_USERNAME = os.getenv('CREATIO_PROD_USERNAME', 'Supervisor')
CREATIO_PASSWORD = os.getenv('CREATIO_PROD_PASSWORD')

session = requests.Session()
session.verify = True


def authenticate():
    """Authenticate with Creatio."""
    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    payload = {
        "UserName": CREATIO_USERNAME,
        "UserPassword": CREATIO_PASSWORD
    }

    response = session.post(login_url, json=payload)
    if response.status_code != 200:
        print(f"Authentication failed: {response.status_code}")
        sys.exit(1)

    result = response.json()
    if result.get("Code") != 0:
        print(f"Authentication failed: {result}")
        sys.exit(1)

    csrf_token = session.cookies.get("BPMCSRF")
    if csrf_token:
        session.headers.update({"BPMCSRF": csrf_token})

    print(f"[OK] Authenticated to {CREATIO_URL}")
    return True


def odata_query(entity, select=None, filter_str=None, top=100, expand=None):
    """Run an OData query."""
    url = f"{CREATIO_URL}/0/odata/{entity}"

    params = {"$top": top}
    if select:
        params["$select"] = select
    if filter_str:
        params["$filter"] = filter_str
    if expand:
        params["$expand"] = expand

    response = session.get(url, params=params, timeout=120)

    if response.status_code != 200:
        print(f"  OData query to {entity} failed: {response.status_code}")
        return None

    return response.json()


def check_int_excel_report_all():
    """Get all IntExcelReport configurations."""
    print("\n" + "="*60)
    print("1. All IntExcelReport Configurations")
    print("="*60)

    result = odata_query(
        "IntExcelReport",
        top=100
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} report(s):")
        # Get column names from first record
        if result["value"]:
            cols = list(result["value"][0].keys())
            print(f"\nAvailable columns: {cols}")

        for row in result["value"]:
            name = row.get('Name', row.get('IntName', 'Unknown'))
            print(f"\n  Report: {name}")
            # Print all non-null values
            for k, v in row.items():
                if v and k not in ['Id', 'CreatedOn', 'ModifiedOn', 'CreatedById', 'ModifiedById', 'ProcessListeners']:
                    print(f"    {k}: {v}")
        return result["value"]
    else:
        print("Could not retrieve IntExcelReport configurations")

    return []


def check_schema_source():
    """Try to get the schema source/SQL definition."""
    print("\n" + "="*60)
    print("2. Schema Source/Definition for BGSalesByItemView")
    print("="*60)

    # Try SysSchemaSource
    result = odata_query(
        "SysSchema",
        select="Id,Name,Caption,UId,ManagerName",
        filter_str="Name eq 'BGSalesByItemView'"
    )

    if result and result.get("value"):
        schema = result["value"][0]
        schema_id = schema.get("Id")
        uid = schema.get("UId")
        print(f"Schema ID: {schema_id}")
        print(f"Schema UId: {uid}")

        # Try to get the source code
        source_url = f"{CREATIO_URL}/0/odata/SysSchemaSource"
        source_result = odata_query(
            "SysSchemaSource",
            filter_str=f"SysSchemaId eq {schema_id}",
            top=10
        )

        if source_result and source_result.get("value"):
            print("\nSchema source found:")
            for src in source_result["value"]:
                print(json.dumps(src, indent=2, default=str)[:2000])
        else:
            print("No schema source found in SysSchemaSource")

        # Try VwSysSchemaData
        vw_result = odata_query(
            "VwSysSchemaData",
            filter_str=f"UId eq {uid}",
            top=5
        )

        if vw_result and vw_result.get("value"):
            print("\nVwSysSchemaData entry found:")
            for entry in vw_result["value"]:
                print(json.dumps(entry, indent=2, default=str)[:2000])
        else:
            print("No VwSysSchemaData entry found")

    return None


def check_references_in_all_schemas():
    """Search for references to BGSalesByItemView in other schemas."""
    print("\n" + "="*60)
    print("3. Checking References in All Schemas")
    print("="*60)

    # Check if any other schemas reference BGSalesByItemView
    # This is tricky since we can't search schema content via OData

    # Check VwSysSchemaExtending for schema inheritance
    result = odata_query(
        "VwSysSchemaExtending",
        filter_str="contains(ParentSchemaName,'BGSalesByItemView') or contains(SchemaName,'BGSalesByItemView')",
        top=20
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} schema extension(s):")
        for row in result["value"]:
            print(f"  - {row}")
        return result["value"]
    else:
        print("No schema extensions found (or table not accessible)")

    return []


def check_process_schema_parameters():
    """Check if any process parameters reference the view."""
    print("\n" + "="*60)
    print("4. Checking VwSysProcess for References")
    print("="*60)

    # Get list of processes that might reference our view
    result = odata_query(
        "VwSysProcess",
        select="Id,Name,Caption",
        filter_str="contains(Name,'Sales') or contains(Name,'Report') or contains(Name,'Item')",
        top=30
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} potentially related process(es):")
        for row in result["value"]:
            print(f"  - {row.get('Name')} ({row.get('Caption')})")
        return result["value"]
    else:
        print("No related processes found")

    return []


def check_lookups():
    """Check if BGSalesByItemView is used as a lookup anywhere."""
    print("\n" + "="*60)
    print("5. Checking SysLookup for References")
    print("="*60)

    result = odata_query(
        "SysLookup",
        filter_str="contains(Name,'BGSales') or contains(Name,'SalesByItem')",
        top=20
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} lookup(s):")
        for row in result["value"]:
            print(f"  - {row}")
        return result["value"]
    else:
        print("No lookups found referencing BGSales views")

    return []


def check_installed_apps():
    """Check installed applications."""
    print("\n" + "="*60)
    print("6. Checking Installed Applications")
    print("="*60)

    result = odata_query(
        "SysInstalledApp",
        select="Id,Name,Code,Maintainer",
        top=50
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} installed app(s):")
        for row in result["value"]:
            print(f"  - {row.get('Name')} (Code: {row.get('Code')}, Maintainer: {row.get('Maintainer')})")
        return result["value"]
    else:
        print("Could not retrieve installed apps")

    return []


def count_view_records():
    """Count records in BGSalesByItemView."""
    print("\n" + "="*60)
    print("7. Counting BGSalesByItemView Records")
    print("="*60)

    # Use $count
    url = f"{CREATIO_URL}/0/odata/BGSalesByItemView/$count"
    response = session.get(url, timeout=120)

    if response.status_code == 200:
        count = response.text
        print(f"Total records in BGSalesByItemView: {count}")
        return int(count) if count.isdigit() else count
    else:
        print(f"Could not count records: {response.status_code}")
        return None


def check_entity_schema_column():
    """Check VwSysEntitySchemaColumn for view columns."""
    print("\n" + "="*60)
    print("8. Checking VwSysEntitySchemaColumn")
    print("="*60)

    result = odata_query(
        "VwSysEntitySchemaColumn",
        filter_str="contains(SysEntitySchemaName,'BGSalesByItemView')",
        top=50
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} column(s):")
        for row in result["value"]:
            print(f"  - {row.get('Name', row)}")
        return result["value"]
    else:
        print("No columns found (or VwSysEntitySchemaColumn not accessible)")

    return []


def check_package_hierarchy():
    """Check package hierarchy for PampaBay."""
    print("\n" + "="*60)
    print("9. Checking PampaBay Package Hierarchy")
    print("="*60)

    result = odata_query(
        "SysPackageHierarchy",
        select="Id,BaseSysPackageId,DependOnSysPackageId",
        filter_str="",
        top=100,
        expand="BaseSysPackage($select=Name),DependOnSysPackage($select=Name)"
    )

    if result and result.get("value"):
        pampabay_deps = []
        for row in result["value"]:
            base = row.get("BaseSysPackage", {}).get("Name", "")
            dep = row.get("DependOnSysPackage", {}).get("Name", "")
            if "PampaBay" in base or "PampaBay" in dep:
                pampabay_deps.append(row)
                print(f"  - {base} depends on {dep}")

        print(f"\nFound {len(pampabay_deps)} package relationship(s) involving PampaBay")
        return pampabay_deps
    else:
        print("Could not retrieve package hierarchy")

    return []


def get_schema_metadata():
    """Get detailed schema metadata."""
    print("\n" + "="*60)
    print("10. Getting Schema Metadata Details")
    print("="*60)

    # Try SysSchemaProperty for BGSalesByItemView
    result = odata_query(
        "SysSchema",
        filter_str="Name eq 'BGSalesByItemView'",
        expand="SysPackage($select=Name,Maintainer,Version)"
    )

    if result and result.get("value"):
        schema = result["value"][0]
        print(f"Full schema details:")
        print(json.dumps(schema, indent=2, default=str))
        return schema

    return None


def main():
    print("="*60)
    print("BGSalesByItemView Deep Investigation")
    print(f"Target: {CREATIO_URL}")
    print(f"Date: {datetime.now().isoformat()}")
    print("="*60)

    if not CREATIO_PASSWORD:
        print("ERROR: CREATIO_PROD_PASSWORD not set in environment")
        sys.exit(1)

    authenticate()

    results = {
        "int_excel_reports": check_int_excel_report_all(),
        "processes": check_process_schema_parameters(),
        "lookups": check_lookups(),
        "installed_apps": check_installed_apps(),
        "record_count": count_view_records(),
        "package_hierarchy": check_package_hierarchy(),
        "schema_metadata": get_schema_metadata()
    }

    # Try schema source
    check_schema_source()

    print("\n" + "="*60)
    print("INVESTIGATION COMPLETE")
    print("="*60)

    return results


if __name__ == "__main__":
    main()
