#!/usr/bin/env python3
"""
Map each report in UsrReportesPampa to its required filter fields.
This will help us understand which filters to show for each report type.
"""

import os
import sys
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


class CreatioClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.bpmcsrf = None

    def login(self):
        """Authenticate with Creatio"""
        login_url = f"{self.base_url}/ServiceModel/AuthService.svc/Login"
        payload = {"UserName": self.username, "UserPassword": self.password}

        resp = self.session.post(login_url, json=payload, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("Code") == 0:
                self.bpmcsrf = self.session.cookies.get("BPMCSRF")
                return True
        return False

    def odata_query(self, entity, params=""):
        """Execute OData query"""
        url = f"{self.base_url}/0/odata/{entity}"
        if params:
            url += f"?{params}"

        headers = {"Content-Type": "application/json"}
        if self.bpmcsrf:
            headers["BPMCSRF"] = self.bpmcsrf

        resp = self.session.get(url, headers=headers, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        return None


def investigate_reports(env_name, url, username, password):
    """Get all reports and their configurations"""
    print(f"\n{'='*70}")
    print(f"ENVIRONMENT: {env_name}")
    print(f"{'='*70}")

    client = CreatioClient(url, username, password)
    if not client.login():
        print(f"  Login failed!")
        return None

    print(f"  Login successful")

    results = {
        "environment": env_name,
        "reports": [],
        "excel_templates": []
    }

    # Query 1: Get all UsrReportesPampa entries (the report definitions)
    print(f"\n  Querying UsrReportesPampa (report definitions)...")
    pampa_query = "$select=Id,Name,UsrCode,UsrURL,UsrDescription&$orderby=Name"
    pampa_data = client.odata_query("UsrReportesPampa", pampa_query)

    if pampa_data and pampa_data.get("value"):
        reports = pampa_data["value"]
        print(f"  Found {len(reports)} reports in UsrReportesPampa\n")

        for r in reports:
            report_info = {
                "Id": r.get("Id"),
                "Name": r.get("Name"),
                "Code": r.get("UsrCode"),
                "HasLookerURL": bool(r.get("UsrURL")),
                "Description": r.get("UsrDescription", "")[:50] if r.get("UsrDescription") else ""
            }
            results["reports"].append(report_info)

            has_url = "YES (Looker)" if r.get("UsrURL") else "NO (Excel)"
            print(f"    [{r.get('UsrCode') or '---':20}] {r.get('Name')[:35]:35} | URL: {has_url}")
    else:
        print(f"  No reports found in UsrReportesPampa")

    # Query 2: Get IntExcelReport entries (Excel template configurations)
    print(f"\n  Querying IntExcelReport (Excel templates)...")
    excel_query = "$select=Id,IntName,IntEntitySchemaNameId,IntEsq&$orderby=IntName"
    excel_data = client.odata_query("IntExcelReport", excel_query)

    if excel_data and excel_data.get("value"):
        templates = excel_data["value"]
        print(f"  Found {len(templates)} Excel templates\n")

        for t in templates:
            template_info = {
                "Id": t.get("Id"),
                "Name": t.get("IntName"),
                "EntitySchemaId": t.get("IntEntitySchemaNameId"),
                "HasESQ": bool(t.get("IntEsq"))
            }
            results["excel_templates"].append(template_info)

            has_esq = "YES" if t.get("IntEsq") else "NO"
            print(f"    {t.get('IntName')[:45]:45} | ESQ: {has_esq}")
    else:
        print(f"  No Excel templates found")

    # Query 3: Check if there are filter field configurations
    print(f"\n  Checking for filter field schema/attributes...")

    # Look for any entity that might contain filter configuration
    # Check if UsrReportesPampa has additional filter columns
    pampa_schema_query = "$select=Id,Name,UsrCode,UsrURL"
    pampa_schema = client.odata_query("UsrReportesPampa", "$top=1")
    if pampa_schema and pampa_schema.get("value"):
        sample = pampa_schema["value"][0]
        print(f"\n  UsrReportesPampa available columns:")
        for key in sample.keys():
            print(f"    - {key}")

    return results


def analyze_report_categories(results):
    """Categorize reports by their filter requirements"""
    print(f"\n{'='*70}")
    print("ANALYSIS: Report Categories")
    print(f"{'='*70}")

    if not results:
        return

    reports = results.get("reports", [])
    templates = results.get("excel_templates", [])

    # Categorize by Looker vs Excel
    looker_reports = [r for r in reports if r["HasLookerURL"]]
    excel_reports = [r for r in reports if not r["HasLookerURL"]]

    print(f"\n  LOOKER STUDIO REPORTS ({len(looker_reports)}):")
    print("  These open in new browser tab - no filter fields needed in Creatio UI")
    for r in looker_reports:
        print(f"    - {r['Name']}")

    print(f"\n  EXCEL REPORTS ({len(excel_reports)}):")
    print("  These use IntExcelReport templates - may need filter fields")
    for r in excel_reports:
        code = r["Code"] or r["Name"]
        # Try to find matching Excel template
        matching = [t for t in templates if code.lower() in t["Name"].lower() or r["Name"].lower() in t["Name"].lower()]
        if matching:
            print(f"    - {r['Name']} -> Template: {matching[0]['Name']}")
        else:
            print(f"    - {r['Name']} -> No matching template found")

    # Identify Commission-related reports
    print(f"\n  COMMISSION REPORTS (need Year-Month + Sales Group filters):")
    commission_reports = [r for r in reports if "commission" in r["Name"].lower()]
    for r in commission_reports:
        print(f"    - {r['Name']}")

    # Identify date-filter reports
    print(f"\n  DATE-BASED REPORTS (need Created/Shipping/Delivery date filters):")
    date_reports = [r for r in reports if not r["HasLookerURL"] and "commission" not in r["Name"].lower()]
    for r in date_reports:
        print(f"    - {r['Name']}")


def main():
    # Get credentials
    prod_url = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com")
    prod_user = os.environ.get("CREATIO_PROD_USERNAME", "Supervisor")
    prod_pass = os.environ.get("CREATIO_PROD_PASSWORD", "")

    print("=" * 70)
    print("REPORT FILTER REQUIREMENTS MAPPING")
    print("=" * 70)

    # Investigate PROD (primary source of truth)
    results = investigate_reports("PROD", prod_url, prod_user, prod_pass)

    if results:
        analyze_report_categories(results)

        # Save results to JSON for reference
        output_path = "/home/magown/creatio-report-fix/docs/REPORT_FILTER_MAPPING.json"
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n  Results saved to: {output_path}")


if __name__ == "__main__":
    main()
