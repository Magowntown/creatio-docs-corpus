# Commission Fix - Action Log

**Session Date**: 2026-01-19
**Operator**: Claude Code Assistant
**Environment**: PROD (pampabay.creatio.com)

---

## Timeline of Actions

### Phase 1: Investigation (Morning)

| Time | Action | Result |
|------|--------|--------|
| - | Identified 263 orders missing commission earners | Backlog from Oct 2024 - Jan 2026 |
| - | Created commission earners for backlog | 263 earners created |
| - | Fixed commission rates and names | Updated to correct values |
| - | Discovered BGCommissionReportDataView not populating | Root cause investigation started |

### Phase 2: Root Cause Analysis

| Time | Action | Result |
|------|--------|--------|
| - | Launched 3 parallel investigations | Process, Schema, Report |
| - | Found BGIsNote schema mismatch | INTEGER vs BOOLEAN |
| - | Found view JOIN requires BGNumberInvoice | Many orders lack this |
| - | Documented BGCommissionEarnerSimple view option | Alternative approach |

### Phase 3: BGIsNote Schema Fix

| Time | Action | Result |
|------|--------|--------|
| - | Created SQL fix file | `BGCommissionReportDataView_BGIsNote_fix.sql` |
| - | Tested minimal view creation | SUCCESS - boolean accepted |
| - | Attempted CREATE OR REPLACE VIEW | FAILED - cannot change column type |
| - | Used DROP + CREATE in transaction | SUCCESS - view recreated |

**SQL Executed in pgAdmin**:
```sql
BEGIN;
DROP VIEW IF EXISTS public."BGCommissionReportDataView";
CREATE VIEW public."BGCommissionReportDataView" AS
-- (full view definition with FALSE/TRUE)
COMMIT;
```

**Result**: Query execution time: 0 sec

### Phase 4: View Population Attempts

| Time | Action | Result |
|------|--------|--------|
| - | Attempted INSERT into view | FAILED - view not insertable |
| - | Pivoted to source table | BGCommissionReportQBDownload |
| - | Test insert into source table | SUCCESS |
| - | First bulk insert script | FAILED - FK constraint on BGCustomerId |
| - | V2 script (omit BGCustomerId) | SUCCESS - 249 records created |

**Error Encountered**:
```
23503: insert or update violates foreign key constraint
"FK_BGCommissionReportQBDownload_BGCustomerId"
```

**Solution**: Omit BGCustomerId field (nullable)

### Phase 5: Verification

| Time | Action | Result |
|------|--------|--------|
| - | Checked view record count | 31,471 → 34,583 (+3,112) |
| - | User ran Get QuickBooks Commissions | +159 more records |
| - | Final view count | 34,883 records |
| - | Verified BGIsNote returns boolean | ✅ type: bool |
| - | Verified auto-earner creation | ✅ 37 created today |

---

## Commands Executed

### Python Scripts Run

```bash
# QB Download population (V2 - FK safe)
python3 /tmp/populate_qb_download_v2.py

# Gap analysis
python3 /tmp/final_gap_analysis.py

# BGIsNote location search
python3 /tmp/find_bgisnote.py

# View state verification
python3 /tmp/get_current_view.py
```

### SQL Executed (pgAdmin)

```sql
-- Test view creation
CREATE OR REPLACE VIEW public."BGCommissionReportDataView_TEST" AS
SELECT '00000000-0000-0000-0000-000000000001'::uuid AS "Id",
       FALSE AS "BGIsNote",
       'Test Record' AS "BGDescription";

-- Production view fix (in transaction)
BEGIN;
DROP VIEW IF EXISTS public."BGCommissionReportDataView";
CREATE VIEW public."BGCommissionReportDataView" AS
-- (173 lines of view definition)
COMMIT;
```

---

## Errors Encountered and Resolutions

### Error 1: Syntax Error

**Error**: `Npgsql.PostgresException: 42601: syntax error at or near "If"`

**Cause**: User copied extra text with SQL

**Resolution**: Provided clean SQL starting with CREATE

### Error 2: Cannot Change Column Type

**Error**: `42P16: cannot change data type of view column "BGIsNote" from integer to boolean`

**Cause**: PostgreSQL limitation with CREATE OR REPLACE VIEW

**Resolution**: Used DROP + CREATE in transaction

### Error 3: Cannot Insert Into View

**Error**: `cannot insert into view "BGCommissionReportDataView"`

**Cause**: View has JOINs/UNIONs - not directly insertable

**Resolution**: Insert into source table BGCommissionReportQBDownload

### Error 4: Foreign Key Constraint

**Error**: `23503: insert or update violates foreign key constraint "FK_BGCommissionReportQBDownload_BGCustomerId"`

**Cause**: BGCustomerId references Customer table

**Resolution**: Omit BGCustomerId field from insert

---

## Files Created

