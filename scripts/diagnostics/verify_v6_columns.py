#!/usr/bin/env python3
"""
Verify IWPayments and Order column names for V6 Commission Process.
Queries OData metadata and sample records to confirm exact column names
needed for Script Task code.
"""

import os
import sys
import re
import requests
from dotenv import load_dotenv

load_dotenv()

CREATIO_URL = os.getenv("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.getenv("CREATIO_USERNAME", "Supervisor")
PASSWORD = os.getenv("CREATIO_PASSWORD", "")

session = requests.Session()


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


def get_entity_columns(entity):
    """Get columns from OData $metadata for an entity."""
    url = f"{CREATIO_URL}/0/odata/$metadata"
    resp = session.get(url, headers={"Accept": "application/xml"})
    if resp.status_code != 200:
        print(f"Metadata request failed: {resp.status_code}")
        return []

    # Parse XML to find entity columns
    text = resp.text
    # Find the EntityType block for our entity
    pattern = rf'<EntityType Name="{entity}"[^>]*>(.*?)</EntityType>'
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        print(f"Entity {entity} not found in metadata")
        return []

    block = match.group(1)
    # Extract Property names
    props = re.findall(r'<Property Name="(\w+)"', block)
    # Extract NavigationProperty names
    nav_props = re.findall(r'<NavigationProperty Name="(\w+)"', block)
    return props, nav_props


def get_sample_record(entity, select=None, top=1, filter_str=None):
    """Fetch a sample record to see actual column data."""
    url = f"{CREATIO_URL}/0/odata/{entity}"
    params = {"$top": str(top)}
    if select:
        params["$select"] = ",".join(select)
    if filter_str:
        params["$filter"] = filter_str
    resp = session.get(url, params=params)
    if resp.status_code != 200:
        print(f"  Query error: {resp.status_code} - {resp.text[:300]}")
        return []
    return resp.json().get("value", [])


def check_columns(entity, expected_columns):
    """Check which expected columns exist in an entity."""
    print(f"\n{'='*60}")
    print(f"Checking {entity} entity columns")
    print(f"{'='*60}")

    props, nav_props = get_entity_columns(entity)
    if not props:
        print("  Could not retrieve metadata, trying sample record approach")
        # Fallback: fetch a sample record with all columns
        records = get_sample_record(entity)
        if records:
            all_cols = list(records[0].keys())
            props = [c for c in all_cols if not c.startswith("@")]
            nav_props = []

    all_columns = set(props) | set(nav_props)

    results = {}
    for col_name, alternatives, confidence in expected_columns:
        found = None
        if col_name in all_columns:
            found = col_name
        else:
            for alt in alternatives:
                if alt in all_columns:
                    found = alt
                    break

        status = "FOUND" if found else "MISSING"
        actual = found or "NOT FOUND"
        results[col_name] = {"status": status, "actual": actual, "confidence": confidence}

        icon = "✅" if found else "❌"
        match_note = f" (as '{found}')" if found and found != col_name else ""
        print(f"  {icon} {col_name}{match_note} [{confidence}]")
        if not found:
            # Show similar columns
            similar = [c for c in all_columns if col_name.lower().replace("id", "") in c.lower()]
            if similar:
                print(f"     Similar: {', '.join(sorted(similar)[:5])}")

    return results, props, nav_props


def main():
    login()

    # ===== IWPayments columns =====
    iw_payments_expected = [
        # (expected_name, [alternatives], confidence)
        ("IWCommission", ["IWCommissionAmount"], "HIGH"),
        ("IWSalesAmount", ["IWCalculatedSalesAmount"], "HIGH"),
        ("IWCommissionCalculated", [], "HIGH"),
        ("IWCommissionStatusId", ["IWCommissionStatus"], "CONFIRMED"),
        ("OwnerId", ["Owner"], "CONFIRMED"),
        ("IWIsReturn", [], "HIGH"),
        ("IWDescription", ["Description", "IWPaymentDescription"], "MEDIUM"),
        ("IWSalesGroupId", ["IWSalesGroup"], "HIGH"),
        ("IWSalesRepId", ["IWSalesRep"], "HIGH"),
        ("IWTransTypeId", ["IWTransType"], "HIGH"),
        ("IWYearMonthId", ["IWYearMonth"], "HIGH"),
        ("IWPaymentsInvoiceId", ["IWPaymentsInvoice"], "HIGH"),
        ("IWAmount", [], "HIGH"),
        ("DueDate", [], "HIGH"),
    ]

    iw_results, iw_props, iw_nav = check_columns("IWPayments", iw_payments_expected)

    # Show ALL IW-prefixed columns for reference
    print(f"\n  All IW-prefixed columns in IWPayments:")
    iw_cols = sorted([c for c in (iw_props or []) if c.startswith("IW") or c.startswith("iw")])
    for c in iw_cols:
        print(f"    - {c}")

    # ===== Order columns =====
    order_expected = [
        ("Amount", [], "CONFIRMED"),
        ("TaxAmount", ["IWTaxAmount", "Tax"], "HIGH"),
        ("IWSalesRepId", ["SalesRepId", "IWSalesRep"], "MEDIUM"),
        ("IWSalesGroupId", ["SalesGroupId", "BGSalesGroupId", "IWSalesGroup"], "MEDIUM"),
        ("Description", ["IWDescription"], "MEDIUM"),
        ("OwnerId", ["Owner"], "CONFIRMED"),
        ("SubTotal", ["IWSubTotal"], "HIGH"),
        ("ShippingCharge", ["IWShippingCharge", "BGShippingCharge"], "MEDIUM"),
    ]

    order_results, order_props, order_nav = check_columns("Order", order_expected)

    # Show sales-related columns on Order
    print(f"\n  Sales/Group/Rep columns on Order:")
    sales_cols = sorted([c for c in (order_props or []) if any(
        kw in c.lower() for kw in ["sales", "group", "rep", "commission", "iw"]
    )])
    for c in sales_cols:
        print(f"    - {c}")

    # ===== BGCommissionEarner columns =====
    earner_expected = [
        ("BGOrder", ["BGOrderId"], "HIGH"),
        ("BGCommissionRate", ["CommissionRate", "Rate"], "HIGH"),
        ("Id", [], "CONFIRMED"),
    ]

    earner_results, earner_props, earner_nav = check_columns("BGCommissionEarner", earner_expected)

    print(f"\n  All BGCommissionEarner columns:")
    for c in sorted(earner_props or []):
        print(f"    - {c}")

    # ===== BGYearMonth columns =====
    ym_expected = [
        ("Name", [], "CONFIRMED"),
        ("Id", [], "CONFIRMED"),
    ]
    ym_results, ym_props, _ = check_columns("BGYearMonth", ym_expected)

    # ===== BGSalesGroup columns =====
    sg_expected = [
        ("Id", [], "CONFIRMED"),
        ("Name", [], "CONFIRMED"),
    ]
    sg_results, sg_props, _ = check_columns("BGSalesGroup", sg_expected)

    # ===== IWCommissionStatus lookup =====
    print(f"\n{'='*60}")
    print("Verifying IWCommissionStatus lookup values")
    print(f"{'='*60}")

    expected_statuses = {
        "Pending": "930bb1c6-ca67-4ac0-8f96-a5ea4018a366",
        "Done": "deb80242-b56a-4b94-967a-0e170e2198d8",
        "Returned": "ee14b2ce-163a-4fb2-abea-e739636794ed",
        "Error": "26c1b9de-75c9-46c7-8963-e02b8a63f261",
        "Order Deleted": "8c2313f4-7e27-4781-afef-d16deb90cc6d",
    }

    status_records = get_sample_record("IWCommissionStatus", top=20)
    if status_records:
        found_statuses = {r.get("Name"): r.get("Id") for r in status_records}
        for name, expected_guid in expected_statuses.items():
            actual_guid = found_statuses.get(name, "")
            match = actual_guid.lower() == expected_guid.lower() if actual_guid else False
            icon = "✅" if match else "❌"
            print(f"  {icon} {name}: expected={expected_guid}")
            if actual_guid and not match:
                print(f"     ACTUAL: {actual_guid}")
            elif not actual_guid:
                print(f"     NOT FOUND in lookup")
        # Show any extra statuses
        extra = set(found_statuses.keys()) - set(expected_statuses.keys())
        if extra:
            print(f"\n  Additional statuses found: {extra}")
    else:
        print("  Could not query IWCommissionStatus entity")

    # ===== Transaction Type lookup =====
    print(f"\n{'='*60}")
    print("Verifying IWTransType lookup values")
    print(f"{'='*60}")

    expected_trans = {
        "Sale": "b4494f26-26c2-4aa6-951c-658d0828d0d0",
        "Credit Memo": "c26d3478-7ac1-49e9-97f9-1c0809552f1f",
    }

    trans_records = get_sample_record("IWTransType", top=20)
    if trans_records:
        found_trans = {r.get("Name"): r.get("Id") for r in trans_records}
        for name, expected_guid in expected_trans.items():
            actual_guid = found_trans.get(name, "")
            match = actual_guid.lower() == expected_guid.lower() if actual_guid else False
            icon = "✅" if match else "❌"
            print(f"  {icon} {name}: expected={expected_guid}")
            if actual_guid and not match:
                print(f"     ACTUAL: {actual_guid}")
            elif not actual_guid:
                print(f"     NOT FOUND in lookup")
    else:
        print("  Could not query IWTransType entity")

    # ===== Sample IWPayments record =====
    print(f"\n{'='*60}")
    print("Sample IWPayments record (most recent)")
    print(f"{'='*60}")

    samples = get_sample_record("IWPayments", top=1)
    if samples:
        for key, val in sorted(samples[0].items()):
            if not key.startswith("@"):
                print(f"  {key}: {val}")

    # ===== Summary =====
    print(f"\n{'='*60}")
    print("SUMMARY - Column Name Verification")
    print(f"{'='*60}")

    all_results = {
        "IWPayments": iw_results,
        "Order": order_results,
        "BGCommissionEarner": earner_results,
    }

    issues = []
    for entity, results in all_results.items():
        for col, info in results.items():
            if info["status"] == "MISSING":
                issues.append(f"  ❌ {entity}.{col} — NOT FOUND")
            elif info["actual"] != col:
                issues.append(f"  ⚠️  {entity}.{col} → use '{info['actual']}' instead")

    if issues:
        print("\nAction items:")
        for i in issues:
            print(i)
    else:
        print("\n✅ All column names verified successfully!")


if __name__ == "__main__":
    main()
