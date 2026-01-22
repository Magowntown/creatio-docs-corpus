#!/usr/bin/env python3
"""
Direct query to get UsrReportesPampa entries with debug output
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

print(f"Connecting to: {prod_url}")

session = requests.Session()

# Login
login_url = f"{prod_url}/ServiceModel/AuthService.svc/Login"
payload = {"UserName": prod_user, "UserPassword": prod_pass}

resp = session.post(login_url, json=payload, timeout=30)
print(f"Login response: {resp.status_code}")

if resp.status_code != 200:
    print(f"Login failed: {resp.text[:200]}")
    exit(1)

data = resp.json()
print(f"Login code: {data.get('Code')}")

if data.get("Code") != 0:
    print(f"Login error: {data.get('Message')}")
    exit(1)

bpmcsrf = session.cookies.get("BPMCSRF")
headers = {"Content-Type": "application/json", "BPMCSRF": bpmcsrf}

# Try different entity names that might contain report definitions
entities_to_check = [
    "UsrReportesPampa",
    "BGPampaReport",
    "BGReportesPampa",
    "PampaReport",
    "UsrReporte",
    "BGReport"
]

for entity in entities_to_check:
    print(f"\n{'='*50}")
    print(f"Checking entity: {entity}")
    print(f"{'='*50}")

    url = f"{prod_url}/0/odata/{entity}?$top=5"
    resp = session.get(url, headers=headers, timeout=30)

    print(f"Status: {resp.status_code}")

    if resp.status_code == 200:
        data = resp.json()
        values = data.get("value", [])
        print(f"Found {len(values)} records")
        for v in values:
            print(f"  - {v.get('Name', v.get('Id', 'Unknown'))}")
    elif resp.status_code == 404:
        print(f"Entity not found")
    else:
        print(f"Error: {resp.text[:200]}")

# Check what lookup schemas exist
print(f"\n{'='*50}")
print("Searching for Report-related lookup schemas...")
print(f"{'='*50}")

# Query SysSchema for report-related schemas
schema_url = f"{prod_url}/0/odata/SysSchema?$filter=contains(Name,'Report') or contains(Name,'Pampa')&$select=Id,UId,Name,ManagerName&$top=30"
resp = session.get(schema_url, headers=headers, timeout=60)

if resp.status_code == 200:
    data = resp.json()
    schemas = data.get("value", [])
    print(f"Found {len(schemas)} matching schemas:")
    for s in schemas:
        print(f"  {s.get('ManagerName', 'N/A'):20} | {s.get('Name')}")
else:
    print(f"Error querying schemas: {resp.status_code}")

# Check DataService for report lookups
print(f"\n{'='*50}")
print("Checking DataService for BGPampaReport lookup...")
print(f"{'='*50}")

# Use DataService/SelectQuery to check
ds_url = f"{prod_url}/0/DataService/json/SyncReply/SelectQuery"
select_payload = {
    "RootSchemaName": "SysLookup",
    "OperationType": 0,
    "Columns": {
        "Items": {
            "Name": {"ExpressionType": 0, "Path": "Name"},
            "SysEntitySchemaUId": {"ExpressionType": 0, "Path": "SysEntitySchemaUId"}
        }
    },
    "Filters": {
        "FilterType": 6,
        "LogicalOperation": 0,
        "Items": {
            "NameFilter": {
                "FilterType": 1,
                "ComparisonType": 11,
                "LeftExpression": {"ExpressionType": 0, "Path": "Name"},
                "RightExpression": {"ExpressionType": 2, "Parameter": {"DataValueType": 1, "Value": "Report"}}
            }
        }
    }
}

resp = session.post(ds_url, json=select_payload, headers=headers, timeout=30)
if resp.status_code == 200:
    result = resp.json()
    if result.get("success") and result.get("rows"):
        print("Found report-related lookups:")
        for row in result["rows"][:10]:
            print(f"  - {row.get('Name')}")
    else:
        print(f"No lookups found matching 'Report'")
else:
    print(f"DataService error: {resp.status_code}")
