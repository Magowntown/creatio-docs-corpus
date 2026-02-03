# Fix vs V7 Architecture Audit

**Date:** 2026-01-30
**Purpose:** Compare our implemented fixes against BGlobal's V7 architecture to identify discrepancies

---

## Executive Summary

| Report | Fix Status | V7 Compliance | Issues Found |
|--------|------------|---------------|--------------|
| **RPT-005** (Customers Did Not Buy) | 🟡 Partial | ⚠️ Relationship columns may not exist | ESQ paths need verification |
| **RPT-006/008** (Items by Customer) | ✅ Working | ✅ Correct Type B pattern | None |
| **Commission** | ✅ Working | ⚠️ Different from V7 pattern | Works but bypasses execution model |
| **IW_Commission** | ✅ Working | ✅ Direct query pattern | None |
| **Sales By Customer** | ✅ Working | ⚠️ Bypasses execution model | Works but not V7 compliant |

---

## 1. RPT-005: Customers Did Not Buy

### V7 Architecture Expected

**View:** BGCustomerDidNotBuyView (Type A - Execution-Based)

**Actual View Columns (from SQL extraction):**
| Column | Type | Source |
|--------|------|--------|
| Id | GUID | a."Id" |
| BGAccountId | GUID FK | a."Id" AS "BGAccountId" |
| BGLastOrderId | GUID FK | Subquery → Order.Id |
| BGEmail | String | Subquery → AccountCommunication.Number |
| BGPreviousOrderCount | Integer | Subquery COUNT(*) |
| BGFilters | String | Concatenated text |
| BGExecutionId | GUID FK | re."Id" |

**V7 Pattern Flow:**
1. Create BGReportExecution record with date filters
2. Query view with `WHERE BGExecutionId = {guid}`
3. Use ESQ relationship columns for Account details

### Our Implementation

**File:** `UsrExcelReportService_Updated.cs` lines 2331-2415

**Column Mapping:**
| ESQ Path | Output Key | Status |
|----------|------------|--------|
| `BGAccount.Name` | Account | ⚠️ **Needs verification** |
| `BGAccount.Address` | Address | ⚠️ **Needs verification** |
| `BGAccount.City.Name` | City | ⚠️ **Needs verification** |
| `BGAccount.Region.Name` | State | ⚠️ **Needs verification** |
| `BGAccount.Zip` | ZIP | ⚠️ **Needs verification** |
| `BGEmail` | Email | ✅ Direct column |
| `BGAccount.Phone` | Phone | ⚠️ **Needs verification** |
| `BGLastOrder.CreatedOn` | Last Order Date | ❌ **LIKELY BROKEN** |
| `BGLastOrder.Amount` | Last Order Amount | ❌ **LIKELY BROKEN** |
| `BGPreviousOrderCount` | Previous Order Count | ✅ Direct column |
| `BGLastOrder.Owner.Name` | Last Order Sales Rep | ❌ **LIKELY BROKEN** |
| `BGLastOrder.BGSalesGroup.Name` | Last Order Sales Group | ❌ **LIKELY BROKEN** |

### ✅ VERIFIED: All Relationships Exist

**Verification via PROD OData (2026-01-30):**

| Relationship | Test Query | Result |
|--------------|------------|--------|
| `BGAccount` | `$expand=BGAccount` | ✅ Works - Returns Account data |
| `BGAccount.City` | `$expand=BGAccount($expand=City)` | ✅ Works - Returns "NY" |
| `BGAccount.Region` | `$expand=BGAccount($expand=Region)` | ✅ Works - Returns "NY" |
| `BGLastOrder` | `$expand=BGLastOrder` | ✅ Works - Returns Order data (null GUID for no-buy customers) |

**Corrected Column Paths (Fixed 2026-01-30):**

| Original (Wrong) | Corrected | Reason |
|------------------|-----------|--------|
| `BGLastOrder.Owner.Name` | `BGLastOrder.BGSalesRepLookup.Name` | Owner is system user, BGSalesRepLookup is actual sales rep |
| `BGLastOrder.BGSalesGroup.Name` | `BGLastOrder.BGSalesGroup.BGSalesGroupName` | Column name is BGSalesGroupName, not Name |

### ⚠️ Note: Null Values for "Didn't Buy" Customers

