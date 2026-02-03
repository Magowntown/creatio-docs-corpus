# IWQBIntegration Package - Reports Consolidation Plan

**Date:** 2026-01-21
**Status:** Planning
**Target:** Consolidate all report fixes into IWQBIntegration package for PROD deployment

---

## Executive Summary

This document outlines the strategy to consolidate all Reports section fixes into the IWQBIntegration package, ensuring Commission, IW_Commission, and all other reports work correctly without interrupting Pampa Bay's business processes.

---

## Current State Analysis

### Report Status Overview

| Report | Status | Data Source | Package Location |
|--------|--------|-------------|------------------|
| **Commission** | ✅ Working (PROD) | BGCommissionReportDataView | PampaBayQuickBooks (view), IWQBIntegration (handler) |
| **IW_Commission** | ✅ Working (DEV) | IWCommissionReportDataView | IWQBIntegration |
| Looker Studio reports | ⚠️ CSP Blocked | Looker URLs | N/A - opens new tab |
| Other Excel reports | ⚠️ Template issues | Various IntExcelReport | IntExcelExport library |

### Component Inventory

#### 1. Backend Service (UsrExcelReportService)

| Environment | Location | Status |
|-------------|----------|--------|
| **DEV** | PampaBayVer2 package | ✅ Updated |
| **PROD** | PampaBayVer2 package | ✅ Deployed |

**File:** `source-code/UsrExcelReportService_Updated.cs`

**Key Features:**
- Handles Commission filtering via BGExecutionId
- Handles IW_Commission filtering via direct ESQ
- ESQ sanitization for @P placeholder reports (RPT-002)
- GetReport endpoint for Excel downloads

#### 2. Frontend Handler (UsrPage_ebkv9e8)

| Environment | UID | Package | Status |
|-------------|-----|---------|--------|
| **DEV** | 561d9dd4-8bf2-4f63-a781-54ac48a74972 | BGApp_eykaguu | ✅ Hybrid handler |
| **PROD** | 561d9dd4-8bf2-4f63-a781-54ac48a74972 | BGApp_eykaguu | ✅ Hybrid handler |

**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js`

**Key Features:**
- Detects Looker Studio URLs → opens in new tab
- No URL → calls UsrExcelReportService for Excel
- Shows Year-Month/Sales Group filters for Commission reports
- Resolves UsrReportesPampa → IntExcelReport mapping

#### 3. SQL Views

| View | Entity Schema | Package | Status |
|------|---------------|---------|--------|
| BGCommissionReportDataView | ✅ Registered | PampaBayQuickBooks | ✅ Working |
| IWCommissionReportDataView | ✅ Registered | IWQBIntegration | ✅ Working (DEV) |

**SQL Scripts:**
- `scripts/sql/BGCommissionReportDataView_fix_PROD.sql` - Commission view fix
- Package element: `IWSQLViewIWCommissionReportDataView` - IW_Commission view

#### 4. IntExcelReport Configurations

| Report | IntExcelReport ID | Entity Schema | Status |
|--------|-------------------|---------------|--------|
| Rpt Commission | (lookup) | BGCommissionReportDataView | ✅ Configured |
| IW_Commission | 07c77859-b7e5-43f3-97c6-14113f6a1f6f | IWCommissionReportDataView | ✅ Configured |
| Rpt Sales By Line | 0b40d51d-4935-4918-97f2-45352aed341f | Various | ⚠️ Needs ESQ fix |
| Items by Customer | (lookup) | Various | ⚠️ Template issue |

---

## Consolidation Strategy

### Priority Order

1. **Commission** - Primary report, already working in PROD
2. **IW_Commission** - Secondary report, working in DEV, needs PROD deployment
3. **Other Excel reports** - Various issues, fix as needed

### Package Responsibility

| Package | Responsibility |
|---------|----------------|
| **IWQBIntegration** | All report-related schemas, views, and IW-specific logic |
| **PampaBayVer2** | Backend service (UsrExcelReportService) |
| **BGApp_eykaguu** | Frontend handler (UsrPage_ebkv9e8) |
| **IntExcelExport** | Library (unchanged - do not modify) |

---

## Components to Deploy to PROD

### Phase 1: IW_Commission (HIGH PRIORITY)

| Component | Action | Package | Risk |
|-----------|--------|---------|------|
| IWCommissionReportDataView (SQL) | Deploy SQL script | IWQBIntegration | Low |
| IWCommissionReportDataView (Entity) | Deploy entity schema | IWQBIntegration | Low |
| IntExcelReport config | Update via SQL | Database | Low |
| Excel template | Already in IntExcelExport | N/A | None |

**SQL Script for PROD:**
```sql
-- 1. Create/update SQL view
-- Copy from: IWSQLViewIWCommissionReportDataView package element

