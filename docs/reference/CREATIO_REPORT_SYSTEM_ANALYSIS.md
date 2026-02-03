# Creatio Report System Analysis
## DEV Environment - Commission Report & IW_Commission Report

**Last updated:** January 12, 2026
**Environment:** https://dev-pampabay.creatio.com
**Target reports:** `Rpt Commission` (primary), `IW_Commission` (secondary)

## ✅ Gate Status (as of 2026-01-10)
|| Gate | Status | Description |
||------|--------|-------------|
|| A | ✅ PASSED | API baseline (Commission + IW_Commission) |
|| B | ✅ PASSED | Handler deployed with hidden iframe |
|| C | ✅ PASSED | DL-001 browser download working |
|| D | ✅ PASSED | Commission dynamic filter sweep (3 combos; strict PASS/FAIL/INCONCLUSIVE semantics) |

---

## ★ Verification Commands

> "Give Claude a way to verify its work. It will 2-3x the quality." - Boris Cherny

```bash
python3 scripts/testing/test_report_service.py                    # Commission
CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py  # IW
```

---

## AI orchestration usage (how to use this document)
- This file is a **technical reference** (flows, endpoints, mappings). It is not the execution checklist.
- Execute work via the orchestration map in `CLAUDE.md` Section 1.5 and log results in `docs/TEST_LOG.md`.
- DL-001 (real browser download) is the gate before hardening.

## Version context (critical)
- **PROD was originally designed/implemented on Creatio v7 (Classic UI)**, while **DEV is on Creatio v8 (Freedom UI)**.
- The migration plan is to **upgrade PROD to v8** and then **move/align DEV packages and page contents into PROD**.

Implications for this repo:
- When comparing “PROD vs DEV”, differences may reflect **UI framework + platform version**, not just business logic.
- The long-term “correct” solution should be **Freedom UI compatible** (v8) and minimize reliance on any **marketplace add-on implementation details** that can change during upgrades.

---

## Glossary (load-bearing terms)
- **UsrReportesPampa / BGPampaReport**: UI lookup that drives the “Report” dropdown on `UsrPage_ebkv9e8`.
- **IntExcelReport**: the real Excel template definition record. The UI selection must ultimately map to an `IntExcelReport.Id`.
- **ReportId**: `IntExcelReport.Id`.
- **ExportFilterKey**: key returned by report generation endpoints (format: `ExportFilterKey_...`). It is a pointer to a server-side generated export file.
- **reportNameSegment** (DEV): the URL segment used for `GetReport/{key}/{reportNameSegment}` downloads (e.g. `Commission`, `IW_Commission`).
- **fileName** (PROD): the URL segment used for `GetExportFilteredData/{fileName}/{key}` downloads. In Classic-era mixin code this is also the downloaded filename.
- **BGReportExecution**: execution context table. Stores selected filter values (e.g. `BGYearMonth`, `BGSalesGroup`).
- **BGExecutionId**: column used to join the report’s dataset to the `BGReportExecution` row.
- **BGCommissionReportDataView**: Commission report root dataset/view. In PROD it is filtered by `BGExecutionId`.
- **BGCommissionSalesGroupByYearMonth**: SQL-view-backed model used to constrain Sales Group options when a Year‑Month is selected (valid combos source).

## Hierarchy: what drives what (Commission)
1. **UI selections** on `UsrPage_ebkv9e8`
   - Report (UsrReportesPampa)
   - Year‑Month (BGYearMonth)
   - Sales Group (BGSalesGroup)
2. **Execution context**
   - PROD: insert `BGReportExecution` with the selected Year‑Month + Sales Group
3. **Dataset query**
   - Commission uses `BGCommissionReportDataView`
   - PROD filters by `BGExecutionId = <executionId>`
4. **Export key creation**
   - PROD: `IntExcelReportService/GetExportFiltersKey` → `ExportFilterKey_...`
   - DEV: `UsrExcelReportService/Generate` → `ExportFilterKey_...`
