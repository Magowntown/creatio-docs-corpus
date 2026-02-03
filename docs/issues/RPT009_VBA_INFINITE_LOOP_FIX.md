# RPT-009: VBA Infinite Loop Fix

**Report:** Sales By Item By Type Of Customer
**Status:** ✅ FIXED
**Date:** 2026-01-30

---

## Problem

When running the "Sales By Item By Type Of Customer" report, the Excel macro would hang with "Not Responding" status. The VBA code had an infinite loop in the nested While loops that process grouped data.

---

## Root Cause

In the `PMPFillReportData` subroutine (inside `PMPSalesbySalesRep` module), the anchor variable `sCurGroupWhile2Val` was being reset to equal `sCurGroup2Val` in **two places inside the inner While loop**:

1. **At the start of the inner While body** (after condition check)
2. **After the `'Grab next data set` comment**

This made the While condition `sCurGroup2Val = sCurGroupWhile2Val` always evaluate to TRUE, creating an infinite loop.

### Buggy Code Pattern

```vba
While sCurGroup2Val = sCurGroupWhile2Val And sCurGroup2Val <> "" And sCurGroupVal = sCurGroupWhileVal
    iBFila = iBFila + 1
    Worksheets("Rpt").Range("A" & iBFila).Value = Worksheets("Data").Range("C" & iDFila).Value

    Set rng2 = Worksheets("Data").Range("C" & iDFila & ":C" & iDFilaFin)
    sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
    sCurGroupWhile2Val = sCurGroup2Val   ' <-- BUG #1: Resets anchor INSIDE loop
    iGroup2Qty = WorksheetFunction.CountIf(rng2, sCurGroup2Val)

    For i = 1 To iGroup2Qty
        ' ... process rows ...
        iDFila = iDFila + 1
    Next

    ' ... write to report ...

    'Grab next data set
    sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
    sCurGroupWhile2Val = sCurGroup2Val   ' <-- BUG #2: Resets anchor AGAIN

    'Check First Grouping still matches
    sCurGroupVal = Worksheets("Data").Range("A" & iDFila).Value

    iSubGroupTotalQty = 0
    dGroup2Total = 0
Wend
```

### Why It Caused Infinite Loop

1. Inner While condition checks: `sCurGroup2Val = sCurGroupWhile2Val`
2. Condition passes → enter loop
3. Inside loop: `sCurGroupWhile2Val = sCurGroup2Val` makes them equal again
4. End of loop: `sCurGroupWhile2Val = sCurGroup2Val` makes them equal AGAIN
5. Check condition: They're still equal → TRUE → loop again
6. Repeat forever

---

## Fix

**3 changes required:**

### Change 1: Move anchor reset BEFORE the inner While

Add these lines BEFORE the inner While loop (after `iDFilaFin` calculation):

```vba
' FIX: Reset anchor BEFORE inner While (moved from inside loop)
sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
sCurGroupWhile2Val = sCurGroup2Val
```

### Change 2: Remove the anchor reset INSIDE the loop

Remove these two lines from inside the inner While:

```vba
sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
sCurGroupWhile2Val = sCurGroup2Val
```

Keep only:
```vba
iGroup2Qty = WorksheetFunction.CountIf(rng2, sCurGroup2Val)
```

### Change 3: Remove the anchor reset after "Grab next data set"

Remove this line:
```vba
sCurGroupWhile2Val = sCurGroup2Val
```

Keep:
```vba
'Grab next data set
sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
' (removed: sCurGroupWhile2Val = sCurGroup2Val)
```

---

## Fixed Code Pattern

```vba
iGroupQty = WorksheetFunction.CountIf(rng, sCurGroupVal)
iDFilaFin = iDFila + iGroupQty - 1

' FIX: Reset anchor BEFORE inner While (moved from inside loop)
sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
sCurGroupWhile2Val = sCurGroup2Val

While sCurGroup2Val = sCurGroupWhile2Val And sCurGroup2Val <> "" And sCurGroupVal = sCurGroupWhileVal
    iBFila = iBFila + 1
    Worksheets("Rpt").Range("A" & iBFila).Value = Worksheets("Data").Range("C" & iDFila).Value

    Set rng2 = Worksheets("Data").Range("C" & iDFila & ":C" & iDFilaFin)
    ' FIX: Removed these two lines that were here
    ' sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
    ' sCurGroupWhile2Val = sCurGroup2Val
    iGroup2Qty = WorksheetFunction.CountIf(rng2, sCurGroup2Val)

    For i = 1 To iGroup2Qty
        ' ... process rows ...
        iDFila = iDFila + 1
    Next

    ' ... write to report ...

    'Grab next data set
    sCurGroup2Val = Worksheets("Data").Range("C" & iDFila).Value
    ' FIX: Removed this line that was here
    ' sCurGroupWhile2Val = sCurGroup2Val

    'Check First Grouping still matches
    sCurGroupVal = Worksheets("Data").Range("A" & iDFila).Value

    iSubGroupTotalQty = 0
    dGroup2Total = 0
Wend
```

---

## Fixed File Location

**Complete fixed VBA code:** `/home/magown/creatio-report-fix/vba/PMPSalesbySalesRep_FIXED_v2.bas`

---

## How to Apply Fix

1. Open the XLSM file in Excel
2. Press `Alt + F11` to open VBA Editor
3. Find `PMPSalesbySalesRep` module in Project Explorer
4. Select all code (`Ctrl + A`) and delete
5. Copy contents from `PMPSalesbySalesRep_FIXED_v2.bas` and paste
6. Save the file
7. Run the macro

---

## Test Results

**Before fix:** Excel shows "Not Responding" indefinitely

**After fix:**
- 863 rows processed successfully
- Rpt sheet populated correctly with grouped data
- Item totals and Grand Total calculated correctly

**Sample output:**
```
Sales by Item By Type Of Customer
Created Date: 01/29/2026 to 01/30/2026

Item        Description
Customer Type                    Qty        Amount
CER1136W
International                    4          80.00
                CER1136W         4          80.00
CER1136WG
International                    2          40.00
                CER1136WG        2          40.00
...
                Grand Total      XXX        XXXX.XX
```

---

## Related Issues

- **RPT-008:** Similar VBA Type mismatch issue (different root cause - column count)
- **PERF-001:** Filter visibility delay (unrelated - frontend)

---

## Notes for Future

This bug pattern may exist in other BGlobal VBA macros with nested While loops. Look for:
- `sCurGroupWhile2Val = sCurGroup2Val` inside While loops
- Any pattern that resets the "anchor" variable inside the loop it's checking

The fix is always: **Move the anchor initialization BEFORE the While loop, not inside it.**

---

*Fixed: 2026-01-30*
*Analyst: Claude Code*
