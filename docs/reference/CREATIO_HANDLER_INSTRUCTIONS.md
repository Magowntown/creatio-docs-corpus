# Report Button Handler Implementation for `UsrPage_ebkv9e8` (DEV)

## ✅ Status (as of 2026-01-12)
- **Gate A:** ✅ PASSED - API baseline verified
- **Gate B:** ✅ PASSED - Handler deployed with hidden iframe
- **Gate C:** ✅ PASSED - DL-001 browser download working
- **Gate D:** ✅ PASSED - Commission dynamic filter sweep (3 combos; strict PASS/FAIL/INCONCLUSIVE semantics)
- **DL-003:** ✅ Fixed - macro-enabled workbooks are served as `.xlsm` via `UsrExcelReportService/GetReport`.
- **DL-003B:** ✅ Fixed - Commission Generate no longer throws `FormatException` for the known failing combo (`2025-01` + `RDGZ & Consulting LLC`).
- **FLT-004:** 🔄 Active - Commission export can be header-only for older Year‑Months because `Year-Month.Name` is not populated for most rows in DEV (lookup-based filtering excludes everything).

## Overview
This document describes the **verified working** Report button handler logic for the Freedom UI page `UsrPage_ebkv9e8` in DEV.

Canonical implementation:
- `client-module/UsrPage_ebkv9e8_Updated.js`

## ★ Verification (Boris Cherny's #1 Tip)

> "Give Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the quality."

```bash
# Verify API works
python3 scripts/testing/test_report_service.py

# Verify handler is deployed (search for marker)
grep -l "reportDownloadFrame" client-module/*.js
```

## AI orchestration usage (who should use this doc)
- **Claude Code:** uses this doc to implement/deploy the handler and troubleshoot runtime/compilation mismatches.
- **ChatGPT:** should not change code; instead runs **DL-001** in a real browser and logs results to `docs/TEST_LOG.md`.
- **Gemini:** reviews handler changes for regressions and upgrade resilience.

Workflow references:
- Roles + gates + handoffs: `CLAUDE.md` Section 1.5
- Test logging: `docs/TEST_LOG.md`

## Version & migration context (must not be ignored)
- **PROD was originally implemented on Creatio v7 (Classic UI)**.
- **DEV is Creatio v8 (Freedom UI)**.
- PROD is being upgraded to **v8**, and DEV packages/content are expected to be migrated into PROD.

Implication for AI work:
- Treat the **DEV v8/Freedom UI flow** as the target architecture.
- Do not “chase” Classic UI (v7) download patterns (e.g., `UsrURL` + `window.open(...)`) as the long-term solution.
- Prefer solutions that are resilient to **marketplace add-on updates**.

## Assessment: PROD vs DEV report flows (catalogue; verified Jan 10, 2026)
- **PROD (verified):** Classic-era IntExcel export pattern
  - Key creation: `POST /0/rest/IntExcelReportService/GetExportFiltersKey` → `ExportFilterKey_...`
  - Download: `GET /0/rest/IntExcelReportService/GetExportFilteredData/{fileName}/{key}` → `.xlsx`
  - Note: `GET /0/rest/IntExcelReportService/GetReport/...` returns **404** in PROD.
  - **Filtering mechanism:** the ESQ passed to `GetExportFiltersKey` filters by `BGExecutionId` (execution context from `BGReportExecution`).
  - **Sales Group cascade:** compiled PROD page code filters the Sales Group lookup via `BGCommissionSalesGroupByYearMonth` when a Year‑Month is selected.
  - **IW caveat:** `IWPayments` does not exist in PROD today (pre-upgrade).
- **DEV (Freedom UI target flow):**
  - Generate: `POST /0/rest/UsrExcelReportService/Generate` → `ExportFilterKey_...`
  - Download (preferred, DL-003 fix): `GET /0/rest/UsrExcelReportService/GetReport/{key}/{reportNameSegment}` → `.xlsm` (macro-enabled)
  - Download (legacy): `GET /0/rest/IntExcelReportService/GetReport/{key}/{reportNameSegment}` → `.xlsx` (may be macro-enabled; can fail to open in Excel)
  - **Filtering mechanism:** `ReportUtilities.Generate(...)` reads `FiltersConfig` (and optionally `Esq`) from the wrapper service request.