5. **File download**
   - PROD: `IntExcelReportService/GetExportFilteredData/{fileName}/{key}`
   - DEV (preferred, DL-003 fix): `UsrExcelReportService/GetReport/{key}/{reportNameSegment}` (serves `.xlsm` when macros exist; otherwise `.xlsx`)
   - DEV (legacy): `IntExcelReportService/GetReport/{key}/{reportNameSegment}` (serves `.xlsx` even when macros exist)

## Sales Group cascade (UX improvement; DEV/Freedom UI)
To reduce “empty export” confusion, the page can **cascade Sales Group options by the selected Year‑Month**:
- **Commission:** constrain Sales Group lookup using `BGCommissionSalesGroupByYearMonth` (source-of-truth valid combos).
- **IW_Commission:** uses the **Payments object** (`IWPayments` / `IWPaymentsInvoice`) to derive valid Sales Groups for the selected Year‑Month.

Latest findings (important for troubleshooting):
- **PROD already implements the Commission cascade** in compiled page code (filters Sales Group via `BGCommissionSalesGroupByYearMonth`). If DEV shows “no groups” for a month that PROD supports, treat it as **data parity** rather than assuming the cascade logic is wrong.
- **IWPayments does not exist in PROD today** (pre-upgrade), so IW cascade logic is currently DEV-only unless/until PROD is upgraded to v8 and receives the IW data model.

Rule:
- If no valid groups are found for a selected Year‑Month, the UI should warn but still allow exporting (export may legitimately be header-only).
- To avoid blocking the user, the lookup may fall back to showing **all** Sales Groups when the cascade source returns zero results (data-parity scenarios).

## PROD observations (verified)
As of **January 10, 2026**, PROD Commission export behaves like Classic-era `IntExcelreportMixin`:
- `POST /0/rest/IntExcelReportService/GetExportFiltersKey` returns an `ExportFilterKey_...`.
- Download is **not** `GetReport` (that endpoint returns 404 in PROD). Instead, the client downloads via:
  - `GET /0/rest/IntExcelReportService/GetExportFilteredData/{fileName}/{key}`

Filtering mechanism (PROD):
- The page inserts a `BGReportExecution` record storing the selected `BGYearMonth` + `BGSalesGroup`.
- The report ESQ filters `BGCommissionReportDataView` by `BGExecutionId = <executionId>`.
- Evidence: the captured POST body to `IntExcelReportService/GetExportFiltersKey` includes `columnPath":"BGExecutionId"` (see `test-artifacts/flow-review/prod/payloads/*GetExportFiltersKey.json`).

Evidence (script validation):
- Command (historical):
  - `python3 scripts/testing/test_commission_execution_filters.py --env prod --count 5`
- Result: **5/5 passing combinations** found (7 attempts) using the real PROD flow.

Recommended PROD validation (safe, minimal):
```bash
python3 scripts/testing/test_commission_execution_filters.py --env prod --count 3
```

What we learned from PROD (Commission semantics):
- **Root dataset**: `BGCommissionReportDataView`, filtered by `BGExecutionId` (execution context from `BGReportExecution`).
- **Sales Group consistency**: in a sampled execution (`2025-11` / `Pampa Bay - Online`, 205 rows), both `BGOrder.BGSalesGroup` and `BGSalesRep.BGSalesGroupLookup` were populated and matched **205/205** rows.
- **Year‑Month meaning**: `BGYearMonth` behaves like a *commission period*, not a naive `Order.Date` / `Order.BGInvoiceDate` month.
  - For `Sale` rows in the same sample, `BGYearMonth` matched the month of `BGTransactionDate` for **199/202** rows.
  - For `Credit Memo` rows, we observed shifting into the following period (e.g., `BGYearMonth` matching `month(BGTransactionDate + 1 month)`), consistent with refunds/credits being applied to a later commission period.

