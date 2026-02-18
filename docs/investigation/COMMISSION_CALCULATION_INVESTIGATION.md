# Commission Calculation Investigation

**Date:** 2026-02-03
**Purpose:** Ensure IWPayments commission fields are correctly populated
**Status:** 🔍 Investigation Complete

---

## Executive Summary

The commission calculation system consists of:
1. **BGCommissionEarner** - Links Order → Sales Rep → Commission Rate (supports multiple earners)
2. **IWPayments** - Stores calculated commission data
3. **Business Process (V2)** - Calculates and updates commission when Payment is added/modified/deleted

**Current Issue:** V2 process only triggers on Payment changes, NOT on Order changes. V3 has Order trigger but causes 26x duplicates.

---

## Entity Relationship Map

```
┌──────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                     │
└──────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────┐
                    │       ORDER         │
                    ├─────────────────────┤
                    │ Amount              │ ← Total order value
                    │ BGSubTotal          │ ← Subtotal (pre-tax)
                    │ BGShippingCharge    │ ← Shipping cost
                    │ BGSalesTaxFloat     │ ← Tax amount
                    │ BGTotalNoShipping   │ ← Total minus shipping
                    │ BGSalesRepLookupId  │ ← Primary sales rep
                    └─────────┬───────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ BGCommissionEarner│  │    INVOICE      │  │ (Multiple earners)│
├─────────────────┤  ├─────────────────┤  └─────────────────┘
│ BGOrderId       │  │ OrderId         │
│ BGSalesRepId    │  │ Amount          │
│ BGCommissionRate│  └────────┬────────┘
│ BGName          │           │
└─────────────────┘           ▼
                    ┌─────────────────────┐
                    │     IWPayments      │
                    ├─────────────────────┤
    QB-Populated →  │ IWAmount            │ ← Total payment
                    │ IWPaymentsInvoiceId │ ← Link to Invoice
                    │ IWAccountId         │ ← Customer account
                    ├─────────────────────┤
    Calculated →    │ IWSalesAmount       │ ← Commissionable amount
                    │ IWCommissionAmount  │ ← Calculated commission
                    │ IWCommissionCalculated │ ← True when done
                    │ IWCommissionStatus  │ ← "Done" / "Pending"
                    │ IWOwnerId           │ ← From Order.Owner
                    └─────────────────────┘
```

---

## Key Entities Analyzed

### 1. IWPayments (Payment Record)

| Column | Type | Source | Purpose |
|--------|------|--------|---------|
| **IWAmount** | Decimal | QuickBooks | Total payment amount |
| **IWSalesAmount** | Decimal | Calculated | Commissionable amount (excl. tax/shipping) |
| **IWCommissionAmount** | Decimal | Calculated | Commission = SalesAmount × Rate |
| **IWCommissionCalculated** | Boolean | Process | Flag: calculation complete |
| **IWCommissionStatus** | String | Process | "Done" or "Pending" |
| **IWPaymentsInvoiceId** | GUID | QuickBooks | Link to Invoice |
| **IWPaymentsFactoryOrderId** | GUID | - | Direct Order link (often empty) |
| **IWBGSalesRepId** | GUID | - | Sales rep (often empty) |
| **IWOwnerId** | GUID | Process | Copied from Order.Owner |

### 2. Order (Source of Commission Data)

| Column | Type | Purpose |
|--------|------|---------|
| **Amount** | Decimal | Total order amount |
| **BGSubTotal** | Decimal | Subtotal before tax |
| **BGShippingCharge** | Decimal | Shipping cost |
| **BGSalesTaxFloat** | Decimal | Tax amount |
| **BGTotalNoShipping** | Decimal | Total minus shipping |
| **BGSalesRepLookupId** | GUID | Primary sales rep |

### 3. BGCommissionEarner (Commission Rate Configuration)

| Column | Type | Purpose |
|--------|------|---------|
| **BGOrderId** | GUID | Link to Order |
| **BGSalesRepId** | GUID | Link to Sales Rep |
| **BGCommissionRate** | Decimal | Commission percentage (e.g., 15.0) |
| **BGName** | String | Display name (e.g., "Jim Martin 6%") |
| **BGAddedManually** | Boolean | Manual vs automated entry |

**Key Finding:** Multiple earners per Order are supported. Each earner has their own rate.

---

## Commission Calculation Formula

Based on process analysis:

