#!/usr/bin/env python3
"""
Compare UsrPage_ebkv9e8 schemas between DEV and PROD to understand
why visual changes aren't reflecting in PROD.
"""

import os
import sys
import json
import requests
from datetime import datetime

# Load environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

        resp = self.session.post(login_url, json=payload)
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

        resp = self.session.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        return None


def investigate_environment(name, url, username, password):
    """Investigate UsrPage_ebkv9e8 schemas in an environment"""
    print(f"\n{'='*60}")
    print(f"ENVIRONMENT: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")

    client = CreatioClient(url, username, password)
    if not client.login():
        print(f"  ❌ Login failed!")
        return None

    print(f"  ✅ Login successful")

    results = {
        "name": name,
        "url": url,
        "schemas": [],
        "business_rules": [],
        "packages": {}
    }

    # Query 1: Find all UsrPage_ebkv9e8 schemas
    print(f"\n  Querying SysSchema for UsrPage_ebkv9e8...")
    schema_query = "$filter=Name eq 'UsrPage_ebkv9e8'&$select=Id,UId,Name,Caption,SysPackageId,ExtendParentId,ParentId,ManagerName,ModifiedOn&$orderby=ModifiedOn desc"
    schema_data = client.odata_query("SysSchema", schema_query)

    if schema_data and schema_data.get("value"):
        schemas = schema_data["value"]
        print(f"  Found {len(schemas)} UsrPage_ebkv9e8 schema(s):")

        for s in schemas:
            schema_id = s.get("Id")
            uid = s.get("UId")
            pkg_id = s.get("SysPackageId")
            parent_id = s.get("ExtendParentId") or s.get("ParentId")
            manager = s.get("ManagerName")
            modified = s.get("ModifiedOn", "")[:19]

            # Get package name
            pkg_name = "Unknown"
            if pkg_id:
                pkg_query = f"$filter=Id eq {pkg_id}&$select=Name"
                pkg_data = client.odata_query("SysPackage", pkg_query)
                if pkg_data and pkg_data.get("value"):
                    pkg_name = pkg_data["value"][0].get("Name", "Unknown")
                    results["packages"][pkg_id] = pkg_name

            schema_info = {
                "Id": schema_id,
                "UId": uid,
                "Package": pkg_name,
                "PackageId": pkg_id,
                "ParentId": parent_id,
                "Manager": manager,
                "ModifiedOn": modified
            }
            results["schemas"].append(schema_info)

            print(f"\n    Schema UID: {uid}")
            print(f"    Package: {pkg_name}")
            print(f"    Manager: {manager}")
            print(f"    ParentId: {parent_id}")
            print(f"    Modified: {modified}")
    else:
        print(f"  ⚠️  No schemas found")

    # Query 2: Find business rules
    print(f"\n  Querying SysSchema for business rules (BGUsrPage_ebkv9e8BusinessRule)...")
    br_query = "$filter=contains(Name,'BGUsrPage_ebkv9e8')&$select=Id,UId,Name,Caption,SysPackageId,ExtendParentId,ManagerName,ModifiedOn&$orderby=ModifiedOn desc"
    br_data = client.odata_query("SysSchema", br_query)

    if br_data and br_data.get("value"):
        rules = br_data["value"]
        print(f"  Found {len(rules)} business rule(s):")

        for r in rules:
            uid = r.get("UId")
            name = r.get("Name")
            pkg_id = r.get("SysPackageId")
            modified = r.get("ModifiedOn", "")[:19]

            # Get package name
            pkg_name = results["packages"].get(pkg_id)
            if not pkg_name and pkg_id:
                pkg_query = f"$filter=Id eq {pkg_id}&$select=Name"
                pkg_data = client.odata_query("SysPackage", pkg_query)
                if pkg_data and pkg_data.get("value"):
                    pkg_name = pkg_data["value"][0].get("Name", "Unknown")
                    results["packages"][pkg_id] = pkg_name

            rule_info = {
                "UId": uid,
                "Name": name,
                "Package": pkg_name,
                "ModifiedOn": modified
            }
            results["business_rules"].append(rule_info)

            print(f"\n    Rule: {name}")
            print(f"    Package: {pkg_name}")
            print(f"    Modified: {modified}")
    else:
        print(f"  ⚠️  No business rules found")

    # Query 3: Check package dependencies to understand loading order
    print(f"\n  Checking package dependency hierarchy...")

    # Get packages that contain our schemas
    packages_of_interest = list(set(s.get("Package") for s in results["schemas"]))
    print(f"  Packages with UsrPage_ebkv9e8: {packages_of_interest}")

    for pkg_name in packages_of_interest:
        if pkg_name == "Unknown":
            continue
        pkg_query = f"$filter=Name eq '{pkg_name}'&$select=Id,Name,Position,DependsOnPackages"
        pkg_data = client.odata_query("SysPackage", pkg_query)
        if pkg_data and pkg_data.get("value"):
            pkg = pkg_data["value"][0]
            print(f"\n    Package: {pkg_name}")
            print(f"    Position: {pkg.get('Position')}")
            # Note: DependsOnPackages may not be in OData

    return results


