#!/usr/bin/env python3
"""Find BGSalesGroup Id(s) by Name via OData.

Usage:
  python3 scripts/testing/find_bgsalesgroup.py "Pampa Bay - Regular"

Or via env:
  export CREATIO_SALES_GROUP_NAME="Pampa Bay - Regular"
  python3 scripts/testing/find_bgsalesgroup.py

Reads credentials from .env if present.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.parse import quote

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv

load_dotenv()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")


def main() -> None:
    name = None
    if len(sys.argv) > 1:
        name = " ".join(sys.argv[1:]).strip()
    if not name:
        name = os.environ.get("CREATIO_SALES_GROUP_NAME", "").strip()

    if not name:
        raise SystemExit('Provide a sales group name as an argument or set CREATIO_SALES_GROUP_NAME')

    session = requests.Session()
    resp = session.post(
        f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
        json={"UserName": USERNAME, "UserPassword": PASSWORD},
        timeout=30,
    )
    if resp.status_code != 200:
        raise SystemExit(f"Login failed: HTTP {resp.status_code} {resp.text[:200]}")

    bpmcsrf = session.cookies.get("BPMCSRF", "")

    # OData filter for exact Name match.
    # Quote single quotes per OData spec by doubling them.
    odata_name = name.replace("'", "''")
    url = (
        f"{CREATIO_URL}/0/odata/BGSalesGroup"
        f"?$filter=Name%20eq%20'{quote(odata_name)}'"
        f"&$select=Id,Name&$top=10"
    )

    r = session.get(url, headers={"BPMCSRF": bpmcsrf}, timeout=30)
    print(f"HTTP {r.status_code}")
    if r.status_code != 200:
        print(r.text[:500])
        raise SystemExit(1)

    data = r.json()
    rows = data.get("value", [])
    if not rows:
        print("No matches")
        return

    print(f"Matches: {len(rows)}")
    for row in rows:
        print(f"- {row.get('Name')} -> {row.get('Id')}")


if __name__ == "__main__":
    main()
