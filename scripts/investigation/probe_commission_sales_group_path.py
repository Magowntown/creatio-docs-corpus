#!/usr/bin/env python3
"""Probe Commission Sales Group columnPath via DataService notFoundColumns checks.

Goal
- Determine the correct ESQ filter columnPath to use for *Sales Group* filtering on the
  Commission report (root schema: BGCommissionReportDataView).

Why
- In DEV, BGCommissionReportDataView does not expose BGYearMonthId/BGSalesRepId.
  It exposes lookups like BGYearMonth and BGSalesRep. For Sales Group, we likely need
  a relationship path off BGSalesRep (e.g., BGSalesRep.<SalesGroupLookupColumn>). This
  script attempts to discover that path conclusively.

How it works
- Uses /0/DataService/json/SyncReply/SelectQuery.
- Requests candidate columnPaths and reads response.notFoundColumns.

Usage
  export CREATIO_URL="https://dev-pampabay.creatio.com"
  export CREATIO_USERNAME="..."
  export CREATIO_PASSWORD="..."

  python3 scripts/investigation/probe_commission_sales_group_path.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import getpass
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests

# Ensure repo root is on sys.path so we can import scripts.* when executed directly.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._env import load_dotenv


# Load local .env if present (gitignored). This lets you run without exporting vars each time.
load_dotenv()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
CREATIO_USERNAME = os.environ.get("CREATIO_USERNAME", "")
CREATIO_PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# DataService calls against large views can be slow in DEV. Make timeout configurable.
CREATIO_TIMEOUT_SECONDS = int(os.environ.get("CREATIO_TIMEOUT_SECONDS", "180"))
CREATIO_RETRIES = int(os.environ.get("CREATIO_RETRIES", "3"))
# For "existence" probing we don't need actual rows. Some environments may still execute,
# but rowCount=0 can reduce load if supported.
CREATIO_PROBE_ROWCOUNT = int(os.environ.get("CREATIO_PROBE_ROWCOUNT", "0"))

SELECT_QUERY_URL = f"{CREATIO_URL}/0/DataService/json/SyncReply/SelectQuery"
LOGIN_URL = f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login"


_GUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def _extract_guid(value: Any) -> Optional[str]:
    """Best-effort extract a GUID string from a Creatio response value."""
    if isinstance(value, str) and _GUID_RE.match(value):
        return value
    if isinstance(value, dict):
        # Common Creatio shapes include {"value": "<guid>", "displayValue": "..."}
        for k in ("value", "Value", "id", "Id"):
            v = value.get(k)
            if isinstance(v, str) and _GUID_RE.match(v):
                return v
    return None


@dataclass
class ProbeResult:
    root_schema: str
    requested: List[str]
    found: List[str]
    not_found: List[str]
    sample_row: Optional[Dict[str, Any]]


class Creatio:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self) -> None:
        if not self.username or not self.password:
            # If running interactively, prompt instead of forcing env vars.
            if sys.stdin.isatty():
                if not self.username:
                    self.username = input("Creatio username (CREATIO_USERNAME): ").strip()
                if not self.password:
                    self.password = getpass.getpass("Creatio password (CREATIO_PASSWORD): ")
            else:
                raise SystemExit("Set CREATIO_USERNAME and CREATIO_PASSWORD in your environment")

        resp = self.session.post(
            LOGIN_URL,
            json={"UserName": self.username, "UserPassword": self.password},
            timeout=30,
        )
        if resp.status_code != 200:
            raise SystemExit(f"Login failed: HTTP {resp.status_code} {resp.text[:200]}")

    def headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "BPMCSRF": self.session.cookies.get("BPMCSRF", ""),
        }

    def select_query(
        self,
        root_schema: str,
        column_paths: List[str],
        *,
        row_count: int = 1,
        filters: Optional[Dict[str, Any]] = None,
        timeout_seconds: int = CREATIO_TIMEOUT_SECONDS,
        retries: int = CREATIO_RETRIES,
    ) -> Dict[str, Any]:
        items: Dict[str, Any] = {}
        for i, p in enumerate(column_paths):
            items[f"C{i}"] = {"expression": {"columnPath": p}}

        body: Dict[str, Any] = {
            "rootSchemaName": root_schema,
            "operationType": 0,
            "columns": {"items": items},
            "rowCount": row_count,
        }
        if filters is not None:
            body["filters"] = filters

        last_err: Optional[Exception] = None
        for attempt in range(1, max(retries, 1) + 1):
            try:
                resp = self.session.post(
                    SELECT_QUERY_URL,
                    json=body,
                    headers=self.headers(),
                    timeout=timeout_seconds,
                )
                if resp.status_code != 200:
                    raise RuntimeError(
                        f"SelectQuery failed: {root_schema} HTTP {resp.status_code} {resp.text[:500]}"
                    )
                return resp.json()
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                last_err = e
                if attempt >= retries:
                    break
                # Simple backoff without importing time in global scope.
                import time

                sleep_s = min(2 ** attempt, 10)
                print(
                    f"WARN: SelectQuery timeout/connection error for {root_schema} (attempt {attempt}/{retries}, timeout={timeout_seconds}s). Retrying in {sleep_s}s...",
                    file=sys.stderr,
                )
                time.sleep(sleep_s)

        raise RuntimeError(
            f"SelectQuery failed after {retries} attempt(s) for {root_schema}. "
            f"Consider increasing CREATIO_TIMEOUT_SECONDS (currently {timeout_seconds}). Last error: {last_err}"
        )


def _alias_index(alias: Any) -> Optional[int]:
    if not isinstance(alias, str):
        return None
    if alias.startswith("C") and alias[1:].isdigit():
        return int(alias[1:])
    return None


def probe_columns(creatio: Creatio, root_schema: str, column_paths: List[str]) -> ProbeResult:
    payload = creatio.select_query(root_schema, column_paths, row_count=CREATIO_PROBE_ROWCOUNT)

    raw_not_found = payload.get("notFoundColumns") or payload.get("NotFoundColumns") or []

    # Creatio may return notFoundColumns either as:
    # - column aliases (e.g. "C0", "C1" ...), OR
    # - column paths.
    # We map aliases back to the requested column paths when possible.
    not_found_paths: List[str] = []
    for item in raw_not_found:
        idx = _alias_index(item)
        if idx is not None and 0 <= idx < len(column_paths):
            not_found_paths.append(column_paths[idx])
        elif isinstance(item, str):
            not_found_paths.append(item)

    not_found_set = set(not_found_paths)
    found = [p for p in column_paths if p not in not_found_set]

    rows = payload.get("rows") or payload.get("Rows") or []
    sample_row = rows[0] if rows else None

    return ProbeResult(
        root_schema=root_schema,
        requested=column_paths,
        found=found,
        not_found=sorted(not_found_set),
        sample_row=sample_row,
    )


def _print_probe(title: str, result: ProbeResult) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("Root schema:", result.root_schema)
    print("Requested:", len(result.requested))
    print("Found:", len(result.found))
    print("Not found:", len(result.not_found))

    if result.not_found:
        print("\nNot found columnPaths:")
        for p in sorted(result.not_found):
            print("  -", p)

    if result.found:
        print("\nFound columnPaths:")
        for p in sorted(result.found):
            print("  +", p)

    if result.sample_row:
        # Show only keys we asked for (mapped by our C{i} aliases), plus Id if present.
        keys = list(result.sample_row.keys())
        preview = {k: result.sample_row[k] for k in keys[: min(len(keys), 25)]}
        print("\nSample row (truncated):")
        print(json.dumps(preview, indent=2)[:2000])


def _candidate_sales_group_cols_for_bgsalesrep() -> List[str]:
    """Most likely Sales Group lookup columns reachable from BGCommissionReportDataView.BGSalesRep."""
    # Keep this list high-signal. If the probe doesn't find a match, extend it.
    return [
        # Most probable
        "BGSalesGroup",
        "BGSalesGroupLookup",
        # Common generic names
        "SalesGroup",
        "SalesGroupLookup",
        # Variants we sometimes see in custom schemas
        "BGSalesGroupRef",
        "SalesGroupRef",
    ]


def _candidate_sales_group_paths_for_commission() -> List[str]:
    """Build relationship-path candidates off BGCommissionReportDataView.BGSalesRep.

    We probe these directly on BGCommissionReportDataView and rely on notFoundColumns
    to tell us which paths are valid.
    """
    tails = _candidate_sales_group_cols_for_bgsalesrep()

    out: List[str] = [
        # In case the view already exposes the sales group directly.
        "BGSalesGroup",
        "BGSalesGroupLookup",
        "SalesGroup",
        "SalesGroupLookup",
    ]

    for tail in tails:
        out.append(f"BGSalesRep.{tail}")
        out.append(f"BGSalesRep.{tail}.Id")
        out.append(f"BGSalesRep.{tail}.Name")

    # Deduplicate while preserving order
    seen = set()
    deduped: List[str] = []
    for p in out:
        if p not in seen:
            seen.add(p)
            deduped.append(p)
    return deduped


def _mk_equals_filter(column_path: str, guid_value: str) -> Dict[str, Any]:
    """Build a simple comparison filter group for DataService SelectQuery."""
    return {
        "filterType": 6,
        "items": {
            "F0": {
                "filterType": 1,
                "comparisonType": 3,
                "leftExpression": {"columnPath": column_path},
                "rightExpression": {"parameter": {"dataValueType": 10, "value": guid_value}},
            }
        },
    }


def main() -> None:
    creatio = Creatio(CREATIO_URL, CREATIO_USERNAME, CREATIO_PASSWORD)
    creatio.login()
    print("Login: OK")

    # 1) Optional baseline sanity: confirm key lookup columns exist on BGCommissionReportDataView
    # This can be slow in some DEV environments; set CREATIO_SKIP_BASELINE=1 to skip.
    if os.environ.get("CREATIO_SKIP_BASELINE", "0") not in ("1", "true", "TRUE", "yes", "YES"):
        baseline_paths = ["BGYearMonth", "BGSalesRep", "BGExecutionId"]
        baseline = probe_columns(creatio, "BGCommissionReportDataView", baseline_paths)
        _print_probe("Baseline columns on BGCommissionReportDataView", baseline)
    else:
        print("Skipping baseline probe (CREATIO_SKIP_BASELINE=1)")

    # 2) Probe Sales Group relationship paths off BGCommissionReportDataView.BGSalesRep
    commission_candidates = _candidate_sales_group_paths_for_commission()
    commission_probe = probe_columns(creatio, "BGCommissionReportDataView", commission_candidates)
    _print_probe("Candidate Sales Group columnPaths on BGCommissionReportDataView", commission_probe)

    if not commission_probe.found:
        print("\nNo Sales Group-like columnPaths were found from the candidate list.")
        print("Extend _candidate_sales_group_cols_for_bgsalesrep() and rerun.")
        raise SystemExit(2)

    # If we can extract an actual SalesGroupId value from the sample row, we can also
    # validate filtering works (optional, but increases confidence).
    extracted_group_ids: List[Tuple[str, str]] = []
    if commission_probe.sample_row:
        for alias, raw in commission_probe.sample_row.items():
            guid = _extract_guid(raw)
            if guid:
                idx = int(alias[1:]) if alias.startswith("C") and alias[1:].isdigit() else None
                if idx is not None and idx < len(commission_candidates):
                    extracted_group_ids.append((commission_candidates[idx], guid))

    # 4) Print a recommended columnPath for filter injection
    # We prefer a *lookup* columnPath (not .Id/.Name) because we will compare it to a GUID.
    preferred = [p for p in commission_probe.found if p.startswith("BGSalesRep.") and not p.endswith((".Id", ".Name"))]

    print("\n" + "=" * 80)
    print("RECOMMENDATION")
    if preferred:
        print("Use this as the Commission Sales Group filter columnPath (first match):")
        print("  ", preferred[0])
        if len(preferred) > 1:
            print("\nOther valid alternatives found:")
            for p in preferred[1:]:
                print("  ", p)
    else:
        print("No relationship lookup columnPath found on BGCommissionReportDataView via BGSalesRep.<col>.")
        print("You may need to extend candidate lists or inspect schema metadata.")

    # 5) Optional: attempt a filtered SelectQuery if we extracted a sample SalesGroupId
    if preferred and extracted_group_ids:
        # Pick a GUID extracted from one of the relationship paths we probed
        src_col, group_id = extracted_group_ids[0]
        candidate_path = preferred[0]
        print("\n" + "=" * 80)
        print("OPTIONAL VALIDATION")
        print(f"Attempting to filter BGCommissionReportDataView by {candidate_path} == {group_id}")
        print(f"(Sample GUID extracted from columnPath: {src_col})")

        try:
            filtered = creatio.select_query(
                "BGCommissionReportDataView",
                ["BGYearMonth", "BGSalesRep", candidate_path],
                row_count=5,
                filters=_mk_equals_filter(candidate_path, group_id),
            )
            rows = filtered.get("rows") or []
            print(f"Filtered SelectQuery returned {len(rows)} rows (rowCount=5).")
            if rows:
                print("First row keys:", list(rows[0].keys())[:30])
        except Exception as e:
            print(f"Filtered validation failed (still useful to know the path exists): {e}")


if __name__ == "__main__":
    main()
