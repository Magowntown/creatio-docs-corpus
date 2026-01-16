#!/usr/bin/env python3
"""
Find Commission report in UsrReportesPampa and understand the mapping.
"""

import os
import requests
import json

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

def main():
    session = requests.Session()

    # Login
    print("=== Logging in ===")
    response = session.post(f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
                           json={"UserName": USERNAME, "UserPassword": PASSWORD},
                           timeout=30)
    print("Login:", "OK" if response.status_code == 200 else "FAILED")

    headers = {
        "Content-Type": "application/json",
        "BPMCSRF": session.cookies.get("BPMCSRF", "")
    }

    esq_url = f"{CREATIO_URL}/0/dataservice/json/SyncReply/SelectQuery"

    # Get ALL UsrReportesPampa records
    print("\n" + "="*60)
    print("=== ALL UsrReportesPampa records ===")
    print("="*60)

    esq_body = {
        "rootSchemaName": "UsrReportesPampa",
        "operationType": 0,
        "allColumns": True,
        "rowCount": 50
    }
    response = session.post(esq_url, json=esq_body, headers=headers, timeout=30)

    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        print(f"\nFound {len(rows)} records:")

        for i, row in enumerate(rows, 1):
            print(f"\n--- Record {i} ---")
            print(f"  Id: {row.get('Id')}")
            print(f"  Name: {row.get('Name')}")
            print(f"  UsrCode: {row.get('UsrCode')}")
            print(f"  UsrURL: {row.get('UsrURL')}")
            print(f"  UsrActive: {row.get('UsrActive')}")
            # Print any other columns that might be FK
            for k, v in row.items():
                if k not in ['Id', 'Name', 'UsrCode', 'UsrURL', 'UsrActive', 'Description',
                             'CreatedOn', 'ModifiedOn', 'CreatedBy', 'ModifiedBy', 'ProcessListeners']:
                    print(f"  {k}: {v}")

    # Get ALL IntExcelReport records to compare
    print("\n" + "="*60)
    print("=== ALL IntExcelReport records ===")
    print("="*60)

    esq_body = {
        "rootSchemaName": "IntExcelReport",
        "operationType": 0,
        "allColumns": True,
        "rowCount": 50
    }
    response = session.post(esq_url, json=esq_body, headers=headers, timeout=30)

    if response.status_code == 200:
        data = response.json()
        rows = data.get("rows", [])
        print(f"\nFound {len(rows)} IntExcelReport records:")

        for row in rows:
            name = row.get("IntName", "N/A")
            entity = row.get("IntEntitySchemaName", {})
            if isinstance(entity, dict):
                entity_name = entity.get("displayValue", "N/A")
            else:
                entity_name = entity
            print(f"  - {name} (ID: {row.get('Id')}) -> Entity: {entity_name}")

    # Check if there's a relationship through UsrCode matching IntName
    print("\n" + "="*60)
    print("=== Looking for potential mappings ===")
    print("="*60)
    print("\nPotential matches between UsrReportesPampa.UsrCode and IntExcelReport.IntName:")
    print("(You need to verify which UsrReportesPampa.UsrCode corresponds to which IntExcelReport)")

if __name__ == "__main__":
    main()
