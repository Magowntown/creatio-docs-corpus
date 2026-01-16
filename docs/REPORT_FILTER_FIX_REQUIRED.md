# Report Filter Issue - Root Cause and Fix Required

## ✅ Status: FIXED (as of 2026-01-09)

| Issue | Status | Verification |
|-------|--------|--------------|
| FLT-001 (Commission filters) | ✅ FIXED | API test shows filtered row count |
| FLT-002 (IW_Commission filters) | ✅ FIXED | YearMonth reduces data correctly |

## Executive Summary

Report generation and download work in DEV, but filters originally were not being applied. **Commission and IW_Commission filtering are now fixed and validated in DEV** (via server-side `FiltersConfig`/`Esq`).

## Open follow-up: Sales Group cascade parity + v8-first hardening
Commission filter mechanism is fixed and **Gate D (3 combos) is passed**, but there is an active UX/data-parity follow-up:
- Sales Group cascade can appear “wrong” in DEV when `BGCommissionSalesGroupByYearMonth` has 0 rows for a month that PROD/business expects.

v8-first direction:
- Keep the DEV mechanism (`FiltersConfig`/`Esq`) as the durable solution.
- Treat PROD behavior as baseline discovery (execution-id filtering) during pre-upgrade.

Optional improvements (keep focus on pre-filtered exports):
- **Cascade Sales Group options by Year‑Month** (Commission + IW_Commission):
  - Commission: use `BGCommissionSalesGroupByYearMonth`.
  - IW_Commission: uses the **Payments object** (`IWPayments` / `IWPaymentsInvoice`).
- **Preflight has-data / rowcount check** before generating the workbook (warn early; allow export anyway).

Important finding (DEV, 2026-01-09): deriving test combos from `Order.Date` + `Order.BGSalesGroup` often produced **header-only** Commission exports (0 data rows). This suggests Commission rows are not a simple projection of Orders by those fields.

Important semantic note (PROD baseline, 2026-01-10): Commission “Year‑Month” behaves like a *commission period* (sale rows largely align to transaction month; credit memos can be allocated to a later period). Therefore, order-derived combos are not a reliable way to validate Year‑Month filtering.

Recommended validation scripts:
```bash
# DEV/v8: (already passed Gate D) run again only if data/templates change.
python3 scripts/testing/test_commission_dynamic_filters.py --env dev --count 3

# PROD baseline (pre-upgrade): validates the execution-id flow.
python3 scripts/testing/test_commission_execution_filters.py --env prod --count 3

# DEV/v8 regression: IW_Commission
CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py
```

Validation semantics:
- PASS requires >0 rows AND a single `Year‑Month` and `Sales Group` value in the Excel `Data` sheet matching the selected filters.
- If the Excel `Year‑Month` column is empty/missing, treat as **INCONCLUSIVE** under strict validation.
  - Diagnostic-only: add `--allow-derived-yearmonth` to allow deriving Year‑Month from dates.

Use the output as evidence in `docs/TEST_LOG.md` (include IDs + file sizes + whether the Excel “Data” sheet contains only the selected Year‑Month and Sales Group).

## ★ Verification Commands

> "Give Claude a way to verify its work. It will 2-3x the quality." - Boris Cherny

```bash
# Commission with YearMonth filter
CREATIO_YEAR_MONTH_NAME=2025-08 python3 scripts/testing/test_report_service.py

# IW_Commission with YearMonth filter
CREATIO_REPORT_CODE=IW_Commission CREATIO_YEAR_MONTH_NAME=2025-11 python3 scripts/testing/test_report_service.py
```

## AI orchestration usage
- This document is primarily for **Claude Code** when working FLT-001 / FLT-002.
- Verification should be done with `python3 scripts/testing/test_report_service.py` and logged in `docs/TEST_LOG.md`.
- Follow the orchestration map (roles + gates + handoffs): `CLAUDE.md` Section 1.5

## Version & migration context
- **PROD was originally Creatio v7 (Classic UI)**.
- **DEV is Creatio v8 (Freedom UI)** and is the target state.
- During the v7→v8 migration, prefer mechanisms that are stable in v8 and less dependent on marketplace client internals.

For filtering specifically:
- **v8-first (target architecture):** in this DEV/v8 environment, `ReportUtilities.Generate(...)` reads `FiltersConfig` (and optionally `Esq`).
- Do not rely on ESQ JSON string stitching as the primary filtering mechanism in DEV.
- **PROD baseline (pre-upgrade):** Commission export filtering is execution-context driven: the ESQ sent to `IntExcelReportService/GetExportFiltersKey` filters by `BGExecutionId` (a `BGReportExecution` row). Directly filtering `BGCommissionReportDataView` by Year‑Month / Sales Group is not equivalent to the real PROD flow.

## Confirmed root causes (DEV)

### 1) Wrong filter mechanism (load-bearing)
In this DEV environment, `IntExcelExport.Utilities.ReportUtilities.Generate(...)` reads a `FiltersConfig` string (and optionally an `Esq` object) on its request object.

This was confirmed via:
- `GET /0/rest/UsrExcelReportService/GetMethods`
  - RequestProps include `ReportId`, `FiltersConfig`, `Esq`

Implication: modifying/stitching ESQ JSON (`EsqString` / `IntEsq.filters`) is not the effective mechanism here.

### 2) Commission: old column paths don’t exist
For Commission (`BGCommissionReportDataView`), the schema does **not** expose `BGYearMonthId` / `BGSalesRepId`. Correct paths:
- `BGYearMonth`
- `BGSalesRep.BGSalesGroupLookup` (SalesGroup)

### 3) IW_Commission: missing schema name + `filters: null` in IntEsq
IW_Commission has `IntEntitySchemaName` blank, and its stored `IntEsq` includes `"filters": null`.

Using `FiltersConfig` avoids depending on `filters.items`, but we still need `rootSchemaName` (from `IntEsq`) to pick the IW column mapping.

## What should be fixed (implemented in `UsrExcelReportService`)

Update the service to:
1. Determine the report root schema name:
   - Use `IntEntitySchemaName` when present
   - Else parse `rootSchemaName` from `IntEsq`
2. Build a `FiltersConfig` filter group JSON with comparison filters for:
   - YearMonthId (if provided)
   - SalesGroupId (passed from UI as `SalesRepId`)
3. Set `FiltersConfig` on the internal request object passed to `ReportUtilities.Generate`.
4. (Optional but recommended) set `Esq` via `ReportUtilities.GetReportEsq(reportId)`.

Reference implementation / snapshot:
- `source-code/UsrExcelReportService_Updated.cs`

## DEV mappings

Commission:
- YearMonth: `BGYearMonth`
- SalesGroup: `BGSalesRep.BGSalesGroupLookup`

IW:
- YearMonth: `IWBGYearMonth`
- SalesGroup: `IWPaymentsInvoice.BGSalesGroup`

## Verification steps

Use:
- `python3 scripts/testing/test_report_service.py`

Examples:
- Unfiltered Commission:
  - `CREATIO_YEAR_MONTH_NAME=__NONE__ python3 scripts/testing/test_report_service.py`
- Filtered Commission:
  - `CREATIO_YEAR_MONTH_NAME=2025-08 python3 scripts/testing/test_report_service.py`
- IW:
  - `CREATIO_REPORT_CODE=IW_Commission CREATIO_YEAR_MONTH_NAME=2025-11 python3 scripts/testing/test_report_service.py`

---
*Updated: 2026-01-09*  
*Environment: dev-pampabay.creatio.com*
