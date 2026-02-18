# IWQBIntegration - Team Instructions

**Date:** 2026-01-30 (Updated: 2026-02-03)
**Package:** IWQBIntegration v8.3.2.4199
**Status:** 🔴 **BLOCKED** - Missing dependency in PROD

---

## ⚠️ CRITICAL: Dependency Required (Discovered 2026-02-03)

**IWInterWeavePaymentApp is NOT installed in PROD.** This must be imported FIRST.

| Package | DEV | PROD | Action |
|---------|-----|------|--------|
| PampaBay | ✅ | ✅ | None |
| PampaBayQuickBooks | ✅ | ✅ | None |
| **IWInterWeavePaymentApp** | ✅ | ❌ | **Export from DEV, import to PROD first** |
| IWQBIntegration | ✅ | ❌ | Import after dependency |

### Pre-Requisite: Import IWInterWeavePaymentApp

**Before starting the procedure below:**

1. Go to DEV: `https://dev-pampabay.creatio.com/0/ClientApp/#/WorkspaceExplorer/`
2. Navigate to: Configuration → Packages → IWInterWeavePaymentApp
3. Right-click → Export package
4. Save as: `IWInterWeavePaymentApp_YYYYMMDD.zip`
5. Go to PROD: `https://pampabay.creatio.com/0/ClientApp/#/WorkspaceExplorer/`
6. Navigate to: Configuration → Install from file
7. Select the exported zip
8. Compile the package
9. **Then proceed with IWQBIntegration import below**

---

## Overview

This document provides step-by-step instructions for importing the IWQBIntegration package from DEV to PROD. Follow these instructions in order.

**Estimated Time:** 2-4 hours (including testing)

**Prerequisites:**
- PROD admin access
- Database backup capability
- Access to Configuration section
- **IWInterWeavePaymentApp already imported to PROD** (see above)

---

## Phase 0: DEV Readiness Verification (REQUIRED FIRST)

**Before exporting to PROD, verify the package is correctly configured in DEV.**

### 0.1 DEV Package Verification

| Item | Expected | Verified |
|------|----------|----------|
| IWQBIntegration package exists | ✅ v8.3.2.4199 | ☐ |
| IWInterWeavePaymentApp exists | ✅ | ☐ |
| 25 IW columns on Order entity | ✅ | ☐ |

### 0.2 DEV Process Configuration (CRITICAL)

Navigate to: `DEV → System Designer → Process Library → Search "IWCalculateCommission"`

| Process | Required State | Verified |
|---------|----------------|----------|
| IWCalculateCommissiononPaymentV2 | ✅ **ACTIVE** | ☐ |
| IWCalculateCommissiononPayment (V1) | ⬜ Inactive | ☐ |
| IWCalculateCommissiononPaymentIWQBIntegrationV3 | ⬜ **MUST BE INACTIVE** (26x cascade risk!) | ☐ |
| IWCalculateCommissiononPaymentCustomV4 | ⬜ Inactive | ☐ |

**⚠️ WARNING:** If V3 is active, it triggers on ANY Order modification and causes 26x duplicate entries. See `IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` for details.

### 0.3 DEV System Settings

Navigate to: `DEV → System Designer → System Settings → Search "IWEnable"`

| Setting | Required Value | Exists | Verified |
|---------|----------------|--------|----------|
| IWEnableCommissionV3 | **false** | ☐ Create if missing | ☐ |
| IWEnableCommissionV4 | **false** | ☐ Create if missing | ☐ |
| IWCalcInvoicePaymentsAmountWithProcess | true/false (verify) | ✅ In package | ☐ |

**To create missing settings:**
1. System Designer → System Settings → Add
2. Code: `IWEnableCommissionV3`
3. Name: `Enable Commission V3`
4. Type: Boolean
5. Default Value: **false**
6. Repeat for `IWEnableCommissionV4`

### 0.4 DEV Functional Test

Before exporting, test commission calculation in DEV:

1. Find an Order with Payments: `Orders → Filter by "Has Payments"`
2. Edit a Payment amount
3. Verify:
   - Commission recalculated (check Payment record)
   - Only ONE process execution (check Process Log)
   - No 26x duplicate entries

### 0.5 Export Packages from DEV

**Only after all above checks pass:**

1. Export `IWInterWeavePaymentApp`:
   ```
   DEV → Configuration → IWInterWeavePaymentApp → Export
   Save as: IWInterWeavePaymentApp_YYYYMMDD.zip
   ```

