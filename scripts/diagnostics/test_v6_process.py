#!/usr/bin/env python3
"""
Post-deployment verification for IWOrderandPaymentsSync.
Tests that the process exists, is published, signals are registered,
and commission calculations produce correct results.

Usage:
    source .env && python3 scripts/diagnostics/test_v6_process.py
    source .env && python3 scripts/diagnostics/test_v6_process.py --check-only
    source .env && python3 scripts/diagnostics/test_v6_process.py --verify-order ORDER_ID
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()

CREATIO_URL = os.getenv("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.getenv("CREATIO_USERNAME", "Supervisor")
PASSWORD = os.getenv("CREATIO_PASSWORD", "")

session = requests.Session()

# ─── Commission Status GUIDs ───
STATUS_PENDING = "930bb1c6-ca67-4ac0-8f96-a5ea4018a366"
STATUS_DONE = "deb80242-b56a-4b94-967a-0e170e2198d8"
STATUS_RETURNED = "ee14b2ce-163a-4fb2-abea-e739636794ed"
STATUS_ERROR = "26c1b9de-75c9-46c7-8963-e02b8a63f261"
STATUS_ORDER_DELETED = "8c2313f4-7e27-4781-afef-d16deb90cc6d"

STATUS_NAMES = {
    STATUS_PENDING: "Pending",
    STATUS_DONE: "Done",
    STATUS_RETURNED: "Returned",
    STATUS_ERROR: "Error",
    STATUS_ORDER_DELETED: "Order Deleted",
}

# ─── Transaction Type GUIDs ───
TRANS_SALE = "b4494f26-26c2-4aa6-951c-658d0828d0d0"
TRANS_CREDIT_MEMO = "c26d3478-7ac1-49e9-97f9-1c0809552f1f"

V6_PROCESS_NAME = "IWOrderandPaymentsSync"


def login():
    session.get(f"{CREATIO_URL}/0/", allow_redirects=True)
    resp = session.post(
        f"{CREATIO_URL}/ServiceModel/AuthService.svc/Login",
        json={"UserName": USERNAME, "UserPassword": PASSWORD},
    )
    if resp.status_code != 200 or resp.json().get("Code") != 0:
        print(f"Login failed: {resp.text}")
        sys.exit(1)
    session.get(f"{CREATIO_URL}/0/odata/", allow_redirects=True)
    bpmcsrf = session.cookies.get("BPMCSRF", "")
    if not bpmcsrf:
        for c in session.cookies:
            if "CSRF" in c.name.upper():
                bpmcsrf = c.value
                break
    session.headers.update({
        "BPMCSRF": bpmcsrf,
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    print(f"Logged in to {CREATIO_URL}")


def odata_get(entity, params=None):
    url = f"{CREATIO_URL}/0/odata/{entity}"
    resp = session.get(url, params=params or {})
    if resp.status_code != 200:
        return None, f"HTTP {resp.status_code}: {resp.text[:300]}"
    return resp.json().get("value", []), None


# ═══════════════════════════════════════════════
# CHECK 1: Process Exists and Is Published
# ═══════════════════════════════════════════════
def check_process_exists():
    print(f"\n{'='*60}")
    print("CHECK 1: Process Exists and Is Published")
    print(f"{'='*60}")

    records, err = odata_get("VwSysProcess", {
        "$filter": f"contains(Name,'{V6_PROCESS_NAME}')",
        "$select": "Id,Name,IsActiveVersion,Enabled,NeedUpdateSourceCode,NeedUpdateStructure",
        "$top": "5",
    })
    if err:
        print(f"  ❌ Query failed: {err}")
        return False

    if not records:
        # Try broader search
        records, err = odata_get("VwSysProcess", {
            "$filter": "contains(Name,'CommissionCalculator')",
            "$select": "Id,Name,IsActiveVersion,Enabled",
            "$top": "10",
        })
        if records:
            print(f"  ❌ '{V6_PROCESS_NAME}' not found. Similar processes:")
            for r in records:
                print(f"     - {r.get('Name')} (Active={r.get('IsActiveVersion')}, Enabled={r.get('Enabled')})")
        else:
            print(f"  ❌ No commission calculator processes found")
        return False

    for r in records:
        name = r.get("Name", "")
        active = r.get("IsActiveVersion", False)
        enabled = r.get("Enabled", False)
        need_src = r.get("NeedUpdateSourceCode", None)
        need_struct = r.get("NeedUpdateStructure", None)

        print(f"  Process: {name}")
        print(f"    IsActiveVersion: {active} {'✅' if active else '❌'}")
        print(f"    Enabled: {enabled} {'✅' if enabled else '❌'}")
        if need_src is not None:
            print(f"    NeedUpdateSourceCode: {need_src} {'⚠️ NEEDS PUBLISH' if need_src else '✅'}")
        if need_struct is not None:
            print(f"    NeedUpdateStructure: {need_struct} {'⚠️ NEEDS PUBLISH' if need_struct else '✅'}")

        if active and enabled:
            if need_src or need_struct:
                print(f"  ⚠️  Process exists but needs re-Publishing!")
                return False
            print(f"  ✅ Process is active and published")
            return True

    print(f"  ❌ Process found but not Active/Enabled")
    return False


# ═══════════════════════════════════════════════
# CHECK 2: Old Processes Disabled
# ═══════════════════════════════════════════════
def check_old_processes_disabled():
    print(f"\n{'='*60}")
    print("CHECK 2: Old Processes Disabled")
    print(f"{'='*60}")

    old_processes = [
        "IWCalculateCommissiononPaymentV4",
        "IWCalculateCommissiononPaymentV5",
        "IWFillCommissionReportPaymentsFieldsV2",
        "IWRecalculateCommissionOnOrderChangeV2",
    ]

    all_ok = True
    for proc_name in old_processes:
        records, err = odata_get("VwSysProcess", {
            "$filter": f"Name eq '{proc_name}'",
            "$select": "Id,Name,IsActiveVersion,Enabled",
            "$top": "1",
        })
        if err:
            print(f"  ⚠️  Could not query {proc_name}: {err}")
            continue

        if not records:
            print(f"  ✅ {proc_name}: Not found (OK)")
            continue

        r = records[0]
        active = r.get("IsActiveVersion", False)
        if active:
            print(f"  ❌ {proc_name}: Still ACTIVE — must disable")
            all_ok = False
        else:
            print(f"  ✅ {proc_name}: Not active version")

    return all_ok


# ═══════════════════════════════════════════════
# CHECK 3: Process Log (Recent Executions)
# ═══════════════════════════════════════════════
def check_process_log():
    print(f"\n{'='*60}")
    print("CHECK 3: Recent V6 Process Executions")
    print(f"{'='*60}")

    # Check last 24 hours
    since = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")

    records, err = odata_get("SysProcessLog", {
        "$filter": f"contains(Name,'{V6_PROCESS_NAME}') and StartDate gt {since}",
        "$select": "Id,Name,StartDate,CompleteDate,Status,ErrorDescription",
        "$orderby": "StartDate desc",
        "$top": "20",
    })
    if err:
        print(f"  ⚠️  Could not query process log: {err}")
        return None

    if not records:
        print(f"  ℹ️  No V6 executions in last 24 hours")
        print(f"     This is expected if V6 was just published or no triggers have fired")
        return None

    completed = 0
    errored = 0
    running = 0

    for r in records:
        status = r.get("Status", "")
        start = r.get("StartDate", "")
        end = r.get("CompleteDate", "")
        error = r.get("ErrorDescription", "")

        if "Error" in str(status) or error:
            errored += 1
            icon = "❌"
        elif end:
            completed += 1
            icon = "✅"
        else:
            running += 1
            icon = "🔄"

        print(f"  {icon} Start: {start[:19]}  End: {str(end)[:19] if end else 'running'}  Status: {status}")
        if error:
            print(f"     Error: {error[:200]}")

    print(f"\n  Summary: {completed} completed, {errored} errors, {running} running (of {len(records)} total)")

    if errored > 0:
        print(f"  ⚠️  {errored} executions had errors — check Process Log in Creatio")

    return {"completed": completed, "errored": errored, "running": running}


# ═══════════════════════════════════════════════
# CHECK 4: IWPayments Commission Results
# ═══════════════════════════════════════════════
def check_payment_results(order_id=None):
    print(f"\n{'='*60}")
    if order_id:
        print(f"CHECK 4: Payment Commission Results for Order {order_id}")
    else:
        print("CHECK 4: Recent Payment Commission Results")
    print(f"{'='*60}")

    select_cols = (
        "Id,IWAmount,IWCommissionAmount,IWSalesAmount,"
        "IWCommissionCalculated,IWIsReturn,"
        "IWCommissionStatusId,IWPaymentsInvoiceId,"
        "IWBGSalesRepId,IWSalesGroupId,IWBGYearMonthId,"
        "IWBGTransactionTypeId,IWDescription,IWOwnerId"
    )

    if order_id:
        filter_str = f"IWPaymentsInvoiceId eq {order_id}"
    else:
        # Get recent payments with Done or Returned status
        filter_str = (
            f"(IWCommissionStatusId eq {STATUS_DONE}"
            f" or IWCommissionStatusId eq {STATUS_RETURNED})"
        )

    records, err = odata_get("IWPayments", {
        "$filter": filter_str,
        "$select": select_cols,
        "$top": "10",
        "$orderby": "CreatedOn desc" if not order_id else None,
    })
    if err:
        print(f"  ❌ Query failed: {err}")
        return False

    if not records:
        print(f"  ℹ️  No matching payment records found")
        if order_id:
            print(f"     No payments linked to order {order_id}")
        else:
            print(f"     No payments with Done/Returned status yet")
        return None

    all_valid = True
    for i, r in enumerate(records):
        payment_id = r.get("Id", "?")
        amount = r.get("IWAmount", 0)
        commission = r.get("IWCommissionAmount", 0)
        sales_amount = r.get("IWSalesAmount", 0)
        calculated = r.get("IWCommissionCalculated", False)
        is_return = r.get("IWIsReturn", False)
        status_id = r.get("IWCommissionStatusId", "")
        order_fk = r.get("IWPaymentsInvoiceId", "")
        sales_rep = r.get("IWBGSalesRepId", "")
        sales_group = r.get("IWSalesGroupId", "")
        year_month = r.get("IWBGYearMonthId", "")
        trans_type = r.get("IWBGTransactionTypeId", "")
        description = r.get("IWDescription", "")
        owner = r.get("IWOwnerId", "")

        status_name = STATUS_NAMES.get(str(status_id).lower(), status_id)
        print(f"\n  Payment #{i+1}: {payment_id[:8]}...")
        print(f"    Amount:      {amount}")
        print(f"    SalesAmount: {sales_amount}")
        print(f"    Commission:  {commission}")
        print(f"    Calculated:  {calculated}")
        print(f"    IsReturn:    {is_return}")
        print(f"    Status:      {status_name}")
        print(f"    OrderId:     {order_fk}")

        # Validation checks
        issues = []

        if status_name in ("Done", "Returned"):
            if not calculated:
                issues.append("IWCommissionCalculated should be true for Done/Returned")

            if sales_amount == 0 and amount != 0:
                issues.append("SalesAmount is 0 but Amount is not — calculation may have failed")

            if commission == 0:
                issues.append("CommissionAmount is 0 — check commission rate")

            if not sales_rep:
                issues.append("IWBGSalesRepId is empty — SalesRep not copied from Order")

            if not sales_group:
                issues.append("IWSalesGroupId is empty — SalesGroup not copied from Order")

            if not year_month:
                issues.append("IWBGYearMonthId is empty — YearMonth lookup failed")

            if not trans_type:
                issues.append("IWBGTransactionTypeId is empty — TransactionType not set")

            if status_name == "Done" and is_return:
                issues.append("Status is Done but IsReturn is True — inconsistent")

            if status_name == "Returned" and not is_return:
                issues.append("Status is Returned but IsReturn is False — inconsistent")

            expected_trans = TRANS_CREDIT_MEMO if is_return else TRANS_SALE
            if str(trans_type).lower() != expected_trans.lower() and trans_type:
                issues.append(f"TransactionType mismatch: expected {'Credit Memo' if is_return else 'Sale'}")

        if issues:
            all_valid = False
            for issue in issues:
                print(f"    ⚠️  {issue}")
        else:
            print(f"    ✅ All fields populated correctly")

    return all_valid


# ═══════════════════════════════════════════════
# CHECK 5: ChangeData Null Column Test
# ═══════════════════════════════════════════════
def check_changedata_null_issue():
    print(f"\n{'='*60}")
    print("CHECK 5: ChangeData Null Column Detection")
    print(f"{'='*60}")
    print("  Checking for payments where status was set but other fields are null...")
    print("  (This detects the known ChangeData bug where columns write as null)")

    # Look for Done/Returned payments where key fields are empty
    records, err = odata_get("IWPayments", {
        "$filter": (
            f"(IWCommissionStatusId eq {STATUS_DONE}"
            f" or IWCommissionStatusId eq {STATUS_RETURNED})"
            " and IWCommissionAmount eq 0"
        ),
        "$select": "Id,IWAmount,IWCommissionAmount,IWSalesAmount,IWCommissionCalculated,IWCommissionStatusId",
        "$top": "5",
    })
    if err:
        print(f"  ⚠️  Could not query: {err}")
        return None

    if not records:
        print(f"  ✅ No Done/Returned payments with zero commission found")
        print(f"     ChangeData appears to be working correctly")
        return True

    print(f"  ⚠️  Found {len(records)} Done/Returned payments with CommissionAmount=0")
    print(f"     This MAY indicate the ChangeData null bug")
    print(f"     Check if these orders have commission earners configured:")
    for r in records:
        print(f"     - Payment {r.get('Id', '?')[:8]}... Amount={r.get('IWAmount', 0)}")

    return False


# ═══════════════════════════════════════════════
# CHECK 6: Signal Registration
# ═══════════════════════════════════════════════
def check_signal_registration():
    print(f"\n{'='*60}")
    print("CHECK 6: Signal Registration")
    print(f"{'='*60}")

    expected_entities = ["IWPayments", "Order", "OrderProduct"]

    # Check SysProcessElementData for signal elements
    records, err = odata_get("VwSysProcess", {
        "$filter": f"contains(Name,'{V6_PROCESS_NAME}')",
        "$select": "Id,Name",
        "$top": "1",
    })

    if err or not records:
        print(f"  ⚠️  Could not find process to check signals")
        return None

    process_id = records[0].get("Id")
    print(f"  Process ID: {process_id}")
    print(f"  Expected signals for entities: {', '.join(expected_entities)}")
    print(f"  ℹ️  Signal registration cannot be fully verified via OData")
    print(f"     To verify: Open Process Designer → check each Signal element has green checkmark")
    print(f"     If signals don't fire: Re-Publish the process (Publish button, NOT Compile All)")

    return None


# ═══════════════════════════════════════════════
# CHECK 7: Verify Specific Order
# ═══════════════════════════════════════════════
def verify_order(order_id):
    print(f"\n{'='*60}")
    print(f"VERIFY ORDER: {order_id}")
    print(f"{'='*60}")

    # Read the order
    records, err = odata_get("Order", {
        "$filter": f"Id eq {order_id}",
        "$select": "Id,Number,Amount,BGTaxAmount,BGSubTotal,BGShippingCharge,BGSalesRepLookupId,BGSalesGroupId,OwnerId,BGOrderDescription",
        "$top": "1",
    })
    if err:
        print(f"  ❌ Could not read order: {err}")
        return False

    if not records:
        print(f"  ❌ Order not found: {order_id}")
        return False

    order = records[0]
    print(f"  Order: {order.get('Number', '?')}")
    print(f"    Amount:       {order.get('Amount', 0)}")
    print(f"    Tax:          {order.get('BGTaxAmount', 0)}")
    print(f"    SubTotal:     {order.get('BGSubTotal', 0)}")
    print(f"    Shipping:     {order.get('BGShippingCharge', 0)}")
    print(f"    SalesRep:     {order.get('BGSalesRepLookupId', 'NONE')}")
    print(f"    SalesGroup:   {order.get('BGSalesGroupId', 'NONE')}")
    print(f"    Owner:        {order.get('OwnerId', 'NONE')}")

    # Check commission earner
    earners, err = odata_get("BGCommissionEarner", {
        "$filter": f"BGOrderId eq {order_id}",
        "$select": "Id,BGCommissionRate,BGOrderId",
        "$top": "5",
    })
    if err:
        print(f"  ⚠️  Could not query commission earners: {err}")
    elif not earners:
        print(f"  ⚠️  No BGCommissionEarner record for this order!")
        print(f"     V6 will set status to Error for payments on this order")
    else:
        for e in earners:
            rate = e.get("BGCommissionRate", 0)
            print(f"    CommissionRate: {rate}%")

    # Check payments
    print(f"\n  Payments for this order:")
    check_payment_results(order_id)

    # Calculate expected values
    amount = order.get("Amount", 0) or 0
    tax = order.get("BGTaxAmount", 0) or 0

    if amount > 0 and earners:
        rate = earners[0].get("BGCommissionRate", 0) or 0
        print(f"\n  Expected calculation (for a hypothetical full-amount payment):")
        print(f"    PaymentAmount = {amount} (full order)")
        print(f"    SalesAmount = {amount} - ({tax} * {amount} / {amount}) = {amount - tax}")
        print(f"    Commission = {amount - tax} * ({rate} / 100) = {(amount - tax) * rate / 100:.2f}")

    return True


# ═══════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Test IWOrderandPaymentsSync")
    parser.add_argument("--check-only", action="store_true",
                        help="Only check process exists and is published (no data checks)")
    parser.add_argument("--verify-order", type=str,
                        help="Verify commission calculation for a specific Order GUID")
    parser.add_argument("--skip-old", action="store_true",
                        help="Skip check for old processes being disabled")
    args = parser.parse_args()

    login()

    results = {}

    # Always run: process exists check
    results["process_exists"] = check_process_exists()

    if args.check_only:
        print(f"\n{'='*60}")
        print("RESULT: Check-only mode")
        print(f"{'='*60}")
        print(f"  Process exists and published: {'✅' if results['process_exists'] else '❌'}")
        return

    # Check old processes
    if not args.skip_old:
        results["old_disabled"] = check_old_processes_disabled()

    # Check signals
    check_signal_registration()

    # Check process log
    results["log"] = check_process_log()

    if args.verify_order:
        verify_order(args.verify_order)
    else:
        # General payment results check
        results["payments"] = check_payment_results()

        # ChangeData null detection
        results["changedata"] = check_changedata_null_issue()

    # ═══════════════════════════════════════════════
    # FINAL SUMMARY
    # ═══════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")

    if results.get("process_exists"):
        print("  ✅ V6 process exists and is published")
    else:
        print("  ❌ V6 process NOT found or not published")
        print("     → Open Process Designer → Create/Publish IWOrderandPaymentsSync")
        print(f"     → See: docs/investigation/V6_PROCESS_BUILDER_GUIDE.md")

    if results.get("old_disabled") is False:
        print("  ⚠️  Old processes still active — disable after V6 is verified")

    log = results.get("log")
    if log and log["errored"] > 0:
        print(f"  ⚠️  {log['errored']} process errors in last 24h — check Process Log")

    if results.get("changedata") is False:
        print("  ⚠️  Possible ChangeData null bug detected — may need Script Task fallback")

    if results.get("payments") is False:
        print("  ⚠️  Some payment records have validation issues")

    print(f"\n  Test commands:")
    print(f"    Verify specific order:  python3 {__file__} --verify-order <ORDER_GUID>")
    print(f"    Quick check:            python3 {__file__} --check-only")


if __name__ == "__main__":
    main()
