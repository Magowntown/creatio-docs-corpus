#!/usr/bin/env python3
"""
Investigation script using OData API to check BGSalesByItemView dependencies.
"""

import os
import sys
import json
import requests
from datetime import datetime

# Load environment
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


def odata_query(entity, select=None, filter=None, top=100, expand=None):
    """Run an OData query."""
    url = f"{CREATIO_URL}/0/odata/{entity}"

    params = {"$top": top}
    if select:
        params["$select"] = select
    if filter:
        params["$filter"] = filter
    if expand:
        params["$expand"] = expand

    response = session.get(url, params=params, timeout=120)

    if response.status_code != 200:
        print(f"  OData query to {entity} failed: {response.status_code}")
        print(f"  Response: {response.text[:300]}")
        return None

    return response.json()


def check_sysschema():
    """Check SysSchema for BGSalesByItemView."""
    print("\n" + "="*60)
    print("1. Checking SysSchema for BGSalesByItemView")
    print("="*60)

    result = odata_query(
        "SysSchema",
        select="Id,Name,Caption,UId,ManagerName,ExtendParent",
        filter="contains(Name,'BGSalesByItemView')",
        expand="SysPackage($select=Name)"
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} matching schema(s):")
        for row in result["value"]:
            print(f"  - Name: {row.get('Name')}")
            print(f"    UId: {row.get('UId')}")
            print(f"    Package: {row.get('SysPackage', {}).get('Name', 'N/A')}")
            print(f"    Manager: {row.get('ManagerName')}")
        return result["value"]
    else:
        print("No schemas found matching 'BGSalesByItemView' in SysSchema")

    return []


def check_all_bg_schemas():
    """Check all BG-prefixed schemas."""
    print("\n" + "="*60)
    print("2. Checking all BG-prefixed schemas (entities/views)")
    print("="*60)

    result = odata_query(
        "SysSchema",
        select="Id,Name,Caption,ManagerName",
        filter="startswith(Name,'BGSales')",
        top=50,
        expand="SysPackage($select=Name)"
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} BGSales-prefixed schema(s):")
        for row in result["value"]:
            pkg = row.get('SysPackage', {}).get('Name', 'N/A')
            print(f"  - {row.get('Name')} (Package: {pkg}, Manager: {row.get('ManagerName')})")
        return result["value"]
    else:
        print("No BGSales-prefixed schemas found")

    return []


def check_int_excel_reports():
    """Check IntExcelReport configurations."""
    print("\n" + "="*60)
    print("3. Checking IntExcelReport configurations")
    print("="*60)

    # First check all reports with BGSales views
    result = odata_query(
        "IntExcelReport",
        select="Id,Name,IntCode,IntViewName,IntFileName",
        filter="contains(IntViewName,'BGSales')",
        top=50
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} report(s) using BGSales views:")
        for row in result["value"]:
            print(f"  - {row.get('Name')} (Code: {row.get('IntCode')})")
            print(f"    View: {row.get('IntViewName')}")
            print(f"    File: {row.get('IntFileName')}")
        return result["value"]
    else:
        print("No IntExcelReport configs found with BGSales views")

    return []


def check_packages():
    """Check BG-prefixed packages."""
    print("\n" + "="*60)
    print("4. Checking BG-prefixed packages")
    print("="*60)

    result = odata_query(
        "SysPackage",
        select="Id,Name,Maintainer,Version",
        filter="startswith(Name,'BG')",
        top=50
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} BG-prefixed package(s):")
        for row in result["value"]:
            print(f"  - {row.get('Name')} (v{row.get('Version')}) by {row.get('Maintainer')}")
        return result["value"]

    return []


def check_view_sample():
    """Sample data from BGSalesByItemView."""
    print("\n" + "="*60)
    print("5. Sampling BGSalesByItemView structure (top 3 rows)")
    print("="*60)

    result = odata_query(
        "BGSalesByItemView",
        top=3
    )

    if result and result.get("value"):
        print(f"Successfully queried BGSalesByItemView. Sample row:")
        if result["value"]:
            # Get column names from first row
            columns = list(result["value"][0].keys())
            print(f"\nColumns found ({len(columns)}):")
            for col in sorted(columns):
                print(f"  - {col}")
            print(f"\nSample data:")
            print(json.dumps(result["value"][0], indent=2, default=str)[:1000])
        return result["value"]
    else:
        print("Could not query BGSalesByItemView")

    return []


