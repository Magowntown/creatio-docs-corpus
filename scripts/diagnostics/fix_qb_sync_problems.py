#!/usr/bin/env python3
"""
Fix QB sync problem records by marking them as Processed.

Targets:
1. Error records where Order has NO invoice number (should never sync)
2. Error records where Order is very old (pre-2024)
3. Error records where Order ALREADY has BGQuickBooksId (ghost errors - already synced)

Does NOT touch:
- Recent errors with invoices and no QB ID (legitimate retry candidates)
- Re-Process records (need manual decision)

Usage:
  source .env
  CREATIO_URL=$CREATIO_PROD_URL CREATIO_USERNAME=$CREATIO_PROD_USERNAME CREATIO_PASSWORD=$CREATIO_PROD_PASSWORD \
    python3 scripts/diagnostics/fix_qb_sync_problems.py [--dry-run]
"""

import os
import sys
import json
import requests
from datetime import datetime

CREATIO_URL = os.environ.get("CREATIO_URL", "https://pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")

STATUS_PROCESSED = "e7428193-4cf1-4d1b-abae-00e93ab5e1c5"
STATUS_ERROR = "bdfc60c7-55fd-4cbd-9a2c-dca2def46d80"

DRY_RUN = "--dry-run" in sys.argv

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
    print(f"✓ Logged in to {CREATIO_URL}")
    if DRY_RUN:
        print("⚠️  DRY RUN MODE - no changes will be made")


def get_error_records():
    """Get all error records."""
    all_errors = []
    for skip in range(0, 700, 200):
        r = session.get(f"{CREATIO_URL}/0/odata/BGQuickBooksIntegrationLogDetail", params={
            "$select": "Id,BGName,BGRecordId",
            "$filter": f"BGStatus/Id eq {STATUS_ERROR}",
            "$skip": str(skip),
            "$top": "200",
            "$count": "true"
        })
        if r.status_code == 200:
            batch = r.json().get("value", [])
            all_errors.extend(batch)
            total = r.json().get("@odata.count", "?")
            if not batch:
                break
        else:
            print(f"  Query failed at skip={skip}: {r.status_code}")
            break

    print(f"\n  Total Error records: {total} (retrieved {len(all_errors)})")
    return all_errors


def categorize_record(rec):
    """Check Order data and categorize the record."""
    record_id = rec.get("BGRecordId", "")
    if not record_id:
        return "no_invoice", "No BGRecordId"

    o = session.get(f"{CREATIO_URL}/0/odata/Order", params={
        "$select": "Id,Number,BGNumberInvoice,BGInvoiceNumber,CreatedOn,BGQuickBooksId",
        "$filter": f"Id eq {record_id}",
        "$top": "1"
    })

    if o.status_code != 200 or not o.json().get("value"):
        return "no_invoice", "Order not found in DB"

    order = o.json()["value"][0]
    inv = order.get("BGNumberInvoice", "") or order.get("BGInvoiceNumber", "") or ""
    created = order.get("CreatedOn", "")[:10]
    has_qb = bool(order.get("BGQuickBooksId", ""))
    order_num = order.get("Number", "?")

    if not inv:
        return "no_invoice", f"{order_num} has no invoice number"
    if created < "2024-01-01":
        return "old_order", f"{order_num} created {created}"
    if has_qb:
        return "already_synced", f"{order_num} invoice={inv} already has BGQuickBooksId"

    return "keep", f"{order_num} invoice={inv} - legitimate retry candidate"


def mark_as_processed(detail_id, reason):
    """Mark a log detail record as Processed."""
    if DRY_RUN:
        print(f"  [DRY RUN] Would mark {detail_id} as Processed: {reason}")
        return True

    url = f"{CREATIO_URL}/0/odata/BGQuickBooksIntegrationLogDetail({detail_id})"
    payload = {
        "BGStatusId": STATUS_PROCESSED,
    }
    r = session.patch(url, json=payload)
    if r.status_code in [200, 204]:
        return True
    else:
        print(f"  ✗ Failed to update {detail_id}: {r.status_code} - {r.text[:200]}")
        return False


def main():
    print("=" * 80)
    print("QB SYNC PROBLEM FIXER")
    print(f"Environment: {CREATIO_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    if not USERNAME or not PASSWORD:
        print("\n❌ Set credentials. See script header for usage.")
        sys.exit(1)

    login()

    # Get all error records
    error_records = get_error_records()

    # Categorize each record
    categories = {"no_invoice": [], "old_order": [], "already_synced": [], "keep": []}
    print("\n  Categorizing records...")

    for i, rec in enumerate(error_records):
        cat, reason = categorize_record(rec)
        categories[cat].append({"id": rec["Id"], "name": rec["BGName"], "reason": reason})

        if (i + 1) % 50 == 0:
            print(f"    Processed {i + 1}/{len(error_records)}...")

    print(f"\n  Categorization complete:")
    print(f"    No invoice:      {len(categories['no_invoice'])}")
    print(f"    Old orders:      {len(categories['old_order'])}")
    print(f"    Already synced:  {len(categories['already_synced'])}")
    print(f"    Keep (retry):    {len(categories['keep'])}")

    # Mark records as Processed
    to_fix = categories["no_invoice"] + categories["old_order"] + categories["already_synced"]
    print(f"\n{'=' * 80}")
    print(f"MARKING {len(to_fix)} RECORDS AS PROCESSED")
    print(f"{'=' * 80}")

    success = 0
    failed = 0
    for rec in to_fix:
        print(f"  → {rec['name']:<55} ({rec['reason'][:40]})")
        if mark_as_processed(rec["id"], rec["reason"]):
            success += 1
        else:
            failed += 1

    print(f"\n{'=' * 80}")
    print(f"RESULTS")
    print(f"{'=' * 80}")
    print(f"  Successfully updated: {success}")
    print(f"  Failed:               {failed}")
    print(f"  Kept for retry:       {len(categories['keep'])}")

    # Log results
    log = {
        "timestamp": datetime.now().isoformat(),
        "environment": CREATIO_URL,
        "dry_run": DRY_RUN,
        "fixed": [{"id": r["id"], "name": r["name"], "reason": r["reason"]} for r in to_fix],
        "kept": [{"id": r["id"], "name": r["name"]} for r in categories["keep"]],
        "success_count": success,
        "failed_count": failed,
    }
    log_path = "scripts/diagnostics/qb_fix_results.json"
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2, default=str)
    print(f"\n  Results saved to: {log_path}")

    # Verify final counts
    print(f"\n  Verifying final status counts...")
    for status_id, status_name in [
        ("c97db3bc-634d-4c90-8432-ec7141c87640", "Pending"),
        ("e7428193-4cf1-4d1b-abae-00e93ab5e1c5", "Processed"),
        ("bdfc60c7-55fd-4cbd-9a2c-dca2def46d80", "Error"),
        ("ff92e20c-da27-4255-96bc-57e32f0944f4", "Re-Process"),
    ]:
        r = session.get(f"{CREATIO_URL}/0/odata/BGQuickBooksIntegrationLogDetail", params={
            "$select": "Id",
            "$filter": f"BGStatus/Id eq {status_id}",
            "$top": "1",
            "$count": "true"
        })
        count = r.json().get("@odata.count", "?") if r.status_code == 200 else "error"
        print(f"    {status_name:<12}: {count}")


if __name__ == "__main__":
    main()
