# IW_Commission Report - Implementation Strategy

**Date**: 2026-01-13 (Updated: 2026-01-14)
**Status**: Implementation
**Packages**: IWQBIntegration, PampaBayVer2

---

## Executive Summary

IW_Commission report will use QuickBooks payment data from `IWPayments` entity, with a simple view for lookup resolution and direct filtering (no BGExecutionId dependency).

---

## Creatio View-Based Object Requirements

> **Source**: [CustomerFX - Using Database Views in Creatio](https://customerfx.com/article/using-database-views-in-creatio/) and [Creatio Community](https://community.creatio.com/questions/creating-view-type-object-creatio)

### Critical Requirements for View-Based Objects

1. **Object name must match database view name exactly**

2. **Check "Represents Structure of Database View"** - This prevents Creatio from creating a table

3. **Parent object should be BaseEntity** - Provides standard Id and audit columns

4. **View MUST include BaseEntity columns:**
   - `Id` (GUID, unique values required)
   - `CreatedOn` (DateTime)
   - `CreatedById` (GUID)
   - `ModifiedOn` (DateTime)
   - `ModifiedById` (GUID)
   - `ProcessListeners` (Integer, typically 0)

5. **Lookup column naming convention:**
   - Database view column: `UsrAccountId` (includes "Id" suffix)
   - Creatio object column: `UsrAccount` (NO "Id" suffix, type = Lookup)

6. **Naming convention (recommended):** Use "Vw" prefix, e.g., `UsrVwAccountInfo`

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Data Flow                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  QuickBooks ──(InterWeave)──► IWPayments                        │
│                                    │                             │
│                                    ▼                             │
│                        IWCommissionReportDataView                │
│                                    │                             │
│                                    ▼                             │
│                          IW_Commission Report                    │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Creatio Native ──────────► BGCommissionReportDataView          │
│                                    │                             │
│                                    ▼                             │
│                           Commission Report                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Package Organization

| Component | Package | Notes |
|-----------|---------|-------|
| `IWCommissionReportDataView` | **IWQBIntegration** | New view |
| `IWPayments` (existing) | IWQBIntegration | Data source |
| `UsrExcelReportService` | **PampaBayVer2** | Move here |

---

## IWPayments Schema Reference

| Column | Type | Purpose |
|--------|------|---------|
| `Id` | GUID | Primary key |
| `IWPaymentDue` | DateTime | **Payment date (filter key)** |
| `IWAmount` | Decimal | Payment amount |
| `IWCommissionAmount` | Decimal | Commission amount |
| `IWSalesGroupId` | GUID | **Sales Group (filter key)** |
| `IWAccountId` | GUID | Customer account |
| `IWPaymentsInvoiceId` | GUID | Link to Creatio Order |
| `IWQBInvoiceNumber` | Text | QuickBooks Invoice Number |
| `IWDescription` | Text | Description |
| `IWMemo` | Text | Memo/notes |
| `IWOwnerId` | GUID | Record owner |

---

## Implementation Steps

### Step 1: Create PostgreSQL View (CORRECTED)

**File:** `scripts/sql/IWCommissionReportDataView.sql`

> **IMPORTANT**: View MUST include all BaseEntity columns for Creatio object inheritance to work.

```sql
-- IWCommissionReportDataView
-- Package: IWQBIntegration
-- Purpose: Resolves lookups for IW_Commission report
-- Filter: Direct on IWPaymentDue (date) + IWSalesGroupId (GUID)
-- REQUIREMENT: Must include BaseEntity columns (Id, CreatedOn, CreatedById, ModifiedOn, ModifiedById, ProcessListeners)

CREATE OR REPLACE VIEW public."IWCommissionReportDataView" AS
SELECT
    -- BaseEntity required columns
    iw."Id",
    iw."CreatedOn",
    iw."CreatedById",
    iw."ModifiedOn",
    iw."ModifiedById",
    0 AS "ProcessListeners",

    -- IW-specific columns
    iw."IWPaymentDue" AS "IWTransactionDate",
    iw."IWAmount",
    iw."IWCommissionAmount",
    iw."IWQBInvoiceNumber",
    iw."IWDescription",
    iw."IWMemo",

    -- Lookup columns (keep "Id" suffix in view, Creatio object removes it)
    iw."IWSalesGroupId",
    sg."BGName" AS "IWSalesGroupName",
    iw."IWAccountId",
    acct."Name" AS "IWAccountName",
    iw."IWPaymentsInvoiceId",
    ord."Number" AS "IWOrderNumber",
    iw."IWOwnerId"
FROM "IWPayments" iw
LEFT JOIN "BGSalesGroup" sg ON iw."IWSalesGroupId" = sg."Id"
LEFT JOIN "Account" acct ON iw."IWAccountId" = acct."Id"
LEFT JOIN "Order" ord ON iw."IWPaymentsInvoiceId" = ord."Id";
```

### Step 2: Register Entity Schema in Creatio (CORRECTED)

> **Source**: [Creatio Academy - Object Schema](https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/development-tools/creatio-ide/configuration-elements/object)

**URL:** `https://dev-pampabay.creatio.com/0/ClientApp/#/WorkspaceExplorer`

1. Select **IWQBIntegration** package
2. Click **Add** → **Object**

**General Section:**
- Code: `IWCommissionReportDataView`
- Title: `IW Commission Report Data View`

**Inheritance Section:**
- Parent object: `BaseEntity`
- Replace parent: ☐ Unchecked

**Behavior Section:**
- ☑️ **Represents Structure of Database View** ← CRITICAL

**Columns (Add via left sidebar):**

| Title | Code | Type | Notes |
|-------|------|------|-------|
| Transaction Date | IWTransactionDate | Date/Time | |
| Amount | IWAmount | Decimal | |
| Commission Amount | IWCommissionAmount | Decimal | |
| QB Invoice Number | IWQBInvoiceNumber | Text (250) | |
| Description | IWDescription | Text (500) | |
| Memo | IWMemo | Text (500) | |
| Sales Group | IWSalesGroup | **Lookup** → BGSalesGroup | NO "Id" suffix! |
| Sales Group Name | IWSalesGroupName | Text (250) | |
| Account | IWAccount | **Lookup** → Account | NO "Id" suffix! |
| Account Name | IWAccountName | Text (250) | |
| Payments Invoice | IWPaymentsInvoice | **Lookup** → Order | NO "Id" suffix! |
| Order Number | IWOrderNumber | Text (100) | |
| Owner | IWOwner | **Lookup** → Contact | NO "Id" suffix! |

> **Note**: BaseEntity columns (Id, CreatedOn, CreatedById, ModifiedOn, ModifiedById, ProcessListeners) are inherited automatically - do NOT add them manually.

> **Note**: For Lookup columns, the Creatio object column name does NOT include "Id" suffix, but the database view column DOES include "Id" suffix. Creatio handles this mapping automatically.

### Step 3: Configure IntExcelReport

```sql
-- Link IW_Commission to the new view
UPDATE "IntExcelReport"
SET "IntEntitySchemaNameId" = (
    SELECT "UId" FROM "SysSchema"
    WHERE "Name" = 'IWCommissionReportDataView'
    LIMIT 1
)
WHERE "Id" = '07c77859-b7e5-43f3-97c6-14113f6a1f6f';
```

### Step 4: Update C# Service

Add to `BuildFiltersConfig` method in `UsrExcelReportService.cs`:

```csharp
// IW_Commission: Direct filtering (no BGExecutionId)
else if (entitySchemaName == "IWCommissionReportDataView")
{
    // Date filter on IWTransactionDate (mapped from IWPaymentDue)
    if (request.YearMonthId != Guid.Empty)
    {
        var yearMonthName = GetYearMonthName(userConnection, request.YearMonthId);
        DateTime startDate, endDate;
        if (TryParseYearMonth(yearMonthName, out startDate, out endDate))
        {
            items.Add(string.Format(
                "\"DateRangeFilter\":{0}",
                BuildDateRangeFilterJson("IWTransactionDate", startDate, endDate)
            ));
        }
    }

    // Sales Group filter directly on IWSalesGroupId
    if (request.SalesRepId != Guid.Empty)
    {
        items.Add(string.Format(
            "\"SalesGroupFilter\":{0}",
            BuildFilterJson("IWSalesGroupId", request.SalesRepId)
        ));
    }
}
```

### Step 5: Move Service to PampaBayVer2

1. Open Creatio Configuration
2. Navigate to **PampaBayVer2** package
3. Add → Source Code Schema
4. Name: `UsrExcelReportService`
5. Copy updated code content
6. Save and compile
7. Test both reports
8. Remove old schema from previous package

---

## Filter Comparison

| Aspect | Commission | IW_Commission |
|--------|------------|---------------|
| Entity Schema | `BGCommissionReportDataView` | `IWCommissionReportDataView` |
| Date Column | `BGTransactionDate` | `IWTransactionDate` |
| Sales Group Column | Via `BGExecutionId` JOIN | `IWSalesGroupId` (direct) |
| Filter Method | Indirect (execution record) | **Direct** |
| Package | Existing BG | **IWQBIntegration** |

---

## Verification Tests

### IW_Commission Tests

```bash
# Test 1: No filters (all data)
CREATIO_REPORT_CODE=IW_Commission \
python3 scripts/testing/test_report_service.py --env dev
# Expected: 4 rows

# Test 2: With Year-Month filter
CREATIO_REPORT_CODE=IW_Commission \
CREATIO_YEAR_MONTH_NAME=2025-11 \
python3 scripts/testing/test_report_service.py --env dev
# Expected: Records from Nov 2025

# Test 3: With Sales Group filter
CREATIO_REPORT_CODE=IW_Commission \
CREATIO_SALES_GROUP_ID=75be0759-4bd0-4913-ad7b-d03a10567cd2 \
python3 scripts/testing/test_report_service.py --env dev
# Expected: Pampa Bay Independent records only
```

### Regression Tests

```bash
# Commission must still work
CREATIO_REPORT_CODE=Commission \
CREATIO_YEAR_MONTH_NAME=2024-12 \
CREATIO_SALES_GROUP_ID=edfefb79-77b6-43fe-932b-c012d9a2fc9d \
python3 scripts/testing/test_report_service.py --env dev
# Expected: Same as before (55 rows for Dec 2024 + RDGZ)
```

---

## Rollback Plan

1. **View issues**: `DROP VIEW "IWCommissionReportDataView";`
2. **Service issues**: Restore previous code from git
3. **Config issues**: Reset `IntEntitySchemaNameId` to NULL

---

## Checklist

- [x] Create view SQL file (`scripts/sql/IWCommissionReportDataView_clean.sql`)
- [x] Run SQL in DEV database (2026-01-13 - executed successfully)
- [x] Update UsrExcelReportService.cs (IW filtering code added, lines 308-333)
- [x] Update view to include BaseEntity columns (2026-01-14)
- [x] Delete old entity schema and recreate with Lookup columns (2026-01-14)
- [x] Register entity schema in IWQBIntegration (with Lookup columns, NOT Unique identifier)
- [x] Update IntExcelReport configuration
- [x] Deploy C# service to DEV
- [x] Test IW_Commission (all filter combos) - **PASSED** (2026-01-14)
- [x] Test Commission (regression) - **PASSED** (56 rows)
- [ ] Move service to PampaBayVer2
- [x] Final verification - Year-Month + Sales Group filters working
- [ ] Update TEST_LOG.md with results

## Errors Encountered & Resolutions

### Error 1: "Failed to update structure" (2026-01-14)
- **Cause**: Used "Unique identifier" type for GUID columns
- **Fix**: Use Lookup type for foreign keys, Text for non-FK GUIDs

### Error 2: "ADD CONSTRAINT cannot be performed on relation" (2026-01-14)
- **Cause**: View missing BaseEntity columns (CreatedById, ModifiedById, ProcessListeners)
- **Fix**: Update view SQL to include all 6 BaseEntity columns
- **Reference**: [CustomerFX - Using Database Views in Creatio](https://customerfx.com/article/using-database-views-in-creatio/)

### Error 3: "Column by path IWTransactionDate not found in schema IWPayments" (2026-01-14)
- **Cause**: IntExcelExport library internally uses base table schema (IWPayments) for filter application, not the view
- **Symptom**: Report generates OK without filters, but fails when YearMonthId filter is passed
- **Fix**: Use base table column names in FiltersConfig filters:
  - `IWPaymentDue` instead of `IWTransactionDate` (view alias)
  - `IWSalesGroup` (without "Id" suffix - Creatio Lookup convention)
- **Key insight**: The library's filter application path differs from its column/data path

### Error 4: "ArgumentNullException: Value cannot be null" for date filters (2026-01-14)
- **Cause**: IntExcelExport library cannot handle DateTime filters in FiltersConfig (throws null in Json.Deserialize)
- **Symptom**: Any date filter (dataValueType 7) causes failure regardless of filter structure
- **Solution**: Implemented custom generator (`GenerateIWCommissionWithDateFilter`) that bypasses IntExcelExport library

### Error 5: "Cannot access entries in Create mode" (2026-01-14)
- **Cause**: Incorrect ZipArchiveMode enum value (used 1=Create instead of 2=Update)
- **Fix**: Changed `Enum.ToObject(zipArchiveModeType, 1)` to `Enum.ToObject(zipArchiveModeType, 2)`

## Final Solution (2026-01-14)

The Year-Month filter for IW_Commission required a **complete bypass of the IntExcelExport library**:

1. **Custom Generator** (`GenerateIWCommissionWithDateFilter`):
   - Intercepts IW_Commission + YearMonthId in Generate() method
   - Queries data directly via EntitySchemaQuery with date range filters
   - Populates Excel template via ZIP/XML manipulation

2. **Direct ESQ Query** (`QueryIWCommissionData`):
   - Filters on `IWTransactionDate` >= startDate and < endDate
   - Optionally filters on `IWSalesGroup` for Sales Group
   - Returns `List<Dictionary<string, object>>` for Excel population

3. **ZIP-based Excel Population** (`PopulateWithZipXml`):
   - Uses reflection to load `System.IO.Compression.ZipArchive`
   - Opens .xlsm as ZIP archive in Update mode
   - Modifies `xl/worksheets/sheet1.xml` with data rows
   - Preserves macros (vbaProject.bin) intact

## Current Status (2026-01-14)

| Feature | Status | Notes |
|---------|--------|-------|
| Report generation | ✅ Working | Uses IWCommissionReportDataView |
| Sales Group filter | ✅ Working | Direct filtering via custom generator |
| Year-Month filter | ✅ Working | Custom generator bypasses library limitation |
| Commission regression | ✅ Verified | No impact to existing report |
