#!/usr/bin/env python3
"""Analyze OrderPageV2 schema metadata to find PaymentStatus default."""

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

IWQB_ORDER_PAGE_SCHEMA_ID = "6c9e5e8b-9d0b-41b4-b24d-bec395eb68bf"
PLANNED_STATUS_ID = "bfe38d3d-bd57-48d7-a2d7-82435cd274ca"

class CreatioClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._login(username, password)

    def _login(self, username, password):
        login_url = f"{self.base_url}/ServiceModel/AuthService.svc/Login"
        resp = self.session.post(login_url, json={
            "UserName": username,
            "UserPassword": password
        })
        if resp.status_code != 200 or resp.json().get("Code") != 0:
            raise Exception(f"Login failed: {resp.text}")
        print(f"Logged in to {self.base_url}")

    def get_media(self, entity, record_id, media_property):
        url = f"{self.base_url}/0/odata/{entity}({record_id})/{media_property}"
        resp = self.session.get(url)
        return resp.content if resp.status_code == 200 else None

def main():
    print("=" * 70)
    print("ANALYZE ORDERPAGEV2 SCHEMA METADATA")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # Get MetaData
    print("\n1. Getting MetaData...")
    metadata = client.get_media("SysSchema", IWQB_ORDER_PAGE_SCHEMA_ID, "MetaData")

    if not metadata:
        print("   Failed to get MetaData")
        return

    print(f"   Got {len(metadata)} bytes")

    # Decode and analyze
    meta_str = metadata.decode('utf-8')

    # Save to file for inspection
    output_file = "/home/magown/creatio-report-fix/scripts/fix/iwqb_orderpagev2_metadata.json"
    with open(output_file, 'w') as f:
        f.write(meta_str)
    print(f"   Saved to: {output_file}")

    # Try to parse as JSON
    print("\n2. Parsing metadata...")
    try:
        meta_json = json.loads(meta_str)
        print(f"   Successfully parsed as JSON")
        print(f"   Top-level keys: {list(meta_json.keys())}")

        # Look for PaymentStatus or Planned in the structure
        def search_dict(d, search_terms, path=""):
            findings = []
            if isinstance(d, dict):
                for k, v in d.items():
                    current_path = f"{path}.{k}" if path else k
                    # Check key names
                    for term in search_terms:
                        if term.lower() in k.lower():
                            findings.append((current_path, k, v))
                    # Check string values
                    if isinstance(v, str):
                        for term in search_terms:
                            if term.lower() in v.lower():
                                findings.append((current_path, "value", v))
                    # Recurse
                    findings.extend(search_dict(v, search_terms, current_path))
            elif isinstance(d, list):
                for i, item in enumerate(d):
                    findings.extend(search_dict(item, search_terms, f"{path}[{i}]"))
            return findings

        search_terms = ["PaymentStatus", "Payment", "Planned", PLANNED_STATUS_ID, "defValue", "defaultValue"]
        findings = search_dict(meta_json, search_terms)

        print(f"\n3. Search results for: {search_terms}")
        print("-" * 60)

        if findings:
            for path, key, value in findings:
                val_str = str(value)[:200] if len(str(value)) > 200 else str(value)
                print(f"\n   Path: {path}")
                print(f"   Key: {key}")
                print(f"   Value: {val_str}")
        else:
            print("   No matches found for search terms")

        # Check specific structure areas
        print("\n4. Checking common locations for defaults...")

        # Check attributes
        if "Attributes" in meta_json:
            attrs = meta_json.get("Attributes", {})
            print(f"   Attributes count: {len(attrs)}")
            for attr_name, attr_val in attrs.items():
                if "Payment" in attr_name:
                    print(f"\n   Found attribute: {attr_name}")
                    print(f"   Value: {json.dumps(attr_val, indent=2)[:500]}")

        # Check methods
        if "Methods" in meta_json:
            methods = meta_json.get("Methods", {})
            print(f"   Methods count: {len(methods)}")
            for method_name in methods:
                if "init" in method_name.lower() or "default" in method_name.lower():
                    print(f"   Method: {method_name}")

        # Check diff
        if "Diff" in meta_json:
            diff = meta_json.get("Diff", [])
            print(f"   Diff entries: {len(diff)}")
            for entry in diff:
                if isinstance(entry, dict):
                    name = entry.get("name", "")
                    if "Payment" in name:
                        print(f"\n   Diff entry for: {name}")
                        print(f"   {json.dumps(entry, indent=2)[:500]}")

    except json.JSONDecodeError as e:
        print(f"   Not valid JSON: {e}")
        print(f"\n   Raw content preview:")
        print(meta_str[:2000])

    # Also get Descriptor
    print("\n5. Getting Descriptor...")
    descriptor = client.get_media("SysSchema", IWQB_ORDER_PAGE_SCHEMA_ID, "Descriptor")
    if descriptor:
        desc_str = descriptor.decode('utf-8')
        desc_file = "/home/magown/creatio-report-fix/scripts/fix/iwqb_orderpagev2_descriptor.json"
        with open(desc_file, 'w') as f:
            f.write(desc_str)
        print(f"   Saved to: {desc_file}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
