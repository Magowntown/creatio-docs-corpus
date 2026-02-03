# IWQBIntegration Deep Dive Analysis

**Date:** 2026-01-30
**Related:** IWQBINTEGRATION_CONFLICT_ASSESSMENT.md

---

## Deep Dive #1: Commission Process Version Comparison

### Version Evolution

| Aspect | V1 (Base) | V2 | V3 (QB) | V4 (Custom) |
|--------|-----------|----|----|-------------|
| **Total Lines** | ~2,743 | ~3,041 | ~3,112 | ~3,257 |
| **Parameters** | 72 | 78 | 79 | 84 |
| **ChangeDataUserTasks** | 2 | 3 | 3 | 4 |
| **Start Signals** | 3 | 3 | **4** | 3 |
| **Exclusive Gateways** | 3 | 4 | 4 | 4 |

### Key Differences

| Feature | V1 | V2 | V3 | V4 |
|---------|----|----|----|----|
| Payment Modified trigger | ✓ | ✓ | ✓ | ✓ |
| Payment Added trigger | ✓ | ✓ | ✓ | ✓ |
| Payment Deleted trigger | ✓ | ✓ | ✓ | ✓ |
| **Order Modified trigger** | ✗ | ✗ | **✓** | ✗ |
| Error handling | Basic | Enhanced | Enhanced | Enhanced |
| Additional validation | None | +1 task | +1 task | +2 tasks |

### Recommendation

