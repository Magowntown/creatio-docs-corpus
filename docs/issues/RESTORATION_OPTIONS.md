# URGENT: Report Restoration Options

**Status:** Client reports broken for 3 weeks - reports opening in browser tabs instead of downloading Excel
**Root Cause:** Freedom UI (v8) migration removed Classic-era Excel mixin logic
**Updated:** 2026-01-28

---

## Executive Summary

### What Was Working (Before Freedom UI Migration)

```
CLASSIC UI (v7) FLOW:
┌─────────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│ Report Button Click │────>│ BGIntExcelreportMixin│────>│IntExcelReportService│
└─────────────────────┘     │ (Classic UI Mixin)   │     │ GetExportFiltersKey │
                            │                      │     │ GetExportFilteredData│
                            └──────────────────────┘     └────────────────────┘
                                     │                            │
                                     │                            v
                                     │                    ┌────────────────┐
                                     │                    │ Excel Download │
                                     v                    └────────────────┘
                            [Looker: window.open(URL)]
```

### What Broke (After Freedom UI Migration)

```
FREEDOM UI (v8) FLOW:
┌─────────────────────┐     ┌──────────────────────────────┐
│ Report Button Click │────>│ BGlobalLookerStudio Handler  │
└─────────────────────┘     │ (ONLY handles Looker!)       │
                            │                              │
                            │ - Builds URL params          │
                            │ - window.open(UsrURL + Param)│
                            │                              │
                            │ NO EXCEL LOGIC EXISTS!       │
                            └──────────────────────────────┘
                                         │
                                         v
                               ALL reports open in new tab
                               (Excel reports broken!)
```

---

## Root Cause Analysis

1. **Original PROD (v7 Classic UI)** used `BGIntExcelreportMixin` - a Classic UI mixin that called `IntExcelReportService` endpoints for Excel downloads

2. **Freedom UI (v8) parent schema** (`BGlobalLookerStudio_UsrPage_ebkv9e8`) ONLY handles Looker Studio reports:
   - Builds filter parameters for Looker URLs
   - Calls `window.open(UsrURL + Param)`
   - **Has NO Excel download logic**

3. **After migration**, Excel reports were routed to `window.open()` which only works for Looker URLs (HTTP URLs), not Excel downloads

4. **Classic UI mixins don't work in Freedom UI** - they are incompatible UI frameworks

---

## Available Options

### Option A: Empty Handler (Restore Parent Behavior)
**File:** `client-module/UsrPage_ebkv9e8_RESTORE_ORIGINAL.js`
**Result:** ❌ Will NOT fix Excel - parent only handles Looker

```javascript
// Empty handler - delegates everything to parent
handlers: []
```

### Option B: Use Original IntExcelReportService
**File:** `client-module/UsrPage_ebkv9e8_ORIGINAL_INTEXCEL.js`
**Result:** Uses BGlobal's original IntExcelReportService endpoints

```
Flow:
1. Report button clicked
2. Check UsrURL: Has URL? -> Looker (delegate to parent)
                 No URL? -> Excel (use IntExcelReportService)
3. For Excel:
   - POST /0/rest/IntExcelReportService/GetExportFiltersKey
   - GET /0/rest/IntExcelReportService/GetExportFilteredData/{name}/{key}
```

**Pros:**
- Uses BGlobal's original service (not our custom code)
- Closest to what worked before

**Cons:**
- May not have filtering (filters were set via BGReportExecution in Classic UI)
- IntExcelReportService endpoints may not work the same in v8

### Option C: Use Our UsrExcelReportService
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19_LookerFix.js` (currently in PROD)
**Result:** Uses our custom service with proper filtering

```
Flow:
1. Report button clicked
2. Check UsrURL: Has URL? -> Looker (delegate to parent)
                 No URL? -> Excel (use UsrExcelReportService)
3. For Excel:
   - POST /0/rest/UsrExcelReportService/Generate
   - GET /0/rest/UsrExcelReportService/GetReport/{key}/{name}
```

**Pros:**
- Has proper filtering logic built in
- We control the code

**Cons:**
- Requires our backend UsrExcelReportService to be deployed

### Option D: Diagnostic Handler (Temporary)
**File:** `client-module/UsrPage_ebkv9e8_DIAGNOSTIC.js`
**Result:** Logs everything to help debug

Deploy this temporarily to understand what's happening in PROD.

---

## Recommended Actions

### Immediate (Today)

1. **Verify PROD credentials** - Update `.env` if needed (current ones are failing)

2. **Deploy Diagnostic Handler** to PROD to understand current state:
   ```
   URL: https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
   Content: client-module/UsrPage_ebkv9e8_DIAGNOSTIC.js
   ```

3. **Test which endpoints exist in PROD:**
   - `/0/rest/IntExcelReportService/GetExportFiltersKey` - Original BGlobal endpoint
   - `/0/rest/UsrExcelReportService/Generate` - Our custom endpoint

### If IntExcelReportService Works

Deploy `UsrPage_ebkv9e8_ORIGINAL_INTEXCEL.js` - this uses BGlobal's original service

### If Only UsrExcelReportService Works

Deploy `BGApp_eykaguu_UsrPage_ebkv9e8_v19_LookerFix.js` - this uses our custom service (v19)

---

## What Client Needs to Know

The reports page worked differently before the Freedom UI migration:

| Before (Classic UI v7) | After (Freedom UI v8) |
|------------------------|----------------------|
| Excel reports used Classic-era mixin | Classic mixins don't exist in Freedom UI |
| `BGIntExcelreportMixin` handled downloads | Parent schema only handles Looker URLs |
| IntExcelReportService was triggered by mixin | No automatic Excel triggering |

**Solution:** Deploy a Freedom UI handler that properly routes Excel reports to the correct service endpoint.

---

## Files Reference

| File | Purpose |
|------|---------|
| `client-module/UsrPage_ebkv9e8_RESTORE_ORIGINAL.js` | Empty handler (won't fix Excel) |
| `client-module/UsrPage_ebkv9e8_ORIGINAL_INTEXCEL.js` | Uses original IntExcelReportService |
| `client-module/UsrPage_ebkv9e8_DIAGNOSTIC.js` | Diagnostic logging |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19_LookerFix.js` | Uses UsrExcelReportService |
| `client-module/BGlobalLookerStudio_UsrPage_ebkv9e8_Fixed.js` | Parent schema (Looker only) |

---

## CRITICAL Understanding

The client says "it was working before without our work" - this is TRUE for Classic UI (v7).

However, **Freedom UI (v8) requires a custom handler** because:
1. Classic-era mixins don't exist in Freedom UI
2. The BGlobal parent schema only handles Looker reports
3. Excel reports need explicit handling that wasn't needed in Classic UI

There is no "restore to original" that will fix Excel in Freedom UI - a handler is REQUIRED.
