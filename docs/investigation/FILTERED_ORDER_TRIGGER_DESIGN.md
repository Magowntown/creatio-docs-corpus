# Filtered Order Trigger Design for Commission V2

**Date:** 2026-02-05
**Status:** 📋 DESIGN COMPLETE - Ready for Implementation
**Purpose:** Add Order change trigger to V2 commission process without causing 26x cascade

---

## Executive Summary

This document specifies the exact Signal Start Event configuration needed to close the gap in V2 commission process where Order total changes don't trigger commission recalculation.

**The Solution:** Use Creatio's "In any of the selected fields" trigger option to monitor ONLY commission-affecting Order columns.

---

## Problem Statement

| Process | Order Trigger | Result |
|---------|---------------|--------|
| **V2 (Current Active)** | ❌ None | Order changes don't update Payment commission |
| **V3 (Disabled)** | "In any field" | 26x cascade - triggers on ANY Order change |

### Why V3 Causes 26x Cascade

V3's Signal Start Event (StartSignal4) monitors the Order entity with "In any field" option:
- ANY Order modification (even Description change) triggers the process
- Process runs for ALL Payments linked to that Order
- Result: One Order save → 26 commission recalculations

---

## Proposed Solution: Filtered Order Trigger

### Signal Start Event Configuration

Add a new Signal Start Event (StartSignal4) to V2 with these settings:

| Parameter | Value |
|-----------|-------|
| **Which type of signal is received?** | Object signal |
| **Object** | Order |
| **Which event should trigger the signal?** | Record modified |
| **Changes expected** | **In any of the selected fields** |
| **Fields to monitor** | (see table below) |
| **Run following elements in background** | ✅ Yes |

### Fields to Monitor (Commission-Affecting Only)

| Field Name | Column Code | Data Type | Why Monitor |
|------------|-------------|-----------|-------------|
| Amount | Amount | Decimal | Total order value |
| Subtotal | BGSubTotal | Decimal | Pre-tax commissionable base |
| Shipping Charge | BGShippingCharge | Decimal | Excluded from commission |
| Sales Tax | BGSalesTaxFloat | Decimal | Excluded from commission |

**Formula Reference:**
```
IWSalesAmount = Order.Amount - Order.BGShippingCharge - Order.BGSalesTaxFloat
IWCommissionAmount = IWSalesAmount × (BGCommissionEarner.BGCommissionRate / 100)
```

### Fields NOT to Monitor (No Commission Impact)

| Field | Why Exclude |
|-------|-------------|
| Description | Text field, no commission impact |
| Status | Workflow field, no commission impact |
| Owner | Assignment field, no commission impact |
| CreatedOn/ModifiedOn | System fields |
| Notes | Text field, no commission impact |
| Customer | Lookup field, commission rates are per-Order not per-Customer |

---

## Process Flow After Trigger

When the filtered Order trigger fires:

```
┌─────────────────────────────────────────┐
│ StartSignal4: Order Modified            │
│ (Only on Amount/BGSubTotal/BGShipping/  │
│  BGSalesTaxFloat changes)               │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ ReadDataUserTask: Read Order            │
│ - Get Order record by [#StartSignal4.RecordId#]
│ - Fetch: Amount, BGSubTotal, BGShipping, Tax
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ ReadDataUserTask: Read Invoices         │
│ - Filter: OrderId = Order.Id            │
│ - Get all linked Invoices               │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ ReadDataUserTask: Read IWPayments       │
│ - Filter: IWPaymentsInvoiceId IN (Invoices)
│ - Get all Payments for this Order       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ ReadDataUserTask: Read BGCommissionEarner│
│ - Filter: BGOrderId = Order.Id          │
│ - Get commission rates for this Order   │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ FormulaTask: Calculate Commission       │
│ - SalesAmount = Amount - Shipping - Tax │
│ - CommissionAmount = SalesAmount × Rate │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ ModifyDataUserTask: Update IWPayments   │
│ - Set IWSalesAmount = calculated        │
│ - Set IWCommissionAmount = calculated   │
│ - Set IWCommissionCalculated = true     │
│ - Set IWCommissionStatus = "Done"       │
└────────────────┬────────────────────────┘
                 │
                 ▼
                END
```

---

## Implementation Options

### Option A: Modify V2 Process (Recommended)

Add StartSignal4 directly to existing V2 process.

**Pros:**
- Single process, single version to maintain
- Reuses existing read/calculate/update logic

**Cons:**
- Modifying production-active process
- Requires careful testing

### Option B: Create Subprocess

Create new `IWRecalculateCommissionOnOrderChange` subprocess with the filtered trigger.

