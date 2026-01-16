#!/usr/bin/env python3
"""Compare IntEsq between DEV and PROD for Commission report."""

import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()

DEV_URL = os.getenv("CREATIO_URL", "https://dev-pampabay.creatio.com")
DEV_USER = os.getenv("CREATIO_USERNAME", "Supervisor")
DEV_PASS = os.getenv("CREATIO_PASSWORD")

PROD_URL = os.getenv("CREATIO_PROD_URL", "https://pampabay.creatio.com")
PROD_USER = os.getenv("CREATIO_PROD_USERNAME", "Supervisor")
PROD_PASS = os.getenv("CREATIO_PROD_PASSWORD")

class CreatioClient:
    def __init__(self, base_url, username, password, name=""):
        self.base_url = base_url.rstrip("/")
        self.name = name
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
        print(f"✓ Logged in to {self.name}: {self.base_url}")

    def query(self, entity, columns=None, filters=None, limit=100):
        url = f"{self.base_url}/0/odata/{entity}"
        params = {"$top": str(limit)}
        if columns:
            params["$select"] = ",".join(columns)
        if filters:
            params["$filter"] = filters

        resp = self.session.get(url, params=params)
        if resp.status_code != 200:
            print(f"Query error: {resp.status_code} - {resp.text[:300]}")
            return []
        return resp.json().get("value", [])

def main():
    print("=" * 70)
    print("Comparing IntEsq between DEV and PROD")
    print("=" * 70)

    dev = CreatioClient(DEV_URL, DEV_USER, DEV_PASS, "DEV")
    prod = CreatioClient(PROD_URL, PROD_USER, PROD_PASS, "PROD")

    # Get Commission report from both
    for env, client in [("DEV", dev), ("PROD", prod)]:
        print(f"\n{'=' * 30} {env} {'=' * 30}")
        reports = client.query(
            "IntExcelReport",
            columns=["Id", "IntName", "IntEsq", "IntEntitySchemaNameId"],
            filters="contains(IntName, 'Commission')",
            limit=5
        )

        for r in reports:
            print(f"\nReport: {r.get('IntName')}")
            print(f"  Id: {r.get('Id')}")
            print(f"  IntEntitySchemaNameId: {r.get('IntEntitySchemaNameId')}")

            intEsq = r.get('IntEsq', '')
            if intEsq:
                # Parse and pretty-print key parts
                try:
                    esq = json.loads(intEsq)
                    print(f"  rootSchemaName: {esq.get('rootSchemaName')}")

                    # Check for @P1@ placeholder
                    if '@P1@' in intEsq:
                        print(f"  ⚠️ Contains @P1@ placeholder!")
                        # Find where
                        filters = esq.get('filters', {}).get('items', {})
                        for key, flt in filters.items():
                            rightExpr = flt.get('rightExpression', {})
                            param = rightExpr.get('parameter', {})
                            value = param.get('value', '')
                            if value == '@P1@':
                                leftExpr = flt.get('leftExpression', {})
                                columnPath = leftExpr.get('columnPath', 'unknown')
                                print(f"    Filter on '{columnPath}' uses @P1@ placeholder")
                    else:
                        print(f"  ✓ No @P1@ placeholder")

                except json.JSONDecodeError:
                    print(f"  IntEsq: {intEsq[:200]}...")
            else:
                print(f"  IntEsq: (empty)")

    print("\n" + "=" * 70)
    print("Comparison complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