def main():
    # Get credentials from environment
    dev_url = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
    dev_user = os.environ.get("CREATIO_USERNAME", "Supervisor")
    dev_pass = os.environ.get("CREATIO_PASSWORD", "")

    prod_url = os.environ.get("CREATIO_PROD_URL", "https://pampabay.creatio.com")
    prod_user = os.environ.get("CREATIO_PROD_USERNAME", "Supervisor")
    prod_pass = os.environ.get("CREATIO_PROD_PASSWORD", "")

    print("=" * 70)
    print("COMPARING UsrPage_ebkv9e8 SCHEMAS: DEV vs PROD")
    print("=" * 70)

    # Investigate both environments
    dev_results = investigate_environment("DEV", dev_url, dev_user, dev_pass)
    prod_results = investigate_environment("PROD", prod_url, prod_user, prod_pass)

    # Compare results
    print("\n" + "=" * 70)
    print("COMPARISON ANALYSIS")
    print("=" * 70)

    if dev_results and prod_results:
        print("\n📋 SCHEMA COUNT:")
        print(f"   DEV:  {len(dev_results['schemas'])} schema(s)")
        print(f"   PROD: {len(prod_results['schemas'])} schema(s)")

        print("\n📋 BUSINESS RULES:")
        print(f"   DEV:  {len(dev_results['business_rules'])} rule(s)")
        print(f"   PROD: {len(prod_results['business_rules'])} rule(s)")

        print("\n📋 PACKAGES WITH UsrPage_ebkv9e8:")
        dev_packages = set(s.get("Package") for s in dev_results["schemas"])
        prod_packages = set(s.get("Package") for s in prod_results["schemas"])

        print(f"   DEV:  {dev_packages}")
        print(f"   PROD: {prod_packages}")

        only_dev = dev_packages - prod_packages
        only_prod = prod_packages - dev_packages

        if only_dev:
            print(f"   ⚠️  Only in DEV: {only_dev}")
        if only_prod:
            print(f"   ⚠️  Only in PROD: {only_prod}")

        # Identify which schema is "active" (most recently modified, non-child)
        print("\n📋 SCHEMA HIERARCHY ANALYSIS:")
        for env_name, results in [("DEV", dev_results), ("PROD", prod_results)]:
            print(f"\n   {env_name}:")

            # Sort by modification date
            schemas = sorted(results["schemas"], key=lambda x: x.get("ModifiedOn", ""), reverse=True)

            # Identify parent vs child schemas
            parent_schemas = [s for s in schemas if not s.get("ParentId")]
            child_schemas = [s for s in schemas if s.get("ParentId")]

            print(f"   Parent schemas: {len(parent_schemas)}")
            for s in parent_schemas:
                print(f"      - {s['Package']}: {s['UId']} (modified {s['ModifiedOn']})")

            print(f"   Child schemas: {len(child_schemas)}")
            for s in child_schemas:
                print(f"      - {s['Package']}: {s['UId']} extends {s['ParentId']} (modified {s['ModifiedOn']})")

        print("\n" + "=" * 70)
        print("RECOMMENDATIONS")
        print("=" * 70)

        # Check if there's a mismatch in which schema we're editing
        prod_schemas = prod_results["schemas"]
        if len(prod_schemas) > 1:
            print("\n⚠️  PROD has MULTIPLE UsrPage_ebkv9e8 schemas!")
            print("   This may cause confusion about which schema to edit.")
            print("\n   Schema priority in Freedom UI is typically:")
            print("   1. Child schemas (extend parent)")
            print("   2. Later package position wins over earlier")
            print("\n   Ensure you're editing the CORRECT schema:")
            for s in prod_schemas:
                url = f"{prod_url}/0/ClientApp/#/ClientUnitSchemaDesigner/{s['UId']}"
                print(f"\n   Package: {s['Package']}")
                print(f"   URL: {url}")

        # Check for business rule interference
        prod_rules = prod_results["business_rules"]
        if prod_rules:
            print("\n⚠️  PROD has business rules for this page!")
            print("   Business rules can override handler visibility logic.")
            for r in prod_rules:
                print(f"\n   Rule: {r['Name']}")
                print(f"   Package: {r['Package']}")
                print(f"   Modified: {r['ModifiedOn']}")


if __name__ == "__main__":
    # Load .env file
    env_path = "/home/magown/creatio-report-fix/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value

    main()
