# BGlobal V7 Creatio Architecture - Complete Reference

**Date:** 2026-01-30
**Source:** PampaBay package extraction + PROD OData investigation + codebase analysis
**Purpose:** Comprehensive understanding of how BGlobal designed reports to work in V7

---

## Executive Summary

BGlobal implemented **two distinct report generation patterns** in Creatio V7:

| Pattern | Name | Filter Mechanism | View Design | Example Reports |
|---------|------|------------------|-------------|-----------------|
| **Type A** | Execution-Based | BGReportExecution table stores filters | `JOIN "BGReportExecution" ON true` | Commission, Customers Did Not Buy, Sales by Sales Group |
| **Type B** | Direct | ESQ filters at query time | Simple SELECT (no execution JOIN) | Items by Customer, Sales by Item |

**Critical Understanding:** BGlobal's design relies on:
1. **BGReportExecution** as a filter mediator table
2. **IntExcelReport** for template configuration
3. **IntExcelExport library** for report generation
4. **SQL Views** with execution-based filtering built-in
5. **ESQ relationship columns** for cross-entity data access

---

## 1. BGReportExecution Table - The Filter Hub

### Purpose

Stores filter parameters as database records. Views JOIN to this table and filter internally using stored values.

### Schema

| Column | Type | Purpose |
|--------|------|---------|
| `Id` | GUID | Primary key (becomes BGExecutionId in views) |
| `BGReportName` | Text | Report identifier ("Commission", "Customers Did Not Buy", etc.) |
| `BGCreatedFrom` | DateTime | Order creation date range start |
| `BGCreatedTo` | DateTime | Order creation date range end |
| `BGShippingFrom` | DateTime | Ship date range start |
| `BGShippingTo` | DateTime | Ship date range end |
| `BGDeliveryFrom` | DateTime | Delivery date range start |
| `BGDeliveryTo` | DateTime | Delivery date range end |
| `BGYearMonthId` | Lookup → BGYearMonth | Year-month period (Commission) |
| `BGSalesGroupId` | Lookup → BGSalesGroup | Sales group filter |
| `BGCustomerId` | Lookup → Account | Customer filter |
| `BGOrderStatusId` | Lookup → UsrStatus | Order status filter |
| `BGUserId` | GUID | User who ran the report (audit) |

### How It Works

```
USER SELECTS FILTERS → CREATE BGReportExecution RECORD → QUERY VIEW
                              ↓
                   BGReportExecution
                   {
                     Id: "abc-123",
                     BGReportName: "Customers Did Not Buy",
                     BGCreatedFrom: 2026-01-01,
                     BGCreatedTo: 2026-01-31
                   }
                              ↓
           VIEW (with JOIN to BGReportExecution):
           SELECT ... FROM Account a
           JOIN BGReportExecution re ON true
           WHERE NOT EXISTS (
             SELECT 1 FROM Order o
             WHERE ... AND o.CreatedOn >= re.BGCreatedFrom
                     AND o.CreatedOn <= re.BGCreatedTo
           )
                              ↓
           ESQ QUERY: WHERE BGExecutionId = 'abc-123'
```

---

## 2. SQL View Architecture

### Type A: Execution-Based Views (BGCustomerDidNotBuyView)

**Extracted from PampaBay package:**