Practical implication (keep focus on pre-filtered Excel):
- When validating “filters are applied”, do **not** derive Year‑Month combos from Orders by date month. Use commission-backed discovery (`BGCommissionSalesGroupByYearMonth` or `BGCommissionReportDataView`) so your selected (Year‑Month, Sales Group) pairs actually correspond to commission rows.

The goal is not to “make DEV behave like Classic”; it is to document PROD behavior so the v8/Freedom implementation can match the intended filtering semantics after upgrade.

---

## Next steps (v8-first; canonical)
1) **Gate E regression:** validate IW_Commission end-to-end in DEV (API-level first; then browser-level if needed).
2) **Sales Group cascade parity:** validate the DEV cascade using a known-good (Year‑Month, Sales Group) combo from commission-backed discovery.
3) **If DEV cascade is empty for business-expected months:** treat as data parity; then implement a v8-first fallback cascade (derive valid Sales Groups from `BGCommissionReportDataView` when `BGCommissionSalesGroupByYearMonth` returns 0 rows).

## Executive Summary (DEV-verified)

### ✅ Download is working (bytes)
- `POST /0/rest/UsrExcelReportService/Generate` → returns `key` (e.g. `ExportFilterKey_...`)
- The report bytes returned by GetReport are a valid ZIP workbook (`PK` header).

### ⚠️ DL-003: Excel open failure risk (extension mismatch)
- In this environment, workbooks often contain macros (`xl/vbaProject.bin`) but the marketplace `IntExcelReportService/GetReport` endpoint serves filename `.xlsx`.
- Some Excel installations refuse to open macro-enabled content when served as `.xlsx`.

### ⚠️ DL-003B: Commission Generate FormatException for some combos
Observed user-facing error in DEV:
- `Failed to generate report: FormatException: Input string was not in a correct format.`
- Example combo: Year‑Month `2025-01`, Sales Group `RDGZ & Consulting LLC`.

Most likely root cause (DEV env detail):
- `IntExcelReport.IntEntitySchemaName` can be a **lookup** in DEV (OData returns `{ value, displayValue }`).
- Backend code that reads it as a string (`GetTypedColumnValue<string>("IntEntitySchemaName")`) can throw `FormatException`.

Implementation constraint discovered during deploy (DEV, 2026-01-12):
- This Creatio build does **not** compile with `entity.GetDisplayValue(...)` (CS1061).
- Fix must use ESQ joined lookup name column (`IntEntitySchemaName.Name`) instead of `GetDisplayValue`.

Fix direction:
- In `UsrExcelReportService`, resolve root schema name using joined `IntEntitySchemaName.Name` (via ESQ column `IntEntitySchemaName.Name` aliased as `IntEntitySchemaNameName`), with `IntEsq.rootSchemaName` as fallback.

Verification:
- Deploy/publish updated `UsrExcelReportService` and re-run the exact combo; Generate should return a key.

### ✅ Target download endpoint (DL-003 fix)
- `GET /0/rest/UsrExcelReportService/GetReport/{key}/{reportNameSegment}` → serves the same bytes but with:
  - filename `.xlsm` + macro-enabled MIME type when macros exist
  - filename `.xlsx` + standard xlsx MIME type when macros do not exist
- Canonical v8 UI trigger remains: **hidden iframe** navigation to the download URL.

This repo should **not** steer toward a base64-return workaround unless we later re-verify that `GetReport` becomes unavailable.

### ✅ Commission filtering is now working (after backend fix)
In this DEV environment, filtering is applied by `IntExcelExport.Utilities.ReportUtilities.Generate(...)` reading a `FiltersConfig` string (and optionally an `Esq` object) on its request object.

We verified the request contract by calling:
- `GET /0/rest/UsrExcelReportService/GetMethods`

Which showed:
- `Generate(IntExcelReportServiceRequest) -> String`
- RequestProps include: `ReportId:Guid`, `FiltersConfig:String`, `Esq:EntitySchemaQuery`

Implication: modifying/stitching ESQ JSON (`EsqString` / `IntEsq.filters`) is not the effective mechanism here.

