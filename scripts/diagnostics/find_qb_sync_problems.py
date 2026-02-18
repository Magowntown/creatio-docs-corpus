#!/usr/bin/env python3
"""
Find QB sync problem records in PROD:
1. Orders in Error/Re-Process status
2. Orders without invoice numbers that shouldn't be syncing
3. Old orders causing sync failures
4. Persistent failures from specific logs (Log_27_01_2026, Log_04_02_2026)

Usage:
  source .env
  CREATIO_URL=$CREATIO_PROD_URL CREATIO_USERNAME=$CREATIO_PROD_USERNAME CREATIO_PASSWORD=$CREATIO_PROD_PASSWORD \
    python3 scripts/diagnostics/find_qb_sync_problems.py
"""

import os
import sys
import json
import requests
from datetime import datetime

CREATIO_URL = os.environ.get("CREATIO_URL", "https://pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

# Status GUIDs
STATUS_PENDING    = "c97db3bc-634d-4c90-8432-ec7141c87640"
STATUS_PROCESSED  = "e7428193-4cf1-4d1b-abae-00e93ab5e1c5"
STATUS_ERROR      = "bdfc60c7-55fd-4cbd-9a2c-dca2def46d80"
STATUS_PROCESSING = "fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef"
STATUS_REPROCESS  = "ff92e20c-da27-4255-96bc-57e32f0944f4"

STATUS_NAMES = {
    STATUS_PENDING: "Pending",
    STATUS_PROCESSED: "Processed",
    STATUS_ERROR: "Error",
    STATUS_PROCESSING: "Processing",
    STATUS_REPROCESS: "Re-Process",
}

session = requests.Session()

def login():
    session.get(f"{CREATIO_URL}/0/", allow_redirects=True)
    response = session.post(
        f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
        json={"UserName": USERNAME, "UserPassword": PASSWORD}
    )
    if response.status_code != 200 or response.json().get("Code") != 0:
        print(f"Login failed: {response.text[:200]}")
        sys.exit(1)

    session.get(f"{CREATIO_URL}/0/odata/", allow_redirects=True)
    bpmcsrf = session.cookies.get("BPMCSRF", "")
    if not bpmcsrf:
        for cookie in session.cookies:
            if "CSRF" in cookie.name.upper():
                bpmcsrf = cookie.value
                break

    session.headers.update({
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json;odata=verbose",
        "Accept": "application/json"
    })
    print(f"✓ Logged in to {CREATIO_URL}\n")


def odata_query(entity, select=None, filter=None, top=None, orderby=None, count=False, expand=None):
    url = f"{CREATIO_URL}/0/odata/{entity}"
    params = {}
    if select:
        params["$select"] = select
    if filter:
        params["$filter"] = filter
    if top:
        params["$top"] = str(top)
    if orderby:
        params["$orderby"] = orderby
    if count:
        params["$count"] = "true"
    if expand:
        params["$expand"] = expand

    response = session.get(url, params=params)
    if response.status_code != 200:
        print(f"  Query error ({entity}): {response.status_code} - {response.text[:300]}")
        return None
    return response.json()


def find_integration_logs():
    """Find all QB Integration Log parents."""
    print("=" * 80)
    print("1. QB INTEGRATION LOGS (Parent Records)")
    print("=" * 80)

    result = odata_query(
        "BGQuickBooksIntegrationLog",
        select="Id,BGName,CreatedOn,ModifiedOn",
        orderby="CreatedOn desc",
        top=20
    )

    logs = []
    if result and result.get("value"):
        print(f"{'Name':<30} {'Created':<20} {'Id'}")
        print("-" * 90)
        for rec in result["value"]:
            name = rec.get("BGName", "N/A")
            created = rec.get("CreatedOn", "")[:16].replace("T", " ")
            log_id = rec.get("Id", "")
            print(f"{name:<30} {created:<20} {log_id}")
            logs.append(rec)
    else:
        print("  No integration logs found")

    return logs


def find_error_records():
    """Find all log detail records in Error or Re-Process status."""
    print("\n" + "=" * 80)
    print("2. ERROR / RE-PROCESS RECORDS")
    print("=" * 80)

    error_records = []

    for status_id, status_name in [(STATUS_ERROR, "Error"), (STATUS_REPROCESS, "Re-Process")]:
        result = odata_query(
            "BGQuickBooksIntegrationLogDetail",
            select="Id,BGName,BGRecordId,BGStatusId,BGErrorMessage,CreatedOn,ModifiedOn,BGQuickBooksIntegrationLogId",
            filter=f"BGStatusId eq {status_id}",
            orderby="ModifiedOn desc",
            top=100,
            count=True
        )

        count = result.get("@odata.count", 0) if result else 0
        print(f"\n  {status_name}: {count} records")

        if result and result.get("value"):
            for rec in result["value"]:
                error_records.append({
                    "detail_id": rec.get("Id", ""),
                    "name": rec.get("BGName", "N/A"),
                    "record_id": rec.get("BGRecordId", ""),
                    "status": status_name,
                    "error": rec.get("BGErrorMessage", "")[:200],
                    "created": rec.get("CreatedOn", "")[:16],
                    "modified": rec.get("ModifiedOn", "")[:16],
                    "log_id": rec.get("BGQuickBooksIntegrationLogId", ""),
                })

    return error_records


def enrich_with_order_data(error_records):
    """For each error record, look up the associated Order."""
    print("\n" + "=" * 80)
    print("3. ENRICHING WITH ORDER DATA")
    print("=" * 80)

    enriched = []
    for i, rec in enumerate(error_records):
        record_id = rec["record_id"]
        if not record_id:
            rec["order_number"] = "NO_RECORD_ID"
            rec["invoice_number"] = ""
            rec["order_date"] = ""
            rec["has_invoice"] = False
            enriched.append(rec)
            continue

        order = odata_query(
            "Order",
            select="Id,Number,BGNumberInvoice,BGInvoiceNumber,BGInvoiceDate,CreatedOn,BGQuickBooksId",
            filter=f"Id eq {record_id}",
            top=1
        )

        if order and order.get("value"):
            o = order["value"][0]
            rec["order_number"] = o.get("Number", "N/A")
            rec["invoice_number"] = o.get("BGNumberInvoice", "") or o.get("BGInvoiceNumber", "") or ""
            inv_date = o.get("BGInvoiceDate", "")
            rec["order_date"] = o.get("CreatedOn", "")[:10]
            rec["invoice_date"] = inv_date[:10] if inv_date else ""
            rec["has_invoice"] = bool(rec["invoice_number"])
            rec["has_qb_id"] = bool(o.get("BGQuickBooksId", ""))
        else:
            rec["order_number"] = "ORDER_NOT_FOUND"
            rec["invoice_number"] = ""
            rec["order_date"] = ""
            rec["invoice_date"] = ""
            rec["has_invoice"] = False
            rec["has_qb_id"] = False

        enriched.append(rec)

        if (i + 1) % 10 == 0:
            print(f"  Processed {i + 1}/{len(error_records)} records...")

    print(f"  Done. Enriched {len(enriched)} records.")
    return enriched


def find_pending_without_invoice():
    """Find Pending/Re-Process records where the Order has no invoice number."""
    print("\n" + "=" * 80)
    print("4. PENDING/RE-PROCESS RECORDS WITH NO INVOICE NUMBER")
    print("=" * 80)

    # First get Pending records
    result = odata_query(
        "BGQuickBooksIntegrationLogDetail",
        select="Id,BGName,BGRecordId,BGStatusId",
        filter=f"BGStatusId eq {STATUS_PENDING} or BGStatusId eq {STATUS_REPROCESS}",
        top=200,
        count=True
    )

    count = result.get("@odata.count", 0) if result else 0
    print(f"  Total Pending/Re-Process records: {count}")

    no_invoice = []
    if result and result.get("value"):
        for rec in result["value"]:
            record_id = rec.get("BGRecordId", "")
            if not record_id:
                continue

            order = odata_query(
                "Order",
                select="Id,Number,BGNumberInvoice,BGInvoiceNumber,CreatedOn",
                filter=f"Id eq {record_id}",
                top=1
            )

            if order and order.get("value"):
                o = order["value"][0]
                inv = o.get("BGNumberInvoice", "") or o.get("BGInvoiceNumber", "") or ""
                if not inv:
                    no_invoice.append({
                        "detail_id": rec.get("Id", ""),
                        "order_number": o.get("Number", "N/A"),
                        "order_date": o.get("CreatedOn", "")[:10],
                        "status": STATUS_NAMES.get(rec.get("BGStatusId", ""), "Unknown"),
                    })

    print(f"  Records with NO invoice number: {len(no_invoice)}")
    if no_invoice:
        print(f"\n  {'Order#':<15} {'Created':<12} {'Status':<12} {'Detail ID'}")
        print("  " + "-" * 75)
        for r in no_invoice:
            print(f"  {r['order_number']:<15} {r['order_date']:<12} {r['status']:<12} {r['detail_id']}")

    return no_invoice


def display_results(enriched):
    """Display categorized results."""
    print("\n" + "=" * 80)
    print("5. CATEGORIZED PROBLEM RECORDS")
    print("=" * 80)

    # Category 1: No invoice number
    no_inv = [r for r in enriched if not r.get("has_invoice")]
    print(f"\n  A) Orders WITHOUT invoice number ({len(no_inv)} records) → SHOULD NOT SYNC")
    if no_inv:
        print(f"  {'Order#':<15} {'Created':<12} {'Status':<8} {'Error (truncated)'}")
        print("  " + "-" * 80)
        for r in no_inv:
            err = r.get("error", "")[:50]
            print(f"  {r.get('order_number','?'):<15} {r.get('order_date','?'):<12} {r['status']:<8} {err}")

    # Category 2: Old orders (before 2025)
    old = [r for r in enriched if r.get("has_invoice") and r.get("order_date", "9999") < "2025-01-01"]
    print(f"\n  B) OLD orders (before 2025) with errors ({len(old)} records)")
    if old:
        print(f"  {'Order#':<15} {'Invoice#':<12} {'Created':<12} {'Error (truncated)'}")
        print("  " + "-" * 80)
        for r in old:
            err = r.get("error", "")[:50]
            print(f"  {r.get('order_number','?'):<15} {r.get('invoice_number','?'):<12} {r.get('order_date','?'):<12} {err}")

    # Category 3: Recent orders with connection errors
    conn_err = [r for r in enriched
                if r.get("has_invoice")
                and r.get("order_date", "") >= "2025-01-01"
                and ("connect" in r.get("error", "").lower() or "timeout" in r.get("error", "").lower())]
    print(f"\n  C) Recent orders with CONNECTION errors ({len(conn_err)} records) → RETRY CANDIDATES")
    if conn_err:
        print(f"  {'Order#':<15} {'Invoice#':<12} {'Created':<12}")
        print("  " + "-" * 80)
        for r in conn_err:
            print(f"  {r.get('order_number','?'):<15} {r.get('invoice_number','?'):<12} {r.get('order_date','?'):<12}")

    # Category 4: Recent orders with other errors
    other = [r for r in enriched
             if r.get("has_invoice")
             and r.get("order_date", "") >= "2025-01-01"
             and r not in conn_err]
    print(f"\n  D) Recent orders with OTHER errors ({len(other)} records)")
    if other:
        print(f"  {'Order#':<15} {'Invoice#':<12} {'Created':<12} {'Error (truncated)'}")
        print("  " + "-" * 80)
        for r in other:
            err = r.get("error", "")[:60]
            print(f"  {r.get('order_number','?'):<15} {r.get('invoice_number','?'):<12} {r.get('order_date','?'):<12} {err}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    to_exclude = no_inv + old
    print(f"\n  Records to EXCLUDE (mark as Processed): {len(to_exclude)}")
    print(f"    - No invoice number: {len(no_inv)}")
    print(f"    - Old orders (pre-2025): {len(old)}")
    print(f"  Connection errors (retry candidates): {len(conn_err)}")
    print(f"  Other errors (investigate): {len(other)}")

    # Output the detail IDs for exclusion
    exclude_ids = [r["detail_id"] for r in to_exclude if r.get("detail_id")]
    if exclude_ids:
        print(f"\n  Detail IDs to mark as Processed:")
        for did in exclude_ids:
            print(f"    {did}")

    return {
        "no_invoice": no_inv,
        "old_orders": old,
        "connection_errors": conn_err,
        "other_errors": other,
        "exclude_ids": exclude_ids,
    }


def check_status_counts():
    """Quick count of all statuses."""
    print("\n" + "=" * 80)
    print("6. OVERALL STATUS COUNTS")
    print("=" * 80)

    for status_id, status_name in STATUS_NAMES.items():
        result = odata_query(
            "BGQuickBooksIntegrationLogDetail",
            select="Id",
            filter=f"BGStatusId eq {status_id}",
            top=1,
            count=True
        )
        count = result.get("@odata.count", 0) if result else 0
        print(f"  {status_name:<12}: {count:>6,}")


def main():
    print("=" * 80)
    print("QB SYNC PROBLEM FINDER")
    print(f"Environment: {CREATIO_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    if not USERNAME or not PASSWORD:
        print("\n❌ Set CREATIO_USERNAME and CREATIO_PASSWORD")
        print("   source .env")
        print("   CREATIO_URL=$CREATIO_PROD_URL CREATIO_USERNAME=$CREATIO_PROD_USERNAME \\")
        print("   CREATIO_PASSWORD=$CREATIO_PROD_PASSWORD python3 scripts/diagnostics/find_qb_sync_problems.py")
        sys.exit(1)

    login()

    # Step 1: Find log parents
    logs = find_integration_logs()

    # Step 2: Find error records
    error_records = find_error_records()

    # Step 3: Enrich with order data
    if error_records:
        enriched = enrich_with_order_data(error_records)
    else:
        enriched = []

    # Step 4: Find pending records without invoices
    no_inv_pending = find_pending_without_invoice()

    # Step 5: Display categorized results
    if enriched:
        results = display_results(enriched)
    else:
        results = {"exclude_ids": []}
        print("\n  No error records found!")

    # Step 6: Overall counts
    check_status_counts()

    # Save results to JSON for the fix script
    output = {
        "timestamp": datetime.now().isoformat(),
        "environment": CREATIO_URL,
        "error_records": enriched,
        "pending_no_invoice": no_inv_pending,
        "exclude_ids": results.get("exclude_ids", []),
        "pending_no_invoice_ids": [r["detail_id"] for r in no_inv_pending],
    }

    output_path = "scripts/diagnostics/qb_sync_problems.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  Results saved to: {output_path}")

    print("\n" + "=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    all_exclude = results.get("exclude_ids", []) + [r["detail_id"] for r in no_inv_pending]
    print(f"\n  Total records to exclude: {len(all_exclude)}")
    print(f"  Run: python3 scripts/diagnostics/fix_qb_sync_problems.py")
    print(f"  This will mark excluded records as 'Processed' to stop retries.")


if __name__ == "__main__":
    main()
