#!/usr/bin/env python3
"""
Investigation script to check BGSalesByItemView dependencies and structure in PROD.
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
    # Get BPMCSRF token
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

    # Get CSRF token from cookies
    csrf_token = session.cookies.get("BPMCSRF")
    if csrf_token:
        session.headers.update({"BPMCSRF": csrf_token})

    print(f"[OK] Authenticated to {CREATIO_URL}")
    return True


def run_select_query(sql):
    """Run a SELECT query via DataService."""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"

    # Use raw SQL via CustomQuery endpoint
    url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/GetReportData"

    # Alternative: use OData or direct SQL endpoint
    # For now, let's try using ESQ on SysSchema
    return None


def query_esq(root_schema, columns, filters=None):
    """Run an ESQ query."""
    url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"

    payload = {
        "rootSchemaName": root_schema,
        "operationType": 0,
        "columns": {
            "items": {}
        }
    }

    for col in columns:
        if isinstance(col, dict):
            payload["columns"]["items"][col["alias"]] = {
                "caption": col.get("caption", col["alias"]),
                "expression": {
                    "expressionType": 0,
                    "columnPath": col["path"]
                }
            }
        else:
            payload["columns"]["items"][col] = {
                "caption": col,
                "expression": {
                    "expressionType": 0,
                    "columnPath": col
                }
            }

    if filters:
        payload["filters"] = filters

    response = session.post(url, json=payload, timeout=120)
    if response.status_code != 200:
        print(f"Query failed: {response.status_code}")
        print(response.text[:500])
        return None

    return response.json()


def build_filter(column_path, value, comparison_type=3):
    """Build a filter for ESQ. comparison_type 3 = Equal."""
    return {
        "filterType": 1,
        "comparisonType": comparison_type,
        "isEnabled": True,
        "trimDateTimeParameterToDate": False,
        "leftExpression": {
            "expressionType": 0,
            "columnPath": column_path
        },
        "rightExpression": {
            "expressionType": 2,
            "parameter": {
                "dataValueType": 1,
                "value": value
            }
        }
    }


def check_sysschema_for_view():
    """Check SysSchema table for BGSalesByItemView definition."""
    print("\n" + "="*60)
    print("1. Checking SysSchema for BGSalesByItemView")
    print("="*60)

    # Query SysSchema for the view
    filters = {
        "items": {
            "NameFilter": {
                "filterType": 1,
                "comparisonType": 11,  # Contains
                "isEnabled": True,
                "leftExpression": {
                    "expressionType": 0,
                    "columnPath": "Name"
                },
                "rightExpression": {
                    "expressionType": 2,
                    "parameter": {
                        "dataValueType": 1,
                        "value": "BGSalesByItemView"
                    }
                }
            }
        }
    }

    result = query_esq("SysSchema", [
        "Id", "Name", "Caption", "UId",
        {"path": "SysPackage.Name", "alias": "PackageName"},
        "ManagerName", "ExtendParent"
    ], filters)

    if result and result.get("rows"):
        print(f"Found {len(result['rows'])} matching schema(s):")
        for row in result["rows"]:
            print(f"  - Name: {row.get('Name')}")
            print(f"    Package: {row.get('PackageName')}")
            print(f"    UId: {row.get('UId')}")
            print(f"    ManagerName: {row.get('ManagerName')}")
            print(f"    ExtendParent: {row.get('ExtendParent')}")
        return result["rows"]
    else:
        print("No schemas found matching 'BGSalesByItemView'")
        return []


def check_sysview():
    """Check if there's a SysView entry."""
    print("\n" + "="*60)
    print("2. Checking SysView table")
    print("="*60)

    # Try to query SysView if it exists
    try:
        filters = {
            "items": {
                "NameFilter": {
                    "filterType": 1,
                    "comparisonType": 11,
                    "isEnabled": True,
                    "leftExpression": {
                        "expressionType": 0,
                        "columnPath": "Name"
                    },
                    "rightExpression": {
                        "expressionType": 2,
                        "parameter": {
                            "dataValueType": 1,
                            "value": "BGSalesByItem"
                        }
                    }
                }
            }
        }

        result = query_esq("VwSysSchemaInWorkspace", [
            "Id", "Name", "Caption", "UId",
            {"path": "SysPackage.Name", "alias": "PackageName"}
        ], filters)

        if result and result.get("rows"):
            print(f"Found {len(result['rows'])} schema(s) in VwSysSchemaInWorkspace:")
            for row in result["rows"]:
                print(f"  - {row.get('Name')} (Package: {row.get('PackageName')})")
            return result["rows"]
        else:
            print("No matching entries in VwSysSchemaInWorkspace")
    except Exception as e:
        print(f"Error querying VwSysSchemaInWorkspace: {e}")

    return []