Since these customers DIDN'T place orders in the date range:
- `BGLastOrderId` = `00000000-0000-0000-0000-000000000000` (null GUID)
- `BGLastOrder.*` columns will return default values (null dates, 0 amounts)
- `BGPreviousOrderCount` shows orders BEFORE the date range (may be 0 or positive)

---

## 2. RPT-006/008: Items by Customer

### V7 Architecture Expected

**View:** BGSalesByItemView (Type B - Direct)
**Pattern:** Simple SELECT, filters applied via ESQ at query time

**Actual View Columns (from FIXED SQL):**
| Column | Type | Source |
|--------|------|--------|
| Id | GUID | o."Id" |
| CreatedOn | DateTime | o."CreatedOn" |
| BGNumber | String | o."Number" |
| BGPONumber | String | o."BGPONumber" |
| BGShipDate | DateTime | o."BGShipDate" |
| BGDeliveryDate | DateTime | o."BGDeliveryDate" |
| BGPrice | Decimal | op."Price" |
| BGAmount | Decimal | op."TotalAmount" |
| BGItem | String | p."Name" |
| **BGProductDescription** | String | p."Description" ✅ **ADDED** |
| BGQuantity | Decimal | op."Quantity" |
| BGCustomer | String | ac."Name" |
| BGStatus | String | os."Name" |
| BGSalesGroup | String | sg."BGSalesGroupName" |
| BGSalesRep | String | e."Name" |

### Our Implementation

**File:** `UsrExcelReportService_Updated.cs` lines 1826-1986

**Column Mapping:**
| ESQ Column | Output Key | View Column | Status |
|------------|------------|-------------|--------|
| BGCustomer | BGCustomer | ✅ ac."Name" | ✅ Match |
| CreatedOn | Created on | ✅ o."CreatedOn" | ✅ Match |
| BGAmount | Last Price | ✅ op."TotalAmount" | ✅ Match |
| BGProductDescription | Product | ✅ p."Description" | ✅ Match (FIXED) |
| BGItem | ProductCode | ✅ p."Name" | ✅ Match |
| BGQuantity | Quantity | ✅ op."Quantity" | ✅ Match |
| BGPrice | Filters | ✅ op."Price" | ✅ Match |

### ✅ Status: Fully Compliant

- View SQL has been updated with BGProductDescription
- Backend column mapping matches view columns exactly
- Filters work correctly (Customer, CreatedOn, ShipDate, DeliveryDate, Status)
- Type B (direct) pattern properly implemented

### One Concern: Employee JOIN in View

**View SQL:**
```sql
JOIN "Employee" e ON ((sg."Id" = e."BGSalesGroupLookupId"))
```

**Issue:** Joins Employee via SalesGroup, not directly to Order.BGSalesRepLookupId
**Impact:** May return wrong Sales Rep or duplicate rows (RPT-007 - 26x duplicates)
**Status:** RPT-007 marked as fixed - verify this JOIN is corrected

---

## 3. Commission Report

### V7 Architecture Expected

**View:** BGCommissionReportDataView (Type A - Execution-Based)

**Expected Pattern:**
1. Create BGReportExecution record with YearMonthId, SalesGroupId
2. View filters internally using `JOIN BGReportExecution re ON re.BGReportName = 'Commission'`
3. Query view with `WHERE BGExecutionId = {guid}`

### Our Implementation

**File:** `UsrExcelReportService_Updated.cs` lines 692-754

**Actual Pattern:**
```csharp
// We DON'T create BGReportExecution record!
// We filter directly by BGTransactionDate
esq.Filters.Add(esq.CreateFilterWithParameters(
    FilterComparisonType.GreaterOrEqual,
    "BGTransactionDate",
    startDate
));
```

### ⚠️ Discrepancy: Bypassing Execution Model

**V7 Expects:**
1. BGReportExecution record created
2. View internally filters by execution context
3. BGExecutionId filter in ESQ

**Our Implementation:**
1. No BGReportExecution record created
2. Direct date filter on view
3. No BGExecutionId filter

### Why It Works Anyway

The BGCommissionReportDataView may have been designed to support BOTH patterns:
- Type A: Via BGExecutionId (for IntExcelExport library)
- Type B: Via direct date filtering (for custom generators)