**Pros:**
- V2 remains unchanged
- Easier to disable if issues occur
- Can be developed/tested independently

**Cons:**
- Two processes doing similar work
- Potential timing conflicts if both fire

### Option C: Create V5 Process

Create new V5 that includes both Payment triggers AND filtered Order trigger.

**Pros:**
- Clean slate, no legacy issues
- Can consolidate best parts of V2/V3/V4

**Cons:**
- Must disable V2 when enabling V5
- More migration work

---

## Recommended Approach: Option B (Subprocess)

Create a lightweight subprocess specifically for Order-triggered commission recalculation:

**Process Name:** `IWRecalculateCommissionOnOrderChange`

**Trigger:**
- Signal Start Event on Order
- "Record modified" event
- "In any of the selected fields": Amount, BGSubTotal, BGShippingCharge, BGSalesTaxFloat

**Logic:**
1. Read Order data
2. Find all Payments via Invoice chain
3. Recalculate commission for each
4. Update IWPayments records

**Enabling:**
- Enable this subprocess alongside V2
- V2 handles Payment changes, subprocess handles Order changes
- No overlap in triggers

---

## Academy-Documented Patterns (Creatio Best Practices)

> **Source:** `creatio-docs-full/markdown/*how-to-work-with-data*.md`

### Pattern 1: Read Data from Record That Triggered Process

When Signal Start Event fires, it provides the `Unique identifier of record` parameter containing the Order.Id.

**Configuration (ReadOrder element):**

| Parameter | Value |
|-----------|-------|
| Which data read mode to use? | **Read the first record in the selection** |
| Which object to read data from? | Order |
| Filter | Id = Compare with parameter → Signal.RecordId |
| How to sort records? | (not needed - Id filter returns single record) |
| Which columns to read? | **Read data from selected columns only** |
| Columns | Amount, BGSubTotal, BGShippingCharge, BGSalesTaxFloat |

**Academy Note:** "We recommend limiting the number of columns to read data from, as reading too many columns will affect process performance."

### Pattern 2: Read Linked Records (Order → Invoice Chain)

To get Invoices linked to the Order, use a second Read Data element.

**Configuration (ReadInvoices element):**