### Scripts
- `/tmp/populate_qb_download.py` - Original (FK issue)
- `/tmp/populate_qb_download_v2.py` - Fixed (FK safe)
- `/tmp/final_gap_analysis.py` - Data integrity check
- `/tmp/find_bgisnote.py` - BGIsNote location search
- `/tmp/get_current_view.py` - View state verification
- `/tmp/test_isnote_fix.py` - BGIsNote schema test
- `/tmp/minimal_test_fix.sql` - Test view SQL

### Documentation
- `/tmp/CURRENT_STATUS.md` - Status summary
- `/home/magown/creatio-report-fix/docs/COMMISSION_FIX_COMPLETE.md` - Full documentation

### SQL
- `/home/magown/creatio-report-fix/scripts/sql/BGCommissionReportDataView_BGIsNote_fix.sql` - View fix

---

## API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ServiceModel/AuthService.svc/Login` | POST | Authentication |
| `/0/odata/BGCommissionEarner` | GET/POST | Commission earners |
| `/0/odata/BGCommissionReportQBDownload` | GET/POST | QB download records |
| `/0/odata/BGCommissionReportDataView` | GET | View data |
| `/0/odata/Order` | GET | Order data |

---

## Verification Checklist

- [x] BGIsNote returns boolean (verified: type=bool)
- [x] Manual earners created (263 records)
- [x] Auto-earner creation working (37 today)
- [x] QB Download records created (249 records)
- [x] View population increased (34,883 total)
- [x] Reports show more data (Dec: +296%, Jan: +1414%)

---

---

## Phase 6: Report Configuration Fix (2026-01-19)

### Issue
Reports other than Commission failed with error: `ArgumentNullOrEmptyException: Value for argument 'queryConfig' must be specified`

### Root Cause
- `IntExcelReport` entries existed but had empty `IntEsq` field (Entity Schema Query JSON)
- Name mismatches between `UsrReportesPampa` and `IntExcelReport` (case sensitivity, trailing spaces)

### Actions Taken

| Action | Result |
|--------|--------|
| Analyzed all 13 active reports | Found 5 working, 8 broken |
| Fixed name case mismatches | "Rpt Sales by Line" → "Rpt Sales By Line" |
| Added ESQ to 7 reports | Created JSON config for each view |
| Fixed "Items by Customer" case | "Items By Customer" → "Items by Customer" |
| Renamed "Rpt Customer Did Not Buy" | → "Rpt CustomersDidNotBuyOverAPeriodOfTime" |

### Reports Fixed

| Report | Fix Applied |
|--------|-------------|
| Sales By Item By Type Of Customer | Added ESQ (BGSalesByItemView) |
| Items by Customer | Fixed name case + Added ESQ |
| Sales By Line With Ranking | Added ESQ (BGSalesByLineView) |
| Sales By Sales Rep | Fixed case + Added ESQ (BGSalesBySalesRepView) |
| Sales by Customer Year Comparison | Fixed case + Added ESQ (BGSalesByCustomerView) |
| Sales Rep Monthly Report | Added ESQ (BGSalesBySalesRepView) |
| Customers did not buy | Renamed + Added ESQ |
| Sales By Line | Fixed name case |

### ESQ Format Used

```json
{
  "rootSchemaName": "ViewName",
  "operationType": 0,
  "filters": {
    "className": "Terrasoft.FilterGroup",
    "isEnabled": true,
    "filterType": 6,
    "logicalOperation": 0,
    "items": {}
  },
  "columns": {"items": {}}
}
```

### View Mappings

| Report | Database View |
|--------|---------------|
| Sales By Line | BGSalesByLineView |
| Sales By Item | BGSalesByItemView |
| Sales By Customer | BGSalesByCustomerView |
| Sales By Sales Group | BGSalesBySalesGroupView |
| Sales By Customer Type | BGSalesByCustomerView |
| Sales By Item By Type Of Customer | BGSalesByItemView |
| Commission | BGCommissionReportDataView |
| Items by Customer | BGSalesByItemView |
| Customers did not buy | BGSalesByCustomerView |
| Sales By Line With Ranking | BGSalesByLineView |
| Sales By Sales Rep | BGSalesBySalesRepView |
| Sales by Customer Year Comparison | BGSalesByCustomerView |
| Sales Rep Monthly Report | BGSalesBySalesRepView |

### Final Status

All 13 reports now ✅ READY:
```
✅ Sales By Item
✅ Sales By Line
✅ Sales By Customer
✅ Sales By Sales Group
✅ Sales By Customer Type
✅ Sales By Item By Type Of Customer
✅ Commission
✅ Items by Customer
✅ Customers did not buy over a period of time
✅ Sales By Line With Ranking
✅ Sales By Sales Rep
✅ Sales by Customer Year Comparison
✅ Sales Rep Monthly Report
```

### Scripts Created

- `/tmp/fix_remaining_reports.py` - Main fix script
- `/tmp/fix_final_two.py` - Fixed last 2 edge cases
- `/tmp/verify_matching.py` - Verification script

---

*Log created: 2026-01-19*
