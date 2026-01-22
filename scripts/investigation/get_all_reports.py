#!/usr/bin/env python3
"""
Get all reports from UsrReportesPampa and IntExcelReport with full details
"""

import os
import json
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

print("=" * 80)
print("ALL REPORTS IN UsrReportesPampa")
print("=" * 80)

# Get all UsrReportesPampa records
url = f"{prod_url}/0/odata/UsrReportesPampa?$orderby=Name"
resp = session.get(url, headers=headers, timeout=60)

if resp.status_code == 200:
    data = resp.json()
    reports = data.get("value", [])
    print(f"\nFound {len(reports)} reports:\n")

    looker_reports = []
    excel_reports = []

    for r in reports:
        has_url = bool(r.get("UsrURL"))
        report_info = {
            "Id": r.get("Id"),
            "Name": r.get("Name"),
            "Code": r.get("UsrCode"),
            "URL": r.get("UsrURL", "")[:50] if r.get("UsrURL") else "",
            "Active": r.get("UsrActive", True)
        }

        if has_url:
            looker_reports.append(report_info)
        else:
            excel_reports.append(report_info)

        status = "LOOKER" if has_url else "EXCEL"
        active = "ACTIVE" if r.get("UsrActive", True) else "INACTIVE"
        print(f"[{status:6}] [{active:8}] {r.get('Name')}")
        print(f"         Code: {r.get('UsrCode') or '(none)'}")
        if has_url:
            print(f"         URL: {r.get('UsrURL')[:60]}...")
        print()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nLooker Studio reports: {len(looker_reports)}")
    for r in looker_reports:
        print(f"  - {r['Name']}")

    print(f"\nExcel reports (no Looker URL): {len(excel_reports)}")
    for r in excel_reports:
        print(f"  - {r['Name']}")

else:
    print(f"Error: {resp.status_code}")
    print(resp.text[:500])

# Get IntExcelReport entries
print("\n" + "=" * 80)
print("EXCEL TEMPLATES (IntExcelReport)")
print("=" * 80)

url = f"{prod_url}/0/odata/IntExcelReport?$select=Id,IntName,IntEntitySchemaNameId&$orderby=IntName"
resp = session.get(url, headers=headers, timeout=60)

if resp.status_code == 200:
    data = resp.json()
    templates = data.get("value", [])
    print(f"\nFound {len(templates)} Excel templates:\n")

    # Group by whether they match Pampa report names
    for t in templates:
        name = t.get("IntName", "")
        # Check if this matches any Pampa report
        pampa_match = any(
            name.lower() == r.get("Name", "").lower() or
            name.lower() == f"rpt {r.get('Name', '')}".lower() or
            name.lower().replace("rpt ", "") == r.get("Name", "").lower() or
            r.get("UsrCode", "").lower() == name.lower()
            for r in excel_reports
        ) if excel_reports else False

        match_indicator = "MATCH" if pampa_match else "     "
        print(f"[{match_indicator}] {name}")

# Analysis of filter requirements
print("\n" + "=" * 80)
print("FILTER REQUIREMENTS ANALYSIS")
print("=" * 80)

print("""
Based on the handler code and report structure:

COMMISSION REPORTS:
  - Need: Year-Month (required), Sales Group (required)
  - Hide: Date filters (Created/Shipping/Delivery From/To)
  - Show: Warning label about QuickBooks data

NON-COMMISSION EXCEL REPORTS:
  - Need: Date filters (Created/Shipping/Delivery From/To)
  - Hide: Year-Month, Sales Group, Warning label
  - Some may need Status Order filter

LOOKER STUDIO REPORTS:
  - Open in new tab - no Creatio filters needed
  - Looker Studio has its own filter UI
  - CSP blocks iframe embedding in Freedom UI

PROPOSED VISIBILITY LOGIC:
  1. Default: Show date filters, hide Commission filters
  2. On report selection:
     - If "Commission" in name: Show Commission filters, hide date filters
     - Else: Keep defaults
""")

# Save results
output = {
    "looker_reports": looker_reports,
    "excel_reports": excel_reports,
    "filter_logic": {
        "commission": {
            "show": ["BGWarningLabel", "GridContainer_3asa01r", "BGYearMonth", "BGSalesGroup"],
            "hide": ["CreatedFrom", "CreatedTo", "ShippingFrom", "ShippingTo", "DeliveryFrom", "DeliveryTo"]
        },
        "non_commission": {
            "show": ["CreatedFrom", "CreatedTo", "ShippingFrom", "ShippingTo", "DeliveryFrom", "DeliveryTo"],
            "hide": ["BGWarningLabel", "GridContainer_3asa01r", "BGYearMonth", "BGSalesGroup"]
        },
        "looker": {
            "show": [],
            "hide": ["BGWarningLabel", "GridContainer_3asa01r", "BGYearMonth", "BGSalesGroup",
                    "CreatedFrom", "CreatedTo", "ShippingFrom", "ShippingTo", "DeliveryFrom", "DeliveryTo"],
            "action": "opens_new_tab"
        }
    }
}

output_path = "/home/magown/creatio-report-fix/docs/REPORT_FILTER_MAPPING.json"
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved to: {output_path}")