def check_process_elements():
    """Check for process elements that reference the view."""
    print("\n" + "="*60)
    print("6. Checking SysProcessElement for BGSalesByItemView references")
    print("="*60)

    # This might not work but worth trying
    result = odata_query(
        "VwSysProcessMILog",
        select="Id,Name,Caption",
        filter="contains(Caption,'SalesByItem') or contains(Name,'SalesByItem')",
        top=20
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} process references:")
        for row in result["value"]:
            print(f"  - {row.get('Name')} ({row.get('Caption')})")
        return result["value"]
    else:
        print("No direct process references found")

    return []


def check_bgreportexecution():
    """Check BGReportExecution for reports using this view."""
    print("\n" + "="*60)
    print("7. Checking BGReportExecution history")
    print("="*60)

    result = odata_query(
        "BGReportExecution",
        select="Id,BGReportName,BGReportCode,CreatedOn",
        filter="contains(BGReportCode,'Item') or contains(BGReportName,'Item')",
        top=10
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} report execution(s) related to 'Item':")
        for row in result["value"]:
            print(f"  - {row.get('BGReportName')} (Code: {row.get('BGReportCode')})")
            print(f"    Created: {row.get('CreatedOn')}")
        return result["value"]
    else:
        print("No BGReportExecution records found for 'Item' reports")

    return []


def check_schema_dependencies():
    """Check for schema dependencies using VwSysSchemaDependency if available."""
    print("\n" + "="*60)
    print("8. Checking schema dependencies")
    print("="*60)

    # Try querying for references to our view
    result = odata_query(
        "SysSchemaProperty",
        filter="contains(Value,'BGSalesByItemView')",
        top=20
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} schema property references:")
        for row in result["value"]:
            print(f"  - {row}")
        return result["value"]
    else:
        print("No schema property references found (or SysSchemaProperty not accessible)")

    return []


def check_sql_scripts():
    """Check SysSqlScript for references."""
    print("\n" + "="*60)
    print("9. Checking SQL scripts for references")
    print("="*60)

    result = odata_query(
        "SysSqlScript",
        select="Id,Name",
        filter="contains(Name,'BGSales')",
        top=20
    )

    if result and result.get("value"):
        print(f"Found {len(result['value'])} SQL script(s) with BGSales reference:")
        for row in result["value"]:
            print(f"  - {row.get('Name')}")
        return result["value"]
    else:
        print("No SQL scripts found referencing BGSales")

    return []


def check_entity_columns():
    """Try to get entity column information."""
    print("\n" + "="*60)
    print("10. Checking entity metadata for BGSalesByItemView")
    print("="*60)

    # Try the metadata endpoint
    url = f"{CREATIO_URL}/0/odata/$metadata"
    response = session.get(url, timeout=60)

    if response.status_code == 200:
        # Search for BGSalesByItemView in metadata
        if "BGSalesByItemView" in response.text:
            print("BGSalesByItemView found in OData metadata")
            # Extract the entity definition
            start = response.text.find('Name="BGSalesByItemView"')
            if start > 0:
                # Find the EntityType block
                block_start = response.text.rfind('<EntityType', 0, start)
                block_end = response.text.find('</EntityType>', start)
                if block_start > 0 and block_end > 0:
                    entity_block = response.text[block_start:block_end+13]
                    print("\nEntity definition (truncated):")
                    print(entity_block[:2000])
                    return entity_block
        else:
            print("BGSalesByItemView NOT found in OData metadata")
    else:
        print(f"Could not retrieve metadata: {response.status_code}")

    return None


def main():
    print("="*60)
    print("BGSalesByItemView Environment Impact Investigation (OData)")
    print(f"Target: {CREATIO_URL}")
    print(f"Date: {datetime.now().isoformat()}")
    print("="*60)

    if not CREATIO_PASSWORD:
        print("ERROR: CREATIO_PROD_PASSWORD not set in environment")
        sys.exit(1)

    authenticate()

    results = {
        "sysschema": check_sysschema(),
        "bg_schemas": check_all_bg_schemas(),
        "int_excel_reports": check_int_excel_reports(),
        "packages": check_packages(),
        "view_sample": check_view_sample(),
        "bgreportexecution": check_bgreportexecution(),
        "sql_scripts": check_sql_scripts(),
    }

    # Check metadata
    check_entity_columns()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    print("\nKey findings:")
    print(f"  - SysSchema entries for BGSalesByItemView: {len(results['sysschema'])}")
    print(f"  - All BGSales-prefixed schemas: {len(results['bg_schemas'])}")
    print(f"  - IntExcelReport configurations using BGSales: {len(results['int_excel_reports'])}")
    print(f"  - BG packages: {len(results['packages'])}")
    print(f"  - View sample rows retrieved: {len(results['view_sample'])}")
    print(f"  - BGReportExecution records: {len(results['bgreportexecution'])}")

    return results


if __name__ == "__main__":
    main()