-- 2. Update IntExcelReport configuration
UPDATE "IntExcelReport"
SET
    "IntEntitySchemaNameId" = (
        SELECT "Id" FROM "SysSchema"
        WHERE "Name" = 'IWCommissionReportDataView'
        LIMIT 1
    ),
    "IntSheetName" = 'Data',
    "IntEsq" = '{"rootSchemaName": "IWCommissionReportDataView", "operationType": 0, "columns": {"items": {"IWSalesRep": {"orderPosition": 0}, "IWSalesGroup": {"orderPosition": 1}, "IWAccount": {"orderPosition": 2}, "IWPONumber": {"orderPosition": 3}, "IWInvoiceDate": {"orderPosition": 4}, "IWAmount": {"orderPosition": 5}, "IWCommissionAmount": {"orderPosition": 6}, "IWCommissionRatePercentage": {"orderPosition": 7}, "IWTransactionDate": {"orderPosition": 8}, "IWTransactionType": {"orderPosition": 9}, "IWIsNote": {"orderPosition": 10}, "IWDescription": {"orderPosition": 11}, "IWYearMonth": {"orderPosition": 12}}}, "filters": {"items": {}}}'
WHERE "IntName" = 'IW_Commission';
```

### Phase 2: Backend Service (Already Deployed)

The UsrExcelReportService in PampaBayVer2 already handles both Commission and IW_Commission. No changes needed for PROD.

### Phase 3: Frontend Handler (Already Deployed)

The Hybrid handler in BGApp_eykaguu already handles all reports. No changes needed for PROD.

---

## Deployment Procedure

### Pre-Deployment Checklist

- [ ] Verify IWQBIntegration package exists in PROD
- [ ] Verify IWInterWeavePaymentApp package exists in PROD
- [ ] Backup current PROD database
- [ ] Identify active users (schedule deployment during low-usage)

### Step 1: Deploy SQL View to PROD

```sql
-- Run in PROD pgAdmin
DROP VIEW IF EXISTS "IWCommissionReportDataView";

CREATE OR REPLACE VIEW "IWCommissionReportDataView" AS
SELECT
    iw."Id",
    iw."CreatedById",
    iw."CreatedOn",
    iw."ModifiedById",
    iw."ModifiedOn",
    iw."ProcessListeners",

    iw."IWAmount",
    iw."IWCommissionAmount",
    CASE
        WHEN iw."IWAmount" > 0 AND iw."IWAmount" != 0
        THEN ROUND((iw."IWCommissionAmount" / iw."IWAmount") * 100, 2)
        ELSE COALESCE(emp."BGDefaultCommission", 0)
    END AS "IWCommissionRatePercentage",

    iw."IWDescription",
    iw."IWQBInvoiceNumber",
    iw."IWMemo",

    ord."Id" AS "IWOrderId",
    COALESCE(ord."BGPONumber", ord."BGCustomerPO", ord."BGPurchaseOrder") AS "IWPONumber",
    ord."Number" AS "IWOrderNumber",
    ord."BGInvoiceDate" AS "IWInvoiceDate",

    iw."IWBGSalesRepId" AS "IWSalesRepId",
    iw."IWPaymentDue" AS "IWTransactionDate",
    iw."IWBGTransactionTypeId" AS "IWTransactionTypeId",
    CASE WHEN iw."IWBGIsNote" = true THEN 1 ELSE 0 END AS "IWIsNote",

    iw."IWSalesGroupId",
    iw."IWAccountId",

    re."Id" AS "IWExecutionId",
    re."BGYearMonthId" AS "IWYearMonthId"

FROM "IWPayments" iw
LEFT JOIN "Order" ord ON iw."IWPaymentsInvoiceId" = ord."Id"
LEFT JOIN "Employee" emp ON iw."IWBGSalesRepId" = emp."Id"
JOIN "BGReportExecution" re ON re."BGReportName" = 'IW_Commission'
LEFT JOIN "BGYearMonth" ym ON ym."Id" = re."BGYearMonthId"

WHERE
    (
        re."BGSalesGroupId" IS NULL
        OR re."BGSalesGroupId" = emp."BGSalesGroupLookupId"
    )
    AND (
        ym."Id" IS NULL
        OR (
            EXTRACT('month' FROM iw."IWPaymentDue") = EXTRACT('month' FROM (ym."BGDateTime" + '1 day'::interval))
            AND EXTRACT('year' FROM iw."IWPaymentDue") = EXTRACT('year' FROM (ym."BGDateTime" + '1 day'::interval))
        )
    );
