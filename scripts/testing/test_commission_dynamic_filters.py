#!/usr/bin/env python3
"""Test Commission report dynamic filtering across multiple Year-Month + Sales Group combinations.

What this does
- Logs into Creatio
- Resolves Commission IntExcelReport
- Loads candidate BGYearMonth + BGSalesGroup lists
- Attempts to find N combinations that produce non-empty output
- For each successful combination:
  - Calls POST /0/rest/UsrExcelReportService/Generate (YearMonthId + SalesRepId)
  - Downloads via GET /0/rest/IntExcelReportService/GetReport/{key}/Commission
  - Saves the workbook under test-artifacts/dynamic-filters/<env>/
  - Inspects the Data sheet to ensure:
      - 'Year-Month' column has only the selected YYYY-MM
      - 'Sales Group' column has only the selected sales group name
  - Detects whether macros exist (xl/vbaProject.bin)

Why
- DL-001 proved one combo works, but we need confidence filters apply dynamically across real data.

Usage
  python3 scripts/testing/test_commission_dynamic_filters.py --env dev --count 3

Credentials
- Reads .env blocks:
  - # DEV: uncommented CREATIO_* lines
  - # PROD: commented '# CREATIO_*=' lines under the PROD header

Safety
- Never prints passwords.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
import xml.etree.ElementTree as ET

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / ".env"

EMPTY_GUID = "00000000-0000-0000-0000-000000000000"


def _parse_env_with_commented_blocks(path: Path) -> Dict[str, Dict[str, str]]:
    """Parse .env and return {"dev": {...}, "prod": {...}}.

    Supported formats:

    Format A (split blocks; PROD commented):
      # DEV
      CREATIO_URL=...
      CREATIO_USERNAME=...
      CREATIO_PASSWORD=...

      # PROD
      # CREATIO_URL=...
      # CREATIO_USERNAME=...
      # CREATIO_PASSWORD=...

    Format B (split blocks; PROD uncommented):
      # DEV
      CREATIO_URL=...
      ...

      # PROD
      CREATIO_URL=...
      ...

    This script never prints secrets.
    """

    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    blocks: Dict[str, Dict[str, str]] = {"dev": {}, "prod": {}}
    current: Optional[str] = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith("#"):
            header = stripped.lstrip("#").strip().lower()
            if header == "dev":
                current = "dev"
                continue
            if header == "prod":
                current = "prod"
                continue

        if current is None:
            continue

        if current == "dev" and not stripped.startswith("#"):
            if "=" in stripped:
                k, v = stripped.split("=", 1)
                blocks["dev"][k.strip()] = v.strip().strip('"').strip("'")
            continue

        if current == "prod":
            # Accept either commented or uncommented key/value lines inside the PROD block.
            s = stripped
            if s.startswith("#"):
                s = s.lstrip("#").strip()
            if "=" in s:
                k, v = s.split("=", 1)
                blocks["prod"][k.strip()] = v.strip().strip('"').strip("'")

    return blocks


class Creatio:
    def __init__(self, base_url: str, username: str, password: str, timeout_s: int = 180):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.timeout_s = timeout_s
        self.session = requests.Session()

    def login(self) -> None:
        resp = self.session.post(
            f"{self.base_url}/ServiceModel/AuthService.svc/Login",
            json={"UserName": self.username, "UserPassword": self.password},
            timeout=30,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"Login failed: HTTP {resp.status_code} {resp.text[:200]}")

    def headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "BPMCSRF": self.session.cookies.get("BPMCSRF", ""),
        }

    def select_query(self, body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/0/DataService/json/SyncReply/SelectQuery"
        resp = self.session.post(url, json=body, headers=self.headers(), timeout=self.timeout_s)
        if resp.status_code != 200:
            raise RuntimeError(f"SelectQuery failed: HTTP {resp.status_code} {resp.text[:300]}")
        data = resp.json()
        # Creatio sometimes returns 500-style JSON with success=false in a 200 response.
        if isinstance(data, dict) and data.get("success") is False and data.get("responseStatus"):
            rs = data.get("responseStatus") or {}
            raise RuntimeError(f"SelectQuery error: {rs.get('ErrorCode')} {rs.get('Message')}")
        return data

    def generate(self, report_id: str, year_month_id: str, sales_group_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/0/rest/UsrExcelReportService/Generate"
        body = {
            "ReportId": report_id,
            "YearMonthId": year_month_id,
            # legacy field name
            "SalesRepId": sales_group_id,
            "ExecutionId": EMPTY_GUID,
            "RecordCollection": [],
        }
        resp = self.session.post(url, json=body, headers=self.headers(), timeout=max(self.timeout_s, 300))
        if resp.status_code != 200:
            raise RuntimeError(f"Generate failed: HTTP {resp.status_code} {resp.text[:300]}")
        return resp.json()

    def download_commission(self, key: str) -> Tuple[bytes, Dict[str, str]]:
        url = f"{self.base_url}/0/rest/IntExcelReportService/GetReport/{key}/Commission"
        resp = self.session.get(url, headers=self.headers(), timeout=max(self.timeout_s, 300))
        if resp.status_code != 200:
            raise RuntimeError(f"GetReport failed: HTTP {resp.status_code} {resp.text[:200]}")
        content = resp.content
        if content[:2] != b"PK":
            raise RuntimeError(f"GetReport did not return xlsx (signature={content[:8]!r})")
        return content, dict(resp.headers)


@dataclass
class Combo:
    year_month_id: str
    year_month_name: str
    sales_group_id: str
    sales_group_name: str


def _sanitize_filename(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._ -]+", "_", s)
    s = s.strip().replace(" ", "_")
    return s[:120] if len(s) > 120 else s


def _resolve_int_excel_report_id(creatio: Creatio, int_name: str) -> str:
    body = {
        "rootSchemaName": "IntExcelReport",
        "operationType": 0,
        "columns": {
            "items": {
                "Id": {"expression": {"columnPath": "Id"}},
                "IntName": {"expression": {"columnPath": "IntName"}},
            }
        },
        "filters": {
            "filterType": 6,
            "items": {
                "IntNameFilter": {
                    "filterType": 1,
                    "comparisonType": 3,
                    "leftExpression": {"expressionType": 0, "columnPath": "IntName"},
                    "rightExpression": {"expressionType": 2, "parameter": {"dataValueType": 1, "value": int_name}},
                }
            },
        },
        "rowCount": 1,
    }
    data = creatio.select_query(body)
    rows = data.get("rows") or []
    if not rows:
        raise RuntimeError(f"IntExcelReport not found for IntName={int_name!r}")
    return rows[0].get("Id") or ""


def _load_year_months(creatio: Creatio, limit: int = 60) -> List[Tuple[str, str]]:
    body = {
        "rootSchemaName": "BGYearMonth",
        "operationType": 0,
        "columns": {
            "items": {
                "Id": {"expression": {"columnPath": "Id"}},
                "Name": {"expression": {"columnPath": "Name"}},
            }
        },
        "rowCount": 500,
    }
    data = creatio.select_query(body)
    rows = data.get("rows") or []
    out: List[Tuple[str, str]] = []
    for r in rows:
        ym_id = r.get("Id")
        name = r.get("Name")
        if isinstance(ym_id, str) and isinstance(name, str) and re.fullmatch(r"\d{4}-\d{2}", name.strip()):
            out.append((ym_id, name.strip()))
    # newest first by YYYY-MM lexical sort
    out.sort(key=lambda t: t[1], reverse=True)
    return out[:limit]


def _load_sales_groups(creatio: Creatio, limit: int = 60) -> List[Tuple[str, str]]:
    # In this DEV instance, the display/name column is BGSalesGroupName (not Name).
    body = {
        "rootSchemaName": "BGSalesGroup",
        "operationType": 0,
        "columns": {
            "items": {
                "Id": {"expression": {"columnPath": "Id"}},
                "BGSalesGroupName": {"expression": {"columnPath": "BGSalesGroupName"}},
            }
        },
        "rowCount": 500,
    }
    data = creatio.select_query(body)
    rows = data.get("rows") or []
    out: List[Tuple[str, str]] = []
    for r in rows:
        sg_id = r.get("Id")
        name = r.get("BGSalesGroupName")
        if isinstance(sg_id, str) and isinstance(name, str) and name.strip():
            out.append((sg_id, name.strip()))

    def score(n: str) -> Tuple[int, str]:
        # Prefer Pampa Bay groups first, otherwise alphabetical.
        return (0 if "pampa bay" in n.lower() else 1, n.lower())

    out.sort(key=lambda t: score(t[1]))
    return out[:limit]


def _xlsx_has_macros(xlsx_bytes: bytes) -> bool:
    with zipfile.ZipFile(io_bytes(xlsx_bytes), "r") as z:
        return any(n.lower().endswith("xl/vbaproject.bin") for n in z.namelist())


def io_bytes(b: bytes):
    # small helper to avoid importing io at module import (keeps script startup minimal)
    import io

    return io.BytesIO(b)


def _excel_serial_to_datetime(v: str) -> Optional[datetime]:
    """Convert an Excel date serial (days since 1899-12-30) into a datetime.

    The Commission export stores dates as numeric serials in many files.
    """

    try:
        n = float(v)
    except Exception:
        return None

    # Excel epoch (Windows 1900 date system): 1899-12-30
    # This is the commonly used correction in Python.
    base = datetime(1899, 12, 30)
    return base + timedelta(days=n)


def _value_to_datetime(v: Any) -> Optional[datetime]:
    if v in (None, ""):
        return None

    # Unwrap common Creatio lookup/date object shapes.
    if isinstance(v, dict) and "value" in v:
        v = v.get("value")
        if v in (None, ""):
            return None

    s = str(v).strip()

    # Try ISO-like strings first
    try:
        # 2025-10-05 or 2025-10-05T00:00:00
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        pass

    # Try common US format
    for fmt in ("%m/%d/%Y", "%m/%d/%Y %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass

    # Finally, Excel serial
    return _excel_serial_to_datetime(s)


def _xlsx_extract_unique_values(
    xlsx_bytes: bytes,
    *,
    target_sheet: str = "Data",
    year_month_expected: Optional[str] = None,
    sales_group_expected: Optional[str] = None,
    scan_rows_limit: int = 500,
    allow_derived_yearmonth: bool = False,
) -> Dict[str, Any]:
    """Parse xlsx and validate Sales Group + Year-Month.

    Load-bearing rule for Gate D:
    - Prefer validating against the explicit "Year-Month" column when present.
    - If the Year-Month column is missing or empty, you generally cannot prove
      Year‑Month filtering worked (deriving from dates can be wrong, especially
      for credit memo/refund semantics).

    If allow_derived_yearmonth=True, we will fall back to deriving YYYY-MM from
    "Transaction Date" (preferred) or "Invoice Date". This is intended for
    legacy/diagnostic use only.

    Returns a dict with:
      - ok (bool)
      - reason (optional)
      - header_row
      - detected columns
      - unique values found (samples)
      - nonempty_data_rows (approx within scan limit)
      - derived_year_month_source
    """

    with zipfile.ZipFile(io_bytes(xlsx_bytes), "r") as z:
        names = set(z.namelist())
        if "xl/workbook.xml" not in names:
            return {"ok": False, "reason": "missing xl/workbook.xml"}

        ns = dict(m="http://schemas.openxmlformats.org/spreadsheetml/2006/main")
        rel_ns = dict(r="http://schemas.openxmlformats.org/package/2006/relationships")

        wb_root = ET.fromstring(z.read("xl/workbook.xml"))
        sheets: List[Dict[str, str]] = []
        for sh in wb_root.findall("m:sheets/m:sheet", ns):
            sheets.append(
                {
                    "name": sh.attrib.get("name") or "",
                    "rId": sh.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id") or "",
                }
            )

        rels_root = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rid_to_target: Dict[str, str] = {}
        for rel in rels_root.findall("r:Relationship", rel_ns):
            rid_to_target[rel.attrib.get("Id") or ""] = rel.attrib.get("Target") or ""

        shared_strings: List[str] = []
        if "xl/sharedStrings.xml" in names:
            ss_root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in ss_root.findall("m:si", ns):
                texts = [t.text or "" for t in si.findall(".//m:t", ns)]
                shared_strings.append("".join(texts))

        def cell_value(cell_el: ET.Element) -> Optional[str]:
            t = cell_el.attrib.get("t")
            v_el = cell_el.find("m:v", ns)
            if v_el is None:
                is_el = cell_el.find("m:is", ns)
                if is_el is not None:
                    texts = [t.text or "" for t in is_el.findall(".//m:t", ns)]
                    return "".join(texts)
                return None
            v = v_el.text
            if v is None:
                return None
            if t == "s":
                try:
                    idx = int(v)
                    return shared_strings[idx] if 0 <= idx < len(shared_strings) else v
                except Exception:
                    return v
            return v

        def col_letters(ref: str) -> str:
            return "".join(ch for ch in ref if ch.isalpha())

        def col_index(letters: str) -> int:
            n = 0
            for ch in letters:
                n = n * 26 + (ord(ch.upper()) - 64)
            return n

        def find_sheet(name_pref: str) -> Optional[str]:
            for s in sheets:
                if s["name"] == name_pref:
                    return s["name"]
            return sheets[0]["name"] if sheets else None

        sheet_name = find_sheet(target_sheet)
        if not sheet_name:
            return {"ok": False, "reason": "no sheets"}

        sheet = next((s for s in sheets if s["name"] == sheet_name), None)
        if not sheet:
            return {"ok": False, "reason": f"sheet {sheet_name} not found"}
        target = rid_to_target.get(sheet["rId"], "")
        if not target:
            return {"ok": False, "reason": "missing worksheet target"}

        sheet_path = "xl/" + target.lstrip("/")
        if sheet_path not in names:
            return {"ok": False, "reason": f"missing {sheet_path}"}

        sh_root = ET.fromstring(z.read(sheet_path))
        # Row 1 = header
        rows = sh_root.findall(".//m:sheetData/m:row", ns)
        if not rows:
            return {"ok": False, "reason": "empty sheet"}

        # Find first row with >=3 non-empty cells (header)
        header_row_el: Optional[ET.Element] = None
        header_row_num: Optional[int] = None
        for row_el in rows:
            r = int(row_el.attrib.get("r", "0") or "0")
            cells = row_el.findall("m:c", ns)
            non_empty = 0
            for c in cells:
                v = cell_value(c)
                if v not in (None, ""):
                    non_empty += 1
            if non_empty >= 3:
                header_row_el = row_el
                header_row_num = r
                break

        if header_row_el is None or header_row_num is None:
            return {"ok": False, "reason": "no header row detected"}

        header_cells: List[Tuple[str, str]] = []
        for c in header_row_el.findall("m:c", ns):
            ref = c.attrib.get("r") or ""
            v = cell_value(c)
            if ref and v not in (None, ""):
                header_cells.append((col_letters(ref), str(v).strip()))

        header_cells.sort(key=lambda kv: col_index(kv[0]))

        def find_header_col(substrs: Iterable[str]) -> Optional[Tuple[str, str]]:
            for col, name in header_cells:
                n = name.lower()
                if any(s in n for s in substrs):
                    return col, name
            return None

        ym_col = find_header_col(["year-month", "year month", "year", "month"])
        sg_col = find_header_col(["sales group", "salesgroup"])
        tx_col = find_header_col(["transaction date", "transaction"])
        inv_col = find_header_col(["invoice date", "invoice"])

        if not ym_col or not sg_col:
            return {
                "ok": False,
                "reason": "missing expected headers",
                "detected_headers": header_cells[:40],
                "year_month_col": ym_col,
                "sales_group_col": sg_col,
                "transaction_date_col": tx_col,
                "invoice_date_col": inv_col,
            }

        ym_vals: set[str] = set()
        sg_vals: set[str] = set()
        tx_yearmonths: set[str] = set()
        inv_yearmonths: set[str] = set()
        nonempty_rows = 0

        def row_has_data(row_el: ET.Element) -> bool:
            for c in row_el.findall("m:c", ns):
                v = cell_value(c)
                if v not in (None, ""):
                    return True
            return False

        def find_value_in_row(row_el: ET.Element, col_letter: str) -> Optional[str]:
            for c in row_el.findall("m:c", ns):
                ref = c.attrib.get("r") or ""
                if ref and col_letters(ref) == col_letter:
                    v = cell_value(c)
                    return None if v in (None, "") else str(v).strip()
            return None

        scanned = 0
        for row_el in rows:
            r = int(row_el.attrib.get("r", "0") or "0")
            if r <= header_row_num:
                continue
            if scanned >= scan_rows_limit:
                break
            scanned += 1

            if row_has_data(row_el):
                nonempty_rows += 1

            ym_v = find_value_in_row(row_el, ym_col[0])
            sg_v = find_value_in_row(row_el, sg_col[0])
            tx_v = find_value_in_row(row_el, tx_col[0]) if tx_col else None
            inv_v = find_value_in_row(row_el, inv_col[0]) if inv_col else None

            if ym_v:
                ym_vals.add(ym_v)
            if sg_v:
                sg_vals.add(sg_v)

            tx_dt = _value_to_datetime(tx_v) if tx_v else None
            if tx_dt:
                tx_yearmonths.add(tx_dt.strftime("%Y-%m"))

            inv_dt = _value_to_datetime(inv_v) if inv_v else None
            if inv_dt:
                inv_yearmonths.add(inv_dt.strftime("%Y-%m"))

        # Sales Group must be a single value.
        sg_ok = (len(sg_vals) == 1)
        if sales_group_expected is not None and sg_vals:
            sg_ok = sg_ok and (next(iter(sg_vals)) == sales_group_expected)

        # Prefer explicit Year-Month column.
        year_month_source = "year-month-col"
        effective_yearmonths: set[str] = set(ym_vals)

        if not effective_yearmonths:
            if allow_derived_yearmonth:
                if tx_yearmonths:
                    effective_yearmonths = set(tx_yearmonths)
                    year_month_source = "transaction-date-derived"
                elif inv_yearmonths:
                    effective_yearmonths = set(inv_yearmonths)
                    year_month_source = "invoice-date-derived"
                else:
                    year_month_source = "unavailable"
            else:
                year_month_source = "missing-year-month-values"

        ym_ok = (len(effective_yearmonths) == 1)
        if year_month_expected is not None:
            if not effective_yearmonths:
                ym_ok = False
            else:
                ym_ok = ym_ok and (next(iter(effective_yearmonths)) == year_month_expected)

        ok = bool(ym_ok and sg_ok and nonempty_rows > 0)
        reason = None
        if not ok:
            if nonempty_rows <= 0:
                reason = "no-data-rows"
            elif not sg_ok:
                reason = "sales-group-mismatch"
            elif year_month_source == "missing-year-month-values":
                reason = "missing-year-month-values"
            elif not ym_ok:
                reason = "year-month-mismatch"

        return {
            "ok": ok,
            "reason": reason,
            "sheet": sheet_name,
            "header_row": header_row_num,
            "year_month_col": ym_col,
            "sales_group_col": sg_col,
            "transaction_date_col": tx_col,
            "invoice_date_col": inv_col,
            "unique_year_month_values": sorted(list(ym_vals))[:20],
            "unique_sales_group_values": sorted(list(sg_vals))[:20],
            "derived_year_month_values": sorted(list(effective_yearmonths))[:20],
            "derived_year_month_source": year_month_source,
            "unique_transaction_yearmonths": sorted(list(tx_yearmonths))[:20],
            "unique_invoice_yearmonths": sorted(list(inv_yearmonths))[:20],
            "nonempty_data_rows_scanned": nonempty_rows,
            "scanned_rows": scanned,
        }


def _lookup_to_id_name(v: Any, *, name_fallback: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """Normalize Creatio lookup cell formats.

    DataService responses sometimes return lookups as:
      - {"value": "<guid>", "displayValue": "<name>"}
    or as plain strings.
    """

    if isinstance(v, dict):
        vid = v.get("value")
        d = v.get("displayValue")
        return (vid if isinstance(vid, str) else None, d if isinstance(d, str) else name_fallback)
    if isinstance(v, str) and v.strip():
        return (None, v.strip())
    return (None, name_fallback)


def _discover_combos_from_commission_rows(
    creatio: Creatio,
    *,
    year_month_name_to_id: Dict[str, str],
    row_limit: int = 5000,
    max_candidates: int = 200,
) -> List[Combo]:
    """Discover likely-good (YearMonth, SalesGroup) combos from commission-backed rows."""

    body = {
        "rootSchemaName": "BGCommissionReportDataView",
        "operationType": 0,
        "columns": {
            "items": {
                "BGYearMonthName": {"expression": {"columnPath": "BGYearMonth.Name"}},
                "BGTransactionDate": {"expression": {"columnPath": "BGTransactionDate"}},
                "BGInvoiceDate": {"expression": {"columnPath": "BGOrder.BGInvoiceDate"}},
                "SalesGroupLookup": {"expression": {"columnPath": "BGSalesRep.BGSalesGroupLookup"}},
                "SalesGroupName": {"expression": {"columnPath": "BGSalesRep.BGSalesGroupLookup.BGSalesGroupName"}},
            }
        },
        "rowCount": row_limit,
    }

    data = creatio.select_query(body)
    rows = data.get("rows") or []

    counts: Dict[Tuple[str, str], int] = {}
    id_name: Dict[Tuple[str, str], Tuple[str, str]] = {}

    for r in rows:
        ym_name = r.get("BGYearMonthName")
        # Current backend filter contract is a lookup filter on BGYearMonth.
        # For dynamic validation we only consider rows where BGYearMonth is populated.
        if not (isinstance(ym_name, str) and re.fullmatch(r"\d{4}-\d{2}", ym_name.strip())):
            continue

        ym_name = ym_name.strip()
        ym_id = year_month_name_to_id.get(ym_name)
        if not ym_id:
            continue

        sg_id, sg_name = _lookup_to_id_name(r.get("SalesGroupLookup"), name_fallback=r.get("SalesGroupName"))
        if not sg_id or not isinstance(sg_id, str):
            continue
        if not sg_name:
            sg_name = "(unknown)"

        key = (ym_id, sg_id)
        counts[key] = counts.get(key, 0) + 1
        id_name[key] = (ym_name, sg_name)

    ranked = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    combos: List[Combo] = []
    for (ym_id, sg_id), _cnt in ranked[:max_candidates]:
        ym_name, sg_name = id_name[(ym_id, sg_id)]
        combos.append(
            Combo(
                year_month_id=ym_id,
                year_month_name=ym_name,
                sales_group_id=sg_id,
                sales_group_name=sg_name,
            )
        )

    return combos


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", choices=["dev", "prod"], required=True)
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument(
        "--strategy",
        choices=["commission-backed", "bruteforce"],
        default="commission-backed",
        help="How to choose candidate combos: commission-backed is faster and more reliable.",
    )
    ap.add_argument("--int-name", default="Rpt Commission", help="IntExcelReport.IntName to resolve")
    ap.add_argument("--max-months", type=int, default=24)
    ap.add_argument("--max-groups", type=int, default=30)
    ap.add_argument("--commission-row-limit", type=int, default=5000)
    ap.add_argument("--timeout-seconds", type=int, default=180)
    ap.add_argument("--sleep-between", type=float, default=0.5)
    ap.add_argument(
        "--allow-derived-yearmonth",
        action="store_true",
        help=(
            "If the Excel 'Year-Month' column is empty, allow deriving YYYY-MM from dates. "
            "Not recommended for PROD semantics; intended for diagnostic use only."
        ),
    )
    args = ap.parse_args()

    blocks = _parse_env_with_commented_blocks(ENV_PATH)
    cfg = blocks.get(args.env) or {}

    base_url = (cfg.get("CREATIO_URL") or "").rstrip("/")
    username = cfg.get("CREATIO_USERNAME") or ""
    password = cfg.get("CREATIO_PASSWORD") or ""
    if not base_url or not username or not password:
        raise RuntimeError(f"Missing CREATIO_URL/CREATIO_USERNAME/CREATIO_PASSWORD for env={args.env}")

    out_dir = REPO_ROOT / "test-artifacts" / "dynamic-filters" / args.env
    out_dir.mkdir(parents=True, exist_ok=True)

    creatio = Creatio(base_url, username, password, timeout_s=args.timeout_seconds)
    creatio.login()

    report_id = _resolve_int_excel_report_id(creatio, args.int_name)

    year_months = _load_year_months(creatio, limit=max(args.max_months, 5))
    sales_groups = _load_sales_groups(creatio, limit=max(args.max_groups, 5))

    year_month_name_to_id = {name: ym_id for ym_id, name in year_months}

    candidate_combos: List[Combo]
    if args.strategy == "commission-backed":
        candidate_combos = _discover_combos_from_commission_rows(
            creatio,
            year_month_name_to_id=year_month_name_to_id,
            row_limit=args.commission_row_limit,
        )
        # If discovery fails for any reason, fall back to brute force.
        if not candidate_combos:
            candidate_combos = [
                Combo(year_month_id=ym_id, year_month_name=ym_name, sales_group_id=sg_id, sales_group_name=sg_name)
                for (ym_id, ym_name) in year_months
                for (sg_id, sg_name) in sales_groups
            ]
    else:
        candidate_combos = [
            Combo(year_month_id=ym_id, year_month_name=ym_name, sales_group_id=sg_id, sales_group_name=sg_name)
            for (ym_id, ym_name) in year_months
            for (sg_id, sg_name) in sales_groups
        ]

    results: List[Dict[str, Any]] = []
    successes: List[Dict[str, Any]] = []

    attempts = 0
    for combo in candidate_combos:
        if len(successes) >= args.count:
            break

        attempts += 1
        started = time.time()
        try:
            gen = creatio.generate(report_id, combo.year_month_id, combo.sales_group_id)
            key = gen.get("key")
            if not (gen.get("success") and isinstance(key, str) and key):
                raise RuntimeError(f"Generate returned success={gen.get('success')} message={gen.get('message')}")

            content, hdrs = creatio.download_commission(key)

            inspection = _xlsx_extract_unique_values(
                content,
                year_month_expected=combo.year_month_name,
                sales_group_expected=combo.sales_group_name,
                allow_derived_yearmonth=bool(args.allow_derived_yearmonth),
            )

            has_macros = False
            try:
                has_macros = any(n.lower().endswith("xl/vbaproject.bin") for n in zipfile.ZipFile(io_bytes(content)).namelist())
            except Exception:
                has_macros = False

            elapsed = round(time.time() - started, 2)

            safe_name = _sanitize_filename(combo.sales_group_name)
            filename = out_dir / f"Commission_{combo.year_month_name}_{safe_name}_{key[-8:]}.xlsx"
            filename.write_bytes(content)

            ok = bool(inspection.get("ok"))
            reason = (inspection.get("reason") if isinstance(inspection, dict) else None) or None
            status = "pass" if ok else ("inconclusive" if reason == "missing-year-month-values" else "fail")

            row = {
                "status": status,
                "ok": ok,
                "year_month": combo.year_month_name,
                "year_month_id": combo.year_month_id,
                "sales_group": combo.sales_group_name,
                "sales_group_id": combo.sales_group_id,
                "key": key,
                "file": str(filename),
                "file_size": filename.stat().st_size,
                "has_vbaProject_bin": bool(has_macros),
                "content_disposition": hdrs.get("Content-Disposition") or hdrs.get("content-disposition"),
                "inspection": inspection,
                "elapsed_s": elapsed,
            }
            results.append(row)

            if status == "pass":
                successes.append(row)
        except Exception as e:
            elapsed = round(time.time() - started, 2)
            results.append(
                {
                    "status": "fail",
                    "ok": False,
                    "year_month": combo.year_month_name,
                    "year_month_id": combo.year_month_id,
                    "sales_group": combo.sales_group_name,
                    "sales_group_id": combo.sales_group_id,
                    "error": str(e)[:600],
                    "elapsed_s": elapsed,
                }
            )
        finally:
            if args.sleep_between:
                time.sleep(args.sleep_between)

    summary = {
        "env": args.env,
        "strategy": args.strategy,
        "int_name": args.int_name,
        "year_month_validation": "allow-derived" if args.allow_derived_yearmonth else "strict",
        "ts": time.time(),
        "target": base_url,
        "requested_successes": args.count,
        "successes": successes,
        "attempts": attempts,
        "results": results,
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    by_status = {"pass": 0, "fail": 0, "inconclusive": 0}
    for r in results:
        st = r.get("status")
        if st in by_status:
            by_status[st] += 1

    # Print concise console output
    print(
        f"Found {len(successes)}/{args.count} passing combinations in {attempts} attempt(s) (strategy={args.strategy}; ym_validation={'allow-derived' if args.allow_derived_yearmonth else 'strict'})"
    )
    print(f"Attempt outcomes: pass={by_status['pass']} fail={by_status['fail']} inconclusive={by_status['inconclusive']}")
    for i, s in enumerate(successes, start=1):
        insp = s.get("inspection") or {}
        src = insp.get("derived_year_month_source")
        print(
            f"{i}. {s['year_month']} | {s['sales_group']} | rows(scanned)={insp.get('nonempty_data_rows_scanned')} | ym_src={src} | size={s['file_size']} | macros={s['has_vbaProject_bin']}"
        )

    return 0 if len(successes) >= args.count else 2


if __name__ == "__main__":
    raise SystemExit(main())
