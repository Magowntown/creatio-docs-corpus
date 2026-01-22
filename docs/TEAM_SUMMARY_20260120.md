# Commission Report Data Gap - Team Summary

**Date:** January 20, 2026
**For:** Internal Team / e6Solutions / QB Team

---

## The Problem

Commission reports are missing data. For example, Patricia Goncalves should have ~1,250 orders in commission reports but only 27 are appearing.

---

## What We Found

The data flows through 5 stages. We found blockers at multiple points:

```
ORDER → QB SYNC → QB INVOICE → QB PAYMENT → COMMISSION REPORT
  ✅       ⚠️          ⚠️           ❌              ❌
```

### Stage-by-Stage Breakdown

| Stage | What Happens | Status | Issue |
|-------|--------------|--------|-------|
| 1. Order Created | Customer places order in Creatio | ✅ Working | - |
| 2. Sync to QB | Order sent to QuickBooks as invoice | ⚠️ Partial | QB Web Connector offline |
| 3. Invoice in QB | Invoice exists in QuickBooks | ⚠️ Partial | 637 orders never synced (bug) |
| 4. Payment in QB | Accounting marks invoice as paid | ❌ Blocked | Only 2% of invoices paid |
| 5. Commission Report | Payment data appears in report | ❌ Missing | No payment = no commission |

---

## The Numbers

### Today's Sync Results (Jan 2026 Orders)

| Status | Orders |
|--------|--------|
| Successfully synced to QB | 336 |
| Failed - QB offline | 157 |
| **Total January orders** | ~500+ |

### Historical Issue

| Problem | Count |
|---------|-------|
| Orders marked "synced" but actually never synced | **637** |
| Date range | Aug 2023 - Jan 2026 |

### Patricia Goncalves Example

| What We Have | Count | % |
|--------------|-------|---|
| Orders assigned to Patricia | 1,250 | 100% |
| Orders with invoices in QB | ~400? | ~30%? |
| Invoices PAID in QB | 27 | **2.2%** |
| Shows in commission report | 27 | 2.2% |

**97.8% of Patricia's commission is missing because invoices aren't marked as paid in QuickBooks.**

---

## What's Blocking Things

### 1. QB Web Connector is Offline (IT Issue)

- Server `96.56.203.106:8080` is not responding
- Last successful sync: Jan 20 at 8:43 PM
- 157 orders stuck waiting to sync

### 2. Historical Sync Bug (Code Issue)

- 637 orders were marked as "synced" but never actually made it to QB
- The sync code has a bug: marks "success" even when connection fails
- These orders from Aug 2023 - Jan 2026 need to be re-synced

### 3. QB Invoices Not Marked as Paid (Accounting Issue)

- This is the **biggest blocker**
- Invoices exist in QuickBooks but haven't been processed as paid
- Commission sync only pulls PAYMENT data, not invoice data
- Until invoices are paid in QB, they won't appear in commission reports

---

## Who Needs to Do What

### IT / QB Team (URGENT)

1. **Get QB Web Connector back online**
   - Check server at `96.56.203.106`
   - Restart "QuickBooks Web Connector" Windows service
   - Verify port 8080 is accessible

2. **After it's online:** We'll run a SQL script to reset the 637 stuck orders

### QB Accounting Team (URGENT)

3. **Process invoice payments in QuickBooks**
   - Especially December 2025 and January 2026 invoices
   - This is the #1 reason commission data is missing
   - Once invoices are marked paid → commission data will flow

### e6Solutions (Long-term)

4. **Fix the sync bug** that marks orders as "synced" when connection fails

---

## What We Fixed Today

| Fix | Result |
|-----|--------|
| Fixed BGHasQuickBooksLog flags | 626 orders now eligible for sync |
| Fixed ProcessListeners flags | 626 orders can trigger sync |
| Created log entries | 658 orders queued for sync |
| Ran QB sync | 336 orders successfully synced |

---

## Current Commission Data Available

| Month | Records | Commission $ |
|-------|---------|-------------|
| January 2026 | 350 | $13,832 |
| December 2025 | 115 | $4,888 |
| February 2026+ | 34 | $4,518 |

This data IS in the reports. The gap is the thousands of orders that haven't flowed through yet.

---

## Next Steps

1. **IT:** Bring QB Web Connector online
2. **Accounting:** Start processing invoice payments in QB
3. **Us:** Run sync processes after infrastructure is fixed
4. **Everyone:** Monitor commission data growth over next few days

---

---

## Can We Use QB Online Instead?

**Short answer: No.**

| Connection | Environment | Status |
|------------|-------------|--------|
| QB Desktop | **Production** | ❌ Offline |
| QB Online | Sandbox (test) | ⚠️ Wrong environment |

The QB Online connection in Creatio is configured for Intuit's **sandbox** (testing) environment, not production. All real data is in QB Desktop. Switching would require developer + QB admin work to reconfigure for production.

---

## What We Did From Creatio (Complete)

| Action | Result |
|--------|--------|
| Fixed BGHasQuickBooksLog flag | 626 orders |
| Fixed ProcessListeners flag | 626 orders |
| Created QB log entries | 658 orders |
| Synced orders to QB | 336 successfully synced |
| Reset retriable errors | Ready for retry |
| Verified new order flags | ✅ Working correctly |
| Checked QB connection config | Documented settings |
| Investigated QB Online alternative | Not viable (sandbox only) |

**We have done everything possible from Creatio.**

---

## Questions?

Full technical details in:
- `docs/QB_SYNC_INFRASTRUCTURE_ISSUE.md`
- `docs/COMMISSION_DATA_PIPELINE_ANALYSIS.md`

---

*Summary created: January 20, 2026*
*Updated: January 20, 2026 (late) - Added QB Online investigation*
