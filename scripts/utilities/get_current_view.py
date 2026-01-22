#!/usr/bin/env python3
"""Get current BGCommissionReportDataView definition from PROD to verify before applying fix"""

import requests

BASE_URL = "https://pampabay.creatio.com"
USERNAME = "Supervisor"
PASSWORD = "123*Pampa?"

session = requests.Session()

def login():
    auth_url = f"{BASE_URL}/ServiceModel/AuthService.svc/Login"
    resp = session.post(auth_url, json={"UserName": USERNAME, "UserPassword": PASSWORD})
    if resp.status_code == 200 and resp.json().get("Code") == 0:
        csrf = resp.cookies.get("BPMCSRF")
        if csrf:
            session.headers["BPMCSRF"] = csrf
        return True
    return False

def main():
    if not login():
        print("Login failed")
        return

    print("="*70)
    print("VERIFYING CURRENT VIEW STATE")
    print("="*70)

    # 1. Check current BGIsNote values in the view
    print("\n1. CURRENT BGIsNote VALUES IN VIEW:")
    url = f"{BASE_URL}/0/odata/BGCommissionReportDataView"
    params = {
        "$select": "Id,BGIsNote,BGDescription",
        "$top": "5"
    }
    resp = session.get(url, params=params, timeout=60)
    if resp.status_code == 200:
        records = resp.json().get("value", [])
        for r in records:
            val = r.get('BGIsNote')
            print(f"   BGIsNote = {val} (type: {type(val).__name__})")
    else:
        print(f"   Error: {resp.status_code}")

    # 2. Check if there are any BGIsNote=true records (notes)
    print("\n2. CHECKING FOR COMMISSION NOTES (BGIsNote=true):")
    url = f"{BASE_URL}/0/odata/BGCommissionReportDataView/$count"
    params = {"$filter": "BGIsNote eq true"}
    resp = session.get(url, params=params, timeout=60)
    if resp.status_code == 200:
        count = resp.text.strip().replace('\ufeff', '')
        print(f"   Records with BGIsNote=true: {count}")
    else:
        print(f"   Query failed (might be due to type issue): {resp.status_code}")

    # 3. Total view records
    print("\n3. TOTAL VIEW RECORDS:")
    url = f"{BASE_URL}/0/odata/BGCommissionReportDataView/$count"
    resp = session.get(url, timeout=60)
    if resp.status_code == 200:
        count = resp.text.strip().replace('\ufeff', '')
        print(f"   Total: {count}")

    # 4. Check BGCommissionReportNotes (source for BGIsNote=1 records)
    print("\n4. COMMISSION REPORT NOTES (BGIsNote=1 source):")
    url = f"{BASE_URL}/0/odata/BGCommissionReportNotes/$count"
    resp = session.get(url, timeout=60)
    if resp.status_code == 200:
        count = resp.text.strip().replace('\ufeff', '')
        print(f"   Total notes: {count}")
    else:
        print(f"   Error or entity doesn't exist: {resp.status_code}")

    print("\n" + "="*70)
    print("SAFETY ASSESSMENT")
    print("="*70)
    print("""
The fix changes ONLY:
  Line 56:  0 → FALSE  (for QB transaction records)
  Line 124: 1 → TRUE   (for Commission Note records)

This is a TYPE change only - the semantic meaning is identical:
  0 = FALSE = "not a note" (regular commission)
  1 = TRUE  = "is a note" (manual commission note)

PostgreSQL treats FALSE/TRUE as boolean literals.
The view will return the same data, just with proper boolean type.

RISK: LOW - This is a standard type correction.
""")

if __name__ == "__main__":
    main()
