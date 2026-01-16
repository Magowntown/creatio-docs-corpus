# Creatio Report Fix Project

> **AI Agents:** See `CLAUDE.md` for current status and DEV-specific discoveries. Update it after every session.
>
> **Claude Code Users:** See `CLAUDE.md` Section 0 for Boris Cherny's best practices (parallel sessions, Plan mode, verification).

This repo documents and tests fixes for the DEV Creatio Excel report flow used by the Reports page (page schema `UsrPage_ebkv9e8`).

## ✅ Current Status (as of 2026-01-12)

|| Gate | Status | Description |
||------|--------|-------------|
|| Gate A | ✅ PASSED | API baseline (Commission + IW_Commission) |
|| Gate B | ✅ PASSED | Runtime verification (hidden iframe handler deployed) |
| Gate C | ✅ PASSED | DL-001 browser download working |
|| Gate D | ✅ PASSED | Dynamic filter sweep (Commission; 3 combos) + DEV↔PROD compare (PROD PASS; note Year‑Month is a commission period; INCONCLUSIVE if Excel Year‑Month column is blank under strict validation) |
|| Gate E | 🔄 Pending | Regression testing (other reports) |
|| Gate F | 🔄 Pending | Hardening (edge cases, error handling) |
|| Gate G | 🔄 Pending | PROD upgrade checklist |

Additional active items:
- **FLT-004:** Commission export can be **header-only** for older Year‑Months (example: `2025-01` + `RDGZ & Consulting LLC`). Root cause is `Year-Month.Name` not populated for most rows in DEV, so lookup-based filtering excludes everything.

Recently fixed:
- **DL-003:** macro-enabled workbooks are now served as `.xlsm` via `UsrExcelReportService/GetReport`.
- **DL-003B:** Commission Generate no longer throws `FormatException` for the known failing combo (`2025-01` + `RDGZ & Consulting LLC`).

## ★ Verification is Key (Boris Cherny's #1 Tip)

> "Give Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the quality of the final result."

```bash
# API baseline
python3 scripts/testing/test_report_service.py

# IW_Commission
CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py
```

## Version & migration context (critical)
- **PROD was originally designed for Creatio v7 (Classic UI)**.
- **DEV is Creatio v8 (Freedom UI)**.
- PROD is being upgraded to **v8**, and DEV packages/content are expected to be migrated into PROD.

Implication:
- Treat the **DEV v8/Freedom UI flow** as the target architecture.
- Avoid building long-term solutions around Classic UI patterns (e.g., URL-driven exports / `UsrURL` + `window.open(...)`).
- Prefer solutions resilient to **marketplace add-on updates**.

## Assessment summary (catalogue; as of January 10, 2026)
- **PROD verified behavior (Classic-era IntExcel mixin flow):**
  - `POST /0/rest/IntExcelReportService/GetExportFiltersKey` returns an `ExportFilterKey_...`.
  - Download is via `GET /0/rest/IntExcelReportService/GetExportFilteredData/{fileName}/{key}` (returns `.xlsx`).
  - `GET /0/rest/IntExcelReportService/GetReport/...` returns **404** in PROD.
  - **Filtering is execution-context driven:** the ESQ sent to `GetExportFiltersKey` filters by `BGExecutionId` (a `BGReportExecution` row), not by directly filtering `BGCommissionReportDataView` on Year‑Month / Sales Group.
- **DEV behavior (v8/Freedom target flow):**
  - `POST /0/rest/UsrExcelReportService/Generate` returns a key.
  - Preferred download (**after DL-003 deploy/verify**): `GET /0/rest/UsrExcelReportService/GetReport/{key}/{reportNameSegment}` (serves `.xlsm` when macros exist).
  - Legacy download: `GET /0/rest/IntExcelReportService/GetReport/{key}/{reportNameSegment}` (serves `.xlsx` even when macros exist).
  - **Filtering is `FiltersConfig`-driven:** the wrapper service sets `FiltersConfig` (and optionally `Esq`) for `ReportUtilities.Generate(...)`.

## Goals (current)
- Reports page should reliably generate + download an Excel-openable file without browser errors.
  - Note (DL-003): Commission/IW exports are macro-enabled; filename extension should be `.xlsm`.
- Commission: selected YearMonth + SalesGroup lookup values must affect the Excel output.
- IW_Commission: filters must apply correctly in DEV even with blank `IntEntitySchemaName` and stored `IntEsq` containing `"filters": null`.
- Survive **v7→v8 migration** and **marketplace add-on updates** without breaking generation, filtering, or download.
- Keep docs up to date (especially `CLAUDE.md`) with what was verified and what changed.

