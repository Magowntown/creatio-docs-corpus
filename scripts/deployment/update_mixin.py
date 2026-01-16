#!/usr/bin/env python3
"""
Update BGIntExcelreportMixin to use UsrExcelReportService instead of IntExcelReportService
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

SCHEMA_UID = "a589d29b-9da7-4f66-836b-8e39fe0ca376"  # BGIntExcelreportMixin

def main():
    session = requests.Session()

    # Login
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD})
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Get the schema content using ClientUnitSchemaDesignerService
    print("\n=== Getting BGIntExcelreportMixin schema ===")

    # Try to get schema data
    url = f"{CREATIO_URL}/0/ServiceModel/ClientUnitSchemaDesignerService.svc/GetSchema"
    response = session.post(url, json={"schemaUId": SCHEMA_UID}, headers=headers, timeout=30)
    print(f"GetSchema status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        schema = data.get("schema", {})

        body = schema.get("body", "")
        if body:
            print(f"\nFound body ({len(body)} chars)")

            # Count occurrences
            count = body.count('serviceName: "IntExcelReportService"')
            print(f"Found {count} occurrences of serviceName: \"IntExcelReportService\"")

            if count > 0:
                # Replace
                new_body = body.replace(
                    'serviceName: "IntExcelReportService"',
                    'serviceName: "UsrExcelReportService"'
                )

                print(f"\nUpdated body - replaced {count} occurrences")

                # Try saving with minimal required fields
                print("\n=== Saving schema with SaveSchema API ===")
                save_url = f"{CREATIO_URL}/0/ServiceModel/ClientUnitSchemaDesignerService.svc/SaveSchema"

                # Build save request with all schema fields
                save_schema = {
                    "uId": schema.get("uId"),
                    "name": schema.get("name"),
                    "body": new_body,
                    "less": schema.get("less", ""),
                    "dependencies": schema.get("dependencies", []),
                    "localizableStrings": schema.get("localizableStrings", []),
                    "messages": schema.get("messages", []),
                    "images": schema.get("images", []),
                    "parameters": schema.get("parameters", []),
                    "parent": schema.get("parent"),
                    "extendParent": schema.get("extendParent", False),
                    "schemaType": schema.get("schemaType"),
                    "package": schema.get("package"),
                    "caption": schema.get("caption"),
                    "description": schema.get("description", ""),
                    "group": schema.get("group", ""),
                }

                save_request = {"schema": save_schema}

                response = session.post(save_url, json=save_request, headers=headers, timeout=60)
                print(f"SaveSchema status: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        print("✅ Schema saved!")
                        trigger_build(session, headers)
                    else:
                        print(f"❌ Save failed: {result.get('errorInfo', {}).get('message', 'Unknown error')}")

                        # Try alternative: Update via SysSchemaContent table
                        print("\n=== Trying alternative: Update SysSchemaContent ===")
                        update_via_content_table(session, headers, SCHEMA_UID, new_body)
                else:
                    print(f"Error: {response.text[:500]}")
            else:
                print("No occurrences found to replace")
        else:
            print("No body found in schema")
    else:
        print(f"Error: {response.text[:500]}")


def update_via_content_table(session, headers, schema_uid, new_body):
    """Update schema content via SysSchemaContent table"""
    import base64

    # First, find the content record ID
    query_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    select_query = {
        "RootSchemaName": "SysSchemaContent",
        "OperationType": 0,
        "Columns": {"Items": {"Id": {"Expression": {"ExpressionType": 0, "ColumnPath": "Id"}}}},
        "Filters": {
            "FilterType": 6,
            "Items": {
                "SchemaFilter": {
                    "FilterType": 1,
                    "ComparisonType": 3,
                    "LeftExpression": {"ExpressionType": 0, "ColumnPath": "SysSchema.UId"},
                    "RightExpression": {"ExpressionType": 2, "Parameter": {"DataValueType": 0, "Value": schema_uid}}
                }
            }
        }
    }

    response = session.post(query_url, json=select_query, headers=headers, timeout=30)
    print(f"Query SysSchemaContent: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        if rows:
            content_id = rows[0].get("Id")
            print(f"Found content record: {content_id}")

            # Encode body as base64 for binary column
            body_bytes = new_body.encode('utf-8')
            body_base64 = base64.b64encode(body_bytes).decode('ascii')

            # Update the content
            update_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/UpdateQuery"
            update_query = {
                "RootSchemaName": "SysSchemaContent",
                "OperationType": 1,
                "ColumnValues": {
                    "Items": {
                        "Content": {
                            "ExpressionType": 2,
                            "Parameter": {
                                "DataValueType": 13,
                                "Value": body_base64
                            }
                        }
                    }
                },
                "Filters": {
                    "FilterType": 6,
                    "Items": {
                        "IdFilter": {
                            "FilterType": 1,
                            "ComparisonType": 3,
                            "LeftExpression": {"ExpressionType": 0, "ColumnPath": "Id"},
                            "RightExpression": {"ExpressionType": 2, "Parameter": {"DataValueType": 0, "Value": content_id}}
                        }
                    }
                }
            }

            response = session.post(update_url, json=update_query, headers=headers, timeout=60)
            print(f"Update status: {response.status_code}")
            update_result = response.json()
            print(f"Update result: {json.dumps(update_result, indent=2)}")

            if update_result.get("success"):
                print("✅ Content updated via SysSchemaContent!")
                trigger_build(session, headers)
        else:
            print("No content record found")


def trigger_build(session, headers):
    """Trigger compilation"""
    import time
    print("\n=== Triggering compilation ===")
    build_url = f"{CREATIO_URL}/0/ServiceModel/WorkspaceExplorerService.svc/Build"

    for attempt in range(5):
        response = session.post(build_url, json={}, headers=headers, timeout=120)
        build_result = response.json()

        if build_result.get("success"):
            print("✅ Compilation successful!")

            # Test the service
            print("\n=== Testing UsrExcelReportService ===")
            test_url = f"{CREATIO_URL}/0/rest/UsrExcelReportService/Generate"
            test_data = {
                "EsqString": json.dumps({"rootSchemaName": "BGCommissionReportDataView", "allColumns": True}),
                "ReportId": "4ba4f203-7088-41dc-b86d-130c590b3594",
                "RecordCollection": []
            }
            response = session.post(test_url, json=test_data, headers=headers, timeout=60)
            print(f"Test status: {response.status_code}")
            if response.status_code == 200:
                print(f"Result: {json.dumps(response.json(), indent=2)}")
            break
        else:
            error = build_result.get("errorInfo", {}).get("message", "")
            if "another compilation" in error.lower():
                print(f"⏳ Waiting... ({attempt+1})")
                time.sleep(15)
            else:
                print(f"❌ Compilation: {error}")
                break

if __name__ == "__main__":
    main()
