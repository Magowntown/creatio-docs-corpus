# Report Button Investigation - Consolidated Findings

## Version context (why PROD vs DEV differ)
- **PROD** was originally built for **Creatio v7 (Classic UI)**.
- **DEV** is **Creatio v8 (Freedom UI)**.
- PROD is being upgraded to **v8** and is expected to receive **DEV packages/contents**.

Practical implication: when you see differences in client-side behavior (popups, request types, download triggers), it may be because you are comparing **Classic UI patterns** with **Freedom UI patterns**.

## Assessment summary (catalogue; as of January 12, 2026)
- **PROD verified behavior (Classic-era IntExcel mixin flow):**
  - `POST /0/rest/IntExcelReportService/GetExportFiltersKey` returns an `ExportFilterKey_...`.
  - Download is via `GET /0/rest/IntExcelReportService/GetExportFilteredData/{fileName}/{key}` (returns `.xlsx`).
  - `GET /0/rest/IntExcelReportService/GetReport/...` returns **404** in PROD.
  - The ESQ sent to `GetExportFiltersKey` filters the dataset by `BGExecutionId` (execution context), as captured in `test-artifacts/flow-review/prod/payloads/*GetExportFiltersKey.json`.
- **PROD Commission semantic note (verified Jan 10, 2026):** “Year‑Month” behaves like a *commission period* (sale rows typically align to transaction month; credit memos can be allocated to a later period). Do not assume Year‑Month == invoice/date month when validating filtering.
- **DEV target behavior (Freedom UI):**
  - `POST /0/rest/UsrExcelReportService/Generate` returns a key.
  - Download should be via wrapper endpoint `GET /0/rest/UsrExcelReportService/GetReport/{key}/{reportNameSegment}` to serve `.xlsm` (macro-enabled) and avoid DL-003.
  - Legacy endpoint `IntExcelReportService/GetReport` may serve macro-enabled content as `.xlsx`.

Direction:
- Keep the solution **v8/Freedom UI-first** and avoid reliance on Classic-era URL export patterns.

## AI orchestration usage (evidence-first debugging)
- When debugging download failures, do not guess. Use the handoff checklist in `CLAUDE.md` Section 1.5.
- DL-001 failures must include: Generate status, GetReport status + `Content-Disposition`, console errors, and downloaded file details.
- Log all outcomes to `docs/TEST_LOG.md` so the next AI can act immediately.

## ★ Verification Methods (Boris Cherny's #1 Tip)

> "Give Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the quality of the final result."

**Use these verification commands:**

| What to Verify | Command |
|----------------|---------|
| API baseline | `python3 scripts/testing/test_report_service.py` |
| Handler deployed | `python3 scripts/testing/verify_gate_b_v2.py --env dev` |
| Browser download | `python3 scripts/investigation/review_report_flow.py --env dev` |
| Excel filters | Open file, check Data sheet for Year-Month + Sales Group values |

**Gate Status (as of 2026-01-10):**
- ✅ Gate A: API baseline PASSED
- ✅ Gate B: Runtime verification PASSED
- ✅ Gate C: DL-001 browser download PASSED

## Problem Statement
The "Report" button on the DEV Creatio Reports page (`UsrPage_ebkv9e8`) generated an error:
```
"Excel template with Id 9de295e4-7c79-4de6-9218-8bb5e47ce81b not found"
```

## Status (DEV)
- ✅ The underlying mismatch between `UsrReportesPampa` (UI lookup) and `IntExcelReport` (real report definition) is understood and handled in the page handler.
- ✅ The working download flow should use `GET /0/rest/UsrExcelReportService/GetReport/{key}/{reportNameSegment}` (wrapper that serves `.xlsm`).
- Legacy: `IntExcelReportService/GetReport` returns ZIP workbook bytes but may serve filename `.xlsx` even when macros exist.
- ✅ Backend filtering is working for Commission and IW when using the server-side `FiltersConfig`/`Esq` mechanism.
- ⚠ UI may still show **“File wasn't available on site”** if either:
  - a JS exception interrupts the handler flow (e.g. `UsrURL` undefined), or
  - the handler uses an object-URL download approach and revokes the object URL too quickly right after triggering the download.

## Known UI error: `UsrURL` undefined

### Symptoms
- Clicking the Report button appears to start a download, but the browser shows an error like “File wasn't available on site”, and the success toast may not show.

