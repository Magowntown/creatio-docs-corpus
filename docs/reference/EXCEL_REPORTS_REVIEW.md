# Excel Reports Comprehensive Review

**Date:** 2026-01-29
**Purpose:** Review all Excel reports for correct operation
**Status:** IN PROGRESS

---

## All Excel Reports Summary

| # | Report Name | View Schema | Custom Generator | Duplicate Issue | Status |
|---|-------------|-------------|------------------|-----------------|--------|
| 1 | **Rpt Commission** | BGCommissionReportDataView | ✅ Yes (ExecutionId) | No | ✅ Working |
| 2 | **Items by Customer** | BGSalesByItemView | ✅ Yes | ⚠️ YES (Employee JOIN) | 🟡 Needs Fix |
| 3 | **Rpt Sales By Item** | BGSalesByItemView | ✅ Yes | ⚠️ YES (Employee JOIN) | 🟡 Needs Fix |
| 4 | **Rpt Sales By Item By Type** | BGSalesByItemView | ✅ Yes | ⚠️ YES (Employee JOIN) | 🟡 Needs Fix |
| 5 | **Customers did not buy** | BGSalesByCustomerView | ✅ Yes | ❓ Check | 🔴 Test Needed |
| 6 | **Rpt Sales By Line** | BGSalesByItemLineView | ❌ No (uses library) | ❓ Check | 🔴 Test Needed |
| 7 | **Rpt Sales By Sales Group** | BGSalesBySalesGroupView | ❌ No (uses library) | ❓ Check | 🔴 Test Needed |
| 8 | **IW_Commission** | IWCommissionReportDataView | ✅ Yes (YearMonth) | No | 🟡 DEV Only |

---

## Detailed Report Analysis

### 1. Rpt Commission ✅

| Property | Value |
|----------|-------|
| View | BGCommissionReportDataView |
| Pattern | Type A (Execution-Based) |
| Custom Generator | Yes - uses BGReportExecution |
| Filters | YearMonth, SalesGroup |
| Duplicate Issue | No - proper Employee join via BGCommissionEarner |
| Status | ✅ **WORKING** |

**Notes:** Commission uses `BGCommissionEarner` table which links specific sales reps to orders, avoiding duplicates.

---

### 2. Items by Customer 🟡

| Property | Value |
|----------|-------|
| View | BGSalesByItemView |
| Pattern | Type B (Direct) |
| Custom Generator | Yes - `GenerateSalesByItemWithFilters()` |
| Filters | Customer, Created, Shipping, Delivery, Status |
| Duplicate Issue | ⚠️ **YES** - Employee JOIN causes 26x duplicates |
| Status | 🟡 **NEEDS EMPLOYEE JOIN FIX** |

**Issues Found:**
1. ✅ BGProductDescription added - FIXED
2. ✅ CreatedOn column mapping - FIXED
3. ⚠️ Duplicate rows due to Employee JOIN - NEEDS FIX

---

### 3. Rpt Sales By Item 🟡

| Property | Value |
|----------|-------|
| View | BGSalesByItemView |
| Pattern | Type B (Direct) |
| Custom Generator | Yes - same as Items by Customer |
| Filters | Created, Shipping, Delivery, Status |
| Duplicate Issue | ⚠️ **YES** - Same view, same problem |
| Status | 🟡 **NEEDS EMPLOYEE JOIN FIX** |

**Notes:** Shares view with Items by Customer - same fix applies.

---

### 4. Rpt Sales By Item By Type Of Customer 🟡

| Property | Value |
|----------|-------|
| View | BGSalesByItemView |
| Pattern | Type B (Direct) |
| Custom Generator | Yes - same as Items by Customer |
| Filters | Created, Shipping, Delivery, Status |
| Duplicate Issue | ⚠️ **YES** - Same view, same problem |
| Status | 🟡 **NEEDS EMPLOYEE JOIN FIX** |

**Notes:** Also uses BGSalesByItemByTypeOfCustomerView for some reports - needs same BGProductDescription fix.

---

### 5. Customers Did Not Buy 🔴

| Property | Value |
|----------|-------|
| View | BGSalesByCustomerView |
| Pattern | Type A (Execution-Based) |
| Custom Generator | Yes - `GenerateSalesByCustomerWithFilters()` |
| Filters | Created, Shipping, Delivery, Status |
| Duplicate Issue | ❓ **NEEDS CHECK** |
| Status | 🔴 **TEST NEEDED** |

**Check Required:**
1. Does BGSalesByCustomerView have Employee JOIN issue?
2. Test report output for duplicates

---

### 6. Rpt Sales By Line 🔴

