# PROD Deployment Plan - Commission Report Fix

**Date:** 2026-01-14
**Target:** https://pampabay.creatio.com
**Target Package:** IWQBIntegration
**Fix:** FLT-004 (Commission report empty data for Year-Month filters)

---

## PROD Environment Analysis (Verified 2026-01-14)

| Item | DEV | PROD | Notes |
|------|-----|------|-------|
| IWQBIntegration | ✅ Exists | ✅ Exists (74 schemas) | Target package |
| UsrExcelReportService | ✅ In PampaBayVer2 | ❌ Does NOT exist | **NEEDS CREATION** |
| BGCommissionReportDataView | ✅ Fixed | ✅ Exists | **NEEDS SQL VERIFICATION** |
| UsrPage_ebkv9e8 (frontend) | ✅ Exists | ✅ Exists | In IWQBIntegration |
| IntExcelExport library | ✅ Exists | ✅ Exists (22 schemas) | Report generation engine |
| IntExcelReport config | ✅ Configured | ✅ Configured | "Rpt Commission" → BGCommissionReportDataView |

**Key Finding:** Frontend handler `UsrPage_ebkv9e8` already exists in PROD IWQBIntegration. Only the backend service needs to be created.

---

## Pre-Deployment Checklist

| Item | PROD Status | Action Required |
|------|-------------|-----------------|
| IWQBIntegration package | ✅ Exists | None |
| UsrExcelReportService | ❌ Missing | **CREATE SCHEMA** |
| BGCommissionReportDataView (SQL) | ✅ Entity exists | **VERIFY SQL VIEW** |
| UsrPage_ebkv9e8 (frontend) | ✅ Exists | None |
| IntExcelReport configuration | ✅ Correct | None |

---

## Deployment Steps

### Step 1: Verify BGCommissionReportDataView SQL (CRITICAL)

The FLT-004 fix required updating the SQL view's WHERE clause. **This is the root cause fix.**

**Check current PROD view definition:**
```sql
-- Run in PROD pgAdmin
SELECT pg_get_viewdef('"BGCommissionReportDataView"'::regclass, true);
```

**Look for this bug in the WHERE clause:**
```sql
-- BUG (filters on wrong date):
WHERE EXTRACT(month FROM qb."BGTransactionDate") = ...

-- FIXED (filters on output date):
WHERE EXTRACT(month FROM so."BGInvoiceDate") = ...
```

**If bug exists, apply fix:**
```sql
-- The view should filter on so."BGInvoiceDate" (Order invoice date)
-- NOT on qb."BGTransactionDate" (QB download date)
-- See: scripts/sql/BGCommissionReportDataView_fix.sql
```

### Step 2: Create UsrExcelReportService in PROD

**Package:** IWQBIntegration

1. Open PROD Configuration:
   - URL: `https://pampabay.creatio.com/0/ClientApp/#/WorkspaceExplorer`

2. Navigate to **IWQBIntegration** package

3. Click **Add** → **Source Code**

4. Configure:
   - Name: `UsrExcelReportService`
   - Title: `Usr Excel Report Service`

5. Copy code from: `source-code/UsrExcelReportService_Updated.cs`

6. **Save and Publish**

7. Wait for compilation to succeed (may take several minutes)

### Step 3: Verify Configuration (Already Confirmed via API)

The following were verified via API queries on 2026-01-14:
- ✅ `UsrPage_ebkv9e8` frontend handler exists in IWQBIntegration
- ✅ `IntExcelReport` "Rpt Commission" is linked to `BGCommissionReportDataView`
- ✅ `IntExcelExport` library exists (22 schemas)

No action required for these items.

---

## Testing Plan

### Test 1: Basic Report Generation
```
1. Log into PROD
2. Navigate to Commission Report
3. Generate without filters
4. Verify: Report downloads successfully
```

### Test 2: Year-Month Filter (FLT-004 Fix)
```
1. Select Year-Month: December 2024 (or recent month with data)
2. Select Sales Group: Any active group
3. Generate report
4. Verify: Data sheet has rows (not just header)
5. Verify: Dates in report match selected month
```