## Next steps (v8-first; canonical)
1) **Gate E (regression):** re-run IW_Commission end-to-end (API first; then browser if needed).
   - Log results in `docs/TEST_LOG.md`.
2) **Sales Group cascade UX validation (DEV):** validate Year‑Month → Sales Group narrowing using a known-good combo discovered from commission data.
3) **If DEV shows empty cascade for business-expected months:** treat as data parity first; then implement a v8-first fallback cascade (derive valid Sales Groups from `BGCommissionReportDataView` when `BGCommissionSalesGroupByYearMonth` has 0 rows) to avoid “show all groups” and reduce confusion.

## Next solution improvements (stay on task: pre-filtered exports)
These are optional UX/robustness improvements that keep the same backend filtering contract:
- **Cascade Sales Group options by selected Year‑Month** (Commission + IW_Commission):
  - Commission: use commission-backed valid combos via `BGCommissionSalesGroupByYearMonth`.
  - IW_Commission: uses the **Payments object** (`IWPayments` / `IWPaymentsInvoice`) to derive valid Sales Groups for the selected Year‑Month.
  - Note on env parity: `IWPayments` does **not** exist in PROD today (pre-upgrade), so the IW cascade is currently DEV-only unless/until PROD is upgraded to v8 and receives the IW data model.
- **Optional preflight rowcount / has-data check** before generating an export (warn early; do not hard-block).
- **Hardening:** make the `UsrReportesPampa` → `IntExcelReport` mapping more durable (reduce reliance on naming conventions where possible).

## Definition of Done (DoD)
- ✅ From the Reports page (`UsrPage_ebkv9e8`), clicking **Report** produces a real Excel download in a standard browser.
  - Commission/IW: expected `.xlsm` (macro-enabled) to avoid DL-003.
- ✅ Filters (YearMonth + SalesGroup) affect the generated Excel output for Commission and IW_Commission.
- ✅ The solution is not impeded by future package updates to **IntExcelExport**:
  - Do not rely on IntExcelExport **client-side** mixins/handlers.
  - Keep the v8 UI flow stable: **Generate → GetReport**, with **hidden iframe** as the canonical download trigger.
  - Treat `scripts/testing/test_report_service.py` + DL-001 browser test as regression gates after any IntExcelExport update.
- ✅ The v8 approach remains the target during PROD’s v7→v8 migration (do not regress to Classic-era URL export patterns).
- ✅ Credentials remain accessible to AIs via `.env` (gitignored) without being copied into documentation.

## AI orchestration (how to reach DoD efficiently)
Canonical workflow lives in `CLAUDE.md`:
- TDD cycle: `CLAUDE.md` Section 1.2
- Orchestration map (roles + gates + handoffs): `CLAUDE.md` Section 1.5
- Test result source of truth: `docs/TEST_LOG.md`

Key rule:
- Do not start “hardening” or migration work until **DL-001** is logged as **PASS** in `docs/TEST_LOG.md`.

## Non-goals (for now)
- Big refactors / re-writing the whole reporting implementation.
- Adding new database/schema relationships unless we decide it’s required.

## Verified DEV behavior (as of January 12, 2026)

### ✅ Generate + download works (no base64 required)
1. `POST /0/rest/UsrExcelReportService/Generate` returns `success: true` and a `key` like `ExportFilterKey_...`.
2. Download options:
   - **Preferred (after DL-003 deploy/verify):** `GET /0/rest/UsrExcelReportService/GetReport/{key}/{reportNameSegment}` should return a valid workbook payload (ZIP header `PK`) and serve:
     - `.xlsm` when macros exist (`xl/vbaProject.bin`)
     - `.xlsx` otherwise
   - **Legacy (already verified):** `GET /0/rest/IntExcelReportService/GetReport/{key}/{reportNameSegment}` returns ZIP bytes but may serve filename `.xlsx` even when macros exist.

Notes:
- Legacy `.ashx` handlers (e.g. `DownloadExportFile.ashx`) may still error in this environment, but **the current working UI flow does not rely on them**.
- `{reportNameSegment}` is not the `IntExcelReport.IntName`. For Commission it is `Commission` (likely `UsrReportesPampa.UsrCode`).
- **Canonical download trigger:** hidden iframe navigation to `GET /0/rest/UsrExcelReportService/GetReport/{key}/{reportNameSegment}`.
- If the UI shows **“File wasn't available on site”**, first confirm the deployed handler is using the **hidden iframe** (not object-URL downloads) and check the browser console for `TypeError: ... (reading 'UsrURL')` in `UsrPage_ebkv9e8.js`.
  - The `:line` number is in the **compiled output**, so locate the handler in the Schema Designer JSON (search for `GenerateExcelReportRequest` / `UsrURL`) and deploy the canonical handler (`client-module/UsrPage_ebkv9e8_Updated.js`) or add null-guards + try/catch.
