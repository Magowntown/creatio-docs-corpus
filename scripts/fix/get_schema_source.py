#!/usr/bin/env python3
"""Get OrderPageV2 schema source code and find PaymentStatus default."""

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

IWQB_ORDER_PAGE_SCHEMA_ID = "6c9e5e8b-9d0b-41b4-b24d-bec395eb68bf"
IWQB_ORDER_PAGE_UID = "c789af69-bb29-464a-a361-a3abe9d976a2"
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

    def query(self, entity, columns=None, filters=None, limit=100):
        url = f"{self.base_url}/0/odata/{entity}"
        params = {"$top": str(limit)}
        if columns:
            params["$select"] = ",".join(columns)
        if filters:
            params["$filter"] = filters

        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            print(f"Query {entity} failed: {resp.status_code}")
            return []
        return resp.json().get("value", [])

    def get_media(self, entity, record_id, media_property):
        """Get media/binary content from OData entity."""
        url = f"{self.base_url}/0/odata/{entity}({record_id})/{media_property}"
        resp = self.session.get(url)
        return resp.content if resp.status_code == 200 else None

def main():
    print("=" * 70)
    print("GET ORDERPAGEV2 SCHEMA SOURCE")
    print("=" * 70)

    client = CreatioClient(PROD_URL, PROD_USER, PROD_PASS)

    # 1. Get schema content from SysSchemaContent
    print("\n1. Checking SysSchemaContent for schema code...")

    # Try to find content by schema UId
    content = client.query(
        "SysSchemaContent",
        columns=["Id", "SysSchemaId", "Code", "ContentType"],
        filters=f"SysSchemaId eq {IWQB_ORDER_PAGE_SCHEMA_ID}",
        limit=10
    )

    if content:
        print(f"   Found {len(content)} content records")
        for c in content:
            print(f"\n   Content ID: {c.get('Id')}")
            print(f"   ContentType: {c.get('ContentType')}")
            code = c.get('Code', '')
            if code:
                print(f"   Code preview ({len(code)} chars):")
                # Check if it contains PaymentStatus
                if PLANNED_STATUS_ID in code:
                    print(f"   ⚠️  FOUND PLANNED_STATUS_ID in code!")
                    # Find the context
                    idx = code.find(PLANNED_STATUS_ID)
                    start = max(0, idx - 200)
                    end = min(len(code), idx + 200)
                    print(f"   Context: ...{code[start:end]}...")
                elif "PaymentStatus" in code:
                    print(f"   ⚠️  Found 'PaymentStatus' reference")
                    idx = code.find("PaymentStatus")
                    start = max(0, idx - 100)
                    end = min(len(code), idx + 200)
                    print(f"   Context: ...{code[start:end]}...")
                else:
                    print(f"   Code snippet: {code[:500]}...")
    else:
        print("   No content found via SysSchemaId filter")

    # 2. Try to get MetaData directly from schema
    print("\n2. Trying to get MetaData from SysSchema...")
    metadata = client.get_media("SysSchema", IWQB_ORDER_PAGE_SCHEMA_ID, "MetaData")
    if metadata:
        print(f"   Got MetaData: {len(metadata)} bytes")
        try:
            # Try to decode as JSON
            meta_str = metadata.decode('utf-8')
            print(f"   Decoded as string ({len(meta_str)} chars)")

            if PLANNED_STATUS_ID in meta_str:
                print(f"   ⚠️  FOUND PLANNED_STATUS_ID in MetaData!")
                idx = meta_str.find(PLANNED_STATUS_ID)
                start = max(0, idx - 300)
                end = min(len(meta_str), idx + 300)
                print(f"\n   Context around PaymentStatus default:")
                print(f"   {meta_str[start:end]}")

            if "PaymentStatus" in meta_str:
                print(f"\n   All PaymentStatus references:")
                for i, line in enumerate(meta_str.split('\n')):
                    if "PaymentStatus" in line or PLANNED_STATUS_ID in line:
                        print(f"   Line {i}: {line[:200]}")

        except Exception as e:
            print(f"   Could not decode: {e}")
            print(f"   Raw bytes: {metadata[:200]}")
    else:
        print("   Could not get MetaData")

    # 3. Try Descriptor
    print("\n3. Trying to get Descriptor from SysSchema...")
    descriptor = client.get_media("SysSchema", IWQB_ORDER_PAGE_SCHEMA_ID, "Descriptor")
    if descriptor:
        print(f"   Got Descriptor: {len(descriptor)} bytes")
        try:
            desc_str = descriptor.decode('utf-8')
            if PLANNED_STATUS_ID in desc_str:
                print(f"   ⚠️  FOUND PLANNED_STATUS_ID in Descriptor!")
        except:
            pass
    else:
        print("   Could not get Descriptor")

    # 4. Check other Order page schemas for comparison
    print("\n4. Comparing with PampaBay OrderPageV2...")
    pampabay_page = client.query(
        "SysSchema",
        filters="Name eq 'OrderPageV2' and SysPackageId eq 8b0ef6b5-915e-4739-a779-9d54505f19df",
        limit=1
    )
    if pampabay_page:
        pb_id = pampabay_page[0].get('Id')
        print(f"   PampaBay OrderPageV2 ID: {pb_id}")

        pb_content = client.query(
            "SysSchemaContent",
            columns=["Id", "Code", "ContentType"],
            filters=f"SysSchemaId eq {pb_id}",
            limit=5
        )
        if pb_content:
            for c in pb_content:
                code = c.get('Code', '')
                if "PaymentStatus" in code:
                    print(f"   PampaBay has PaymentStatus reference")
                    idx = code.find("PaymentStatus")
                    print(f"   Context: {code[max(0,idx-50):idx+150]}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
