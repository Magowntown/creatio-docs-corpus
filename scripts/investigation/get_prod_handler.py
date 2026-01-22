#!/usr/bin/env python3
"""
Get the currently deployed handler code from PROD child schema
"""

import os
import requests

# Load environment
env_path = "/home/magown/creatio-report-fix/.env"
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value

# PROD credentials
prod_url = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com")
prod_user = os.environ.get("CREATIO_PROD_USERNAME", "Supervisor")
prod_pass = os.environ.get("CREATIO_PROD_PASSWORD", "")

session = requests.Session()

# Login
login_url = f"{prod_url}/ServiceModel/AuthService.svc/Login"
payload = {"UserName": prod_user, "UserPassword": prod_pass}
resp = session.post(login_url, json=payload, timeout=30)
if resp.status_code != 200 or resp.json().get("Code") != 0:
    print(f"Login failed")
    exit(1)

bpmcsrf = session.cookies.get("BPMCSRF")
headers = {"Content-Type": "application/json", "BPMCSRF": bpmcsrf}

print("=" * 70)
print("CHECKING PROD UsrPage_ebkv9e8 SCHEMAS")
print("=" * 70)

# Query all UsrPage_ebkv9e8 schemas
schema_url = f"{prod_url}/0/odata/SysSchema?$filter=Name eq 'UsrPage_ebkv9e8'&$select=Id,UId,Name,SysPackageId,ExtendParent,ModifiedOn&$orderby=ModifiedOn desc"
resp = session.get(schema_url, headers=headers, timeout=60)

if resp.status_code == 200:
    data = resp.json()
    schemas = data.get("value", [])
    print(f"\nFound {len(schemas)} UsrPage_ebkv9e8 schemas:\n")

    for s in schemas:
        uid = s.get("UId")
        pkg_id = s.get("SysPackageId")
        extend = s.get("ExtendParent", False)
        modified = s.get("ModifiedOn", "")[:19]

        # Get package name
        pkg_name = "Unknown"
        if pkg_id:
            pkg_url = f"{prod_url}/0/odata/SysPackage({pkg_id})?$select=Name"
            pkg_resp = session.get(pkg_url, headers=headers, timeout=30)
            if pkg_resp.status_code == 200:
                pkg_data = pkg_resp.json()
                pkg_name = pkg_data.get("Name", "Unknown")

        schema_type = "CHILD" if extend else "PARENT"
        print(f"  [{schema_type:6}] {pkg_name}")
        print(f"          UId: {uid}")
        print(f"          Modified: {modified}")
        print()

        # Get schema body for the child schema (BGApp_eykaguu)
        if pkg_name == "BGApp_eykaguu":
            print(f"  Getting schema body for BGApp_eykaguu child schema...")

            # Use DataService to get schema body
            ds_url = f"{prod_url}/0/DataService/json/SyncReply/SelectQuery"
            select_payload = {
                "RootSchemaName": "SysSchema",
                "OperationType": 0,
                "Columns": {
                    "Items": {
                        "Body": {"ExpressionType": 0, "Path": "Body"}
                    }
                },
                "Filters": {
                    "FilterType": 6,
                    "LogicalOperation": 0,
                    "Items": {
                        "UIdFilter": {
                            "FilterType": 1,
                            "ComparisonType": 3,
                            "LeftExpression": {"ExpressionType": 0, "Path": "UId"},
                            "RightExpression": {"ExpressionType": 2, "Parameter": {"DataValueType": 0, "Value": uid}}
                        }
                    }
                }
            }
            ds_resp = session.post(ds_url, json=select_payload, headers=headers, timeout=60)
            if ds_resp.status_code == 200:
                result = ds_resp.json()
                if result.get("success") and result.get("rows"):
                    body = result["rows"][0].get("Body", "")
                    if body:
                        # Save to file
                        output_path = "/home/magown/creatio-report-fix/client-module/BGApp_eykaguu_UsrPage_ebkv9e8_PROD_Current.js"
                        with open(output_path, "w") as f:
                            f.write(body)
                        print(f"  Saved to: {output_path}")
                        print(f"  Body length: {len(body)} chars")
                        # Show first few lines
                        lines = body.split('\n')[:20]
                        print(f"\n  First 20 lines:")
                        for i, line in enumerate(lines):
                            print(f"    {line}")
                    else:
                        print(f"  Body is empty")
                else:
                    print(f"  No rows returned")
            else:
                print(f"  DataService error: {ds_resp.status_code}")
else:
    print(f"Error: {resp.status_code}")
