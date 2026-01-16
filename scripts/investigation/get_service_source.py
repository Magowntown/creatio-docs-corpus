#!/usr/bin/env python3
"""
Get BGIntExcelReportService2 source code using OData
"""

import os
import requests
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import ARTIFACTS_DIR, ensure_dirs

ensure_dirs()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

def login(session):
    """Login to Creatio"""
    login_url = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"
    login_data = {"UserName": USERNAME, "UserPassword": PASSWORD}
    response = session.post(login_url, json=login_data)
    return response.status_code == 200

def main():
    session = requests.Session()

    print("Logging in...")
    if not login(session):
        print("Login failed")
        return

    bpmcsrf = session.cookies.get("BPMCSRF", "")
    headers = {"BPMCSRF": bpmcsrf}

    # Try OData endpoint for SysSchema
    schema_uid = "ff5499a9-4aec-4403-9511-3394370035d3"

    # Method 1: OData
    odata_url = f"{CREATIO_URL}/0/odata/SysSchema"
    params = {
        "$filter": f"UId eq {schema_uid}",
        "$select": "Id,UId,Name,Body"
    }

    print("\nTrying OData endpoint...")
    response = session.get(odata_url, params=params, headers=headers)
    print(f"OData response: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        if data.get("value"):
            schema = data["value"][0]
            print(f"Schema: {schema.get('Name')}")
            body = schema.get('Body', '')
            print(f"Body length: {len(body) if body else 0}")

            if body:
                out_path = ARTIFACTS_DIR / "service_source.cs"
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(body)
                print(f"Saved to {out_path}")
            return

    # Method 2: Configuration API
    print("\nTrying Configuration API...")
    config_url = f"{CREATIO_URL}/0/ServiceModel/SchemaDesignerService.svc/GetSchema"
    config_data = {"schemaUId": schema_uid}

    response = session.post(config_url, json=config_data, headers={
        **headers,
        "Content-Type": "application/json"
    })
    print(f"Config API response: {response.status_code}")

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'not dict'}")
            print(f"Response: {json.dumps(data, indent=2)[:1000]}")
        except:
            print(f"Response text: {response.text[:1000]}")

    # Method 3: Direct schema read
    print("\nTrying direct schema read...")
    schema_url = f"{CREATIO_URL}/0/rest/CreatioApiGateway/GetSourceCodeBody"
    response = session.post(schema_url, json={"schemaUId": schema_uid}, headers={
        **headers,
        "Content-Type": "application/json"
    })
    print(f"Direct response: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.text[:500]}")

if __name__ == "__main__":
    main()
