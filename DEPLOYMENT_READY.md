# Deployment Ready: RPT-002 Fix

## Status: ✅ FIX IMPLEMENTED - AWAITING DEPLOYMENT

---

## Quick Deploy Instructions

### Step 1: Open Source Code Schema Designer

**PROD:**
```
https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
```

**DEV:**
```
https://dev-pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
```

### Step 2: Replace Code

1. Wait for editor to load
2. Select all (Ctrl+A)
3. Copy contents from: `source-code/UsrExcelReportService_Updated.cs`
4. Paste into editor
5. Click **Save and Publish**
6. Wait for compilation

### Step 3: Verify

Test "Rpt Sales By Line" report:
```python
# Should return success: true (previously failed with GUID error)
payload = {"ReportId": "0b40d51d-4935-4918-97f2-45352aed341f"}
```

---

## What the Fix Does

### Problem
"Rpt Sales By Line" fails with:
```
FormatException: Guid should contain 32 digits with 4 dashes
```

### Root Cause
The ESQ JSON contains `@P1@` placeholder that IntExcelExport library can't parse:
```json
"parameter": {"value": "@P1@"}
```

### Solution
Added `SanitizeEsqJson()` method (lines 1358-1425) that:
1. Detects `@P<number>@` patterns
2. Clears filter items using balanced brace matching
3. Allows filters to be applied via FiltersConfig instead

### Code Location
File: `source-code/UsrExcelReportService_Updated.cs`
Method: `SanitizeEsqJson()` at line 1358
Called by: `GetIntEsqJson()` at line 1441

---

## Affected Reports

| Report | Current Status | After Fix |
|--------|---------------|-----------|
| Rpt Sales By Line | ❌ GUID error | ✅ Works |
| Rpt Commission | ✅ Works | ✅ Works |
| 18 Empty ESQ reports | ❌ queryConfig error | ❌ Need config |

---

## Patricia Goncalves Issue

**NOT RELATED TO THIS FIX**

Patricia's December 2025 commission is missing because 93% of her December invoices haven't been **paid** in QuickBooks yet.

**Action Required:** QB accounting team must process December 2025 invoice payments.

---

## Verification Commands

After deployment:
```bash
# Test report generation
curl -X POST "https://pampabay.creatio.com/0/rest/UsrExcelReportService/Generate" \
  -H "Content-Type: application/json" \
  -d '{"ReportId": "0b40d51d-4935-4918-97f2-45352aed341f"}'

# Expected: {"GenerateResult":{"success":true,"key":"ExportFilterKey_..."}}
```

---

## Rollback

If issues occur, revert to previous code version via Creatio schema history.