- **For standard use:** V2 or V4
- **For QB integration with Order sync:** V3 (but see Deep Dive #2 warnings)
- **For custom multi-tier commission:** V4
- **NEVER enable multiple versions simultaneously**

---

## Deep Dive #2: V3 Order→Payment Cascade (26x Duplicate Root Cause)

### The Problem

**IWCalculateCommissiononPaymentIWQBIntegrationV3** has a unique `StartSignal4` that triggers on **ANY Order modification**. This causes commission recalculation for ALL Payments linked to that Order.

### The Cascade Path

```
User edits Order (any field: Description, Account, Territory, etc.)
    ↓
Order.OnUpdate trigger fires
    ↓
StartSignal4 receives event (NO FILTER - triggers on ANY field change)
    ↓
Process reads Order record
    ↓
Query: SELECT * FROM IWPayments WHERE IWPaymentsInvoice = [Order.Id]
    ↓
For EACH Payment found (e.g., 26 Payments):
    ├─ Recalculate commission
    ├─ Update Payment record
    ├─ Payment.OnUpdate fires
    └─ BGQuickBooksIntegrationLogDetail entry created
    ↓
Result: 1 Order edit = 26 log entries
```

### Why This Exists

**Likely Intent:** Keep commission synchronized when Order details change (e.g., Order.Amount recalculated, CommissionEarner changed).

**Design Flaw:** No filter to trigger ONLY on commission-affecting fields. Currently triggers on:
- Order.Description changed ❌ (doesn't affect commission)
- Order.Account changed ❌ (doesn't affect commission)
- Order.Territory changed ❌ (doesn't affect commission)
- Order.Amount changed ✓ (SHOULD trigger)
- Order.CommissionEarner changed ✓ (SHOULD trigger)

### Fix Options

1. **Disable StartSignal4** - Stop Order→Payment cascade entirely
2. **Add filter to StartSignal4** - Trigger only on commission-affecting columns
3. **Use V2 or V4 instead** - These don't have the Order trigger

### Impact Verification

To check if this is causing your 26x duplicates:
```sql
SELECT
    COUNT(*) as log_entries,
    "BGRecordId" as order_id,
    DATE_TRUNC('minute', "CreatedOn") as time_window
FROM "BGQuickBooksIntegrationLogDetail"
WHERE "CreatedOn" > NOW() - INTERVAL '24 hours'
GROUP BY "BGRecordId", DATE_TRUNC('minute', "CreatedOn")
HAVING COUNT(*) > 5
ORDER BY log_entries DESC;
```

If you see Orders with 26+ log entries in the same minute, this is the cause.

---

## Deep Dive #3: Invoice Race Condition Analysis

### Three Processes, Two Shared Fields

| Process | Trigger Entity | Writes `IWCreditedTotal` | Writes `IWInvoiceCheckbox` |
|---------|----------------|--------------------------|----------------------------|
| IWAccountCheckForInvoices | Invoice | ✗ | ✓ (always TRUE) |
| IWUpdateInvoiceCreditedTotalandCheckbox | InvoiceProduct | ✓ | ✓ (conditional) |
| IWUpdateInvoicePaymentAmountPayments | IWPayments | ✓ | ✗ |

### Race Condition #1: IWCreditedTotal (Lost Update)

**Scenario:** User adds Payment AND modifies InvoiceProduct simultaneously

```
T1: Process 3 reads Invoice (PaymentAmount=200, IWCreditedTotal=0)
T2: Process 2 reads Invoice (PaymentAmount=200, IWCreditedTotal=0)
T3: Process 3 calculates: PaymentAmount=300 (new payment added)
T4: Process 2 calculates: IWCreditedTotal=50 (based on STALE PaymentAmount=200)
T5: Process 3 writes: PaymentAmount=300
T6: Process 2 writes: IWCreditedTotal=50 (WRONG - should have used PaymentAmount=300)
```

**Result:** IWCreditedTotal calculated with outdated PaymentAmount value.

### Race Condition #2: IWInvoiceCheckbox (Write Conflict)

**Scenario:** Invoice modified AND InvoiceProduct modified

```
Process 1 logic: SET IWInvoiceCheckbox = TRUE (always)
Process 2 logic: IF IWCreditedTotal > 0 THEN SET IWInvoiceCheckbox = FALSE
```

**Execution Order A:**
1. Process 2 runs → Sets checkbox = FALSE (has credits)
2. Process 1 runs → Overwrites to TRUE
3. **Result:** Checkbox shows "Invoiced" incorrectly

**Execution Order B:**
1. Process 1 runs → Sets checkbox = TRUE
2. Process 2 runs → Overwrites to FALSE
3. **Result:** Checkbox shows "Has Credits" correctly

**The final value depends on execution order - non-deterministic!**

### Calculation Formula Inconsistency

Process 2 uses TWO different formula orderings:
```
Formula A: IWOwedAfterCredits = Amount - PaymentAmount - IWCreditedTotal
Formula B: IWOutstandingBalance = Amount - IWCreditedTotal - PaymentAmount
```

While mathematically equivalent, if intermediate values are used elsewhere, ordering matters.

### Confirmation: TRUE Race Condition

| Race Type | Present | Fields Affected |
|-----------|---------|-----------------|
| Lost Update | ✓ | IWCreditedTotal |
| Dirty Read | ✓ | PaymentAmount → IWCreditedTotal |
| Write Conflict | ✓ | IWInvoiceCheckbox |
| No Synchronization | ✓ | All shared fields |

### Fix Recommendations

**Option A: Merge Processes**
- Combine Process 2 + Process 3 into single atomic operation
- Single formula for IWCreditedTotal
- Remove Process 1's checkbox logic (let Process 2 handle it)

**Option B: Add Sequence Control**
- Define execution order: Process 3 → Process 2 → Process 1
- Add "wait for previous" mechanism
- Use database triggers for ordering

**Option C: Use Optimistic Locking**
- Add version/timestamp to Invoice record
- Processes check version before write
- Retry if version changed

---

## Summary: Critical Action Items

### Immediate (Before PROD Import)

| Priority | Action | Risk if Ignored |
|----------|--------|-----------------|
| P0 | Decide which commission version to enable (1 only) | Duplicate calculations, data corruption |
| P0 | Disable StartSignal4 in V3 OR switch to V2/V4 | 26x duplicate log entries on every Order edit |
| P1 | Audit Invoice processes, determine IWCreditedTotal owner | Incorrect invoice balances |
| P1 | Disable V1 tax process if V2 is authoritative | Duplicate tax status updates |

### Testing Required

| Test | Expected Result |
|------|-----------------|
| Edit Order (non-amount field) | NO commission recalculation (unless V3 intentional) |
| Add Payment to Invoice | IWCreditedTotal updated once (not multiple times) |
| Modify InvoiceProduct + Add Payment | No race condition, correct final values |
| Generate Commission Report | Correct data, no duplicates |

### Process Configuration Table

| Process | Should Be Active | Reason |
|---------|------------------|--------|
| IWCalculateCommissiononPayment (V1) | ☐ NO | Replaced by newer versions |
| IWCalculateCommissiononPaymentV2 | ☐ Maybe | Standard commission calculation |
| IWCalculateCommissiononPaymentIWQBIntegrationV3 | ☐ Careful | Has Order trigger - causes 26x issue |
| IWCalculateCommissiononPaymentCustomV4 | ☐ Maybe | Most complex, custom rules |
| BGSetOrderProductTaxStatusByOrderSalesTax | ☐ NO | Replaced by V2 |
| IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | ☐ YES | Current tax process |

---

*Deep dive analysis completed: 2026-01-30*
