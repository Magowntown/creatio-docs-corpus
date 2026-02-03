# Items by Customer - VBA Column Order Fix

**Date:** 2026-01-29
**Issue:** Rpt sheet shows incomplete data after Excel download
**Root Cause:** Backend column order mismatched VBA macro expectations
**Status:** Fix ready for deployment

---

## Problem Analysis

The VBA macro `PMPSalesByItem` in the Excel template reads columns **by position**, not by header names:

```
VBA reads:
- Column C: auxTot = Range("C").Value  → Amount to sum
- Column E: Used for item grouping (loops through unique values)
- Outputs to Rpt sheet: Column F (Item), G (Qty total), I (Amount total)
```

**Before (broken):**
| Position | ESQ Column | Header | VBA Expected |
|----------|------------|--------|--------------|
| A | BGItem | ITEM | Customer |
| B | BGNumber | DESCRIPCION | Date |
| C | **BGQuantity** | **Qty** | **Amount (WRONG!)** |
| D | BGAmount | Amount | Product |
| E | **BGCustomer** | **Customer** | **ProductCode (WRONG!)** |
| F | BGDeliveryDate | Date | Quantity |

**After (fixed):**
| Position | ESQ Column | Header | VBA Expected |
|----------|------------|--------|--------------|
| A | BGCustomer | BGCustomer | Customer ✓ |
| B | BGDeliveryDate | Created on | Date ✓ |
| C | **BGAmount** | **Last Price** | **Amount ✓** |
| D | BGNumber | Product | Product ✓ |
| E | **BGItem** | **ProductCode** | **ProductCode ✓** |
| F | BGQuantity | Quantity | Quantity ✓ |
| G | BGPrice | Filters | (extra) |

---

## Code Change

**File:** `source-code/UsrExcelReportService_Updated.cs`
**Function:** `QuerySalesByItemData()` (around line 1826)

```csharp
// BEFORE (broken):
var columnMapping = new List<Tuple<string, string>>
{
    Tuple.Create("BGItem", "ITEM"),              // A
    Tuple.Create("BGNumber", "DESCRIPCION"),    // B
    Tuple.Create("BGQuantity", "Qty"),          // C - VBA reads as Amount! WRONG
    Tuple.Create("BGAmount", "Amount"),         // D
    Tuple.Create("BGCustomer", "Customer"),     // E - VBA groups by this! WRONG
    ...
};

// AFTER (fixed):
var columnMapping = new List<Tuple<string, string>>
{
    Tuple.Create("BGCustomer", "BGCustomer"),         // A: Customer
    Tuple.Create("BGDeliveryDate", "Created on"),     // B: Date
    Tuple.Create("BGAmount", "Last Price"),           // C: Amount - VBA SUMS THIS ✓
    Tuple.Create("BGNumber", "Product"),              // D: Order number
    Tuple.Create("BGItem", "ProductCode"),            // E: Item - VBA GROUPS BY THIS ✓
    Tuple.Create("BGQuantity", "Quantity"),           // F: Quantity
    Tuple.Create("BGPrice", "Filters")                // G: Price (extra)
};
```

---

## Deployment Steps

### 1. Deploy Backend Code

**URL:** `https://dev-pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178`

Copy the updated `QuerySalesByItemData()` function from `source-code/UsrExcelReportService_Updated.cs` lines 1795-1950 approximately.

### 2. Test in DEV

1. Go to Reports page
2. Select "Items by Customer"
3. Select a customer with recent data (e.g., Sisters, Kademi)
4. Set date range with data (e.g., 2026-01-01 to 2026-01-28)
5. Generate report
6. Open downloaded Excel
7. Verify:
   - **Data sheet:** Should have columns A-G with data
   - **Rpt sheet:** Should show aggregated items with totals

### 3. Expected Rpt Output

After fix, the Rpt sheet should show:
- Title row: "Items by Customer"
- For each unique item code:
  - Item code (column F)
  - Quantity total (column G)
  - Amount total (column I)
- Grand totals row at bottom

---

## Technical Details

### VBA Macro Logic (extracted from vbaProject.bin)

```vba
' PMPSalesByItem macro
auxTot = Worksheets("Data").Range("C" & iDFila).Value  ' Reads column C as Amount
iTotItem = iTotItem + auxTot                           ' Sums amounts
Worksheets("Rpt").Range("F" & iBFila).Value = sItem    ' Writes item to col F
Worksheets("Rpt").Range("G" & iBFila).Value = dQtotal  ' Writes qty to col G
Worksheets("Rpt").Range("I" & iBFila).Value = iTotal   ' Writes amount to col I
```

### Template Structure

Original template headers (sharedStrings.xml):
- A: BGCustomer
- B: Created on
- C: Last Price (VBA reads this for Amount)
- D: Product
- E: ProductCode (VBA groups by this)
- F: Quantity
- G: Filters

---

## Related Issues

- **RPT-004:** Items by Customer not generating → Root cause was column order mismatch
- **v54 Frontend:** Customer ID extraction fixed (flat object handling)
- **Backend:** IntExcelReport configured to use BGSalesByItemView ✓

---

*Created: 2026-01-29*