### Root cause (browser console)
A known console error is:
- `TypeError: Cannot read properties of undefined (reading 'UsrURL')`
- `at Object.handler (UsrPage_ebkv9e8.js:1723:33)`

Important:
- `UsrPage_ebkv9e8.js:1723` refers to the **compiled output** of the schema, not the JSON you see in the Schema Designer.

### Where to look in the schema
This error is coming from the Report button handler logic:
- Find the `handlers` entry for `usr.GenerateExcelReportRequest`.
- In one observed Schema Designer view, the handler block was roughly **lines 53–137**, with the download logic around **lines 111–127** (line numbers will vary).
- Look around the response/download section that starts near:
  - `const result = await response.json();`
  - `if (result.success && result.key) { ... }`
  - `/0/rest/UsrExcelReportService/GetReport/...` (preferred)

### Recommended fix pattern
Add defensive checks and error handling:
- Guard against null/undefined before reading report configuration fields like `UsrURL`.
- Ensure the data is actually loaded before you use it:
  - If the handler depends on `UsrURL`, fetch it (or the object that contains it) before attempting to read it.
- Null/undefined guard after parsing JSON:
  - if `result` is falsy, show a clear error and return.
- Wrap the download logic in a `try/catch` so browser/network errors produce actionable messages.

Example patch sketch (canonical hidden iframe):
```js
const result = await response.json();
if (!result) {
  Terrasoft.showErrorMessage("Failed to generate report: No response from server");
  return next?.handle(request);
}

if (result.success && result.key) {
  try {
    // Canonical: hidden iframe download
    let iframe = document.getElementById("reportDownloadFrame");
    if (!iframe) {
      iframe = document.createElement("iframe");
      iframe.id = "reportDownloadFrame";
      iframe.style.display = "none";
      iframe.setAttribute("aria-hidden", "true");
      document.body.appendChild(iframe);
    }
    iframe.src = downloadUrl;
  } catch (downloadError) {
    Terrasoft.showErrorMessage("Error downloading file: " + downloadError.message);
    console.error("Download error:", downloadError);
  }
} else {
  const errorMessage = result.message || result.error || "Unknown error";
  Terrasoft.showErrorMessage("Failed to generate report: " + errorMessage);
}
```

### Historical note (only if object-URL downloads are reintroduced)
Object-URL downloads can fail in Chrome if `URL.revokeObjectURL(...)` happens too early. This repo treats **hidden iframe** as canonical; avoid object URLs as the mainline approach.

### Status
- Preferred fix: deploy the canonical handler (`client-module/UsrPage_ebkv9e8_Updated.js`) which uses **hidden iframe** download (avoids `UsrURL` dependency and object-URL timing issues).
- As of January 9, 2026:
  - **Gate A PASSED:** API baseline verified (Generate + GetReport working for Commission and IW_Commission)
  - **Gate B PASSED:** runtime verification confirms canonical handler is served
  - **Gate C PASSED:** DL-001 browser download verified

### Deployment approach
1. **Preferred:** Use ChatGPT with Playwright to deploy via browser (see `CLAUDE.md` Section 5.3 for prompt)
2. **Manual:** Open `https://dev-pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734`, Ctrl+A, paste contents of `client-module/UsrPage_ebkv9e8_Updated.js`, Ctrl+S
3. **Verify:** Search for `reportDownloadFrame` in the saved code

### Fix options
- Preferred: deploy the updated handler (`client-module/UsrPage_ebkv9e8_Updated.js`) which does not rely on `UsrURL` for downloads.
- Alternative: patch the existing handler at the failing line to guard against null/undefined and ensure `UsrURL` is actually loaded/bound.

## Root Cause Analysis

### The Two Tables
The system has two separate tables for reports:

1. **UsrReportesPampa** (UI Lookup Table)
   - Used as the data source for the `BGPampaReport` dropdown on the Reports page
   - Contains custom fields: `Name`, `UsrCode`, `UsrURL`, `UsrActive`
   - Example: Commission record has ID `9de295e4-7c79-4de6-9218-8bb5e47ce81b`

2. **IntExcelReport** (Excel Report Definition Table)
   - Contains actual Excel report templates
   - Contains: `IntName`, `IntEntitySchemaName`, `IntFile`, `IntExcelReportType`
   - Example: "Rpt Commission" has ID `4ba4f203-7088-41dc-b86d-130c590b3594`