- Historical note: object-URL downloads can fail in Chrome if `URL.revokeObjectURL(...)` happens too early; do **not** use object URLs as the mainline approach.

### ✅ Commission filters are working end-to-end
In this DEV env, filtering is applied by `IntExcelExport.Utilities.ReportUtilities.Generate(...)` reading a `FiltersConfig` string (and optionally an `Esq` object) on its request object.

Commission root schema: `BGCommissionReportDataView`
- YearMonth filter column: `BGYearMonth`
- SalesGroup filter column: `BGSalesRep.BGSalesGroupLookup`

### ✅ IW_Commission generate+download + YearMonth filtering validated
- `IntExcelReport.IntEntitySchemaName` is blank, so the service derives `rootSchemaName` from `IntEsq` to choose IW mappings.
- IW root schema: `IWPayments`
  - YearMonth: `IWBGYearMonth`
  - SalesGroup: `IWPaymentsInvoice.BGSalesGroup`
- Confirmed `{reportNameSegment}` for downloads: `IW_Commission`.
- A year-month with data observed in IW output: `2025-11` (use that for validation).

## Environment setup for scripts

Scripts read credentials from environment variables.

Recommended: copy `.env.example` to `.env` and fill values locally. `.env` is gitignored.

Secret handling:
- Keep credentials in `.env` so any AI working inside this repo workspace can access them when needed.
- Do **not** copy credentials into `README.md`, `docs/`, test logs, or chat transcripts.

Required variables:
- `CREATIO_URL` (default: `https://dev-pampabay.creatio.com`)
- `CREATIO_USERNAME`
- `CREATIO_PASSWORD`

Optional testing inputs (used by `scripts/testing/test_report_service.py`):
- `CREATIO_REPORT_CODE` (default: `Commission`)
- `CREATIO_REPORT_ID` (override; optional)
- `CREATIO_REPORT_INT_NAME` (override; optional)
- `CREATIO_REPORT_NAME_SEGMENT` (override; optional)
- `CREATIO_YEAR_MONTH_NAME` (set to `__NONE__` to skip YearMonth filtering)
- `CREATIO_SALES_GROUP_ID` (optional; SalesGroupId is passed in the API field `SalesRepId` for legacy reasons)

Example (shell):
```bash
export CREATIO_URL="https://dev-pampabay.creatio.com"
export CREATIO_USERNAME="..."
export CREATIO_PASSWORD="..."
```

## Quick tests

End-to-end (Generate + GetReport download + optional Excel row count):
- Commission unfiltered:
  - `CREATIO_YEAR_MONTH_NAME=__NONE__ python3 scripts/testing/test_report_service.py`
- Commission filtered (known data period):
  - `CREATIO_YEAR_MONTH_NAME=2025-08 python3 scripts/testing/test_report_service.py`
- Commission SalesGroup mismatch proof:
  - `CREATIO_YEAR_MONTH_NAME=2025-08 CREATIO_SALES_GROUP_ID=19152054-0a85-46bb-bbf0-b78bfaf203c1 python3 scripts/testing/test_report_service.py`
- IW_Commission:
  - `CREATIO_REPORT_CODE=IW_Commission CREATIO_YEAR_MONTH_NAME=2025-11 python3 scripts/testing/test_report_service.py`

## Directory Structure

```
creatio-report-fix/
├── README.md
├── CLAUDE.md
├── source-code/                 # C# service code snapshots/variants
├── client-module/               # Freedom UI handler code
├── scripts/                     # deployment/testing/investigation scripts
├── docs/                        # analysis + guidance
└── test-artifacts/              # downloaded reports, screenshots, etc.
```

## Important IDs

Reports:
- Commission report (`IntExcelReport.Id`): `4ba4f203-7088-41dc-b86d-130c590b3594`
- IW_Commission report (`IntExcelReport.Id`): `07c77859-b7e5-43f3-97c6-14113f6a1f6f`

Creatio schemas:
- `UsrPage_ebkv9e8` schema uid: `1d5dfc4d-732d-48d7-af21-9e3d70794734`
- `UsrExcelReportService` schema uid: `ed794ab8-8a59-4c7e-983c-cc039449d178`

## Where the fix should land

- Frontend: `client-module/UsrPage_ebkv9e8_Updated.js` already uses the verified working download flow.
- Backend: `UsrExcelReportService` should:
  - set `FiltersConfig` using the correct column paths
  - (optionally) set `Esq` via `ReportUtilities.GetReportEsq(reportId)`
  - handle IW schema name derivation when `IntEntitySchemaName` is blank
