# Comprehensive Investigation Summary

**Date:** 2026-01-29
**Analysis:** 5 parallel sub-agent investigations completed

---

## CRITICAL FINDING #1: ALL PROD Reports Use Execution-Based Pattern

**Every examined Excel report in PROD uses `BGExecutionId = @P1@` filter:**

| Report | PROD View | Filter | Works? |
|--------|-----------|--------|--------|
| Items by Customer | BGItemsByCustomerView | BGExecutionId = @P1@ | ⚠️ Only with filters |
| Rpt Sales By Item | BGSalesByItemLineView | BGExecutionId = @P1@ | ❌ VBA Type mismatch |
| Rpt Sales by Item Line | BGSalesByItemLineView | BGExecutionId = @P1@ | ❓ Untested |
| Rpt Sales By Item By Type | BGSalesByItemLineView | BGExecutionId = @P1@ | ❓ Untested |
| Commission | BGCommissionReportDataView | BGExecutionId = @P1@ | ✅ Working |

---

## CRITICAL FINDING #2: BGSalesByItemView Fix Has NO Impact

**The SQL fix we applied to BGSalesByItemView (Employee JOIN) does NOT affect ANY of the examined PROD reports!**

Why:
- Items by Customer → Uses BGItemsByCustomerView (not BGSalesByItemView)
- Rpt Sales By Item → Uses BGSalesByItemLineView (not BGSalesByItemView)
- All other examined reports → Use different views

**The fix we applied is essentially useless for current PROD configuration.**

---

## CRITICAL FINDING #3: Why Items by Customer Works WITH Filters

The custom generator (`GenerateSalesByItemWithFilters()`) **bypasses IntExcelExport entirely** when filters are present:

```
WITH filters present:
  → Custom generator triggers
  → Queries BGSalesByItemView directly (our code, not IntExcelReport config)
  → Returns data ✅

WITHOUT filters:
  → Falls back to IntExcelExport
  → Uses PROD IntExcelReport config (BGItemsByCustomerView)
  → BGItemsByCustomerView has 0 BGReportExecution records
  → Returns empty/malformed data ❌
  → VBA Type mismatch error
```

---

## CRITICAL FINDING #4: BGReportExecution Record Counts

| Report Name | BGReportExecution Records | Status |
|-------------|---------------------------|--------|
| Commission | **111 records** | ✅ Working |
| Sales By Sales Group | **3 records** | ✅ Working |
| Sales By Customer | **2 records** | ✅ Working |
| Sales Rep Monthly | **1 record** | ✅ Working |
| **Items by Customer** | **0 records** | ❌ Never populated |
| **IW_Commission** | **0 records** | ❌ Never populated |
| **Sales By Item** | **0 records** | ❌ Never populated |

**Commission works because it has 111 execution records. Other reports fail because they have ZERO.**

---

## CRITICAL FINDING #5: Backend Deployment Status Unknown

| Component | In Code Repo | Deployed to PROD? |
|-----------|--------------|-------------------|
| GenerateSalesByItemWithFilters() | ✅ Yes | ❓ Unknown |
| GenerateSalesByCustomerWithFilters() | ✅ Yes | ❓ Unknown |
| QuerySalesByItemData() column order fix | ✅ Yes | ❓ Unknown |
| BGSalesByItemView SQL fix | ✅ Yes | ✅ Applied today |

**Gap:** No deployment confirmation exists for backend code changes.

---

## ROOT CAUSE ANALYSIS

### Why "Rpt Sales By Item" Shows VBA Type Mismatch

1. User runs report WITHOUT filters
2. Custom generator doesn't trigger (no filters)
3. IntExcelExport takes over
4. IntExcelExport queries BGSalesByItemLineView with BGExecutionId filter
5. No BGReportExecution records exist for this report
6. Query returns empty or malformed data
7. VBA macro receives unexpected column structure
8. **Type mismatch error**

### Why "Items by Customer" Works WITH Filters But Fails WITHOUT

Same pattern - custom generator only triggers when filters are present.

---

## OPTIONS TO FIX

### Option A: Make Custom Generators Always Trigger (Recommended)

**Change in UsrExcelReportService.cs:**