```sql
CREATE VIEW "BGCustomerDidNotBuyView" AS
SELECT
    a."Id",
    a."CreatedOn", a."CreatedById", a."ModifiedOn", a."ModifiedById",
    a."ProcessListeners",
    a."Id" AS "BGAccountId",

    -- Subquery: Most recent order ID
    (SELECT o1."Id" FROM "Order" o1
     WHERE o1."AccountId" = a."Id"
       AND o1."StatusId" != '2b9201fc-...'      -- Not Cancelled
       AND o1."BGOrderTypeId" = '154d3407-...'  -- Customer order type
     ORDER BY o1."CreatedOn" DESC LIMIT 1
    ) AS "BGLastOrderId",

    -- Subquery: Email from AccountCommunication
    (SELECT ac."Number" FROM "AccountCommunication" ac
     WHERE ac."AccountId" = a."Id"
       AND ac."CommunicationTypeId" = 'ee1c85c3-...'  -- Email type
     ORDER BY ac."CreatedOn" DESC LIMIT 1
    ) AS "BGEmail",

    -- Subquery: Count of orders BEFORE date range
    (SELECT COUNT(*) FROM "Order" o2
     WHERE o2."AccountId" = a."Id"
       AND o2."StatusId" != '2b9201fc-...'
       AND o2."BGOrderTypeId" = '154d3407-...'
       AND (o2."CreatedOn" - '05:00:00'::interval)::date < re."BGCreatedFrom"::date
    ) AS "BGPreviousOrderCount",

    -- Human-readable filter string
    ('Created Date: ' || COALESCE(to_char(re."BGCreatedFrom", 'mm/dd/yyyy'), '')
     || ' to ' || COALESCE(to_char(re."BGCreatedTo", 'mm/dd/yyyy'), '')
    ) AS "BGFilters",

    -- Execution ID for downstream filtering
    re."Id" AS "BGExecutionId"

FROM "Account" AS a
JOIN "BGReportExecution" AS re ON true  -- CARTESIAN PRODUCT

WHERE
    a."TypeId" = '03a75490-...'  -- Customer account type
    AND NOT EXISTS (
        -- Find accounts with NO orders in the date range
        SELECT 1 FROM "Order" o
        WHERE o."AccountId" = a."Id"
          AND o."BGOrderTypeId" = '154d3407-...'
          AND o."StatusId" != '2b9201fc-...'
          -- Date range from BGReportExecution
          AND (re."BGCreatedFrom" IS NULL
               OR (o."CreatedOn" - '05:00:00'::interval)::date >= re."BGCreatedFrom"::date)
          AND (re."BGCreatedTo" IS NULL
               OR (o."CreatedOn" - '05:00:00'::interval)::date <= re."BGCreatedTo"::date)
    );
```

**Key Design Decisions:**

1. **`JOIN ... ON true`** creates Cartesian product (every account × every execution record)
2. **Filters are in the WHERE clause**, using values from `re.BGCreatedFrom`, `re.BGCreatedTo`
3. **`NOT EXISTS`** finds customers who have NO orders in the date range
4. **Only outputs Account ID** - customer details (Name, Address, City) must come via ESQ relationship columns
5. **Timezone handling**: `- '05:00:00'::interval` adjusts for EST

### Type B: Direct Views (BGSalesByItemView)

```sql
CREATE VIEW "BGSalesByItemView" AS
SELECT
    o."Id",
    o."Number" AS "BGNumber",
    p."Name" AS "BGItem",
    p."Description" AS "BGProductDescription",  -- Added 2026-01-29
    op."Quantity" AS "BGQuantity",
    op."TotalAmount" AS "BGAmount",
    ac."Name" AS "BGCustomer",
    os."Name" AS "BGStatus",
    sg."BGSalesGroupName" AS "BGSalesGroup",
    e."Name" AS "BGSalesRep"
FROM "Order" o
JOIN "OrderProduct" op ON (op."OrderId" = o."Id")
JOIN "Product" p ON (p."Id" = op."ProductId")
JOIN "Account" ac ON (o."AccountId" = ac."Id")
JOIN "OrderStatus" os ON (o."StatusId" = os."Id")
JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id")
JOIN "Employee" e ON (o."BGSalesRepLookupId" = e."Id")
WHERE o."BGOrderTypeId" = '154d3407-...'
  AND os."Id" IN (...)  -- Valid statuses
```

**Key Differences:**
- No BGReportExecution JOIN
- No BGExecutionId column
- Filters applied externally via ESQ at query time
- All columns directly available (no relationship columns needed)

---

## 3. IntExcelReport Configuration

### Table Structure

| Column | Type | Purpose |
|--------|------|---------|
| `Id` | GUID | Primary key (ReportId) |
| `IntName` | Text | Report name (e.g., "Rpt CustomersDidNotBuyOverAPeriodOfTime") |
| `IntEntitySchemaName` | Lookup | View/entity schema reference |
| `IntEsq` | Text | Serialized ESQ JSON |
| `IntFiltersConfig` | Text | Filter template (e.g., "BGExecutionId = @P1@") |
| `IntSheetName` | Text | Excel sheet name (default: "Data") |
| `IntFile` | Binary | Excel template workbook |

### Example: Customers Did Not Buy

**PROD Configuration (ID: `1f65a56a-d7f4-4ce2-b517-c633872ea545`):**