Guidance:
- For DEV/v8, standardize on **Generate → GetReport** (hidden iframe is the canonical download trigger).
- When validating PROD, treat it as **baseline discovery**. Do not change DEV architecture to match Classic-era behavior.

### PROD comparison checklist (no code changes)
Use this when you need to learn how PROD filtering behaves.

Preferred (minimal + repeatable):
```bash
python3 scripts/testing/test_commission_execution_filters.py --env prod --count 3
```

Notes:
- This reproduces the PROD mechanism (`BGReportExecution` + `BGExecutionId` ESQ filter) and uses the correct download endpoint (`GetExportFilteredData`).
- The script records `status` per attempt (`pass`/`fail`/`inconclusive`) and `year_month_validation` in its `summary.json`.
- Log outcomes in `docs/TEST_LOG.md` and summarize key differences in `docs/CREATIO_REPORT_SYSTEM_ANALYSIS.md`.
- Diagnostic-only (not recommended for PROD semantics): add `--allow-derived-yearmonth`.

## Next steps (v8-first; canonical)
1) Regression-test IW_Commission (API-level first; log to `docs/TEST_LOG.md`).
2) Validate Sales Group cascade behavior in DEV using known-good commission-backed combos.
3) If cascade is empty for months expected by the business, treat as data parity and implement fallback cascade logic (v8-first).

## What the handler does (DEV)

1. Resolves the selected `UsrReportesPampa` record to the real `IntExcelReport`:
   - By naming convention (e.g., `UsrReportesPampa.UsrCode = "Commission"` → `IntExcelReport.IntName = "Rpt Commission"`).
2. Cascades the **Sales Group** lookup by the selected **Year‑Month** (UX improvement):
   - Commission: uses `BGCommissionSalesGroupByYearMonth`.
   - IW_Commission: uses the **Payments object** (`IWPayments` / `IWPaymentsInvoice`).
   - If no matching groups exist for the selected Year‑Month, the UI warns but still allows export.
   - Implementation note: if the cascade source returns 0 rows, the UI may fall back to showing all Sales Groups (to avoid blocking selection in data-parity scenarios).
3. Calls `POST /0/rest/UsrExcelReportService/Generate` with:
   - `ReportId` = `IntExcelReport.Id`
   - `YearMonthId` (optional)
   - `SalesRepId` (used as **SalesGroupId** by the current UI; legacy naming)
4. Downloads the file using the preferred endpoint (DL-003 fix):
   - `GET /0/rest/UsrExcelReportService/GetReport/{key}/{reportNameSegment}` (serves filename `.xlsm`)
   - **Canonical trigger:** set a hidden iframe `src` to the download URL (lets the server’s `Content-Disposition: attachment` drive the download).

Legacy (do not prefer):
- `GET /0/rest/IntExcelReportService/GetReport/{key}/{reportNameSegment}` serves macro-enabled workbooks as `.xlsx` in this environment, which can fail to open in Excel.

## Important notes

- Do **not** use legacy `.ashx` export handlers for this flow in DEV.
- Filtering is not applied client-side. In this DEV environment it is applied server-side by `ReportUtilities.Generate(...)` reading `FiltersConfig` on its internal request object.
- `{reportNameSegment}` is not arbitrary. For Commission it is `Commission` (not `Rpt Commission`). It appears to align with `UsrReportesPampa.UsrCode`.
- **Commission Year‑Month semantics (PROD baseline):** treat Year‑Month as a *commission period* (sale rows usually align to `BGTransactionDate` month; credit memos can be allocated to a later period). Do not assume Year‑Month == invoice/date month when validating filters.
- If the browser shows **“File wasn’t available on site”**, confirm the handler is using the **hidden iframe** approach (and that the compiled schema being served matches the deployed handler). Avoid object-URL downloads as the mainline approach.

## Schema location (DEV)
- Designer URL: `https://dev-pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734`
- Schema name: `UsrPage_ebkv9e8`
- Note: there may be multiple `SysSchema` records with this name; use the **most recently modified** one.

