# Commission Data Pipeline Analysis

**Date:** 2026-01-20
**Status:** Root causes identified - multiple blockers in pipeline

---

## Executive Summary

Commission reports are missing data due to **multiple blockers across the data pipeline**. This document traces the complete flow from Order creation to Commission report and identifies where data is getting stuck.

---

## Data Pipeline Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   ORDER     │ -> │  QB SYNC    │ -> │ QB INVOICE  │ -> │ QB PAYMENT  │ -> │ COMMISSION  │
│  Created    │    │  to QB      │    │  Created    │    │  Recorded   │    │   Report    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      ✅                 ⚠️                 ⚠️                 ❌                  ❌
   Working          Partially           Partially         Bottleneck          Missing
                     Blocked             Working                               Data
```

---

## Pipeline Stage Analysis

### Stage 1: Order Creation ✅ WORKING

| Metric | Status |
|--------|--------|
| Orders being created | ✅ Working |
| Commission Earners created | ✅ Working (fixed Jan 19) |
| BGHasQuickBooksLog flag | ✅ Fixed (626 orders) |
| ProcessListeners flag | ✅ Fixed (626 orders) |

### Stage 2: Order → QB Invoice Sync ⚠️ PARTIALLY BLOCKED

| Issue | Count | Status |
|-------|-------|--------|
| Orders synced successfully | 336 | ✅ |
| Connection timeout errors | 57 | ❌ QB Web Connector offline |
| Stuck in "Processing" | 100 | ❌ Connection dropped |
| False "Processed" (no QB ID) | 637 | ❌ Historical bug |
| Missing Discount account | 1 | ❌ QB config needed |
| Customer not found | 1 | ❌ QB config needed |

**Root Causes:**
1. QB Web Connector at `96.56.203.106:8080` is offline
2. Sync code marks orders "Processed" even on connection failure (bug)
3. 637 orders from Aug 2023 - Jan 2026 never actually synced

### Stage 3: QB Invoice Exists ⚠️ PARTIALLY WORKING

For orders that successfully synced (336 today + historical):
- Invoices exist in QuickBooks
- Customer and line items are correct
- Invoice numbers assigned (e.g., 62046, 62051, etc.)

### Stage 4: QB Payment Recording ❌ BOTTLENECK

| Metric | Value |
|--------|-------|
| Patricia's orders with earners | ~1,250 |
| Patricia's invoices PAID in QB | 27 |
| Percentage paid | **2.2%** |

**Root Cause:** QuickBooks invoices exist but haven't been marked as "paid" by the accounting team. Commission sync pulls from `ReceivePayment` records, not `Invoice` records.

### Stage 5: Commission Report ❌ MISSING DATA

Because Stage 4 is blocked, commission reports only show data for the small percentage of invoices that have been paid.

**January 2026 Commission Data Available:**
- 350 records
- $196,511 total amount
- $13,832 commission

---

## Patricia Goncalves Case Study

| Stage | Count | Percentage |
|-------|-------|------------|
| Commission Earners (Orders) | 1,250 | 100% |
| Synced to QB (Invoices) | Unknown | ~30%? |
| Paid in QB | 27 | **2.2%** |
| In Commission Report | 27 | 2.2% |

**97.8% of Patricia's orders are NOT appearing in commission reports** because the invoices haven't been paid in QuickBooks.

---

## Commission Data by Month (Current State)

From `BGCommissionReportQBDownload`:

| Month | Records | Amount | Commission |
|-------|---------|--------|------------|
| Jan 2026 | 350 | $196,511 | $13,832 |
| Dec 2025 | 115 | $33,087 | $4,888 |
| Feb 2026 | 28 | $26,193 | $3,929 |
| Mar 2026 | 4 | $2,318 | $348 |
| Apr 2026 | 1 | $945 | $142 |
| May 2026 | 1 | $662 | $99 |

---

## Blockers Summary

| Blocker | Impact | Owner | Priority |
|---------|--------|-------|----------|
| QB Web Connector offline | 157+ orders can't sync | IT/QB Team | HIGH |
| 637 false-processed orders | Historical orders never synced | IT (SQL fix) | HIGH |
| QB invoices not marked paid | Commission data missing | QB Accounting | HIGH |
| Missing "Discount" account | 1 order blocked | QB Admin | LOW |
| Missing customer in QB | 1 order blocked | QB Admin | LOW |

---

## Required Actions

### Immediate (IT/QB Team)

1. **Bring QB Web Connector online**
   - Server: `96.56.203.106:8080`
   - Check Windows Service "QuickBooks Web Connector"
   - Verify port 8080 is accessible

2. **Reset 637 false-processed orders** (after QB online):
```sql
UPDATE "BGQuickBooksIntegrationLogDetail"
SET "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640',
    "BGErrorMessage" = ''
WHERE "BGStatusId" = 'e7428193-4cf1-4d1b-abae-00e93ab5e1c5'
  AND "BGRecordId" IN (
      SELECT "Id" FROM "Order"
      WHERE "BGQuickBooksId" IS NULL OR "BGQuickBooksId" = ''
  );
```

### Immediate (QB Accounting Team)

3. **Process invoice payments in QuickBooks**
   - December 2025 invoices especially
   - Patricia Goncalves accounts
   - This is the main blocker for commission data

### After Fixes Applied

4. **Run "QB Customer Order Integration"** to sync orders → invoices
5. **Run "Get QuickBooks Commissions"** to pull payment data back

### Long-term (e6Solutions)

6. **Fix sync code bug** - Should mark "Error" on connection failure, not "Processed"
   - Location: `BGQuickBooksLogDetail.ProcessCustomerOrders()`

---

## Verification Queries

### Check Patricia's current status:
```sql
SELECT
    'Earners' as "Source", COUNT(*) as "Count"
FROM "BGCommissionEarner" e
WHERE e."BGName" ILIKE '%Patricia%'
UNION ALL
SELECT
    'QB Download' as "Source", COUNT(*)
FROM "BGCommissionReportQBDownload" q
JOIN "Employee" emp ON emp."Id" = q."BGSalesRepId"
WHERE emp."Name" ILIKE '%Patricia%';
```

### Check sync status:
```sql
SELECT
    CASE WHEN "BGQuickBooksId" IS NOT NULL AND "BGQuickBooksId" != ''
         THEN 'Synced' ELSE 'Not Synced' END as "Status",
    COUNT(*) as "Orders"
FROM "Order"
WHERE "CreatedOn" >= '2026-01-01'
GROUP BY 1;
```

---

*Document created: 2026-01-20*
*For internal team reference*