```json
{
  "IntName": "Rpt CustomersDidNotBuyOverAPeriodOfTime",
  "IntEntitySchemaId": "d55e4a0b-...",  // Points to BGSalesByCustomerView (WRONG!)
  "IntEsq": {
    "rootSchemaName": "BGSalesByCustomerView",  // WRONG - should be BGCustomerDidNotBuyView
    "columns": {
      "BGStatus": {...},
      "BGCustomer": {...},
      "BGShipDate": {...},
      ...
    }
  },
  "IntSheetName": "Data"
}
```

**Problem:** IntEsq references wrong view (`BGSalesByCustomerView` instead of `BGCustomerDidNotBuyView`)

---

## 4. IntExcelExport Library Flow

### How the Library Works

```
1. Receive request with ReportId + filters
2. Read IntExcelReport record (template, ESQ, FiltersConfig)
3. Parse IntEsq JSON → EntitySchemaQuery
4. Apply FiltersConfig (e.g., BGExecutionId = @P1@)
5. Execute ESQ against view
6. Map result columns to Excel template cells
7. Return populated Excel bytes
```

### Filter Application Mechanisms

| Mechanism | Source | Type A (Execution) | Type B (Direct) |
|-----------|--------|-------------------|-----------------|
| **FiltersConfig** | IntExcelReport.IntFiltersConfig | `BGExecutionId = @P1@` | (rarely used) |
| **IntEsq.filters** | IntExcelReport.IntEsq JSON | Static filters | Static filters |
| **Runtime Esq** | Service builds at request time | Additional filters | Primary filter method |

### Why Custom Generators Exist

The IntExcelExport library has limitations:

| Problem | Solution |
|---------|----------|
| DateTime filter deserialization fails | Custom generator with direct ESQ |
| FiltersConfig not applied to some views | Custom generator bypasses library |
| Large datasets cause OutOfMemory | Custom generator with pagination |
| Wrong view reference in IntEsq | Route by IntName, use correct view |

---

## 5. ESQ Relationship Columns

### Critical for Type A Views

Since `BGCustomerDidNotBuyView` only outputs `BGAccountId`, customer details must come via ESQ:

```csharp
// ESQ column paths for Account relationship
esq.AddColumn("BGAccount.Name");        // Customer name
esq.AddColumn("BGAccount.Address");     // Street address
esq.AddColumn("BGAccount.City.Name");   // City (lookup display value)
esq.AddColumn("BGAccount.Region.Name"); // State (lookup display value)
esq.AddColumn("BGAccount.Zip");         // ZIP code
esq.AddColumn("BGAccount.Phone");       // Phone number
```

### How It Works

```
ESQ Query: SELECT BGAccount.Name, BGAccount.Address, ...
           FROM BGCustomerDidNotBuyView
           WHERE BGExecutionId = 'abc-123'

Creatio ORM:
  1. Query BGCustomerDidNotBuyView → get BGAccountId
  2. Auto-JOIN to Account table via foreign key relationship
  3. Return Account.Name, Account.Address, etc.
```

---

## 6. Complete Data Flow

### Type A: Customers Did Not Buy