```
IWSalesAmount = Order.Amount - Order.BGShippingCharge - Order.BGSalesTaxFloat
              = Commissionable base amount

IWCommissionAmount = IWSalesAmount × (BGCommissionEarner.BGCommissionRate / 100)
```

**Example from data:**
```
Payment.IWAmount = $560.00 (from QuickBooks)
Payment.IWSalesAmount = $486.96 (calculated)
Payment.IWCommissionAmount = $73.04
Implied Rate = $73.04 / $486.96 = 15.0%
```

---

## V4 Process Flow (Reference)

Based on process export analysis:

```
┌────────────────────┐
│   START SIGNALS    │
├────────────────────┤
│ • Payment Added    │──┐
│ • Payment Modified │──┼──► ReadDataUserTask1
│ • Payment Deleted  │──┘    (Read IWPayments)
└────────────────────┘           │
                                 ▼
                    ReadDataUserTask2
                    (Read Order via Payment.Order)
                                 │
                                 ▼
                    ReadDataUserTask4
                    (Read BGCommissionEarner)
                                 │
                                 ▼
                    ┌─────────────────────┐
                    │   Decision Gates    │
                    │ • Has Order Total?  │
                    │ • Is Payment Return?│
                    │ • Has Commission Rate?│
                    └──────────┬──────────┘
                               │
                               ▼
                    FormulaTask (Calculate)
                    • Sales Amount = Order.Amount - Tax - Shipping
                    • Commission = SalesAmount × Rate
                               │
                               ▼
                    ChangeDataUserTask1
                    (Update IWPayments)
                    • IWCommissionAmount ← calculated
                    • IWSalesAmount ← calculated
                    • IWCommissionCalculated ← True
                    • IWCommissionStatus ← "Done"
                    • IWOwnerId ← Order.Owner
                               │
                               ▼
                         [ END ]
```

---

## Current Trigger Analysis

### API-Verified Process Inventory (2026-02-05 Updated)

Queried via DataService API against DEV (`dev-pampabay.creatio.com`):

| Process Name | Code | Enabled | Package |
|--------------|------|---------|---------|
| IW Calculate Commission on Payment (V1) | IWCalculateCommissiononPayment | ✅ True | IWQBIntegration |
| **IW Calculate Commission on Payment V2** | IWCalculateCommissiononPaymentV2 | ✅ True | IWQBIntegration |
| **IW Calculate Commission on Payment V3** | IWCalculateCommissiononPaymentV3 | ⚠️ True | IWQBIntegration |
| **IW Calculate Commission on Payment V4** | IWCalculateCommissiononPaymentV4 | ✅ True | IWQBIntegration |
| IWRecalculateCommissionOnOrderChange (V1) | IWRecalculateCommissionOnOrderChange | ✅ True | IWQBIntegration |
| **IWRecalculateCommissionOnOrderChangeV2** | IWRecalculateCommissionOnOrderChangeV2 | ✅ True | IWQBIntegration |

**⚠️ Critical Finding (2026-02-05):** All 4 versions of the main commission process exist and show Enabled=True! V3 has the "any field" trigger that causes 26x cascade - must be disabled before PROD import.

**Key Discovery:** The Order-triggered subprocess (`IWRecalculateCommissionOnOrderChangeV2`) already exists and is ENABLED in DEV!

### V2 Payment Process (Current Active)

| Trigger | Entity | Fields | Status |
|---------|--------|--------|--------|
| Payment Added | IWPayments | Any | ✅ Active |
| Payment Modified | IWPayments | Any | ✅ Active |
| Payment Deleted | IWPayments | Any | ✅ Active |

### Order Change Subprocess (V1 and V2 both exist)

| Version | Status | Notes |
|---------|--------|-------|
| V1 (`IWRecalculateCommissionOnOrderChange`) | ✅ ENABLED | Original - may have cascade issue |
| V2 (`IWRecalculateCommissionOnOrderChangeV2`) | ✅ ENABLED | Likely has filtered trigger |

**⚠️ WARNING:** Both V1 and V2 of the Order change process are ENABLED. This could cause duplicate commission calculations when Order totals change.

### V3 Process Status

V3 (`IWCalculateCommissiononPaymentIWQBIntegrationV3`) was **NOT FOUND** in DEV under the expected name. The V3 cascade bug documentation may refer to a different process or a previously-deleted version.

**Problem (Historical):** V3's Order trigger fired on ANY Order change (even Description), causing commission recalculation for ALL linked Payments.

