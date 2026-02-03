# Items by Customer - Column Mapping Investigation

**Date:** 2026-01-29
**Investigator:** Claude Code
**Environment:** PROD (pampabay.creatio.com)
**Related Issue:** RPT-004 - VBA expecting "Product" column with description

---

## Executive Summary

The "Items by Customer" report has a **column content mismatch** between what the VBA macro expects and what the backend provides:

| Column | VBA Expects | Backend Provides | Issue |
|--------|-------------|------------------|-------|
| **Product (D)** | Product Description | Order Number (BGNumber) | **MISMATCH** |
| **ProductCode (E)** | Product Code | Product Code (BGItem) | OK |

**Root Cause:** BGSalesByItemView does not contain a product description column. The `BGItem` column contains product CODES (e.g., "MAS2890WH"), not descriptions (e.g., "Chip & Dip"). The backend maps `BGNumber` (order number) to the "Product" column position, but VBA expects the actual product description.

---

## Data Source Analysis

### 1. BGSalesByItemView (Current Data Source)

**Record Count:** 4,806,158 rows

**Available Columns:**

| Column Name | Data Type | Sample Value | Description |
|-------------|-----------|--------------|-------------|
| `BGItem` | string | "MAS2890WH" | Product CODE (not description) |
| `BGNumber` | string | "ORD-16512" | Order Number |
| `BGCustomer` | string | "Gaines Jewelers" | Customer Name |
| `BGQuantity` | int | 2 | Quantity Ordered |
| `BGPrice` | float | 26.0 | Unit Price |
| `BGAmount` | float | 52.0 | Line Total |
| `BGDeliveryDate` | datetime | 2018-07-15 | Delivery Date |
| `BGShipDate` | datetime | 2018-07-19 | Ship Date |
| `BGPONumber` | string | "ATL718-100-168842" | PO Number |
| `BGStatus` | string | "Shipped" | Order Status |
| `BGSalesRep` | string | "Bob Stewart" | Sales Rep Name |
| `BGSalesGroup` | string | "Werner Frank" | Sales Group |
| `CreatedOn` | datetime | 2018-07-13 | Created Date |
| `Id`, `CreatedById`, `ModifiedById`, `ModifiedOn`, `ProcessListeners` | system | - | System columns |

**Key Finding:** NO description column exists in this view.

### 2. BGItemsByCustomerView (Original View)

**Record Count:** 0 rows (EMPTY)

This view was never populated. It was likely intended to be populated by a background process that was never implemented.

### 3. Product Entity

The Product entity DOES have description columns:

| Column | Sample Value |
|--------|--------------|
| `Code` | "MAS2890WH" |
| `Name` | "MAS2890WH" |
| `Description` | "Chip & Dip" |
| `BGDescription` | "Chip & Dip" |

**Product.Code matches BGSalesByItemView.BGItem** - we can use this for lookups.

### 4. OrderProduct Entity

Contains product descriptions at the line item level:

| Column | Sample Value |
|--------|--------------|
| `ProductId` | GUID |
| `BGProductInOrderDescription` | "Deep Rectangular Server" |

However, BGSalesByItemView does not join to OrderProduct directly.

---

## IntExcelReport Configuration

**Report ID:** `d213933b-093d-47fc-8da8-422c0d9bf715`
**Report Name:** "Items by Customer"
**Sheet Name:** "Data"
**Entity Schema:** BGSalesByItemView

**ESQ Configuration (IntEsq):**
```json
{
  "rootSchemaName": "BGSalesByItemView",
  "columns": {
    "items": {
      "BGSalesRep": {...},
      "BGSalesGroup": {...},
      "BGCustomer": {...},
      "BGQuantity": {...},
      "BGItem": {...},
      "BGAmount": {...},
      "BGPrice": {...},
      "BGDeliveryDate": {...},
      "BGShipDate": {...},
      "BGPONumber": {...},
      "BGStatus": {...},
      "BGNumber": {...}
    }
  }
}
```

**Note:** No description column is requested because it doesn't exist in the view.

---

## VBA Template Analysis

The VBA macro `PMPSalesByItem` reads columns **by position**, not by header names:

```vba
' Column C: Amount to sum
auxTot = Worksheets("Data").Range("C" & iDFila).Value

' Column E: Used for item grouping (loops through unique items)
' Expects PRODUCT CODE here (e.g., "MAS2890WH")

' Outputs to Rpt sheet:
'   Column F (Item), G (Qty total), I (Amount total)
```

**Template Header Expectations:**

| Position | Template Header | VBA Usage | Current Backend Output |
|----------|----------------|-----------|----------------------|
| A | BGCustomer | Customer name | BGCustomer (OK) |
| B | Created on | Date | BGDeliveryDate (OK) |
| C | Last Price | Amount - VBA SUMS this | BGAmount (OK) |
| D | Product | Product DESCRIPTION | BGNumber (ORDER NUM!) |
| E | ProductCode | Product CODE - VBA GROUPS by this | BGItem (OK) |
| F | Quantity | Quantity | BGQuantity (OK) |
| G | Filters | Extra | BGPrice |

---

## The Problem

**Column D Mismatch:**

| Expected | Actual |
|----------|--------|
| Product Description (e.g., "Chip & Dip") | Order Number (e.g., "ORD-16512") |

The VBA macro likely displays this column to the user or uses it for labeling. Getting an order number instead of a product description is confusing.

---