```
┌─────────────────────────────────────────────────────────────┐
│ USER: Selects Date From: 2026-01-01, Date To: 2026-01-31   │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND: POST /Generate                                    │
│ {                                                           │
│   ReportId: "1f65a56a-...",                                 │
│   CreatedFrom: "2026-01-01",                                │
│   CreatedTo: "2026-01-31"                                   │
│ }                                                           │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ BACKEND: Create BGReportExecution Record                    │
│ INSERT INTO BGReportExecution (                             │
│   Id, BGReportName, BGCreatedFrom, BGCreatedTo              │
│ ) VALUES (                                                  │
│   'exec-guid', 'Customers Did Not Buy',                     │
│   '2026-01-01', '2026-01-31'                                │
│ )                                                           │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ BACKEND: Build ESQ Query                                    │
│ esq = new EntitySchemaQuery("BGCustomerDidNotBuyView")      │
│ esq.AddColumn("BGAccount.Name")                             │
│ esq.AddColumn("BGAccount.Address")                          │
│ esq.AddColumn("BGAccount.City.Name")                        │
│ esq.AddColumn("BGAccount.Region.Name")                      │
│ esq.AddColumn("BGAccount.Zip")                              │
│ esq.AddColumn("BGEmail")                                    │
│ esq.AddColumn("BGAccount.Phone")                            │
│ esq.AddColumn("BGPreviousOrderCount")                       │
│ esq.AddFilter("BGExecutionId", Equal, 'exec-guid')          │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ DATABASE: Execute View Query                                │
│                                                             │
│ BGCustomerDidNotBuyView:                                    │
│   JOIN BGReportExecution re ON true                         │
│   WHERE NOT EXISTS (orders in date range)                   │
│   → Returns accounts that DIDN'T buy in Jan 2026            │
│                                                             │
│ Auto-JOIN to Account via BGAccountId:                       │
│   → Returns Name, Address, City, Region, Zip, Phone         │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ BACKEND: Populate Excel Template                            │
│   Column A: BGAccount.Name                                  │
│   Column B: BGAccount.Address                               │
│   Column C: BGAccount.City.Name                             │
│   Column D: BGAccount.Region.Name                           │
│   Column E: BGAccount.Zip                                   │
│   Column F: BGEmail                                         │
│   Column G: BGAccount.Phone                                 │
│   Column H: BGPreviousOrderCount                            │
└─────────────────────────────┬───────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND: Download Excel File                               │
│ GET /GetReport/ExportFilterKey_{guid}/CustomersDidNotBuy    │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. GUID Reference

| GUID | Entity | Value |
|------|--------|-------|
| `2b9201fc-3891-4ba3-abde-1bb9ce195ecc` | OrderStatus | Cancelled |
| `154d3407-9d8c-49c2-84cd-e85afeb8d55a` | BGOrderType | Customer |
| `03a75490-53e6-df11-971b-001d60e938c6` | AccountType | Customer |
| `ee1c85c3-cfcb-df11-9b2a-001d60e938c6` | CommunicationType | Email |
| `1f65a56a-d7f4-4ce2-b517-c633872ea545` | IntExcelReport | Rpt CustomersDidNotBuyOverAPeriodOfTime |
| `10647dfc-f999-4cf7-a17c-52a070c36ee6` | SysSchema | BGCustomerDidNotBuyView |

---

## 8. Decision Framework

### When to Use Type A (Execution-Based)

✅ Use when:
- Need persistent filter audit trail
- Multiple users may run same report simultaneously
- Complex filter logic that's easier in SQL than ESQ
- Report name identifies the filter context

⚠️ Caution:
- `JOIN ... ON true` creates Cartesian product
- Large datasets × many execution records = OutOfMemory
- Must manage BGReportExecution record lifecycle

### When to Use Type B (Direct)

✅ Use when:
- Filters are simple (date range, customer name)
- No audit trail needed
- View already has all columns needed
- Dataset is manageable size

⚠️ Caution:
- Must build ESQ filters at request time
- No persistent filter record

---

## 9. Fixing RPT-005: Correct Approach

### Option 1: Follow BGlobal's Pattern (Recommended)

1. **Create BGReportExecution record** with date filters
2. **Use ESQ relationship columns** for Account details:
   ```csharp
   esq.AddColumn("BGAccount.Name");
   esq.AddColumn("BGAccount.Address");
   esq.AddColumn("BGAccount.City.Name");
   esq.AddColumn("BGAccount.Region.Name");
   esq.AddColumn("BGAccount.Zip");
   esq.AddColumn("BGEmail");  // Direct from view
   esq.AddColumn("BGAccount.Phone");
   esq.AddColumn("BGPreviousOrderCount");  // Direct from view
   ```
3. **Filter by BGExecutionId** in ESQ
4. **Populate Excel template** with mapped columns

### Option 2: Fix IntExcelReport Configuration

1. **Update IntEsq rootSchemaName** to `BGCustomerDidNotBuyView`
2. **Update IntEsq columns** to use relationship paths
3. Let IntExcelExport library handle report generation

### Option 3: Bypass Execution Pattern (Current Approach)

1. **Route by IntName** (already implemented)
2. **Query view directly** with date filters in ESQ
3. **Risk:** May not match BGlobal's execution audit pattern

---

## 10. Files Reference

| File | Purpose |
|------|---------|
| `sql/BGCustomerDidNotBuyView_ORIGINAL.sql` | Original view definition |
| `sql/BGCommissionReportDataView.sql` | Commission view reference |
| `source-code/UsrExcelReportService_Updated.cs` | Custom backend service |
| `docs/reference/MASTER_CATALOG.md` | Entity/view catalog |
| `docs/reference/SQL_VIEW_MASTER_CATALOG.md` | All 25+ views analysis |

---

*Document created: 2026-01-30*
*Source: PampaBay package extraction + PROD OData + codebase analysis*