2. Export `IWQBIntegration`:
   ```
   DEV → Configuration → IWQBIntegration → Export
   Save as: IWQBIntegration_YYYYMMDD.zip
   ```

### 0.6 Phase 0 Sign-Off

| Check | Completed | Date | By |
|-------|-----------|------|-----|
| Process V2 active, others inactive | ☐ | | |
| System settings created/verified | ☐ | | |
| Functional test passed | ☐ | | |
| IWInterWeavePaymentApp exported | ☐ | | |
| IWQBIntegration exported | ☐ | | |

**Proceed to Phase 1 only after Phase 0 is complete.**

---

## Phase 1: Pre-Flight Verification (30 min)

### Step 1.1: Run Verification Queries

Connect to PROD database and run these queries:

```sql
-- Query 1: Check if Order.SalesTax column exists
-- EXPECTED: At least one row
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'Order' AND column_name LIKE '%SalesTax%';

-- Query 2: Check dependency packages exist
-- EXPECTED: 3 rows (PampaBayQuickBooks, PampaBay, IWInterWeavePaymentApp)
SELECT "Name", "Version", "ModifiedOn"
FROM "SysPackage"
WHERE "Name" IN ('PampaBayQuickBooks', 'PampaBay', 'IWInterWeavePaymentApp')
ORDER BY "Name";

-- Query 3: Check current commission process status
-- NOTE: Record which versions are currently enabled
SELECT "Name", "IsActualVersion", "Enabled"
FROM "SysSchema"
WHERE "Name" LIKE 'IWCalculateCommission%'
ORDER BY "Name";

-- Query 4: Check current tax process status
SELECT "Name", "IsActualVersion", "Enabled"
FROM "SysSchema"
WHERE "Name" LIKE '%TaxStatusByOrderSalesTax%'
ORDER BY "Name";

-- Query 5: Check if IWQBIntegration already exists in PROD
SELECT "Name", "Version", "ModifiedOn"
FROM "SysPackage"
WHERE "Name" = 'IWQBIntegration';
```

### Step 1.2: Record Current State

Fill in this table with query results:

| Check | Result | Notes |
|-------|--------|-------|
| Order.SalesTax exists | ☐ Yes ☐ No | |
| PampaBayQuickBooks version | _______ | |
| PampaBay version | _______ | |
| IWInterWeavePaymentApp version | _______ | |
| Active commission version | _______ | V1/V2/V3/V4/None |
| Active tax process | _______ | V1/V2/Both/None |
| IWQBIntegration exists | ☐ Yes ☐ No | Version: _______ |

### Step 1.3: Verify Query Results

**STOP if any of these fail:**
- ❌ Order.SalesTax column does not exist
- ❌ Any of the 3 dependency packages missing
- ❌ Multiple commission versions currently enabled (must disable extras first)

---

## Phase 2: Create Backup (15 min)

### Step 2.1: Database Backup

```bash
# Create timestamped backup
pg_dump -Fc pampabay > pampabay_prod_pre_iwqb_$(date +%Y%m%d_%H%M%S).backup

# Verify backup was created
ls -la pampabay_prod_pre_iwqb_*.backup
```

### Step 2.2: Export Existing Package (if exists)

If IWQBIntegration already exists in PROD:

1. Navigate to: `Configuration → Packages`
2. Find: `IWQBIntegration`
3. Click: `Export package`
4. Save as: `IWQBIntegration_PROD_backup_YYYYMMDD.zip`

### Step 2.3: Document Record Counts

```sql
-- Record current counts for rollback verification
SELECT 'Order' as entity, COUNT(*) as count FROM "Order"
UNION ALL SELECT 'OrderProduct', COUNT(*) FROM "OrderProduct"
UNION ALL SELECT 'Invoice', COUNT(*) FROM "Invoice"
UNION ALL SELECT 'IWPayments', COUNT(*) FROM "IWPayments";
```

| Entity | Count Before Import |
|--------|---------------------|
| Order | |
| OrderProduct | |
| Invoice | |
| IWPayments | |

---

## Phase 3: Import Package (15 min)

### Step 3.1: Navigate to Configuration

1. Go to: `https://pampabay.creatio.com/0/ClientApp/#/WorkspaceExplorer/`
2. Click: `Configuration`

### Step 3.2: Import Package