| Property | Value |
|----------|-------|
| View | BGSalesByItemLineView |
| Pattern | Type A (Execution-Based) |
| Custom Generator | ❌ No - uses IntExcelExport library |
| Filters | Created, Shipping, Delivery, Status |
| Duplicate Issue | ❓ **NEEDS CHECK** |
| Status | 🔴 **TEST NEEDED** |

**Check Required:**
1. Does BGSalesByItemLineView have Employee JOIN issue?
2. Does IntExcelExport properly apply filters?
3. Test report output

---

### 7. Rpt Sales By Sales Group 🔴

| Property | Value |
|----------|-------|
| View | BGSalesBySalesGroupView |
| Pattern | Type A (Execution-Based) |
| Custom Generator | ❌ No - uses IntExcelExport library |
| Filters | Created, Shipping, Delivery, Status |
| Duplicate Issue | ❓ **NEEDS CHECK** |
| Status | 🔴 **TEST NEEDED** |

**Check Required:**
1. Test report generation
2. Check for OutOfMemoryException
3. Verify filters apply correctly

---

### 8. IW_Commission 🟡

| Property | Value |
|----------|-------|
| View | IWCommissionReportDataView |
| Pattern | Type A (Execution-Based) |
| Custom Generator | Yes - `GenerateIWCommissionWithDateFilter()` |
| Filters | YearMonth, SalesGroup |
| Duplicate Issue | No |
| Status | 🟡 **DEV ONLY** (not in PROD) |

**Notes:** Works in DEV but not deployed to PROD.

---

## Views with Employee JOIN Issue

| View | Employee JOIN Type | Has Duplicates? |
|------|-------------------|-----------------|
| **BGSalesByItemView** | `JOIN Employee e ON (sg."Id" = e."BGSalesGroupLookupId")` | ⚠️ **BUG - 26x** |
| BGSalesByCustomerView | `JOIN Employee e ON (o."BGSalesRepLookupId" = e."Id")` | ✅ Correct |
| BGSalesByItemLineView | `JOIN Employee e ON (o."BGSalesRepLookupId" = e."Id")` | ✅ Correct |
| BGSalesBySalesGroupView | `JOIN Employee e ON (o."BGSalesRepLookupId" = e."Id")` | ✅ Correct |
| BGCommissionReportDataView | `JOIN Employee rep ON (rep."Id" = ce."BGSalesRepId")` | ✅ Correct |

### Investigation Result (2026-01-29) ✅ COMPLETE

**ONLY BGSalesByItemView has the Employee JOIN bug!**

All other views correctly join to the specific sales rep on the Order record using `o."BGSalesRepLookupId" = e."Id"`. Only BGSalesByItemView incorrectly joins ALL employees in the sales group using `sg."Id" = e."BGSalesGroupLookupId"`.

**Fix Script:** `sql/VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql`
```sql
-- FROM (incorrect):
JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId")
-- TO (correct):
LEFT JOIN "Employee" e ON (o."BGSalesRepLookupId" = e."Id")
```

---

## Testing Checklist

### Priority 1: Fix BGSalesByItemView Employee JOIN
- [ ] Apply SQL fix: `sql/VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql`
- [ ] Test Items by Customer - no duplicates
- [ ] Test Rpt Sales By Item - no duplicates
- [ ] Test Rpt Sales By Item By Type - no duplicates

### Priority 2: Test Other Reports (Views Already Correct)
- [x] Customers Did Not Buy - BGSalesByCustomerView has correct Employee JOIN ✅
- [x] Rpt Sales By Line - BGSalesByItemLineView has correct Employee JOIN ✅
- [x] Rpt Sales By Sales Group - BGSalesBySalesGroupView has correct Employee JOIN ✅

### Priority 3: Check Other Views ✅ COMPLETE
- [x] Extract BGSalesByCustomerView SQL - correct: `o."BGSalesRepLookupId" = e."Id"` ✅
- [x] Extract BGSalesByItemLineView SQL - correct: `o."BGSalesRepLookupId" = e."Id"` ✅
- [ ] Extract BGSalesBySalesGroupView SQL - check Employee JOIN

---

## Action Items

| # | Action | Priority | Status |
|---|--------|----------|--------|
| 1 | Fix BGSalesByItemView Employee JOIN | 🔴 High | Pending |
| 2 | Test Customers Did Not Buy report | 🔴 High | Pending |
| 3 | Test Rpt Sales By Line report | 🟡 Medium | Pending |
| 4 | Test Rpt Sales By Sales Group report | 🟡 Medium | Pending |
| 5 | Check all views for Employee JOIN issue | 🟡 Medium | Pending |
| 6 | Add BGProductDescription to other views | 🟢 Low | Pending |

---

*Created: 2026-01-29*