```

### Step 2: Verify Entity Schema in PROD

Check if `IWCommissionReportDataView` entity schema exists in PROD IWQBIntegration package. If not, create it with these columns:

| Column | Type | Notes |
|--------|------|-------|
| IWInvoiceDate | Date | |
| IWAccount | Lookup → Account | |
| IWSalesGroup | Lookup → BGSalesGroup | |
| IWMemo | Text | |
| IWQBInvoiceNumber | Text | |
| IWDescription | Text | |
| IWCommissionAmount | Decimal | |
| IWAmount | Decimal | |
| IWYearMonth | Lookup → BGYearMonth | |
| IWExecution | Lookup → BGReportExecution | |
| IWIsNote | Integer | |
| IWTransactionType | Lookup | |
| IWTransactionDate | Date | |
| IWSalesRep | Lookup → Employee | |
| IWOrder | Lookup → Order | |
| IWPONumber | Text | |
| IWCommissionRatePercentage | Decimal | |
| IWOrderNumber | Text | |

### Step 3: Update IntExcelReport Configuration

```sql
UPDATE "IntExcelReport"
SET
    "IntEntitySchemaNameId" = (
        SELECT "Id" FROM "SysSchema"
        WHERE "Name" = 'IWCommissionReportDataView'
        LIMIT 1
    ),
    "IntSheetName" = 'Data'
WHERE "IntName" = 'IW_Commission';
```

### Step 4: Compile IWQBIntegration Package

1. Open PROD Configuration
2. Navigate to IWQBIntegration package
3. Click "Compile"
4. Wait for completion

### Step 5: Test Reports

| Test | Expected Result |
|------|-----------------|
| Commission (no filters) | Downloads Excel with data |
| Commission (Year-Month filter) | Downloads filtered data |
| Commission (Sales Group filter) | Downloads filtered data |
| IW_Commission (no filters) | Downloads Excel with IWPayments data |
| IW_Commission (Sales Group filter) | Downloads filtered data |

---

## Risk Mitigation

### Non-Interruption Guarantees

| Concern | Mitigation |
|---------|------------|
| Existing Commission report | No changes to BGCommissionReportDataView |
| Business process flows | No changes to QB sync processes |
| Order processing | No changes to OrderPageV2 or Order schema |
| IWPayments data | Only adding a read-only view |

### Rollback Procedure

If issues occur:

1. **SQL View issues:**
   ```sql
   DROP VIEW IF EXISTS "IWCommissionReportDataView";
   ```

2. **Entity Schema issues:**
   - Delete IWCommissionReportDataView entity from IWQBIntegration
   - Recompile package

3. **IntExcelReport issues:**
   ```sql
   UPDATE "IntExcelReport"
   SET "IntEntitySchemaNameId" = NULL
   WHERE "IntName" = 'IW_Commission';
   ```

---

## Known Limitations

### Reports Still Blocked

| Report | Issue | Status |
|--------|-------|--------|
| Looker Studio reports | CSP blocks iframes | ⚠️ Opens in new tab (requires Google permissions) |
| Items by Customer | Template configuration | 🔴 RPT-004 - needs template fix |
| Some other Excel reports | Various IntExcelReport issues | 🔴 Need individual investigation |

### Future Work

| Task | Priority | Notes |
|------|----------|-------|
| CSP-001: Whitelist Looker Studio | HIGH | Requires BGlobal server config |
| LOOKER-001: Google permissions | HIGH | Requires BGlobal action |
| RPT-004: Template fixes | MEDIUM | Individual report templates |
| FUT-001: Server-side macros | LOW | Pre-calculated .xlsx |

---

## Files Reference

### Source Code
| File | Purpose |
|------|---------|
| `source-code/UsrExcelReportService_Updated.cs` | Backend service (deployed) |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js` | Frontend handler (deployed) |

### SQL Scripts
| File | Purpose |
|------|---------|
| `scripts/sql/BGCommissionReportDataView_fix_PROD.sql` | Commission view fix |
| Package: `IWSQLViewIWCommissionReportDataView` | IW_Commission view |

### Documentation
| File | Purpose |
|------|---------|
| `docs/PROD_DEPLOYMENT_PLAN.md` | Original PROD deployment plan |
| `docs/IW_COMMISSION_STRATEGY.md` | IW_Commission implementation details |
| `docs/PACKAGE_COMPARISON.md` | Package relationship analysis |

---

## Sign-Off Checklist

| Step | Completed | Date | Verified By |
|------|-----------|------|-------------|
| Plan reviewed | ☐ | | |
| DEV testing complete | ✅ | 2026-01-21 | IW_Commission working |
| PROD backup taken | ☐ | | |
| SQL view deployed | ☐ | | |
| Entity schema verified | ☐ | | |
| IntExcelReport updated | ☐ | | |
| Package compiled | ☐ | | |
| Commission regression test | ☐ | | |
| IW_Commission test | ☐ | | |
| User acceptance | ☐ | | |

---

*Plan created: 2026-01-21*