def check_entity_dependencies():
    """Check for entities/schemas that reference BGSalesByItemView."""
    print("\n" + "="*60)
    print("3. Checking for entity dependencies (via SysEntitySchemaColumn)")
    print("="*60)

    # Check if any columns reference this view
    filters = {
        "items": {
            "ReferenceFilter": {
                "filterType": 1,
                "comparisonType": 11,
                "isEnabled": True,
                "leftExpression": {
                    "expressionType": 0,
                    "columnPath": "ReferenceSchemaName"
                },
                "rightExpression": {
                    "expressionType": 2,
                    "parameter": {
                        "dataValueType": 1,
                        "value": "BGSalesByItemView"
                    }
                }
            }
        }
    }

    try:
        result = query_esq("SysEntitySchemaColumn", [
            "Id", "Name", "Caption",
            {"path": "SysEntitySchema.Name", "alias": "EntityName"},
            "ReferenceSchemaName"
        ], filters)

        if result and result.get("rows"):
            print(f"Found {len(result['rows'])} column(s) referencing BGSalesByItemView:")
            for row in result["rows"]:
                print(f"  - {row.get('EntityName')}.{row.get('Name')}")
            return result["rows"]
        else:
            print("No columns reference BGSalesByItemView as a lookup")
    except Exception as e:
        print(f"Error: {e}")

    return []


def check_process_references():
    """Check if any business processes reference the view."""
    print("\n" + "="*60)
    print("4. Checking business process references")
    print("="*60)

    # Search SysProcessSchemaParameter for references
    filters = {
        "items": {
            "ValueFilter": {
                "filterType": 1,
                "comparisonType": 11,
                "isEnabled": True,
                "leftExpression": {
                    "expressionType": 0,
                    "columnPath": "SerializedValue"
                },
                "rightExpression": {
                    "expressionType": 2,
                    "parameter": {
                        "dataValueType": 1,
                        "value": "BGSalesByItemView"
                    }
                }
            }
        }
    }

    try:
        result = query_esq("SysProcessSchemaParameter", [
            "Id", "Name",
            {"path": "SysProcessSchema.Caption", "alias": "ProcessCaption"}
        ], filters)

        if result and result.get("rows"):
            print(f"Found {len(result['rows'])} process parameter(s) referencing BGSalesByItemView:")
            for row in result["rows"]:
                print(f"  - Process: {row.get('ProcessCaption')}, Param: {row.get('Name')}")
            return result["rows"]
        else:
            print("No business process parameters directly reference BGSalesByItemView")
    except Exception as e:
        print(f"Error: {e}")

    return []


def check_report_configs():
    """Check IntExcelReport configurations that use this view."""
    print("\n" + "="*60)
    print("5. Checking IntExcelReport configurations")
    print("="*60)

    filters = {
        "items": {
            "ViewFilter": {
                "filterType": 1,
                "comparisonType": 11,
                "isEnabled": True,
                "leftExpression": {
                    "expressionType": 0,
                    "columnPath": "IntViewName"
                },
                "rightExpression": {
                    "expressionType": 2,
                    "parameter": {
                        "dataValueType": 1,
                        "value": "BGSalesByItemView"
                    }
                }
            }
        }
    }

    result = query_esq("IntExcelReport", [
        "Id", "Name", "IntCode", "IntViewName", "IntFileName"
    ], filters)

    if result and result.get("rows"):
        print(f"Found {len(result['rows'])} report(s) using BGSalesByItemView:")
        for row in result["rows"]:
            print(f"  - {row.get('Name')} (Code: {row.get('IntCode')})")
            print(f"    View: {row.get('IntViewName')}")
            print(f"    File: {row.get('IntFileName')}")
        return result["rows"]
    else:
        print("No IntExcelReport configs use BGSalesByItemView")

    return []


def check_view_columns():
    """Check the columns in BGSalesByItemView entity."""
    print("\n" + "="*60)
    print("6. Checking BGSalesByItemView entity columns")
    print("="*60)

    # First, try to get column info from SysEntitySchemaColumn
    filters = {
        "items": {
            "SchemaFilter": {
                "filterType": 1,
                "comparisonType": 3,
                "isEnabled": True,
                "leftExpression": {
                    "expressionType": 0,
                    "columnPath": "SysEntitySchema.Name"
                },
                "rightExpression": {
                    "expressionType": 2,
                    "parameter": {
                        "dataValueType": 1,
                        "value": "BGSalesByItemView"
                    }
                }
            }
        }
    }

    try:
        result = query_esq("SysEntitySchemaColumn", [
            "Id", "Name", "Caption", "DataValueType", "IsRequired"
        ], filters)

        if result and result.get("rows"):
            print(f"Found {len(result['rows'])} column(s) in BGSalesByItemView:")
            for row in result["rows"]:
                print(f"  - {row.get('Name')} ({row.get('Caption')}) - Type: {row.get('DataValueType')}")
            return result["rows"]
        else:
            print("No columns found in SysEntitySchemaColumn (may be a database view, not entity)")
    except Exception as e:
        print(f"Error: {e}")

    return []