### Test 3: Regression
```
1. Test Sales Group filter only (no Year-Month)
2. Test with no filters
3. Verify all combinations work
```

---

## Rollback Plan

### If SQL View Update Fails:
```sql
-- Revert to original view definition (backup first!)
-- Contact DBA for view history/backup
```

### If Service Deployment Fails:
```
1. Delete UsrExcelReportService from PampaBayVer2
2. Recompile package
3. Report will not work until fixed
```

### If Report Breaks After Deployment:
```
1. Check Creatio logs for errors
2. Verify IntExcelReport configuration
3. Verify BGCommissionReportDataView returns data
4. Rollback SQL view if needed
```

---

## Key Differences: DEV vs PROD

| Aspect | DEV | PROD |
|--------|-----|------|
| URL | dev-pampabay.creatio.com | pampabay.creatio.com |
| UsrExcelReportService package | PampaBayVer2 | IWQBIntegration (to be created) |
| UsrPage_ebkv9e8 package | PampaBayVer2 | IWQBIntegration |
| BGCommissionReportDataView | ✅ Fixed | ⚠️ SQL view needs verification |
| IW_Commission support | ✅ Implemented | ❌ Not required yet |

### IWQBIntegration Package Contents (PROD)

| Schema Type | Count | Key Items |
|-------------|-------|-----------|
| EntitySchemaManager | 19 | BGCommissionReportDataView, IWPayments, IWCreditMemos |
| ClientUnitSchemaManager | 15 | UsrPage_ebkv9e8, Orders_FormPage, IWPayments_FormPage |
| ProcessSchemaManager | 9 | IWCalculateCommissiononPaymentCustomV4 |
| AddonSchemaManager | 9 | BGUsrPage_ebkv9e8BusinessRule |

---

## Files to Deploy

| File | Purpose | Target |
|------|---------|--------|
| `source-code/UsrExcelReportService_Updated.cs` | Backend service | IWQBIntegration |
| `scripts/sql/BGCommissionReportDataView_fix.sql` | SQL view fix (if needed) | Database |

---

## Notes

1. **IW_Commission is DEV-only for now** - The PROD deployment focuses on the Commission report fix only. IWCommissionReportDataView entity already exists in PROD IWQBIntegration.

2. **Database access required** - The SQL view fix needs direct database access (pgAdmin or equivalent). Check if the WHERE clause filters on `so."BGInvoiceDate"` (correct) vs `qb."BGTransactionDate"` (bug).

3. **Compile time** - IWQBIntegration has 74 schemas. Compilation may take several minutes.

4. **Test with real data** - Use actual Year-Month values that have commission data in PROD.

5. **Frontend handler already exists** - No need to deploy `UsrPage_ebkv9e8.js`. It's already in IWQBIntegration.

---

## Sign-Off

| Step | Completed | Verified By | Date |
|------|-----------|-------------|------|
| PROD environment analyzed | ✅ | API Queries | 2026-01-14 |
| Frontend handler verified | ✅ | API Query | 2026-01-14 |
| IntExcelReport config verified | ✅ | API Query | 2026-01-14 |
| SQL View created in PROD | ✅ | pgAdmin | 2026-01-15 |
| SQL View returns data | ✅ | SELECT LIMIT 5 | 2026-01-15 |
| Environment compiled | ✅ | User | 2026-01-15 |
| UsrExcelReportService deployed | ✅ | Already existed | 2026-01-15 |
| Test 1: Basic generation | ✅ | test_report_service.py | 2026-01-15 |
| Test 2: Year-Month filter | ✅ | 56 rows (2024-12 + RDGZ) | 2026-01-15 |
| Test 3: Regression | ✅ | Filters working | 2026-01-15 |

---

## Incident Notes (2026-01-15)

**Issue:** Report failed with `PostgresException: 42P01: relation "public.BGCommissionReportDataView" does not exist`

**Root cause:** PostgreSQL view was never created in PROD. Only the Creatio entity schema (metadata) existed.

**Resolution:** Created the view using SQL from `scripts/sql/BGCommissionReportDataView_fix_PROD.sql`

**Prevention:** See `docs/VIEW_DEPLOYMENT_PREVENTION.md` for updated deployment procedures