### ✅ IW_Commission filtering is working (after backend fix)
`IW_Commission` has:
- `IntEntitySchemaName` blank (all-zero `IntEntitySchemaNameId`)
- `IntEsq` contains `"filters": null`

Despite that, IW now works because the service:
- derives the ESQ root schema name from `IntEsq.rootSchemaName` when `IntEntitySchemaName` is empty
- sets `FiltersConfig` (and optionally `Esq`) on the request passed to `ReportUtilities.Generate`

Validated in DEV:
- Generate + download works with `reportNameSegment = IW_Commission`.
- YearMonth filtering works using a year-month that exists in the output (example observed in data: `2025-11`).

---

## 1. Confirmed working flow

```
Frontend (UsrPage_ebkv9e8)
  └─ POST /0/rest/UsrExcelReportService/Generate
       └─ returns { success: true, key: "ExportFilterKey_..." }
  └─ GET  /0/rest/UsrExcelReportService/GetReport/{key}/{reportNameSegment}
       └─ returns workbook bytes (ZIP header: PK; `.xlsm` when macros exist)
```

The canonical frontend implementation for this flow is in `client-module/UsrPage_ebkv9e8_Updated.js`.

---

## 2. DEV filter mappings (load-bearing)

Commission (`BGCommissionReportDataView`):
- YearMonth: `BGYearMonth`
- SalesGroup: `BGSalesRep.BGSalesGroupLookup`

IW (`IWPayments`):
- YearMonth: `IWBGYearMonth`
- SalesGroup: `IWPaymentsInvoice.BGSalesGroup`

Note: the current frontend uses a parameter named `SalesRepId` to carry a **SalesGroupId** (legacy naming).

---

## 3. `GetReport` `{reportNameSegment}` behavior

The `{reportNameSegment}` portion is not arbitrary. For Commission, the working value is `Commission` (not `Rpt Commission`).

This appears to align with `UsrReportesPampa.UsrCode`. For IW, the confirmed working value is `IW_Commission`.

---

## 4. Testing

- End-to-end generate+download (+ optional Excel inspection):
  - `python3 scripts/testing/test_report_service.py`

- Commission dynamic filter sweep (DEV / v8 flow):
  - `python3 scripts/testing/test_commission_dynamic_filters.py --env dev --count 3 --strategy commission-backed --commission-row-limit 20000 --max-months 200`
- Commission execution-id sweep (PROD baseline / Classic-era flow):
  - `python3 scripts/testing/test_commission_execution_filters.py --env prod --count 3`

Notes:
- The dynamic sweep only validates combinations where the dataset actually contains rows.
- **Validation is strict by default:** if the Excel `Year‑Month` column is empty/missing, the run will not count that combo as passing (deriving Year‑Month from dates can be wrong for commission-period semantics).
  - Diagnostic-only: add `--allow-derived-yearmonth`.
- Historical note: on 2026-01-09 in DEV, the commission-backed sweep found **3** passing combinations (see `docs/TEST_LOG.md`).
- Under current strict validation, you may see **INCONCLUSIVE** attempts if the Excel `Year‑Month` column is empty/missing.
- If you cannot reach 3 strict-pass combos, the most likely causes are:
  - insufficient `BGYearMonth` population in `BGCommissionReportDataView`,
  - DEV data is not representative of PROD, or
  - the export template does not populate the `Year‑Month` column reliably.

Useful env vars:
- `CREATIO_REPORT_CODE` (`Commission` or `IW_Commission`)
- `CREATIO_YEAR_MONTH_NAME` (set to `__NONE__` to skip)
- `CREATIO_SALES_GROUP_ID`

---

## Appendix: IDs

Reports:
- `IntExcelReport.Id` (Commission): `4ba4f203-7088-41dc-b86d-130c590b3594`
- `IntExcelReport.Id` (IW_Commission): `07c77859-b7e5-43f3-97c6-14113f6a1f6f`

Service:
- `UsrExcelReportService` schema uid: `ed794ab8-8a59-4c7e-983c-cc039449d178`