1. Click: `Install from file` (or `Import` button)
2. Select: `IWQBIntegration_2026-01-30_08.33.58.zip`
3. Wait for import to complete
4. **DO NOT** compile yet

### Step 3.3: Review Import Log

Check for errors:
- ☐ Import completed without errors
- ☐ All schemas imported successfully
- ☐ No dependency errors

**If errors occurred:** Document error messages and STOP. Consult `IWQBINTEGRATION_CONFLICT_ASSESSMENT.md`.

---

## Phase 4: Configure Processes (30 min) ⚠️ CRITICAL

### Step 4.1: Disable Duplicate Commission Processes

Navigate to: `Configuration → Process Library`

**Disable these processes (set Active = false):**

| Process | Action |
|---------|--------|
| IWCalculateCommissiononPayment (V1) | ☐ DISABLE |
| IWCalculateCommissiononPaymentIWQBIntegrationV3 | ☐ DISABLE |
| IWCalculateCommissiononPaymentCustomV4 | ☐ DISABLE |

**Enable ONLY this process:**

| Process | Action |
|---------|--------|
| IWCalculateCommissiononPaymentV2 | ☐ ENABLE |

### Step 4.2: Disable Duplicate Tax Process

| Process | Action |
|---------|--------|
| BGSetOrderProductTaxStatusByOrderSalesTax (V1) | ☐ DISABLE |
| IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | ☐ ENABLE |

### Step 4.3: Configure System Settings

Navigate to: `System Designer → System settings`

| Setting | Value | Verified |
|---------|-------|----------|
| IWEnableCommissionV3 | **false** | ☐ |
| IWEnableCommissionV4 | **false** | ☐ |
| IWEnableAutoPaymentProcessing | (verify with finance) | ☐ |

### Step 4.4: Verify Configuration

```sql
-- Verify only V2 commission is enabled
SELECT "Name", "Enabled"
FROM "SysSchema"
WHERE "Name" LIKE 'IWCalculateCommission%'
ORDER BY "Name";

-- Expected:
-- IWCalculateCommissiononPayment           | false
-- IWCalculateCommissiononPaymentV2         | true   <-- ONLY this one
-- IWCalculateCommissiononPaymentIWQBIntegrationV3 | false
-- IWCalculateCommissiononPaymentCustomV4   | false
```

---

## Phase 5: Compile (15 min)

### Step 5.1: Compile Package

1. Navigate to: `Configuration → Packages → IWQBIntegration`
2. Click: `Compile`
3. Wait for compilation to complete

### Step 5.2: Compile All (if needed)

If compilation shows dependency errors:

1. Click: `Actions → Compile all`
2. Wait for full compilation

### Step 5.3: Verify Compilation

- ☐ Compilation completed without errors
- ☐ No unresolved dependencies
- ☐ No schema conflicts

---

## Phase 6: Testing (1-2 hours)

### Test 1: Order Form

1. Navigate to: Orders section
2. Open existing Order
3. Verify form loads without errors
4. Check for new IW fields in form
5. **Result:** ☐ Pass ☐ Fail

### Test 2: Create New Order

1. Create new Order
2. Set Sales Tax field
3. Add Product to Order
4. Save Order
5. Verify OrderProduct.TaxStatus was set
6. **Result:** ☐ Pass ☐ Fail

### Test 3: Modify Order (26x Cascade Check)

1. Edit existing Order (change any field)
2. Save Order
3. Check BGQuickBooksIntegrationLogDetail:
   ```sql
   SELECT COUNT(*) as entries, "BGRecordId"
   FROM "BGQuickBooksIntegrationLogDetail"
   WHERE "CreatedOn" > NOW() - INTERVAL '5 minutes'
   GROUP BY "BGRecordId"
   HAVING COUNT(*) > 1;
   ```
4. **Expected:** No duplicate entries (or only 1-2, not 26+)
5. **Result:** ☐ Pass ☐ Fail

### Test 4: Payment Commission

1. Create or find Order with Payments
2. Add new Payment
3. Verify commission calculated (only once)
4. Check for duplicate calculations in logs
5. **Result:** ☐ Pass ☐ Fail

### Test 5: Invoice Updates

1. Add Payment to Invoice
2. Verify Invoice.PaymentAmount updated
3. Verify Invoice.IWCreditedTotal updated
4. Verify Invoice.IWInvoiceCheckbox set correctly
5. **Result:** ☐ Pass ☐ Fail

