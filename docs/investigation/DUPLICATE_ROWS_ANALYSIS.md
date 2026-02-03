# Duplicate Rows Analysis: BGSalesByItemView vs BGItemsByCustomerView

**Date:** 2026-01-29
**Issue:** "Items by Customer" report showing duplicate rows (26x per line item)
**Root Cause:** Employee JOIN creates Cartesian product

---

## Executive Summary

The duplicate rows are caused by using `BGSalesByItemView` instead of the original `BGItemsByCustomerView`. The views have fundamentally different JOIN strategies:

| View | Employee Join | Duplicates? | Status |
|------|---------------|-------------|--------|
| **BGItemsByCustomerView** (Original) | ❌ None | No | Empty (no execution records) |
| **BGSalesByItemView** (Current) | ⚠️ All employees in sales group | Yes (26x) | Has data but wrong design |

---

## Root Cause Analysis

### BGSalesByItemView JOIN (Problematic)

```sql
JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id")
JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId")  -- ⚠️ ALL employees in group
```

This creates a Cartesian product: each order line is duplicated for EVERY employee in the sales group.

**Example:** If "Werner Frank" sales group has 26 employees, each order line appears 26 times.

### BGItemsByCustomerView JOIN (Correct Original Design)

```sql
FROM "Order" o
JOIN "Account" ac ON o."AccountId" = ac."Id"
JOIN "OrderStatus" os ON o."StatusId" = os."Id"
JOIN "OrderProduct" op ON op."OrderId" = o."Id"
JOIN "Product" p ON p."Id" = op."ProductId"
JOIN "BGReportExecution" re ON re."BGCustomerId" = ac."Id"
-- NO EMPLOYEE JOIN - No duplicates!
```

**Key insight:** The original "Items by Customer" report was designed WITHOUT sales rep information.

### Other Views with Correct Employee Join

Some views correctly join to a SPECIFIC employee:

```sql
JOIN "Employee" e ON o."BGSalesRepLookupId" = e."Id"  -- ✅ Specific sales rep
```

This joins to the ONE sales rep assigned to the order, not all employees in the group.

---

## Options Analysis

### Option 1: Fix BGItemsByCustomerView (Restore Original Design)

**Approach:** Make the original view work by creating BGReportExecution records

**Pros:**
- Original BGlobal design
- No duplicates by design
- Has proper column names (BGAccount, BGProduct, BGProductCode, BGLastPrice)
- Execution-based filtering built into view

**Cons:**
- Requires creating BGReportExecution records for each report run
- Need to update backend to create execution records
- More complex flow

**Effort:** High

### Option 2: Fix BGSalesByItemView SQL (Remove Employee Join)

**Approach:** Modify the view to remove or fix the Employee join

**Option 2A - Remove Employee columns entirely:**
```sql
-- Remove these lines:
-- JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id")
-- JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId")
-- Remove: sg."BGSalesGroupName" AS "BGSalesGroup"
-- Remove: e."Name" AS "BGSalesRep"
```

**Option 2B - Join to specific sales rep:**
```sql
-- Replace:
JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId")
-- With:
LEFT JOIN "Employee" e ON (o."BGSalesRepLookupId" = e."Id")
```

**Pros:**
- Fixes root cause
- Simple SQL change
- Maintains existing column structure (mostly)

**Cons:**
- Modifies shared view (may affect other reports)
- Need to verify other reports using this view still work

**Effort:** Low-Medium

### Option 3: Add DISTINCT to Backend ESQ

**Approach:** Add DISTINCT to the ESQ query in UsrExcelReportService.cs

```csharp
esq.IsDistinct = true;
```

**Pros:**
- No SQL view changes
- Quick fix
- Isolated to "Items by Customer" report

**Cons:**
- Masks the underlying issue
- Performance overhead (DISTINCT on large datasets)
- May not work correctly if rows have subtle differences

**Effort:** Low

### Option 4: GROUP BY in Backend

**Approach:** Aggregate results in the backend code after querying

```csharp
var groupedResults = results
    .GroupBy(r => new { r.BGCustomer, r.BGItem, r.BGProductDescription })
    .Select(g => new {
        g.Key.BGCustomer,
        g.Key.BGItem,
        g.Key.BGProductDescription,
        BGQuantity = g.Sum(x => x.BGQuantity),
        BGAmount = g.Sum(x => x.BGAmount)
    });
```

**Pros:**
- No SQL view changes
- Full control over aggregation logic
- Can handle edge cases

**Cons:**
- More complex backend code
- Processing overhead
- May not match VBA aggregation exactly

**Effort:** Medium

### Option 5: Create New Dedicated View

**Approach:** Create `BGSalesByItemViewV2` without Employee join for "Items by Customer"

**Pros:**
- Clean separation
- Doesn't affect other reports
- Can optimize specifically for this report

**Cons:**
- Another view to maintain
- Need to update IntExcelReport config
- Duplication of logic

**Effort:** Medium

---

## Recommendation: Option 2B (Fix Employee Join)

**Best for Future:** Modify `BGSalesByItemView` to use the correct Employee join:

```sql
-- Current (WRONG - joins all employees in group):
JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId")

-- Fixed (CORRECT - joins specific sales rep):
LEFT JOIN "Employee" e ON (o."BGSalesRepLookupId" = e."Id")
```

**Rationale:**
1. **Fixes root cause** - No more Cartesian product
2. **Maintains functionality** - Still has BGSalesRep column
3. **Low risk** - LEFT JOIN handles orders without sales rep
4. **Consistent** - Matches pattern used in other working views
5. **Performance** - No DISTINCT/GROUP BY overhead

---

## Impact Assessment

### Reports Using BGSalesByItemView

| Report | Would Fix Help? |
|--------|-----------------|
| Items by Customer | ✅ Yes - removes duplicates |
| Rpt Sales By Item | ✅ Yes - removes duplicates |
| Rpt Sales By Item By Type Of Customer | ✅ Yes - removes duplicates |

### Verification Query

After fix, run:
```sql
SELECT "BGCustomer", "BGItem", COUNT(*) as cnt
FROM "BGSalesByItemView"
WHERE "BGCustomer" = 'Sisters'
GROUP BY "BGCustomer", "BGItem"
HAVING COUNT(*) > 1;
```

Should return 0 rows if fix is successful.

---

## Implementation Plan

### Step 1: Backup Current View
```sql
-- Save current definition
SELECT pg_get_viewdef('"BGSalesByItemView"', true);
```

### Step 2: Apply Fix
```sql
DROP VIEW IF EXISTS "BGSalesByItemView";
CREATE VIEW "BGSalesByItemView" AS
SELECT
  o."Id",
  o."CreatedOn",
  o."CreatedById",
  o."ModifiedOn",
  o."ModifiedById",
  o."ProcessListeners",
  o."Number" AS "BGNumber",
  o."BGPONumber",
  o."BGShipDate",
  o."BGDeliveryDate",
  op."Price" AS "BGPrice",
  op."TotalAmount" AS "BGAmount",
  p."Name" AS "BGItem",
  p."Description" AS "BGProductDescription",
  op."Quantity" AS "BGQuantity",
  ac."Name" AS "BGCustomer",
  os."Name" AS "BGStatus",
  sg."BGSalesGroupName" AS "BGSalesGroup",
  e."Name" AS "BGSalesRep"
FROM
  "Order" o
  JOIN "Account" ac ON (o."AccountId" = ac."Id")
  JOIN "OrderStatus" os ON (o."StatusId" = os."Id")
  JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id")
  LEFT JOIN "Employee" e ON (o."BGSalesRepLookupId" = e."Id")  -- FIXED: Specific sales rep
  JOIN "OrderProduct" op ON (op."OrderId" = o."Id")
  JOIN "Product" p ON (p."Id" = op."ProductId")
WHERE
  o."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'::uuid
  AND sg.* IS NOT NULL
  AND os."Id" IN (
    '29fa66e3-ef69-4feb-a5af-ec1de125a614',
    '40de86ee-274d-4098-9b92-9ebdcf83d4fc',
    '8ab0f830-908b-40d7-80a3-7f49ef70ce70'
  );
```

### Step 3: Verify
```sql
-- Check for duplicates
SELECT "BGCustomer", "BGItem", "BGNumber", COUNT(*)
FROM "BGSalesByItemView"
GROUP BY "BGCustomer", "BGItem", "BGNumber"
HAVING COUNT(*) > 1
LIMIT 10;
```

### Step 4: Test Reports
- Test "Items by Customer"
- Test "Rpt Sales By Item"
- Test "Rpt Sales By Item By Type Of Customer"

---

## Summary

| Option | Effort | Risk | Fixes Root Cause | Recommended |
|--------|--------|------|------------------|-------------|
| 1. Fix BGItemsByCustomerView | High | Medium | ✅ | No |
| **2B. Fix Employee Join** | Low | Low | ✅ | **Yes** |
| 3. DISTINCT in Backend | Low | Low | ❌ | No |
| 4. GROUP BY in Backend | Medium | Medium | ❌ | No |
| 5. Create New View | Medium | Low | ✅ | No |

**Recommendation: Option 2B** - Fix the Employee join in BGSalesByItemView to use the specific sales rep instead of all employees in the sales group.

---

---

## Investigation Update (2026-01-29)

### Cross-View Analysis Complete ✅

Checked ALL views for Employee JOIN pattern:

| View | JOIN Pattern | Status |
|------|--------------|--------|
| **BGSalesByItemView** | `sg."Id" = e."BGSalesGroupLookupId"` | ⚠️ **ONLY BUG** |
| BGSalesByCustomerView | `o."BGSalesRepLookupId" = e."Id"` | ✅ Correct |
| BGSalesByItemLineView | `o."BGSalesRepLookupId" = e."Id"` | ✅ Correct |
| BGSalesBySalesGroupView | `o."BGSalesRepLookupId" = e."Id"` | ✅ Correct |
| BGCommissionReportDataView | Uses BGCommissionEarner | ✅ Correct |

**Conclusion:** Only BGSalesByItemView needs the fix. All other views use the correct pattern.

### Fix Script Created

**File:** `sql/VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql`

Run in pgAdmin to apply the fix.

---

*Created: 2026-01-29*
*Investigator: Claude Code*
