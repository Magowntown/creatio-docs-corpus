# VBA Directory

> Excel macro fixes for BGlobal report templates.

## Files

| File | Purpose | Issue |
|------|---------|-------|
| `PMPSalesbySalesRep_FIXED.bas` | V1 infinite loop fix | RPT-009 |
| `PMPSalesbySalesRep_FIXED_v2.bas` | V2 refined fix | RPT-009 |

## RPT-009: Infinite Loop Fix

### Problem
BGlobal's nested While loops in the PMPSalesbySalesRep Excel template reset anchor variables inside the loop body, causing infinite loops.

### Root Cause (from CLAUDE.md)
```
VBA anchor variable pattern bug: BGlobal's nested While loops
reset anchor variables inside the loop, causing infinite loops.
```

### Fix
Move anchor reset BEFORE the While loop, remove resets inside loop.

### Before (Broken)
```vba
While Not IsEmpty(ws.Cells(row, 1))
    ' Process row
    anchor = ws.Cells(row, 1)  ' BAD: Reset inside loop
    row = row + 1
Wend
```

### After (Fixed)
```vba
anchor = ws.Cells(row, 1)  ' GOOD: Reset before loop
While Not IsEmpty(ws.Cells(row, 1))
    ' Process row
    row = row + 1
Wend
```

## Related Reports

This fix applies to the "Sales By Item By Type Of Customer" report which uses the PMPSalesbySalesRep Excel template.

## Related Documentation

- `docs/reference/MASTER_CATALOG.md` - Report catalog
- `docs/reference/RISK_CHECKLIST.md` - VBA gotchas section
- `CLAUDE.md` - Lesson learned #13