### Test 6: Commission Report

1. Navigate to Reports page
2. Generate Commission report
3. Set YearMonth filter
4. Click Generate
5. Verify report downloads
6. Verify data is correct
7. **Result:** ☐ Pass ☐ Fail

### Test 7: Regression - Existing Functionality

1. Verify existing Orders display correctly
2. Verify Order search works
3. Verify Invoice section loads
4. Verify no JavaScript console errors
5. **Result:** ☐ Pass ☐ Fail

---

## Phase 7: Post-Import Monitoring

### Day 1 Monitoring

Check every 2 hours for:

```sql
-- Check for process errors
SELECT "Name", "Status", "ErrorDescription"
FROM "SysProcessLog"
WHERE "StartDate" > NOW() - INTERVAL '2 hours'
  AND "Status" = 'Error'
  AND "Name" LIKE 'IW%'
ORDER BY "StartDate" DESC;

-- Check for duplicate log entries (26x issue indicator)
SELECT COUNT(*) as entries, "BGRecordId"
FROM "BGQuickBooksIntegrationLogDetail"
WHERE "CreatedOn" > NOW() - INTERVAL '2 hours'
GROUP BY "BGRecordId"
HAVING COUNT(*) > 5;
```

### Week 1 Monitoring

Daily checks for:
- Commission calculation accuracy
- Invoice balance discrepancies
- User-reported issues

---

## Troubleshooting

### Problem: 26x Duplicate Entries

**Cause:** IWEnableCommissionV3 = true or V3 process still enabled

**Fix:**
```sql
-- Verify V3 is disabled
SELECT "Name", "Enabled" FROM "SysSchema"
WHERE "Name" = 'IWCalculateCommissiononPaymentIWQBIntegrationV3';

-- Verify system setting
SELECT "Code", "TextValue" FROM "SysSettingsValue"
WHERE "Code" = 'IWEnableCommissionV3';
```

### Problem: Tax Status Not Setting

**Cause:** Tax process disabled or Order.SalesTax column missing

**Fix:**
1. Verify V2 tax process is enabled
2. Verify Order.SalesTax column exists
3. Check process log for errors

### Problem: Commission Calculated Multiple Times

**Cause:** Multiple commission versions enabled

**Fix:**
```sql
-- Disable all except V2
UPDATE "SysSchema"
SET "Enabled" = false
WHERE "Name" LIKE 'IWCalculateCommission%'
  AND "Name" != 'IWCalculateCommissiononPaymentV2';
```

### Problem: Form Layout Broken

**Cause:** Multiple packages extending Order form

**Fix:**
1. Open Form Designer
2. Navigate to Order page
3. Rearrange overlapping fields
4. Save and compile

---

## Rollback Procedure

If critical issues occur:

### Option A: Disable Processes (Quick)

```sql
-- Disable all IW processes
UPDATE "SysSchema"
SET "Enabled" = false
WHERE "Name" LIKE 'IW%';
```

### Option B: Restore Database (Full)

```bash
# Restore from backup
pg_restore -d pampabay pampabay_prod_pre_iwqb_YYYYMMDD_HHMMSS.backup
```

---

## Sign-Off

| Phase | Completed | Date | Verified By |
|-------|-----------|------|-------------|
| Pre-Flight Verification | ☐ | | |
| Backup Created | ☐ | | |
| Package Imported | ☐ | | |
| Processes Configured | ☐ | | |
| Compilation Success | ☐ | | |
| Test 1: Order Form | ☐ | | |
| Test 2: Create Order | ☐ | | |
| Test 3: 26x Check | ☐ | | |
| Test 4: Commission | ☐ | | |
| Test 5: Invoice | ☐ | | |
| Test 6: Report | ☐ | | |
| Test 7: Regression | ☐ | | |

**Final Approval:**

Approved by: _________________________ Date: _____________

---

## Document References

| Need | Document |
|------|----------|
| Full risk analysis | `IWQBINTEGRATION_CONFLICT_ASSESSMENT.md` |
| Root cause details | `IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` |
| Complete checklist | `IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md` |
| All findings | `IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md` |
| Improvements | `IWQBINTEGRATION_NEXT_STEPS.md` |
| Master index | `IWQBINTEGRATION_MASTER_CATALOG.md` |

---

*Team instructions prepared: 2026-01-30*