---

## Gap Analysis (Updated 2026-02-05)

### What Works ✅

1. Commission calculates correctly when Payment is added/modified
2. Multiple commission rates supported via BGCommissionEarner
3. Tax and shipping excluded from commissionable amount
4. Commission status tracking works
5. **Order change subprocess EXISTS** - `IWRecalculateCommissionOnOrderChangeV2` is deployed in DEV

### Resolved Gaps ✅

| Gap | Resolution | Status |
|-----|------------|--------|
| **No Order change trigger** | `IWRecalculateCommissionOnOrderChangeV2` exists | ✅ DEPLOYED |
| **No filtered Order trigger** | V2 subprocess likely implements filtered trigger | ✅ EXISTS (verify config) |

### Remaining Issues ⚠️

| Issue | Impact | Priority |
|-------|--------|----------|
| **V3 not found** | Documentation refers to missing process | 🟡 MEDIUM |
| **IWBGSalesRepId not populated** | Payment doesn't know its commission earner | 🟢 LOW |

### Clarification: "Actual Version" vs "Enabled"

In Creatio, a process can be **Enabled** but only the one marked as **Actual version** will execute.

| Process | Enabled | Actual Version | Will Execute? |
|---------|---------|----------------|---------------|
| V1 Payment | ✅ | ❌ | No |
| **V2 Payment** | ✅ | ✅ | **Yes** |
| V1 Order Change | ✅ | ❌ | No |
| **V2 Order Change** | ✅ | ✅ | **Yes** |

**Result:** Only V2 processes execute. V1 being "Enabled" is not a concern.

### Action Required

Before PROD import, verify in DEV:
1. ✅ V2 is set as Actual version (confirmed via API)
2. ✅ `IWRecalculateCommissionOnOrderChangeV2` uses filtered trigger (**BROWSER-VERIFIED 2026-02-05**)
   - Signal: "In any of the selected fields"
   - Fields monitored: Amount with Discount, Shipping Charge, Sub Total, Tax Amount, Total
3. ✅ **Conditional flow formulas corrected** (BROWSER-VERIFIED 2026-02-05)
   - "No": `[#Read Payments.Number of records#]==0`
   - "Order Deleted": `[#Order Deleted.Unique identifier of record#]!=Guid.Empty && [#Read Payments.Number of records#]>0`
   - "Order Added or Modified": `([#Order Modified.Unique identifier of record#]!=Guid.Empty || [#Order Added.Unique identifier of record#]!=Guid.Empty) && [#Read Payments.Number of records#]>0`
4. Test that only ONE process fires per event
5. ⚠️ Set subprocess as "Actual version" before testing with V4

---

## Recommendations (Updated 2026-02-05)

### ✅ Option B Already Implemented!

API discovery revealed that **IWRecalculateCommissionOnOrderChangeV2** already exists in DEV. This is exactly what we recommended in `FILTERED_ORDER_TRIGGER_DESIGN.md`.

### Current Recommendation: Verify and Consolidate

**Phase 0 Actions (Before PROD Import):**

1. **Verify V2 Order subprocess uses filtered trigger:**
   - Open `IWRecalculateCommissionOnOrderChangeV2` in Process Designer
   - Confirm Signal Start Event monitors ONLY: Amount, BGSubTotal, BGShippingCharge, BGSalesTaxFloat
   - If it uses "In any field" → configure to use "In any of the selected fields"

2. **Disable V1 processes:**
   - Disable `IWCalculateCommissiononPayment` (V1)
   - Disable `IWRecalculateCommissionOnOrderChange` (V1)
   - Keep only V2 versions enabled

3. **Test in DEV:**
   - Create Order, add Payment → verify commission calculates once
   - Change Order.Amount → verify commission updates once (no duplicates)
   - Change Order.Description → verify NO commission recalculation

### Process Version Target State

| Process | Actual Version | Notes |
|---------|----------------|-------|
| IWCalculateCommissiononPayment (V1) | ❌ No | Won't execute |
| **IWCalculateCommissiononPaymentV2** | ✅ **Yes** | Active |
| IWRecalculateCommissionOnOrderChange (V1) | ❌ No | Won't execute |
| **IWRecalculateCommissionOnOrderChangeV2** | ✅ **Yes** | Active |

**Note:** "Enabled" status doesn't matter if not set as Actual version.

---

## IWRecalculateCommissionOnOrderChangeV2 Subprocess Verification (2026-02-05)

