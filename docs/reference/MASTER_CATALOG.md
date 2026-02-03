# Master Catalog - Creatio Reports

> **Purpose:** Single source of truth for all entities, schemas, mappings, and configurations.
> **Updated:** 2026-01-28

---

## Table of Contents
1. [Entities & Tables](#entities--tables)
2. [Report Mappings](#report-mappings)
3. [Schemas & Handlers](#schemas--handlers)
4. [Services & Endpoints](#services--endpoints)
5. [Views](#views)
6. [Status GUIDs](#status-guids)
7. [Key Business Processes](#key-business-processes)

---

## Entities & Tables

### UsrReportesPampa (Report Menu)
**Purpose:** Dropdown list of available reports shown to users.

| Column | Type | Description |
|--------|------|-------------|
| Id | GUID | Primary key |
| Name | String | Display name in dropdown |
| UsrCode | String | Code used to find IntExcelReport template |
| UsrURL | String | Looker Studio URL (if Looker report) |

**All Records (18 total):**
| Name | Id | UsrCode | Type |
|------|-----|---------|------|
| Sales By Item | `839e5bf3-8e97-4ba3-8884-9fde4a0230aa` | `SalesByItem` | Excel |
| Sales By Line | `d8483e56-2e28-4402-9988-c30ed393cf2f` | `SalesByLine` | Excel |
| Sales By Customer | `1411148b-e24f-4c34-b4dc-ab05faba8ac3` | `SalesByCustomer` | Looker |
| Sales By Sales Group | `1515dc95-aadf-4471-bc09-aa68f5da2f29` | `SalesBySalesGroup` | Looker |
| Sales By Customer Type | `46ab2fd0-fc1a-4775-a101-e0fc4e7bc58a` | `SalesByCustomerType` | Looker |
| Sales By Item By Type Of Customer | `0d3d4a17-04d5-418c-a5cf-14f9edd3a3b5` | `SalesByItemByTypeOfCustomer` | Excel |
| Sales By Item (duplicate) | `e850b63a-b763-4e92-a2c5-1bbfeef6afd6` | (empty) | Looker |
| **Commission** | `9de295e4-7c79-4de6-9218-8bb5e47ce81b` | `Commission` | Excel |
| **Items by Customer** | `e4045fee-66e4-44ff-b7ad-8d1a9e7a1770` | `ItemsByCustomer` | Excel |
| Customers did not buy... | `4572a978-a1d6-4e1b-bda5-acb77a4a7c17` | `CustomersDidNotBuyOverAPeriodOfTime` | Excel |
| Sales By Line By Type Of Customer | `f13a1f40-80b6-4e7b-bf7a-a591f4977b57` | (empty) | Looker |
| Sales By Item By Type Of Customer | `f2629ca6-a11f-4573-be16-5f4efe035c72` | (empty) | Looker |
| Sales By Item Theme | `f7f97a4b-5ecf-49d8-b26a-13bcc1ecac32` | (empty) | Looker |
| Sales By Line With Ranking | `8f4e7c9e-ae67-4577-a012-e7e827aa6755` | `SalesByLineWithRanking` | Looker |
| Sales By Item Line | `63979873-b6ee-49b5-a0ae-8994d3f027f9` | `SalesByItemLine` | Looker |
| Sales By Sales Rep | `8edb97c8-0cc6-4cf0-9cd5-70291affb47e` | `SalesBySalesRep` | Looker |
| Sales by Customer Year Comparison | `b11339d1-e755-4679-9521-7f63269b863d` | (empty) | Looker |
| Sales Rep Monthly Report | `64823da1-d7b0-4ce5-8b50-2d2599642a67` | (empty) | Looker |

**Excel Reports (5):** Commission, Items by Customer, Sales By Item, Sales By Line, Sales By Item By Type Of Customer, Customers did not buy
**Looker Reports (12):** All others with URLs

---

### IntExcelReport (Excel Templates)
**Purpose:** BGlobal's Excel report template definitions.
**Package:** BGIntExcelReports

| Column | Type | Description |
|--------|------|-------------|
| Id | GUID | Primary key |
| IntName | String | Template name (used for lookup) |
| IntEsq | Text | Serialized ESQ query (JSON) |
| IntFile | Binary | Excel template file |

**Note:** `IntEntitySchemaName` column does NOT exist (schema different than assumed).

**All Records (33 total):**
| IntName | Id |
|---------|-----|
| Warehouse Order | `b652ba04-fa7c-4447-95ba-d73f2d6c1f9e` |
| Rpt Sales By Line | `0b40d51d-4935-4918-97f2-45352aed341f` |
| **Rpt Commission** | `4ba4f203-7088-41dc-b86d-130c590b3594` |
| Rpt Sales By Customer (Collapsed) | `ddb6bfa4-2c58-44b9-814d-91ee0c02c989` |
| Inventory Chart | `7bfec367-e648-44e3-bf24-7569bd215d6e` |
| Rpt Sales By Line With Ranking (Collapsed) | `ba330b02-630e-4f5e-8d60-3e7c0560aa5b` |
| Net Profit Chart (Factory Order) | `b1c0b66d-3de6-4ddc-91f8-59cede9fbda8` |
| Rpt Sales By Customer | `62d81c91-13d2-4edf-9827-1f9e35ce03d9` |
| Rpt CustomersDidNotBuyOverAPeriodOfTime | `1f65a56a-d7f4-4ce2-b517-c633872ea545` |
| Account Email | `eca07ecf-79b5-493e-9e4d-d4f35fa63323` |
| Net Profit Chart (catalog) | `0771aae8-ce47-4f6a-8796-c939ba1ace88` |
| Rpt Sales by Customer Type (Collapsed) | `7592aced-1315-4475-bd13-da12e6c5750b` |
| Rpt Sales by Sales Group (Collapsed) | `6e9d462b-99ef-4e6c-9c7c-f425721be455` |
| Rpt Sales By Item | `c4f4e32c-376d-4b19-b04b-2129dba29d06` |
| Rpt Sales By Sales Group | `a935a791-e2ff-4693-9b50-38a8596a3667` |
| Rpt Sales By Sales Rep | `50b59be9-1fab-449a-a257-11dce5ec1434` |
| Rpt Sales Rep Monthly Report | `5b39f08f-3b55-4963-b74d-eddfb540bdba` |
| Rpt Sales by Sales Rep (Collapsed) | `41afd5e9-7043-4bb8-a52f-0f927bc3505f` |
| Rpt Sales By Customer Year Comparison (Collapsed) | `f336165b-f6b7-4a55-bcf1-3f24bae73d26` |
| Net Profit Chart (Customer Order) | `2110ecbc-e240-4828-bf18-a5f0daf62128` |
| Rpt Sales By Customer Type | `6e11dc16-df10-47c4-97be-9695f3feb77a` |
| Rpt Sales by Customer Year Comparison | `f7e2a69d-8a3e-4f1e-ba8a-d0cd8b3b1a53` |
| Rpt Sales By Line With Ranking | `384bf7f6-28fa-4f65-bd64-1a45d96a09e8` |
| Account Address | `a321f7bf-00cb-4f9a-af7e-02c13913779b` |
| Net Profit Chart (Customer Orders) | `410dd95c-9b1f-4c75-b195-88c1678b5bc3` |
| Net Profit Chart (product) | `0887cc48-f9eb-4241-b853-71735dccef6a` |
| Net Profit Chart (Catalog) Sales Price | `2b9d3c0e-e5a0-463b-b7ae-49926550a6f1` |
| Net Profit Chart (Catalog) Last Price Paid | `6f9f3112-a9b9-4829-870f-278fc172aa29` |
| Rpt Sales By Item By Type Of Customer | `53682214-a63c-407a-b3f1-79d8ab235f18` |
| **Items by Customer** | `d213933b-093d-47fc-8da8-422c0d9bf715` |
| Rpt Sales by Item Line | `1d009377-3cef-4199-9e38-7b47ddb27a0d` |
| test CSV | `eade67be-dfd4-4cd5-a07f-86f0b343a71c` |
| Inventory Adjustment Report | `4bf08cd3-f42d-4ce6-b032-e85dca4f4ddb` |

**IMPORTANT:** `IntName` may differ from `UsrReportesPampa.UsrCode`!
- UsrCode: `ItemsByCustomer` (no spaces)
- IntName: `Items by Customer` (with spaces)
- UsrCode: `Commission`
- IntName: `Rpt Commission` (has "Rpt " prefix)

---

### BGReportExecution (Filter Storage)
**Purpose:** Stores filter parameters for SQL view filtering.
**Package:** BGIntExcelReports

**Note:** `BGIntExcelReportId` column does NOT exist (schema different than assumed).

Need to query actual columns:
```sql
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'BGReportExecution';
```

**Known Usage:**
- Views read filters via `@ReportExecutionId` parameter
- Commission reports create records here before generation
- "Items by Customer" has 0 records (may have never been configured)

---

### BGYearMonth (Year-Month Lookup)
**Purpose:** Available year-month values for Commission filter.

| Column | Type | Description |
|--------|------|-------------|
| Id | GUID | Primary key |
| Name | String | Display name (e.g., "2025-12") |

---

### BGSalesGroup (Sales Group Lookup)
**Purpose:** Sales groups for Commission filter.

| Column | Type | Description |
|--------|------|-------------|
| Id | GUID | Primary key |
| Name | String | Group name |

**Record Count:** ~76 total groups

---

## Report Mappings

### Report Type → Filter Requirements

| Report | YearMonth | SalesGroup | Customer | DateRange | Status |
|--------|-----------|------------|----------|-----------|--------|
| Commission | ✅ | ✅ | ❌ | ❌ | ❌ |
| IW_Commission | ✅ | ✅ | ❌ | ❌ | ❌ |
| Items by Customer | ❌ | ❌ | ✅ | ✅ | ✅ |
| Looker Reports | ❌ | ❌ | ❌ | ✅ | ✅ |
| Other Excel | ❌ | ❌ | ❌ | ✅ | ✅ |

### UsrReportesPampa.UsrCode → IntExcelReport.IntName

| UsrCode | IntName | Match Type |
|---------|---------|------------|
| `ItemsByCustomer` | `Items by Customer` | Display name (spaces) |
| `Commission` | `Commission` or `Rpt Commission` | Direct or Rpt prefix |
| (TBD) | (TBD) | Need to catalog all |

---

## Schemas & Handlers

### Frontend Schemas

| Schema | UID | Package | Purpose |
|--------|-----|---------|---------|
| UsrPage_ebkv9e8 | `561d9dd4-8bf2-4f63-a781-54ac48a74972` | BGApp_eykaguu | Child handler (our code) |
| BGPage_iaptpa6 | (TBD) | BGGlobal_* | Parent schema (BGlobal) |

**Schema Designer URLs:**
- DEV: `https://dev-pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734`
- PROD: `https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972`

### Handler Versions

| Version | File | Status |
|---------|------|--------|
| v22 | `_v22_Bare.js` | **PROD** |
| v21 | `_v21_SafeFilters.js` | Superseded |
| v20 | `_v20_Minimal.js` | Superseded |
| v19.1 | `_v19_LookerFix.js` | Backup |
| v18 | `_v18_AttrBinding.js` | Backup |

### Parent Schema Elements (BGPage_iaptpa6)

| Element Name | Type | Purpose |
|--------------|------|---------|
| GridContainer_oshnwh8 | Container | Parent's report dropdown (hidden by us) |
| GridContainer_fh039aq | Container | Iframe container |
| GridContainer_xdy25v1 | Container | Date filters |
| GridContainer_knkow5v | Container | Status filter |
| Button_vae0g6x | Button | Generate/Report button |
| LookupAttribute_0as4io2 | Attribute | Report selection binding |

---

## Services & Endpoints

### UsrExcelReportService (Our Custom Service)
**Package:** UsrExcelReportService
**Source:** `source-code/UsrExcelReportService_Updated.cs`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/0/rest/UsrExcelReportService/Generate` | POST | Generate Excel report |
| `/0/rest/UsrExcelReportService/GetReport/{key}/{filename}` | GET | Download generated file |

**Generate Request Body:**
```json
{
  "ReportId": "GUID",           // IntExcelReport.Id
  "EsqString": "...",           // Optional: serialized ESQ
  "RecordCollection": [],       // Optional: specific record IDs
  "YearMonth": "GUID",          // For Commission
  "SalesGroupId": "GUID",       // For Commission
  "CustomerName": "string",     // For Items by Customer
  "CreatedFrom": "datetime",    // Date filter
  "CreatedTo": "datetime"       // Date filter
}
```

**Generate Response:**
```json
{
  "success": true,
  "key": "session-key-guid",
  "message": "..."
}
```

---

### BGIntExcelReportService2 (BGlobal Original)
**Package:** BGIntExcelReports

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/0/rest/BGIntExcelReportService2/GetExportFilteredData` | POST | Download from session |
| `/0/rest/BGIntExcelReportService2/GetTemplate` | GET | Download template file |

**Note:** This service only DOWNLOADS - generation was done by IntGenerateExcelReportUserTask.

---

### Other Services (Checked)

| Service | Status | Notes |
|---------|--------|-------|
| IntExcelReportService | 404 | Does not exist |
| AletExcelReportService | 404 | Does not exist |

---

## Views

### BGSalesByItemView
**Purpose:** Data source for "Items by Customer" report.
**Entity Schema Id:** `209a8e5b-a6e3-40f5-b8fb-b37133439fb6`

| Column | Type | Notes |
|--------|------|-------|
| Id | uuid | Primary key |
| BGCustomer | character varying | Customer name (VARCHAR, not GUID!) |
| BGItem | character varying | Item name |
| BGNumber | character varying | Order number |
| BGPONumber | character varying | PO number |
| BGQuantity | integer | Quantity |
| BGPrice | numeric | Unit price |
| BGAmount | numeric | Total amount |
| BGSalesGroup | character varying | Sales group name |
| BGSalesRep | character varying | Sales rep name |
| BGStatus | character varying | Status (VARCHAR, not GUID!) |
| CreatedOn | timestamp | Order creation date |
| BGShipDate | date | Shipping date |
| BGDeliveryDate | date | Delivery date |
| CreatedById | uuid | Created by user |
| ModifiedById | uuid | Modified by user |
| ModifiedOn | timestamp | Modified date |
| ProcessListeners | integer | System field |

**Filter Pattern:**
```sql
WHERE BGCustomer ILIKE '%CustomerName%'
  AND CreatedOn >= @CreatedFrom
  AND CreatedOn <= @CreatedTo
  AND BGStatus = 'Shipped'
```

**Note:** All text fields are VARCHAR - use text comparison, not GUID lookups!

---

### BGCommissionView
**Purpose:** Data source for Commission reports.

| Column | Type | Notes |
|--------|------|-------|
| BGYearMonth | GUID | Links to BGYearMonth lookup |
| BGSalesGroup | GUID | Links to BGSalesGroup lookup |
| (other columns) | ... | Commission details |

**Filter Pattern:**
Uses @ReportExecutionId to read filters from BGReportExecution table.

---

## Status GUIDs

### QB Integration Log Status (BGQuickBooksIntegrationLogDetail)

| Status | GUID |
|--------|------|
| Pending | `c97db3bc-634d-4c90-8432-ec7141c87640` |
| Processed | `e7428193-4cf1-4d1b-abae-00e93ab5e1c5` |
| Error | `bdfc60c7-55fd-4cbd-9a2c-dca2def46d80` |
| Processing | `fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef` |
| Re-Process | `ff92e20c-da27-4255-96bc-57e32f0944f4` |

---

## Key Business Processes

### IntGenerateExcelReportUserTask
**GUID:** `05c5265c-3f51-4114-9862-fc434abe1f6d`
**Purpose:** BGlobal's original Excel generation business process.
**Status:** Exists in PROD but not easily callable from Freedom UI.

**Original Flow (Classic UI):**
```
BGIntExcelreportMixin → IntGenerateExcelReportUserTask → Session storage → BGIntExcelReportService2.GetExportFilteredData
```

**Why Not Used:**
- Mixin pattern doesn't work in Freedom UI
- Business process triggering differs in Freedom UI
- We built UsrExcelReportService as replacement

---

## SQL Diagnostic Queries

### Find all UsrReportesPampa records
```sql
SELECT "Id", "Name", "UsrCode", "UsrURL" FROM "UsrReportesPampa" ORDER BY "Name";
```

### Find all IntExcelReport templates
```sql
SELECT "Id", "IntName", "IntEntitySchemaName" FROM "IntExcelReport" ORDER BY "IntName";
```

### Check BGReportExecution for a report
```sql
SELECT * FROM "BGReportExecution" WHERE "BGIntExcelReportId" = 'report-guid' ORDER BY "CreatedOn" DESC LIMIT 10;
```

### Find view columns
```sql
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'BGSalesByItemView';
```

---

## Package Reference

| Package | Owner | Contents |
|---------|-------|----------|
| BGApp_eykaguu | Pampa Bay | UsrPage_ebkv9e8 handler |
| BGIntExcelReports | BGlobal | IntExcelReport, BGReportExecution, BGIntExcelReportService2 |
| BGGlobal_* | BGlobal | Parent schemas, mixins |
| UsrExcelReportService | Our custom | Excel generation service |

---

## Known Issues

### UsrExcelReportService - ERR_HTTP2_SERVER_REFUSED_STREAM (2026-01-28)
**Error:**
```
POST https://pampabay.creatio.com/0/rest/UsrExcelReportService/Generate
net::ERR_HTTP2_SERVER_REFUSED_STREAM
```

**Meaning:** Server is refusing HTTP/2 connections to this endpoint.

**Possible Causes:**
1. Service not compiled/deployed in PROD
2. Service crashed
3. Configuration issue
4. Server overloaded

**Diagnostic Steps:**
1. Check if service exists: `https://pampabay.creatio.com/0/rest/UsrExcelReportService/`
2. Check Creatio logs in System Designer
3. Recompile the service in Configuration
4. Check if DEV works: `https://dev-pampabay.creatio.com/0/rest/UsrExcelReportService/Generate`

---

## TODO: Need to Catalog

- [ ] All UsrReportesPampa records with UsrCode/UsrURL
- [ ] All IntExcelReport records with IntName/IntEntitySchemaName
- [ ] BGCommissionView columns
- [ ] BGIWCommissionView columns
- [ ] BGSalesByItemView columns (complete)
- [ ] Parent schema BGPage_iaptpa6 full element list
- [ ] Looker report URLs and their filter requirements

---

## Quick Lookup Commands (Browser Console)

```javascript
// Get CSRF token
const csrf = document.cookie.split('; ').find(c => c.startsWith('BPMCSRF='))?.split('=')[1];

// All UsrReportesPampa
fetch("/0/odata/UsrReportesPampa?$select=Id,Name,UsrCode,UsrURL", {headers:{"BPMCSRF":csrf}}).then(r=>r.json()).then(d=>console.table(d.value));

// All IntExcelReport
fetch("/0/odata/IntExcelReport?$select=Id,IntName,IntEntitySchemaName", {headers:{"BPMCSRF":csrf}}).then(r=>r.json()).then(d=>console.table(d.value));

// BGReportExecution count
fetch("/0/odata/BGReportExecution/$count", {headers:{"BPMCSRF":csrf}}).then(r=>r.text()).then(console.log);
```