## Deploying handler changes

1. Open the schema in the Client Unit Schema Designer.
2. Replace the schema content with the contents of `client-module/UsrPage_ebkv9e8_Updated.js`.
3. Save (Ctrl+S).
4. Compile.
5. Navigate to the page to test the Report button.

## Troubleshooting

If the report doesn't generate:
1. Check browser console (F12) for errors.
2. Verify `POST /0/rest/UsrExcelReportService/Generate` is returning `{ success: true, key: ... }`.
3. If the UI shows `FormatException: Input string was not in a correct format.`, check the backend `UsrExcelReportService` implementation:
   - In this DEV environment, `IntExcelReport.IntEntitySchemaName` may be a **lookup** (not a string). The service must not read it via `GetTypedColumnValue<string>("IntEntitySchemaName")`.
   - Deploy the updated `source-code/UsrExcelReportService_Updated.cs` and re-test.

If generate succeeds but download fails (often HTTP 400):
- The `{reportNameSegment}` is likely wrong. It should match the report code used by the UI (e.g. `Commission`, `IW_Commission`).

If the UI shows **“File wasn't available on site”**:
- Check the browser console. A known root cause is:
  - `TypeError: Cannot read properties of undefined (reading 'UsrURL')`
  - `at Object.handler (UsrPage_ebkv9e8.js:1723:33)`

Important:
- The `UsrPage_ebkv9e8.js:1723` line number refers to the **compiled output**, not what you see in the Schema Designer JSON.
- To locate/fix the source, open `UsrPage_ebkv9e8` in the Client Unit Schema Designer and search within the schema for:
  - the request handler `usr.GenerateExcelReportRequest`
  - `Button_bwctkw5`
  - `UsrURL`
  - `GetReport/`
- In one observed Schema Designer view, the relevant handler block was roughly **lines 53–137** (line numbers vary).

What’s happening:
- The deployed handler is trying to read `something.UsrURL`, but the object is undefined/not initialized, which interrupts the normal download flow.

Fix options:
- Preferred: deploy the updated handler (`client-module/UsrPage_ebkv9e8_Updated.js`) which does not rely on `UsrURL` for downloads.
- Alternative: patch the existing handler:
  - Guard against null/undefined before reading `UsrURL`:
    - `if (reportObject && reportObject.UsrURL) { ... }`
  - Ensure the data is actually loaded before you use it:
    - If the handler depends on `UsrURL`, fetch it explicitly (e.g. via OData `UsrReportesPampa(<id>)?$select=UsrURL`) or ensure the attribute/binding that provides it is loaded before the click handler runs.
  - Add defensive checks around the service response parsing:
    - after `const result = await response.json();` add `if (!result) { ... }`
  - Wrap the download logic in a `try/catch` and surface a meaningful message (and `console.error` the actual exception).

If download works but filters aren't applied:
- Confirm `UsrExcelReportService` is published and uses the DEV mechanism (`FiltersConfig`/`Esq`) rather than ESQ JSON injection.
- Call `GET /0/rest/UsrExcelReportService/GetMethods` and confirm request props include `FiltersConfig` and `Esq`.
- See `docs/REPORT_FILTER_FIX_REQUIRED.md` for the current filter mappings.

If using browser automation (Playwright) and the connection times out:
- Report generation can take 30+ seconds on the server
- The Playwright MCP connection has timeout limits that may be exceeded
- Symptoms: `MCP error -32000: Connection closed`, browser goes to `about:blank`
- Workaround: Use manual browser testing or the Python test script (`scripts/testing/test_report_service.py`) for full download validation
- Browser automation is still useful for form filling and verifying there are no immediate JS errors (e.g., the `UsrURL` TypeError)

If deploying backend code fails to compile with `CS1061: 'Entity' does not contain a definition for 'GetDisplayValue'`:
- Do **not** use `entity.GetDisplayValue(...)` in this environment.
- Use an ESQ joined lookup name column instead:
  - `esq.AddColumn("IntEntitySchemaName.Name")` aliased to `IntEntitySchemaNameName`
  - then read via `entity.GetTypedColumnValue<string>("IntEntitySchemaNameName")`
