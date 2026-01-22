#!/usr/bin/env python3
"""
Check the lookup field mappings to understand the report dropdown configuration.
Parent schema uses LookupAttribute_0as4io2 → UsrReporte
Some custom handlers use LookupAttribute_bsixu8a → BGPampaReport
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
print("CHECKING LOOKUP FIELD MAPPINGS")
print("=" * 70)

# Check UsrEntity_e7ac661 schema to see what lookup columns exist
print("\n1. Checking UsrEntity_e7ac661 schema columns...")

# Query entity schema manager for columns
schema_url = f"{prod_url}/0/odata/VwSysEntitySchemaColumn?$filter=SysEntitySchemaUId eq guid'e7ac661a-85b8-4b09-9a90-2abedee8d946'&$select=Name,DataValueType"
resp = session.get(schema_url, headers=headers, timeout=60)

# This might not work, let's try a different approach - query the entity directly
print("\n2. Querying UsrEntity_e7ac661 directly for sample record...")

# First check if the entity exists and what columns it has
entity_url = f"{prod_url}/0/odata/UsrEntity_e7ac661?$top=1"
resp = session.get(entity_url, headers=headers, timeout=30)

if resp.status_code == 200:
    data = resp.json()
    if data.get("value"):
        sample = data["value"][0]
        print(f"Sample record columns in UsrEntity_e7ac661:")
        for key in sorted(sample.keys()):
            val = sample.get(key)
            val_preview = str(val)[:50] if val else "(null)"
            print(f"  - {key}: {val_preview}")
    else:
        print("  Entity exists but no records found")
else:
    print(f"  Error: {resp.status_code}")

# Check specific lookup fields
print("\n3. Checking UsrReporte vs BGPampaReport lookup targets...")

# Query UsrReportesPampa
url = f"{prod_url}/0/odata/UsrReportesPampa?$top=3&$select=Id,Name,UsrCode"
resp = session.get(url, headers=headers, timeout=30)
if resp.status_code == 200:
    data = resp.json()
    reports = data.get("value", [])
    print(f"\n  UsrReportesPampa ({len(reports)} shown):")
    for r in reports:
        print(f"    - {r.get('Name')} [{r.get('UsrCode') or 'no code'}]")

# Check if there's a separate lookup entity for the report field
print("\n4. Checking SysLookup for report-related lookups...")
lookup_url = f"{prod_url}/0/odata/SysLookup?$filter=contains(Name,'Report') or contains(Name,'Pampa')&$select=Id,Name"
resp = session.get(lookup_url, headers=headers, timeout=30)
if resp.status_code == 200:
    data = resp.json()
    lookups = data.get("value", [])
    print(f"  Found {len(lookups)} matching lookups:")
    for l in lookups:
        print(f"    - {l.get('Name')}")

# Check the entity schema configuration
print("\n5. Checking SysEntitySchemaColumn for UsrReporte/BGPampaReport columns...")
col_filter = "contains(Name,'UsrReporte') or contains(Name,'BGPampaReport') or contains(Name,'Report')"
col_url = f"{prod_url}/0/odata/SysEntitySchemaColumn?$filter={col_filter}&$select=Name,Caption,ReferenceSchemaName&$top=20"
resp = session.get(col_url, headers=headers, timeout=30)
if resp.status_code == 200:
    data = resp.json()
    cols = data.get("value", [])
    print(f"  Found {len(cols)} matching columns:")
    for c in cols:
        ref = c.get('ReferenceSchemaName') or '(no reference)'
        print(f"    - {c.get('Name')} → {ref}")
else:
    print(f"  Error: {resp.status_code}")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("""
The parent schema (BGlobalLookerStudio) uses:
  - LookupAttribute_0as4io2 → UsrEntity_e7ac661DS.UsrReporte

This means the report dropdown points to a column named "UsrReporte"
in the UsrEntity_e7ac661 entity, which likely references UsrReportesPampa.

The child schema should:
  1. Listen for changes on LookupAttribute_0as4io2 (parent's attribute)
  2. React to show/hide Commission filters accordingly
""")
