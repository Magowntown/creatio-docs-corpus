#!/usr/bin/env python3
"""Try to update UsrExcelReportService code via DataService."""

import os
import requests
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import SOURCE_CODE_DIR
from scripts._env import load_dotenv

load_dotenv()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# Read the new code from file
with open(SOURCE_CODE_DIR / "UsrExcelReportService_Updated.cs", "r", encoding="utf-8") as f:
    NEW_CODE = f.read()

def main():
    session = requests.Session()

    # Login
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD},
                           timeout=30)
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    # Find the UsrExcelReportService schema
    print("\n=== Finding UsrExcelReportService schema ===")
    search_url = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
    search_data = {
        "rootSchemaName": "SysSchema",
        "operationType": 0,
        "columns": {
            "items": {
                "Id": {"expression": {"columnPath": "Id"}},
                "UId": {"expression": {"columnPath": "UId"}},
                "Name": {"expression": {"columnPath": "Name"}},
                "SysPackage": {"expression": {"columnPath": "SysPackage.Name"}}
            }
        },
        "filters": {
            "filterType": 6,
            "items": {
                "NameFilter": {
                    "filterType": 1,
                    "comparisonType": 3,  # Equals
                    "leftExpression": {"expressionType": 0, "columnPath": "Name"},
                    "rightExpression": {"expressionType": 2, "parameter": {"dataValueType": 1, "value": "UsrExcelReportService"}}
                }
            }
        }
    }
    
    response = session.post(search_url, json=search_data, headers=headers, timeout=30)
    if response.status_code == 200:
        result = response.json()
        rows = result.get("rows", [])
        if rows:
            schema = rows[0]
            print(f"Found: {schema.get('Name')} in {schema.get('SysPackage')}")
            print(f"  Id: {schema.get('Id')}")
            print(f"  UId: {schema.get('UId')}")
            
            schema_id = schema.get('Id')
            schema_uid = schema.get('UId')
            
            # Try to get the SysSchemaContent
            print("\n=== Getting schema content ===")
            content_data = {
                "rootSchemaName": "SysSchemaContent",
                "operationType": 0,
                "columns": {
                    "items": {
                        "Id": {"expression": {"columnPath": "Id"}},
                        "SysSchema": {"expression": {"columnPath": "SysSchema.Name"}},
                        "ContentType": {"expression": {"columnPath": "ContentType"}}
                    }
                },
                "filters": {
                    "filterType": 6,
                    "items": {
                        "SchemaFilter": {
                            "filterType": 1,
                            "comparisonType": 3,
                            "leftExpression": {"expressionType": 0, "columnPath": "SysSchema.Id"},
                            "rightExpression": {"expressionType": 2, "parameter": {"dataValueType": 0, "value": schema_id}}
                        }
                    }
                }
            }
            
            response = session.post(search_url, json=content_data, headers=headers, timeout=30)
            if response.status_code == 200:
                content_result = response.json()
                content_rows = content_result.get("rows", [])
                print(f"Found {len(content_rows)} content records")
                for row in content_rows:
                    print(f"  Content: {row}")
            
            # Try to use ConfigurationService to update the schema
            print("\n=== Trying ConfigurationService ===")
            config_url = f"{CREATIO_URL}/0/ServiceModel/ConfigurationService.svc/UpdateSchemaSource"
            config_data = {
                "schemaUId": schema_uid,
                "source": NEW_CODE
            }
            
            response = session.post(config_url, json=config_data, headers=headers, timeout=60)
            print(f"ConfigurationService Status: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
        else:
            print("Schema not found")
    else:
        print(f"Error: {response.status_code} - {response.text[:300]}")

if __name__ == "__main__":
    main()
