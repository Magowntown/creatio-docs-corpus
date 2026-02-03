# Option A Implementation Plan: Add BGProductDescription to BGSalesByItemView

**Date:** 2026-01-29
**Status:** READY FOR IMPLEMENTATION
**Risk Level:** LOW (based on completed investigations)

---

## Executive Summary

This document provides step-by-step implementation instructions for adding a `BGProductDescription` column to `BGSalesByItemView` to fix the "Items by Customer" report's DESCRIPCION column (currently showing order numbers instead of product descriptions).

---

## Pre-Implementation Checklist

| Item | Status | Notes |
|------|--------|-------|
| Environment impact assessed | ✅ | LOW risk - single package, no dependencies |
| UsrPage frontend impact | ✅ | NO IMPACT - decoupled |
| Backend impact assessed | ✅ | LOW - 1 line change (line 1836) |
| Other reports impact | ✅ | 3 reports use view - additive change safe |
| BGlobal v7 pattern documented | ✅ | View is Type B (direct), not execution-based |
| Rollback plan documented | ✅ | Simple - revert backend column mapping |

---

## Implementation Steps

### Step 1: Modify BGSalesByItemView Schema (Creatio Configuration)

**Location:** PampaBay package > Schemas > BGSalesByItemView

**Creatio Designer URL:**
```
https://pampabay.creatio.com/0/ClientApp/#/EntitySchemaDesigner/{BGSalesByItemView_UId}
```

**Option 1A: Using Entity Designer (Recommended for Creatio Cloud)**

1. Navigate to **System Designer** > **Advanced Settings** > **Configuration**
2. Select **PampaBay** package
3. Find **BGSalesByItemView** schema
4. Click **Edit**
5. Add new column:
   - **Name:** `BGProductDescription`
   - **Title:** `Product Description`
   - **Data Type:** `Text (250)` (or unlimited)
   - **Reference:** Link to Product entity
   - **Column Path:** `[Product:Code=BGItem].Description`

**Option 1B: SQL View Modification (If Direct SQL Access Available)**

```sql
-- Pseudocode - actual SQL depends on current view structure
-- NOTE: Creatio Cloud may not allow direct SQL modification

ALTER VIEW "BGSalesByItemView" AS
SELECT
    -- Existing columns (do not modify)
    v."Id",
    v."CreatedOn",
    v."CreatedById",
    v."ModifiedOn",
    v."ModifiedById",
    v."ProcessListeners",
    v."BGSalesRep",
    v."BGSalesGroup",
    v."BGCustomer",
    v."BGQuantity",
    v."BGItem",           -- Product CODE (e.g., "MAS2890WH")
    v."BGAmount",
    v."BGPrice",
    v."BGDeliveryDate",
    v."BGShipDate",
    v."BGPONumber",
    v."BGStatus",
    v."BGNumber",

    -- NEW COLUMN
    p."Description" AS "BGProductDescription"
FROM
    <existing_source_tables> v
    -- Add JOIN to Product entity
    LEFT JOIN "Product" p ON p."Code" = v."BGItem";
```

### Step 2: Update Backend Column Mapping

**File:** `source-code/UsrExcelReportService_Updated.cs`
**Line:** ~1836

**Before (Current):**
```csharp
var columnMapping = new List<Tuple<string, string>>
{
    Tuple.Create("BGCustomer", "BGCustomer"),         // Column A
    Tuple.Create("BGDeliveryDate", "Created on"),     // Column B
    Tuple.Create("BGAmount", "Last Price"),           // Column C
    Tuple.Create("BGNumber", "Product"),              // Column D - WRONG
    Tuple.Create("BGItem", "ProductCode"),            // Column E
    Tuple.Create("BGQuantity", "Quantity"),           // Column F
    Tuple.Create("BGPrice", "Filters")                // Column G
};
```

**After (Fixed):**
```csharp
var columnMapping = new List<Tuple<string, string>>
{
    Tuple.Create("BGCustomer", "BGCustomer"),              // Column A
    Tuple.Create("BGDeliveryDate", "Created on"),          // Column B
    Tuple.Create("BGAmount", "Last Price"),                // Column C
    Tuple.Create("BGProductDescription", "Product"),       // Column D - FIXED
    Tuple.Create("BGItem", "ProductCode"),                 // Column E
    Tuple.Create("BGQuantity", "Quantity"),                // Column F
    Tuple.Create("BGPrice", "Filters")                     // Column G
};
```

### Step 3: Update IntExcelReport ESQ (Optional)

If reports are generated through IntExcelExport library (fallback path), update the IntEsq JSON:

**IntExcelReport Record:** `d213933b-093d-47fc-8da8-422c0d9bf715` (Items by Customer)