```csharp
// CURRENT (only triggers with filters):
if (hasFilter)
{
    return GenerateSalesByItemWithFilters(userConnection, request);
}

// PROPOSED (always triggers):
return GenerateSalesByItemWithFilters(userConnection, request);
```

**Pros:**
- Bypasses broken IntExcelExport flow entirely
- Uses our tested code path
- Simple change

**Cons:**
- BGSalesByItemView has 4.8M rows
- Need pagination or Excel row limit handling

### Option B: Create BGReportExecution Records (Complex)

Implement the full Type A pattern:
1. Before report generation, create BGReportExecution record
2. Store filter values in execution record
3. Pass ExecutionId to IntExcelExport
4. View filters by ExecutionId

**Pros:**
- Matches BGlobal's original design
- Execution audit trail

**Cons:**
- Complex implementation
- Need to understand BGlobal's v7 pattern fully
- More code to maintain

### Option C: Change PROD IntExcelReport Configs (Medium)

Change IntEntitySchemaName from execution-based views to direct views:
- Items by Customer: BGItemsByCustomerView → BGSalesByItemView
- Rpt Sales By Item: BGSalesByItemLineView → BGSalesByItemView

**Pros:**
- No code changes
- Direct approach

**Cons:**
- BGSalesByItemView has Employee JOIN bug (just fixed)
- Still needs filter injection
- May break other things

---

## IMMEDIATE ACTION ITEMS

### Priority 1: Fix "Rpt Sales By Item" VBA Type Mismatch

**Root Cause:** Report uses BGSalesByItemLineView which requires BGReportExecution records that don't exist.

**Quick Fix:** Add routing for BGSalesByItemLineView in backend:

```csharp
// In Generate() method, add:
if (entitySchemaName == "BGSalesByItemLineView")
{
    return GenerateSalesByItemWithFilters(userConnection, request);
}
```

### Priority 2: Verify Backend Deployment

Check if `UsrExcelReportService_Updated.cs` is actually deployed to PROD:
1. Open PROD source code designer
2. Compare with local file
3. Document deployment status

### Priority 3: Decide on Long-Term Strategy

Choose between:
- Option A (always use custom generators)
- Option B (implement full execution pattern)
- Option C (change IntExcelReport configs)

---

## EXECUTION-BASED PATTERN EXPLAINED

### How Commission Report Works (Reference)

1. **User selects filters** → YearMonth, SalesGroup
2. **Backend creates BGReportExecution record** with filter values
3. **BGCommissionReportDataView** JOINs to BGReportExecution:
   ```sql
   JOIN "BGReportExecution" re ON (re."BGReportName" = 'Commission')
   WHERE (re."BGSalesGroupId" IS NULL OR re."BGSalesGroupId" = ...)
   ```
4. **IntExcelExport queries** with `BGExecutionId = {new_execution_id}`
5. **View returns filtered data** based on execution context

### Why Other Reports Don't Work

- **No business process** creates BGReportExecution records for them
- Views have `BGExecutionId` column but no matching execution records
- IntExcelExport query returns nothing or errors

---

## FILES REFERENCE

| File | Purpose |
|------|---------|
| `source-code/UsrExcelReportService_Updated.cs` | Backend with custom generators |
| `sql/VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql` | Employee JOIN fix (applied) |
| `docs/investigation/PROD_INTEXCELREPORT_CONFIGS.md` | PROD screenshot analysis |
| `docs/investigation/BGSALESBYITEMLINEVIEW_SCHEMA.md` | View column structure |
| `docs/investigation/BGLOBAL_V7_EXECUTION_PATTERN.md` | Execution pattern deep-dive |

---

## SUMMARY

| Finding | Impact | Action |
|---------|--------|--------|
| All PROD reports use execution-based pattern | High | Understand pattern fully |
| BGSalesByItemView fix has no impact | High | Need different approach |
| Custom generators bypass broken flow | Good | Extend to cover all cases |
| 0 BGReportExecution records for most reports | Critical | Create records OR always use custom generators |
| Backend deployment status unknown | Risk | Verify PROD code |

**Recommended Next Step:** Extend custom generator routing to handle BGSalesByItemLineView reports, making them always use our tested code path instead of broken IntExcelExport flow.

---

*Investigation completed: 2026-01-29*