def sample_view_data():
    """Sample data from the view to understand its structure."""
    print("\n" + "="*60)
    print("7. Sampling BGSalesByItemView data (top 5 rows)")
    print("="*60)

    # Try to query the view directly
    try:
        result = query_esq("BGSalesByItemView", [
            "Id"
        ], None)

        if result:
            print(f"View is queryable. Total rows in result: {len(result.get('rows', []))}")
            if result.get("rows"):
                print("Sample row structure:")
                print(json.dumps(result["rows"][0], indent=2)[:500])
            return result
        else:
            print("Could not query BGSalesByItemView directly")
    except Exception as e:
        print(f"Error querying view: {e}")

    return None


def check_packages_with_bg_prefix():
    """Check all packages that might contain BGSalesByItemView-related objects."""
    print("\n" + "="*60)
    print("8. Checking BG-prefixed packages")
    print("="*60)

    filters = {
        "items": {
            "PrefixFilter": {
                "filterType": 1,
                "comparisonType": 2,  # StartsWith
                "isEnabled": True,
                "leftExpression": {
                    "expressionType": 0,
                    "columnPath": "Name"
                },
                "rightExpression": {
                    "expressionType": 2,
                    "parameter": {
                        "dataValueType": 1,
                        "value": "BG"
                    }
                }
            }
        }
    }

    result = query_esq("SysPackage", [
        "Id", "Name", "Maintainer", "Version"
    ], filters)

    if result and result.get("rows"):
        print(f"Found {len(result['rows'])} BG-prefixed package(s):")
        for row in result["rows"]:
            print(f"  - {row.get('Name')} (v{row.get('Version')}) by {row.get('Maintainer')}")
        return result["rows"]

    return []


def check_all_views():
    """Check all database views in the system."""
    print("\n" + "="*60)
    print("9. Checking for other views that might depend on BGSalesByItemView")
    print("="*60)

    # Search schemas that might reference our view
    filters = {
        "items": {
            "NameFilter": {
                "filterType": 1,
                "comparisonType": 11,
                "isEnabled": True,
                "leftExpression": {
                    "expressionType": 0,
                    "columnPath": "Name"
                },
                "rightExpression": {
                    "expressionType": 2,
                    "parameter": {
                        "dataValueType": 1,
                        "value": "BGSales"
                    }
                }
            }
        }
    }

    result = query_esq("SysSchema", [
        "Id", "Name", "Caption",
        {"path": "SysPackage.Name", "alias": "PackageName"},
        "ManagerName"
    ], filters)

    if result and result.get("rows"):
        print(f"Found {len(result['rows'])} BGSales-related schema(s):")
        for row in result["rows"]:
            print(f"  - {row.get('Name')} (Package: {row.get('PackageName')}, Manager: {row.get('ManagerName')})")
        return result["rows"]

    return []


def main():
    print("="*60)
    print("BGSalesByItemView Environment Impact Investigation")
    print(f"Target: {CREATIO_URL}")
    print(f"Date: {datetime.now().isoformat()}")
    print("="*60)

    if not CREATIO_PASSWORD:
        print("ERROR: CREATIO_PROD_PASSWORD not set in environment")
        sys.exit(1)

    authenticate()

    results = {
        "sysschema": check_sysschema_for_view(),
        "vwsysschema": check_sysview(),
        "entity_deps": check_entity_dependencies(),
        "process_refs": check_process_references(),
        "report_configs": check_report_configs(),
        "columns": check_view_columns(),
        "packages": check_packages_with_bg_prefix(),
        "related_views": check_all_views()
    }

    # Try to sample data
    sample_view_data()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    print("\nKey findings:")
    print(f"  - SysSchema entries: {len(results['sysschema'])}")
    print(f"  - Entity dependencies: {len(results['entity_deps'])}")
    print(f"  - Process references: {len(results['process_refs'])}")
    print(f"  - Report configurations: {len(results['report_configs'])}")
    print(f"  - BG packages: {len(results['packages'])}")
    print(f"  - Related BGSales views: {len(results['related_views'])}")

    return results


if __name__ == "__main__":
    main()