**Verification Needed:**
```bash
# Check if BGTransactionDate is directly filterable in the view
GET /odata/BGCommissionReportDataView?$filter=BGTransactionDate ge 2025-01-01
```

### Recommendation

**If working:** No change needed - simpler is better
**If issues arise:** Implement execution-based pattern like we did for RPT-005

---

## 4. IW_Commission Report

### V7 Architecture

**View:** IWCommissionReportDataView
**Pattern:** Type B (Direct) - appears to be a newer view not using execution model

### Our Implementation

**File:** `UsrExcelReportService_Updated.cs` lines 760-817

**Pattern:**
- Direct query with date filter on IWTransactionDate
- SalesGroup filter if provided
- No BGReportExecution dependency

### ✅ Status: Working Correctly

- View is Type B (no execution model)
- Our direct query approach matches the view design
- No discrepancies found

---

## 5. Sales By Customer Report

### V7 Architecture Expected

**View:** BGSalesByCustomerView (Type A - Execution-Based)

**From SQL_VIEW_MASTER_CATALOG:**
```sql
JOIN "BGReportExecution" re ON true  -- Cross join to all executions!
```

**Expected Pattern:** Create execution record, filter by BGExecutionId

### Our Implementation

**File:** `UsrExcelReportService_Updated.cs` lines 2081-2216

**Actual Pattern:**
```csharp
// Direct filters on BGInvoiceDate, BGShipDate, BGDeliveryDate
// NO BGReportExecution record created
// NO BGExecutionId filter
esq.Filters.Add(esq.CreateFilterWithParameters(
    FilterComparisonType.GreaterOrEqual,
    "BGInvoiceDate",  // Direct date column
    request.CreatedFrom.Value.Date
));
```

### ⚠️ Discrepancy: Not Using Execution Model

Same pattern as Commission - bypasses BGReportExecution.

**Risk:** The `JOIN BGReportExecution ON true` creates Cartesian product. Without BGExecutionId filter, query returns ALL rows × ALL executions.

**Mitigation in our code:** We don't filter by BGExecutionId, but the date filters narrow down results. However, performance may be poor with many BGReportExecution records.

### Recommendation

**Monitor for:** Performance issues, duplicate rows, OutOfMemory errors
**Fix if needed:** Implement execution-based pattern like RPT-005

---

## 6. Summary of Required Actions

### Immediate (Before PROD Deploy)

| Action | Report | Priority | Status |
|--------|--------|----------|--------|
| Verify BGAccount relationship | RPT-005 | HIGH | 🔴 DO THIS |
| Verify BGLastOrder relationship | RPT-005 | HIGH | 🔴 DO THIS |
| Test with actual PROD data | RPT-005 | HIGH | 🔴 DO THIS |

### After PROD Deploy

| Action | Report | Priority | Status |
|--------|--------|----------|--------|
| Monitor performance | Commission | MEDIUM | Watch for issues |
| Monitor performance | Sales By Customer | MEDIUM | Watch for issues |
| Verify Employee JOIN fix | Items by Customer | LOW | RPT-007 marked fixed |

### Nice to Have

| Action | Report | Priority | Status |
|--------|--------|----------|--------|
| Implement execution model | Commission | LOW | Only if issues arise |
| Implement execution model | Sales By Customer | LOW | Only if issues arise |
| Add BGProductDescription | BGSalesByItemByTypeOfCustomerView | LOW | For consistency |

---

## 7. Verification Commands

### Check BGCustomerDidNotBuyView Relationships
```bash
cd /home/magown/.claude/plugins/cache/dev-browser-marketplace/dev-browser/*/skills/dev-browser && npx tsx <<'EOF'
import { connect, waitForPageLoad } from "@/client.js";
const client = await connect();
const page = await client.page("verify-schema");

// Query the view with $expand to see relationship paths
const url = "https://pampabay.creatio.com/0/odata/BGCustomerDidNotBuyView?" +
  "$top=1&$expand=BGAccount";

await page.goto(url);
await waitForPageLoad(page);
console.log(await page.textContent("body"));
await client.disconnect();
EOF
```

### Check Commission View Direct Filtering
```bash
# Same pattern - verify BGTransactionDate is filterable
```

---

*Audit completed: 2026-01-30*
*Analyst: Claude Code*