### Process Flow

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Order Modified  │   │  Order Added    │   │ Order Deleted   │
│    Signal       │   │    Signal       │   │    Signal       │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         └──────────┬──────────┴──────────┬──────────┘
                    │                     │
                    ▼                     │
           ┌─────────────────┐            │
           │   Read Order    │            │
           └────────┬────────┘            │
                    │                     │
                    ▼                     │
           ┌─────────────────┐            │
           │  Read Payments  │ ←──────────┘
           │ (Collection)    │   Filter: Order = Signal.RecordId (OR)
           └────────┬────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Payment Found?  │  (Exclusive Gateway)
           └───┬───────┬─────┘
               │       │
    ┌──────────┴──     │     ──┴──────────┐
    ▼                  ▼                  ▼
"No" Flow        "Order Added      "Order Deleted"
    │            or Modified"           │
    │                  │                 │
    ▼                  ▼                 ▼
  [END]      Set Pending       Set "Order Deleted"
               (All Payments)    (All Payments)
```

### Conditional Flow Formulas

| Flow | Formula | Purpose |
|------|---------|---------|
| **"No"** | `[#Read Payments.Number of records#]==0` | Skip if no payments linked |
| **"Order Deleted"** | `[#Order Deleted.Unique identifier of record#]!=Guid.Empty && [#Read Payments.Number of records#]>0` | Handle deleted orders |
| **"Order Added or Modified"** | `([#Order Modified...#]!=Guid.Empty \|\| [#Order Added...#]!=Guid.Empty) && [#Read Payments.Number of records#]>0` | Trigger recalculation |

### Modify Data Configuration

Both "Set Commission status to Pending" and "Set Commission Status to Order Deleted" use:
- **Filter:** `Order = [#Read Order.First item of resulting collection.Id#]`
- **Effect:** Updates ALL payments linked to the Order (handles multiple payments correctly)

### Remaining: Set as Actual Version

The subprocess currently has "Actual version" = false. To enable:
1. Open Process Designer
2. Check "Actual version" checkbox
3. Save process

---

## IW Calculate Commission on Payment V2 Main Process Analysis (2026-02-05)

### Update Payment "Done" Element Configuration

Based on IWQBIntegration package extraction analysis (`investigation/IWQBIntegration/full_content.txt`):

| Column Set | Source | Purpose |
|------------|--------|---------|
| **Commission Amount** | `[#Commission Amount#]` parameter | Calculated commission value |
| **Calculated Sales Amount** | `[#Calculated Sales Amount#]` parameter | Commissionable base |
| **Commission Calculated** | Boolean True | Flag indicating calculation done |
| **Commission Status** | "Done" (localized text value) | Status lookup |
| **Owner** | `Read Order Record.First item.Owner` | Order's owner copied to payment |

### Update Payment "Returned" Element

Sets Commission Status = "Returned" for returned payments.

### Process Elements Verified

| Element | Purpose | Configuration |
|---------|---------|---------------|
| Read Payments Record | Get payment by ID | Filter: Id = Signal.RecordId |
| Read Order Record | Get linked Order | Via Payment.Invoice.Order chain |
| Read BGCommissionEarner | Get commission rate | Filter: Order = Current Order |
| Update Payment "Done" | Set calculated values | 5 columns as above |
| Update Payment "Returned" | Handle refunds | Sets status to "Returned" |

### IWCommissionStatusLookup Environment Status

| Environment | Status | Notes |
|-------------|--------|-------|
| **DEV** | ✅ EXISTS | IWQBIntegration already imported |
| **PROD** | ❌ Missing | Will be created when IWQBIntegration imports |

---

## IW Commission Status Lookup (Complete Reference)

**Schema Name:** `IWCommissionStatusLookup` (Package: IWQBIntegration)

| Status | Description | GUID | Set By |
|--------|-------------|------|--------|
| **Pending** | Awaiting calculation | `930bb1c6-ca67-4ac0-8f96-a5ea4018a366` | Subprocess |
| **Done** | Calculated successfully | `deb80242-b56a-4b94-967a-0e170e2198d8` | V2/V4 Main Process |
| **Error** | Calculation failed | `26c1b9de-75c9-46c7-8963-e02b8a63f261` | V4 (future) |
| **Order Deleted** | Order was deleted | `8c2313f4-7e27-4781-afef-d16deb90cc6d` | Subprocess |
| **Returned** | Payment returned/refunded | `ee14b2ce-163a-4fb2-abea-e739636794ed` | V2/V4 Main Process |

**API Verified (2026-02-05):** All 5 values confirmed in DEV via DataService query.

### Status Ownership Architecture

```
Subprocess (Order triggers)     V4 (Payment triggers + calculation)
─────────────────────────────   ────────────────────────────────────
• Pending (Add/Modify)          • Done (success)
• Order Deleted (Delete)        • Error (failure) [future]
                                • Returned (refund) [future]
```

---

## Fields from QuickBooks vs Calculated

### Populated by QuickBooks Sync

| Field | Source |
|-------|--------|
| IWAmount | QB Payment amount |
| IWPaymentsInvoiceId | QB Invoice link |
| IWAccountId | QB Customer |
| IWQBInvoiceNumber | QB Invoice number |
| IWPaymentNumber | QB Payment number |
| IWMemo | QB Memo |

### Calculated by Business Process

| Field | Calculation |
|-------|-------------|
| IWSalesAmount | Order.Amount - Tax - Shipping |
| IWCommissionAmount | IWSalesAmount × BGCommissionEarner.BGCommissionRate |
| IWCommissionCalculated | True (after calculation) |
| IWCommissionStatus | "Done" (after calculation) |
| IWOwnerId | Order.Owner (copied) |

---

## Next Steps

1. **Decide on approach** (A, B, or C above)
2. **If Option A:** Modify V2 process to add filtered Order trigger
3. **Test thoroughly** in DEV before PROD
4. **Create system settings** for enable/disable flags
5. **Document the final configuration**

---

## V3 Process Element-by-Element Map (2026-02-05)

**Source:** Extracted from `investigation/IWQBIntegration/full_content.txt` lines 19345-19476 and 44775-45250

### V3 Identification

| Property | Value |
|----------|-------|
| **Process Name** | IW Calculate Commission on Payment V3 |
| **Code** | IWCalculateCommissiononPaymentIWQBIntegrationV3 |
| **UId** | `9b615e60-1124-4dc1-8d70-607fcb1a9412` |
| **Parent (V1) UId** | `c2623b8a-338e-4adb-afbe-cb76b68368d9` |
| **IsActiveVersion** | True (⚠️ DANGER) |

### Signal Start Events

| Element | Caption | Trigger Entity | 🚨 Issue |
|---------|---------|----------------|----------|
| `StartSignal1` | Payment Modified | IWPayments | ✅ Safe |
| `StartSignal2` | Payment Added | IWPayments | ✅ Safe |
| `StartSignal3` | Payment Deleted | IWPayments | ✅ Safe |
| **`StartSignal4`** | **Order Modified** | **Order** | **⚠️ 26x CASCADE!** |

**🚨 CRITICAL:** V3's `StartSignal4` (Order Modified) is the root cause of the 26x cascade bug. When ANY Order field changes, V3 fires and recalculates commission for ALL payments linked to that Order via:

```
Filter: IWPaymentsInvoice IN [Order Modified.Unique identifier of record]
```

This means every Order save triggers commission recalculation for ALL linked payments, not just once per order!

### Read Data Elements

| Element | Caption | Entity | Purpose |
|---------|---------|--------|---------|
| `ReadDataUserTask1` | Read Payments Record | IWPayments | Get payment data |
| `ReadDataUserTask2` | Read Order Record | Order | Get order totals for calculation |
| `ReadDataUserTask4` | Read Commission Rate | BGCommissionEarner | Get commission percentage |

**ReadDataUserTask1 Filter Logic (OR):**
1. `Id = [Payment Modified.Unique identifier of record]`
2. `Id = [Payment Added.Unique identifier of record]`
3. `Id = [Payment Deleted.Unique identifier of record]`
4. `IWPaymentsInvoice IN [Order Modified.Unique identifier of record]` ← **RETURNS MULTIPLE!**

### Exclusive Gateways (Decision Points)

| Element | Caption | Purpose |
|---------|---------|---------|
| `ExclusiveGateway1` | Does Order Commission Earner have Commission Rate? | Check if earner exists |
| `ExclusiveGateway2` | Payment Return? | Check if payment is returned |
| `ExclusiveGateway3` | Order Total > 0? | Validate order has value |
| `ExclusiveGateway4` | Check Commission Status | Determine calculation path |

### Conditional Flows

| Element | Caption | Condition |
|---------|---------|-----------|
| `ConditionalSequenceFlow1` | Has Commission Rate | `Commission Rate > 0` |
| `ConditionalSequenceFlow2` | Has Total | `Order.Total > 0` |
| `ConditionalSequenceFlow3` | SalesAmount < 0 | `Calculated < 0` (refund scenario) |
| `ConditionalSequenceFlow5` | Status = "Returned" | `Payment status is Returned` |

### Default Flows (Else paths)

| Element | Caption | Purpose |
|---------|---------|---------|
| `DefaultSequenceFlow1` | No Commission Rate | Skip calculation |
| `DefaultSequenceFlow2` | Not Returned | Normal path |
| `DefaultSequenceFlow3` | Has no Total or 0 | Skip zero orders |
| `DefaultSequenceFlow4` | Status ≠ "Returned" | Normal payment |

### Change Data (Modify Data) Elements

| Element | Caption | Sets Columns |
|---------|---------|--------------|
| `ChangeDataUserTask1` | Update Payment "Done" | CommissionAmount, SalesAmount, Calculated=True, **Status="Done" (text!)** |
| `ChangeDataUserTask2` | Payment is Returned | **Status="Returned" (text!)** |
| `ChangeDataUserTask3` | Update Payment "Returned" | **Status="Returned" (text!)** |
| `ChangeDataUserTask4` | Set Unapplied Amount from Order | UnappliedAmount |

**⚠️ BUG:** V3 sets IWCommissionStatus as TEXT ("Done", "Returned") not as LOOKUP GUID!

**Column GUIDs:**
- `aa12655b-577a-45a4-993a-23c424308504` → Status column (sets "Done")
- `7da555c2-13d2-40a7-9431-67d417a32056` → Status column (sets "Returned")
- `98baee38-7df2-4759-a1eb-7d23f9e206a2` → Status column (sets "Returned")

### Formula Tasks

| Element | Caption | Purpose |
|---------|---------|---------|
| `FormulaTask1` | Calculate Sales Amount | `Order.Amount - Tax - Shipping` |
| `FormulaTask2` | Set Sales Amount | Store result in parameter |
| `FormulaTask3` | Calculate Commission Amount | `SalesAmount × Rate` |

### Process Parameters

| Parameter | Type | Source/Usage |
|-----------|------|--------------|
| `CalculatedSalesAmount` | Decimal | Stores commission base amount |
| `CommissionAmount` | Decimal | Stores calculated commission |
| `CommissionRate` | Decimal | `[#Read Commission Rate.First item.Commission Rate#]` |

---

## V3 vs V4 Comparison

| Feature | V3 | V4 |
|---------|-----|-----|
| Payment Added trigger | ✅ | ✅ |
| Payment Modified trigger | ✅ | ✅ |
| Payment Deleted trigger | ✅ | ✅ |
| **Order Modified trigger** | ⚠️ **YES (causes 26x)** | ❌ **No (safe)** |
| Status set as | Text ("Done") | Should be Lookup |
| Is Active Version | True | True |

**Conclusion:** V4 removed the problematic Order trigger and is safer. However, V3 is currently the "Actual Version" in DEV that executes.

---

## V3 Required Edits (Corrective Actions)

### Option A: Fix V3 In-Place

If keeping V3 as actual version:

1. **DELETE `StartSignal4` (Order Modified)**
   - This removes the 26x cascade trigger
   - Keep only Payment triggers

2. **Fix Status Column Updates**
   - Change from text "Done" to lookup GUID: `deb80242-b56a-4b94-967a-0e170e2198d8`
   - Change from text "Returned" to lookup GUID: `ee14b2ce-163a-4fb2-abea-e739636794ed`

3. **Add Subprocess Call (Optional)**
   - After Update Payment "Done", call `IWRecalculateCommissionOnOrderChangeV2`
   - Or rely on subprocess's independent Order triggers

### Option B: Switch to V4 (Recommended)

1. Set V4 as "Actual Version"
2. Disable V3
3. Fix V4's status columns to use lookup GUIDs
4. Ensure subprocess V2 is enabled for Order changes

---

## Related Documents

- `FILTERED_ORDER_TRIGGER_DESIGN.md` - **Implementation design for Option A** ⭐
- `IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` - Import procedure
- `IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` - V3 cascade root cause
- `IWQBINTEGRATION_CONFLICT_ASSESSMENT.md` - Risk analysis
