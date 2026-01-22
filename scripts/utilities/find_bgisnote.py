#!/usr/bin/env python3
"""Find where BGIsNote is defined/used"""

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
    print("BGIsNote LOCATION SEARCH")
    print("="*70)

    # 1. Check BGCommissionReportDataView schema
    print("\n1. BGCommissionReportDataView (WHERE IT'S USED):")
    print("   - This is the PostgreSQL VIEW that outputs BGIsNote")
    print("   - View URL: https://pampabay.creatio.com/0/ClientApp/#/SchemaDesigner")
    print("   - Schema name: BGCommissionReportDataView")
    
    # Check view sample data
    url = f"{BASE_URL}/0/odata/BGCommissionReportDataView"
    params = {"$select": "Id,BGIsNote,BGDescription", "$top": "3"}
    resp = session.get(url, params=params, timeout=60)
    if resp.status_code == 200:
        records = resp.json().get("value", [])
        for r in records[:3]:
            print(f"   Sample: BGIsNote={r.get('BGIsNote')} (type: {type(r.get('BGIsNote')).__name__})")

    # 2. Check entities that might have BGIsNote as a column
    print("\n2. ENTITIES WITH BGIsNote COLUMN:")
    
    entities_to_check = [
        "BGCommissionReportQBDownload",
        "BGCommissionReportNotes",
        "BGCommissionEarner"
    ]
    
    for entity in entities_to_check:
        url = f"{BASE_URL}/0/odata/{entity}"
        params = {"$select": "Id,BGIsNote", "$top": "1"}
        resp = session.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            data = resp.json().get("value", [])
            if data and "BGIsNote" in data[0]:
                print(f"   ✅ {entity} - HAS BGIsNote column")
            else:
                print(f"   ❌ {entity} - No BGIsNote column")
        else:
            print(f"   ❌ {entity} - No BGIsNote column (or error: {resp.status_code})")

    # 3. View definition location
    print("\n3. BGIsNote IN VIEW DEFINITION:")
    print("""
   The view is defined in PostgreSQL with TWO sources:

   SOURCE 1 (Lines ~56): QB Download transactions
   -------------------------------------------------
   SELECT ... FALSE AS "BGIsNote" ...
   FROM "BGCommissionReportQBDownload" qb
   
   This means regular commission transactions have BGIsNote = FALSE

   SOURCE 2 (Lines ~124): Commission Notes  
   -------------------------------------------------
   UNION ALL
   SELECT ... TRUE AS "BGIsNote" ...
   FROM "BGCommissionReportNotes" n
   
   This means manual commission notes have BGIsNote = TRUE

   LOCATION: The view definition is in PostgreSQL database
   - Schema: public
   - View name: "BGCommissionReportDataView"
   - Access via pgAdmin or Creatio SQL Console
""")

    # 4. SQL file reference
    print("\n4. SQL FIX FILE LOCATION:")
    print("   /home/magown/creatio-report-fix/scripts/sql/BGCommissionReportDataView_BGIsNote_fix.sql")
    print("   This file contains the corrected view with FALSE/TRUE instead of 0/1")

if __name__ == "__main__":
    main()