| Parameter | Value |
|-----------|-------|
| Which data read mode to use? | **Read collection of records** |
| Which object to read data from? | Invoice |
| Filter | OrderId = Compare with parameter → [#ReadOrder.Id#] |
| Read first ... records | 100 (or max expected invoices per order) |
| Which columns to read? | Read data from selected columns only |
| Columns | Id (for linking to Payments) |

**Academy Note:** "Reading more than 5000 records may cause performance issues."

### Pattern 3: Read Collection (Invoice → IWPayments Chain)

**Configuration (ReadPayments element):**

| Parameter | Value |
|-----------|-------|
| Which data read mode to use? | **Read collection of records** |
| Which object to read data from? | IWPayments |
| Filter | IWPaymentsInvoiceId IN [#ReadInvoices.Id collection#] |
| Read first ... records | 500 (or max expected payments) |
| Which columns to read? | Read data from selected columns only |
| Columns | Id, IWAmount, IWSalesAmount, IWCommissionAmount |

### Pattern 4: Read Commission Earner Data

**Configuration (ReadEarners element):**

| Parameter | Value |
|-----------|-------|
| Which data read mode to use? | **Read the first record in the selection** |
| Which object to read data from? | BGCommissionEarner |
| Filter | BGOrderId = Compare with parameter → [#ReadOrder.Id#] |
| Which columns to read? | Read data from selected columns only |
| Columns | BGCommissionRate, BGSalesRepId |

**Note:** If multiple earners exist per Order, change to "Read collection of records" and loop through each.

### Pattern 5: Modify Multiple Records

**Configuration (UpdatePayments element):**

| Parameter | Value |
|-----------|-------|
| Which object data to modify? | IWPayments |
| Modify all records that match condition | Id IN [#ReadPayments.Id collection#] |
| Which column values to set? | (see below) |

**Columns to set:**

| Column | Value Source |
|--------|--------------|
| IWSalesAmount | Formula parameter [#SalesAmount#] |
| IWCommissionAmount | Formula parameter [#CommissionAmount#] |
| IWCommissionCalculated | Lookup value → True |
| IWCommissionStatus | Text value → "Done" |
| IWOwnerId | Parameter → [#ReadOrder.OwnerId#] |

---

## Step-by-Step Configuration Guide

### In Creatio Process Designer:

1. **Create New Process**
   - Name: `IWRecalculateCommissionOnOrderChange`
   - Package: `IWQBIntegration`
   - Run: In Background

2. **Add Signal Start Event**
   - Drag Signal Start Event to canvas
   - Configure:
     - Type: Object signal
     - Object: Order
     - Event: Record modified
     - Changes expected: **In any of the selected fields**
     - Click "+Add column"
     - Add: `Amount`, `BGSubTotal`, `BGShippingCharge`, `BGSalesTaxFloat`

3. **Add Read Data Elements**
   - ReadOrder: Read single Order by signal's RecordId
   - ReadInvoices: Read Invoice collection where OrderId = Order.Id
   - ReadPayments: Read IWPayments collection where InvoiceId in Invoices
   - ReadEarners: Read BGCommissionEarner where BGOrderId = Order.Id

4. **Add Formula Task**
   ```
   SalesAmount = [#ReadOrder.Amount#] - [#ReadOrder.BGShippingCharge#] - [#ReadOrder.BGSalesTaxFloat#]
   CommissionAmount = SalesAmount * ([#ReadEarners.BGCommissionRate#] / 100)
   ```

5. **Add Modify Data Element**
   - Object: IWPayments
   - Filter: Id in [#ReadPayments collection#]
   - Set:
     - IWSalesAmount = [#SalesAmount#]
     - IWCommissionAmount = [#CommissionAmount#]
     - IWCommissionCalculated = true
     - IWCommissionStatus = "Done"

6. **Add End Event**

7. **Save and Publish**

---

## Testing Checklist

### Test 1: Filtered Trigger Fires on Target Fields

| Action | Expected | Actual |
|--------|----------|--------|
| Change Order.Amount | ✅ Process fires | |
| Change Order.BGSubTotal | ✅ Process fires | |
| Change Order.BGShippingCharge | ✅ Process fires | |
| Change Order.BGSalesTaxFloat | ✅ Process fires | |
| Change Order.Description | ❌ Process does NOT fire | |
| Change Order.Status | ❌ Process does NOT fire | |
| Change Order.Owner | ❌ Process does NOT fire | |

### Test 2: Commission Calculation Correct

| Scenario | Expected |
|----------|----------|
| Order.Amount increases | IWPayments.IWCommissionAmount increases |
| Order.BGShippingCharge increases | IWPayments.IWCommissionAmount decreases |
| Order.BGSalesTaxFloat increases | IWPayments.IWCommissionAmount decreases |

### Test 3: No Duplicate Processing

| Check | Expected |
|-------|----------|
| Single Order save | One process execution |
| Process Log entries | No duplicates |
| IWPayments updates | Each record updated once |

---

## Rollback Plan

If issues occur after enabling:

```sql
-- Quick disable: Turn off the subprocess
UPDATE "SysSchema"
SET "Enabled" = false
WHERE "Name" = 'IWRecalculateCommissionOnOrderChange';
```

V2 will continue handling Payment changes normally.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `COMMISSION_CALCULATION_INVESTIGATION.md` | Gap analysis |
| `IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` | V3 cascade root cause |
| `IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` | Import procedure |

---

## Academy Documentation Sources

These patterns are documented in the Creatio Academy (all available offline in `creatio-docs-full/markdown/`):

| Topic | File Pattern | Key Content |
|-------|--------------|-------------|
| **Signal Start Event** | `*signal-start-event*.md` | "In any of the selected fields" option |
| **Work with Data** | `*how-to-work-with-data*.md` | Read/Modify/Add/Delete patterns |
| **Read Data Element** | `*read-data-process*.md` | 4 read modes, filter configuration |
| **Modify Data Element** | `*modify-data-process*.md` | Batch update patterns |
| **Process Parameters** | `*use-process-parameters*.md` | Passing data between elements |
| **Conditional Flow** | `*conditional-flow*.md` | Decision gate configuration |
| **Formula Element** | `*formula*.md` | Calculation expressions |

### Quick Reference Commands

```bash
# Read Signal Start Event documentation
cat creatio-docs-full/markdown/docs_8.x_no-code-customization_bpm-tools_process-elements-reference_events_signal-start-event.md

# Read "Work with Data" use cases
cat creatio-docs-full/markdown/docs_8.x_no-code-customization_bpm-tools_process-element-use-cases_how-to-work-with-data.md

# Read Modify Data element reference
cat creatio-docs-full/markdown/0acbe2e61068999c__bpm-tools_process-elements-reference_system-actions_modify-data-process-element.md
```

---

*Design document created: 2026-02-05*
*Updated: 2026-02-05 - Added Academy-documented patterns*