### The Mismatch
- **NO foreign key exists** between `UsrReportesPampa` and `IntExcelReport`
- The relationship is by **naming convention only**:
  - `UsrReportesPampa.UsrCode = "Commission"` maps to `IntExcelReport.IntName = "Rpt Commission"`
- The UI sends `UsrReportesPampa.Id` but the service expects `IntExcelReport.Id`

### Mapping Table

| UsrReportesPampa (UI) | ID | IntExcelReport | ID |
|-----------------------|----|----------------|----|
| Commission | 9de295e4-... | Rpt Commission | 4ba4f203-... |
| SalesByItem | 839e5bf3-... | Rpt Sales by Item | c4f4e32c-... |
| SalesByLine | d8483e56-... | Rpt Sales by Line | 0b40d51d-... |
| SalesBySalesGroup | 1515dc95-... | Rpt Sales by Sales Group | a935a791-... |
| IW_Commission | 692fe734-... | IW_Commission | 07c77859-... |

## Proposed Solutions

### Option 1: Add Foreign Key Column (Recommended for hardening)
Add a new lookup column `UsrIntExcelReport` to `UsrReportesPampa` that references `IntExcelReport`.

**Pros:** Clean solution, explicit relationship, easy to maintain
**Cons:** Requires schema change and data migration

Decision:
- Treat this as a **Phase 2/3 hardening** task (upgrade-resilience), not a prerequisite for fixing DL-001.

### Option 2: Lookup by Name Pattern in Handler (current Phase 1 approach)
Modify the Freedom UI handler to:
1. Get the selected `UsrReportesPampa` record's `UsrCode`
2. Query `IntExcelReport` for a matching `IntName` (e.g., "Rpt " + UsrCode)
3. Send the `IntExcelReport.Id` to the service

**Pros:** No schema changes needed
**Cons:** Relies on naming convention, fragile if names don't match

### Option 3: Direct Mapping Dictionary
Hardcode a mapping in the handler between `UsrReportesPampa.Id` and `IntExcelReport.Id`.

**Pros:** Simplest to implement
**Cons:** Hardcoded, requires code changes when adding new reports

## Fixed Issues (Already Resolved)

1. ✅ BPMCSRF authentication header added
2. ✅ Download URL pattern fixed (`/GetReport/{key}/{fileName}`)
3. ✅ Hidden iframe download approach (stable download trigger; avoids object URL timing issues)
4. ✅ BGSalesGroup null handling (was BGSalesRep)
5. ✅ Commission + IW filtering fixed in DEV via server-side `FiltersConfig`/`Esq`

## Current Handler Code Location
- Schema UID (active/most recent in DEV): `1d5dfc4d-732d-48d7-af21-9e3d70794734`
- Note: `UsrPage_ebkv9e8` has multiple `SysSchema` records in DEV; ensure you edit the **most recently modified** one.
- File: `client-module/UsrPage_ebkv9e8_Updated.js`

## IntExcelReport Details for Commission
```json
{
  "Id": "4ba4f203-7088-41dc-b86d-130c590b3594",
  "IntName": "Rpt Commission",
  "IntEntitySchemaName": "BGCommissionReportDataView",
  "IntSheetName": "Data"
}
```

## Files Created During Investigation
- `scripts/investigation/investigate_pampa_report.py` - Schema investigation
- `scripts/investigation/find_commission_in_pampa.py` - Table comparison
- `scripts/testing/test_report_service.py` - Service testing
- `scripts/deployment/deploy_page_handler.py` - Handler deployment

## Next Steps
1. Validate IW_Commission end-to-end (Generate + GetReport segment + filters) after the backend service is deployed/published.
2. UX improvement (optional): cascade Sales Group options by selected Year‑Month:
   - Commission: source `BGCommissionSalesGroupByYearMonth`.
   - IW_Commission: uses the **Payments object** (`IWPayments` / `IWPaymentsInvoice`).
3. UX improvement (optional): add a preflight has-data/rowcount check before generating the workbook (warn early; allow export anyway).
4. If additional reports are added, consider Option 1 (explicit FK from `UsrReportesPampa` → `IntExcelReport`) to avoid relying on naming conventions.