Add to `IntEsq` columns:
```json
{
  "rootSchemaName": "BGSalesByItemView",
  "columns": {
    "items": {
      "BGProductDescription": {
        "caption": "Product Description",
        "expression": {"expressionType": 0, "columnPath": "BGProductDescription"}
      }
    }
  }
}
```

---

## Testing Plan

### DEV Environment Testing

1. **Deploy view modification** to DEV
2. **Deploy backend code** to DEV
3. **Test via OData API:**
   ```
   GET /0/odata/BGSalesByItemView?$top=5&$select=BGItem,BGProductDescription
   ```
4. **Generate report:**
   - Navigate to Reports page
   - Select "Items by Customer"
   - Select customer (e.g., "Sisters")
   - Click Download
5. **Verify Excel output:**
   - Open downloaded Excel file
   - Check Column D (DESCRIPCION) shows product descriptions
   - Verify VBA macro processes correctly

### PROD Deployment

After successful DEV testing:

1. **Deploy view modification** to PROD (via package)
2. **Deploy backend code** to PROD (Source Code Schema Designer)
3. **Test with real customer** (e.g., "Sisters")
4. **Verify with Danlyn** that reports match expectations

---

## Rollback Plan

### Immediate Rollback (Backend Only)

If issues arise after deployment, revert line 1836:

```csharp
// Revert to:
Tuple.Create("BGNumber", "Product"),
```

This restores Order Number to Column D. The view modification can remain.

### Full Rollback

1. Export current PampaBay package as backup
2. Revert view schema (remove BGProductDescription column)
3. Revert backend column mapping
4. Compile and publish

---

## Alternative Approach: Backend-Only Fix (No View Modification)

If view modification is blocked or risky, the backend can query Product description directly:

```csharp
// In QuerySalesByItemData(), after fetching BGSalesByItemView data:

// For each row, lookup product description
foreach (var row in results)
{
    var productCode = row["BGItem"]?.ToString();
    if (!string.IsNullOrEmpty(productCode))
    {
        var productDescription = LookupProductDescription(productCode);
        row["Product"] = productDescription;  // Column D in Excel
    }
}

private string LookupProductDescription(string productCode)
{
    var esq = new EntitySchemaQuery(UserConnection.EntitySchemaManager, "Product");
    esq.AddColumn("Description");
    esq.Filters.Add(esq.CreateFilterWithParameters(
        FilterComparisonType.Equal, "Code", productCode));

    var entity = esq.GetEntityCollection(UserConnection).FirstOrDefault();
    return entity?.GetTypedColumnValue<string>("Description") ?? productCode;
}
```

**Pros:** No view modification needed
**Cons:** Performance impact (N+1 queries) - could be mitigated with caching

---

## Related Files

| Purpose | File |
|---------|------|
| Environment impact analysis | `docs/investigation/OPTION_A_ENVIRONMENT_IMPACT.md` |
| Backend impact analysis | `docs/investigation/OPTION_A_BACKEND_IMPACT.md` |
| UsrPage impact analysis | `docs/investigation/OPTION_A_USRPAGE_IMPACT.md` |
| Other reports impact | `docs/investigation/OPTION_A_OTHER_REPORTS_IMPACT.md` |
| BGlobal v7 pattern | `docs/investigation/BGLOBAL_V7_EXECUTION_PATTERN.md` |
| Column mapping investigation | `docs/ITEMS_BY_CUSTOMER_COLUMN_INVESTIGATION.md` |
| VBA fix documentation | `docs/ITEMS_BY_CUSTOMER_VBA_FIX.md` |
| Backend service code | `source-code/UsrExcelReportService_Updated.cs` |

---

## GUIDs Reference

| Entity | GUID |
|--------|------|
| BGSalesByItemView (Schema ID) | `5f969641-af66-48bd-9fca-b532f479684f` |
| BGSalesByItemView (Schema UId) | `d38b4d04-7c79-4b4a-8611-306f86d1e5c9` |
| Items by Customer (IntExcelReport) | `d213933b-093d-47fc-8da8-422c0d9bf715` |
| PampaBay Package | `8b0ef6b5-915e-4739-a779-9d54505f19df` |
| Product Entity | (standard Creatio) |

---

## Decision Required

**Choose implementation approach:**

| Option | Effort | Risk | Persistence |
|--------|--------|------|-------------|
| **A1: View Modification + Backend** | Medium | Low | Best (data at source) |
| **A2: Backend-Only (N+1 queries)** | Low | Low | Good (but slower) |
| **A3: Backend + Caching** | Medium | Low | Good |

**Recommendation:** **Option A1** - Modify the view schema to add BGProductDescription column, then update backend mapping. This is the cleanest solution with best performance.

---

*Created: 2026-01-29*
*Investigator: Claude Code*