## Solution Options

### Option A: Add Product Description to BGSalesByItemView (RECOMMENDED)

**SQL View Modification:**

The BGSalesByItemView is a database view. To add product description:

```sql
-- Pseudocode - actual view needs to join to Product
ALTER VIEW BGSalesByItemView AS
SELECT
    existing columns...,
    p.Description AS BGProductDescription  -- NEW COLUMN
FROM OrderProduct op
    JOIN Product p ON p.Id = op.ProductId
    ... existing joins ...
```

**Pros:**
- Clean solution - description available at view level
- No backend code changes needed
- IntExcelReport ESQ just needs to add the new column

**Cons:**
- Requires database-level change
- Need to understand existing view definition

**Action Required:**
1. Get current BGSalesByItemView SQL definition
2. Add JOIN to Product table for Description
3. Update IntExcelReport ESQ to include BGProductDescription
4. Update backend column mapping

### Option B: Backend Lookup (Current Workaround)

Modify `QuerySalesByItemData()` to lookup product description from Product entity for each row.

**Implementation:**

```csharp
// After querying BGSalesByItemView, for each row:
var productCode = row["BGItem"];
var description = LookupProductDescription(userConnection, productCode);
row["Product"] = description;  // Column D
```

**Pros:**
- No database view changes
- Can implement immediately

**Cons:**
- N+1 query problem (one lookup per row)
- Performance impact for large result sets
- Would need caching of Product descriptions

### Option C: Pre-Build Description Cache

Build a dictionary of ProductCode -> Description before iterating results.

```csharp
// Query all products once
var productDescriptions = GetProductDescriptionMap(userConnection);

// Then for each row:
row["Product"] = productDescriptions.GetValueOrDefault(row["BGItem"], "");
```

**Pros:**
- Better performance than Option B
- No view changes

**Cons:**
- Memory usage for large product catalogs
- Still adds complexity to backend

### Option D: Accept Current Behavior

If the VBA macro only cares about the Product CODE column (position E) for grouping, and doesn't actually display column D to users, the current behavior may be acceptable.

**Investigation needed:** Review what the VBA macro does with column D.

---

## Current Backend Column Mapping

From `source-code/UsrExcelReportService_Updated.cs` (lines 1831-1840):

```csharp
var columnMapping = new List<Tuple<string, string>>
{
    Tuple.Create("BGCustomer", "BGCustomer"),         // Column A: Customer name
    Tuple.Create("BGDeliveryDate", "Created on"),     // Column B: Delivery date
    Tuple.Create("BGAmount", "Last Price"),           // Column C: Amount - VBA SUMS THIS
    Tuple.Create("BGNumber", "Product"),              // Column D: Order number (WRONG!)
    Tuple.Create("BGItem", "ProductCode"),            // Column E: Item code - VBA GROUPS BY THIS
    Tuple.Create("BGQuantity", "Quantity"),           // Column F: Quantity
    Tuple.Create("BGPrice", "Filters")                // Column G: Unit price (extra)
};
```

**The Issue:** `BGNumber` (order number) is mapped to "Product" position but VBA expects description.

---

## Recommendations

1. **Short Term (Option C):** Update backend to cache Product descriptions and inject into column D
2. **Long Term (Option A):** Modify BGSalesByItemView SQL to include Product.Description

### Immediate Fix Implementation

To implement Option C in `QuerySalesByItemData()`:

```csharp
// 1. Before iterating results, build product description cache
var productDescCache = new Dictionary<string, string>();
var productEsq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "Product");
productEsq.AddColumn("Code");
productEsq.AddColumn("Description");
var products = productEsq.GetEntityCollection(userConnection);
foreach (var p in products)
{
    var code = p.GetTypedColumnValue<string>("Code");
    var desc = p.GetTypedColumnValue<string>("Description");
    if (!string.IsNullOrEmpty(code))
        productDescCache[code] = desc ?? "";
}

// 2. Update column mapping to use description
var columnMapping = new List<Tuple<string, string>>
{
    Tuple.Create("BGCustomer", "BGCustomer"),
    Tuple.Create("BGDeliveryDate", "Created on"),
    Tuple.Create("BGAmount", "Last Price"),
    Tuple.Create("_ProductDescription", "Product"),   // Computed column
    Tuple.Create("BGItem", "ProductCode"),
    Tuple.Create("BGQuantity", "Quantity"),
    Tuple.Create("BGPrice", "Filters")
};

// 3. When building row dictionary, inject description
var productCode = entity.GetTypedColumnValue<string>("BGItem");
row["Product"] = productDescCache.GetValueOrDefault(productCode, productCode);
```

---

## Related Reports

These reports also use BGSalesByItemView and may have similar issues:

| Report Name | ID |
|------------|-----|
| Rpt Sales By Item | c4f4e32c-376d-4b19-b04b-2129dba29d06 |
| Rpt Sales By Item By Type Of Customer | 53682214-a63c-407a-b3f1-79d8ab235f18 |

---

## Appendix: Sample Data Verification

**BGItem = Product Code confirmed:**
```
BGSalesByItemView.BGItem: "MAS2890WH"
Product.Code: "MAS2890WH"  (match!)
Product.Description: "Chip & Dip"
```

**This confirms:**
- BGItem contains the product CODE
- Product.Description contains the human-readable name
- We can join on Product.Code = BGSalesByItemView.BGItem

---

*Created: 2026-01-29*
