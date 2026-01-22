# Investigation Summary: Patricia Goncalves & Report Errors
**Date:** 2026-01-19

## Executive Summary

Two issues were investigated:
1. **Patricia Goncalves missing December 2025 commission records**
2. **Report generation errors causing page freeze**

---

## Issue 1: Patricia Goncalves December 2025 Commission

### Finding: NOT A BUG - QuickBooks Payment Workflow Issue

Patricia's December 2025 commission data is missing because **93% of her December invoices haven't been paid in QuickBooks yet**.

### Evidence

| Metric | Value |
|--------|-------|
| Patricia's December 2025 earners | 63 records |
| Orders with invoice numbers | ✅ All have BGNumberInvoice |
| Invoices in QB Download | **2 out of 30** (7%) |
| Invoices NOT in QB Download | **28 out of 30** (93%) |

### Technical Flow

```
Commission Report Data Flow:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Creatio Order → QB Invoice → QB Payment → QB Download → Commission View
     ✅              ✅            ❌            ❌             ❌
  (EXISTS)       (SYNCED)     (NOT DONE)    (MISSING)      (MISSING)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

The commission view JOIN:
```sql
Order.BGNumberInvoice = BGCommissionReportQBDownload.BGCleanInvoiceNumber
```

Since Patricia's December invoices aren't in QB Download (because they haven't been paid in QB), they don't appear in the commission report.

### Why January 2026 Works

Patricia has 132 January 2026 commission records ($41,263.86) because those are invoices that were **paid** in January (regardless of when they were created).

### Action Required

**QuickBooks accounting team** must process payments against December 2025 invoices. Once payments are recorded in QB, the next "Get QuickBooks Commissions" sync will automatically populate the data.

---

## Issue 2: Report GUID Errors and Page Freeze

### Finding: BUG IDENTIFIED - Fix Implemented

"Rpt Sales By Line" fails with:
```
FormatException: Guid should contain 32 digits with 4 dashes
```

### Root Cause

The `IntExcelReport.IntEsq` JSON contains a filter with `@P1@` placeholder:
```json
"parameter": {"value": "@P1@"}
```

The `IntExcelExport.ReportUtilities.ConvertStringToEsq()` method cannot parse `@P1@` as a GUID.

### Fix Implemented

Added `SanitizeEsqJson()` method to `UsrExcelReportService_Updated.cs`:

```csharp
private string SanitizeEsqJson(string esqJson)
{
    // If ESQ contains @P<number>@ patterns, clear the filter items
    // This mimics the working Commission report pattern (0 filter items)
    // Filters are then applied via FiltersConfig instead
}
```

### Affected Reports

| Category | Count | Status |
|----------|-------|--------|
| With @P placeholders | 1 | ✅ **Fixed** by sanitization |
| Valid ESQ (no placeholders) | 14 | ✅ Already work |
| Empty ESQ | 18 | ⚠️ Need configuration |

### Deployment Required

**File:** `source-code/UsrExcelReportService_Updated.cs`

**PROD URL:**
```
https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
```

### Page Freeze Causes

1. **GUID parsing errors** - ✅ Fixed by SanitizeEsqJson
2. **Reports with empty ESQ** - Need configuration
3. **Large reports timing out** - Performance issue (separate)

---

## Files Created/Modified

| File | Purpose |
|------|---------|
| `source-code/UsrExcelReportService_Updated.cs` | Added SanitizeEsqJson() |
| `CLAUDE.md` | Added RPT-002, DATA-004 |
| `/tmp/trace_patricia_december_gap.py` | Investigation script |
| `/tmp/test_sanitize_v2.py` | Sanitization test |

---

## Recommendations

### Immediate Actions
1. **Deploy backend fix** to resolve "Rpt Sales By Line" GUID error
2. **Communicate to QB team** that December invoices need payment processing

### Future Improvements
1. Configure empty ESQ reports (18 reports need IntEsq populated)
2. Add timeout handling for large reports to prevent page freeze
3. Consider caching for frequently-run reports

---

## Verification Commands

```bash
# Test Patricia's December gap
python3 /tmp/trace_patricia_december_gap.py

# Test ESQ sanitization
python3 /tmp/test_sanitize_v2.py

# Comprehensive status check
python3 /tmp/comprehensive_status_check.py
```
