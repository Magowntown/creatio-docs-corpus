# PROD Package Audit - Report-Related Functionality

**Generated:** 2026-01-23
**Last Updated:** 2026-01-23 (v2 - Business Rule Investigation Complete)
**Environment:** pampabay.creatio.com (PROD)
**Scan Scope:** 13 packages (9 primary + 4 additional)

---

## Executive Summary

This audit documents all report-related schemas, services, and dependencies across PROD Creatio packages. The reports system uses a hybrid approach:
1. **Looker Studio** - External dashboards opened in new tabs
2. **Excel Reports** - Generated via `UsrExcelReportService` backend with VBA templates

### Key Findings

| Category | Count | Notes |
|----------|-------|-------|
| Report Definitions (UsrReportesPampa) | 18 | 10 Looker, 8 Excel |
| Excel Templates (IntExcelReport) | 33 | Including "Rpt" prefixed |
| Report Views (Entity Schemas) | 25+ | SQL-backed views |
| Commission-related Schemas | 7 | Critical for commission reports |
| Business Rules (AddonSchemaManager) | **1** | ✅ NO duplicate conflict |
| Business Processes | 10+ | Commission/QB sync related |

### ✅ CRITICAL FINDING: No Business Rule Conflict

**Investigated:** 2026-01-23 via `scripts/investigation/fetch_business_rule_v2.py`

| UId | Description | Status |
|-----|-------------|--------|
| `60ed3410-ca3e-4423-9cf5-8cc0ccc616b2` | BGApp_eykaguu (Original) | ✅ EXISTS |
| `e42d1bec-59a1-46d1-968b-8efd41a0afe6` | Custom (Documented duplicate) | ❌ NOT FOUND |

**Conclusion:** Only ONE `BGUsrPage_ebkv9e8BusinessRule` exists in PROD (in BGApp_eykaguu).
The previously documented duplicate in Custom package **does not exist**.
**v19 deployment can proceed without business rule conflict risk.**

---

## Package Analysis

### 1. Custom

**Status:** Minimal report involvement | **Package ID:** `af2b71ef-e323-410f-9017-8059bfda38c8`

#### Entity Schemas
| Schema | Caption | Modified |
|--------|---------|----------|
| UsrReportesPampa | Reportes Pampa | 2024-01-15 |

**Dependencies:** Extends UsrReportesPampa entity.

#### ✅ Business Rule Investigation (2026-01-23)

**Result: NO SCHEMAS FOUND IN CUSTOM PACKAGE**

The previously documented duplicate `BGUsrPage_ebkv9e8BusinessRule` (UId: `e42d1bec-59a1-46d1-968b-8efd41a0afe6`)
**does not exist** in the Custom package. The package contains no SysSchema records.

This was verified via OData query:
```
SysSchema?$filter=SysPackageId eq af2b71ef-e323-410f-9017-8059bfda38c8
→ No results returned
```

---

### 2. BGApp_eykaguu

**Status:** PRIMARY REPORT PACKAGE - Contains main frontend handler and backend service

#### Client Schemas
| Schema | Caption | Modified | Notes |
|--------|---------|----------|-------|
| `UsrPage_ebkv9e8` | New edit page | 2026-01-23 00:37 | **MAIN HANDLER - ExtendParent=true** |
| BGPage_iaptpa6 | Rpt Excel | 2023-09-19 | Legacy page |

#### Source Code Schemas
| Schema | Caption | Modified | Notes |
|--------|---------|----------|-------|
| `UsrExcelReportService` | UsrExcelReportService | 2026-01-20 11:48 | **MAIN BACKEND SERVICE** |

#### Entity Schemas
| Schema | Caption | Modified |
|--------|---------|----------|
| UsrEntity_e7ac661 | Entity_e7ac661 | 2025-07-14 |

**Key URLs:**
- Frontend: `/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972`
- Backend: `/0/ClientApp/#/SourceCodeSchemaDesigner/9ca2c720-734e-46f0-9944-3c139b57f810`

---

### 3. BGlobalLookerStudio

**Status:** BASE PACKAGE for Looker/Reports page

#### Client Schemas
| Schema | Caption | Modified | Notes |
|--------|---------|----------|-------|
| `UsrPage_ebkv9e8` | New edit page | 2026-01-22 13:18 | **BASE HANDLER - ExtendParent=false** |
| UsrIframe | iframe | 2023-10-23 | Iframe component |
| UsrTest_ListPage | Test list page | 2023-08-08 | |
| UsrTest_Detail | Test detail | 2023-08-08 | |
| UsrTest_FormPage | Test form page | 2023-08-08 | |

#### Entity Schemas
| Schema | Caption | Modified |
|--------|---------|----------|
| UsrReportesPampa | Reportes Pampa | 2023-10-03 |
| UsrStatus | Order Status Pampa | 2024-11-19 |
| UsrEntity_e7ac661 | Entity_e7ac661 | 2023-08-08 |

**Notes:**
- Contains base UsrPage_ebkv9e8 which BGApp_eykaguu extends
- UsrIframe component for embedded content

---

### 4. BpmonlineCloudIntegration

**Status:** No report-related schemas (email/cloud services only)

---

### 5. PampaBay

**Status:** CORE BUSINESS LOGIC - Contains Excel mixin and report views

#### Client Schemas (Report-Related)
| Schema | Caption | Modified | Notes |
|--------|---------|----------|-------|
| `BGIntExcelreportMixin` | BG Excel Report | 2026-01-14 20:38 | **Excel report mixin** |
| BGSchema7018f847Page | Commission Earners | 2024-03-14 | |

#### Source Code Schemas
| Schema | Caption | Modified | Notes |
|--------|---------|----------|-------|
| `BGIntExcelReportService2` | IntExcelReportService2 | 2026-01-20 11:10 | **Alternative Excel service** |
| BGIntegrationHelper | BGIntegrationHelper | 2025-01-14 | |
| BGMoneyConverter | Money Converter | 2024-06-10 | |

#### SQL Scripts (Report Views)
| Script | Modified | Purpose |
|--------|----------|---------|
| BGPostgreSql_CustomerDidNotBuyView | 2025-08-06 | Customer analysis |
| SQLBGItemsByCustomerView | 2025-07-17 | Items by customer |
| VwBGSalesByItemLineView | 2024-11-20 | Sales by item line |
| VwBGVWReportSalesRepMonthly | 2024-06-10 | Monthly sales rep |
| BGPostgreSql_sp_bgprocessstockcalculation | 2025-02-04 | Stock calculation |
| BGTopSalesProductBySalesRepView | 2024-09-12 | Top products |
| VwBGCatalogView | 2024-06-10 | Catalog view |
| VwBGSalesByLineWithRankingView | 2025-01-08 | Sales ranking |
| BGVwProductQuantityByOrderView | 2024-12-19 | Product quantity |
| BGPostgreSql_SalesRepMonthlyReport | 2024-11-28 | Monthly report |
| BGPostgreSql_SalesByCustomerPrevYearComparisonView | 2024-11-21 | Year comparison |
| VwBGSalesByCustomerYearComparisonView | 2024-07-22 | Year comparison |
| VwBGSalesByCustomerTypeView | 2024-11-12 | Customer type |
| VwBGSalesByCustomerView | 2024-11-12 | Sales by customer |
| BGPostgreSQL_BGMonthlyNewAndRepeatCustomerOrderView | 2024-11-01 | New/repeat customers |
| BGVwTopSoldProducts | 2024-09-17 | Top products |
| BGVwTopSalesReps | 2024-09-16 | Top sales reps |
| VwBGSalesByItemView | 2024-08-26 | Sales by item |
| VwBGSalesByLineByTypeOfCustomerView | 2024-07-22 | Sales by type |
| VwBGSalesByItemByTypeOfCustomerView | 2024-07-22 | Sales by type |
| BGSQLViewBGCommissionSalesGroupByYearMonth | 2024-06-19 | Commission by month |
| VwBGSalesBySalesGroupView | 2024-06-13 | Sales group |
| VwBGSalesBySalesRepView | 2024-06-10 | Sales rep |
| VwBGVWReportSalesByLineWithRanking | 2024-06-10 | Line ranking |
| VwBGSalesByItemThemeView | 2024-06-10 | Theme view |
| VwBGVWReportCustomersDidNotBuy | 2024-06-10 | Customer retention |

#### Entity Schemas (Report-Related)
| Schema | Caption | Modified |
|--------|---------|----------|
| BGSalesByCustomerYearComparisonView | Year Comparison | 2023-08-08 |
| BGSalesByCustomerPrevYearComparisonView | Prev Year Comparison | 2024-11-20 |
| BGItemsByCustomerView | Items by Customer | 2025-07-04 |
| BGSalesByLineWithRankingView | Sales Ranking | 2024-08-23 |
| BGCommissionSalesGroupByYearMonth | Commission by Month | 2024-06-19 |
| BGCommissionEarner | Commission Earners | 2024-06-05 |
| BGCustomerDidNotBuyView | Customer Retention | 2024-11-14 |
| BGSalesByItemView | Sales by Item | 2023-08-07 |
| BGSalesRepMonthlyReportView | Monthly Report | 2024-11-28 |
| BGMonthlyNewAndRepeatCustomerOrderView | New/Repeat | 2024-11-01 |
| BGSalesByCustomerView | Sales by Customer | 2023-10-11 |
| BGCatalogView | Catalog | 2023-04-20 |
| BGVwProductQuantityByOrder | Product Qty | 2024-12-18 |
| BGReportDateFilterLookup | Date Filter | 2023-06-21 |
| BGVWReportSalesByLineWithRanking | Line Ranking | 2023-08-10 |
| BGSalesByItemLineView | Item Line | 2024-11-11 |
| BGSalesByItemThemeView | Item Theme | 2023-08-08 |
| BGSalesByItemByTypeOfCustomerView | Item by Type | 2023-08-08 |
| BGSalesByLineByTypeOfCustomerView | Line by Type | 2023-08-08 |
| BGSalesBySalesGroupView | Sales Group | 2023-10-11 |
| BGReportExecution | Report Execution | 2025-06-27 |
| BGSalesBySalesRepView | Sales Rep | 2023-08-07 |
| BGVWCommissionsReport | Commissions | 2023-08-11 |
| BGYearMonth | Year-Month | 2023-10-05 |
| BGVWReportSalesRepMonthly | Monthly | 2023-08-10 |
| BGVWReportCustomersDidNotBuy | Customer Retention | 2023-08-10 |

---

### 6. PampaBay2025

**Status:** Product page extensions (no report schemas)

---

### 7. PampaBayBrandwise

**Status:** Brandwise integration (no direct report schemas)

#### Source Code Schemas
| Schema | Caption | Modified |
|--------|---------|----------|
| BGHelpersBrandwise | Helpers | 2025-05-20 |
| BGBrandwiseWebService | Web Service | 2025-05-20 |

---

### 8. PampaBayQuickBooks

**Status:** COMMISSION DATA SOURCE - Contains commission views and QB integration

#### Client Schemas
| Schema | Caption | Modified |
|--------|---------|----------|
| BGQuickBooksIntegrationLog1Page | QB Log Page | 2023-12-29 |
| BGQuickBooksIntegrationLogd437c30bSection | QB Log Section | 2024-03-22 |
| BGSchemaa889e615Detail | QB Log Detail | 2023-04-12 |

#### Source Code Schemas
| Schema | Caption | Modified |
|--------|---------|----------|
| `BGQuickBooksService` | QuickBooks Service | 2025-11-25 |

#### SQL Scripts
| Script | Modified | Purpose |
|--------|----------|---------|
| BGSQLFunctionShipmentTotalAmount | 2023-02-28 | Shipment totals |
| `BGSQLViewBGCommissionReportDataView` | 2024-06-19 | **COMMISSION DATA VIEW** |

#### Entity Schemas (Critical for Commission)
| Schema | Caption | Modified | Notes |
|--------|---------|----------|-------|
| `BGCommissionReportDataView` | Commission Report Data | 2023-10-06 | **MAIN COMMISSION VIEW** |
| BGCommissionReportNotes | Commission Notes | 2023-02-15 | |
| BGCommissionReportQBDownload | QB Download | 2023-03-02 | |
| BGQuickBooksIntegrationLog | QB Log | 2023-03-31 | |
| BGQuickBooksIntegrationLogDetail | QB Log Detail | 2023-12-14 | |
| BGQuickBooksTransactionType | Transaction Type | 2023-02-15 | |

---

### 9. PampaBayWooCommerce

**Status:** WooCommerce integration (no report schemas)

---

## Report Configuration

### UsrReportesPampa (Report Definitions)

| Report Name | Type | URL/Code | IntExcelReport Template |
|-------------|------|----------|------------------------|
| Commission | Excel | Code: Commission | Rpt Commission |
| Customers did not buy over a period of time | Excel | Code: CustomersDidNotBuyOverAPeriodOfTime | Rpt CustomersDidNotBuyOverAPeriodOfTime |
| Items by Customer | Excel | Code: ItemsByCustomer | Items by Customer |
| Sales By Customer | Looker | lookerstudio.google.com/...3b2a38a0... | - |
| Sales By Customer Type | Looker | lookerstudio.google.com/...adac9cc3... | - |
| Sales by Customer Year Comparison | Looker | lookerstudio.google.com/...f69c61bd... | - |
| Sales By Item (Excel) | Excel | Code: SalesByItem | Rpt Sales By Item |
| Sales By Item (Looker) | Looker | lookerstudio.google.com/...f09fd56f... | - |
| Sales By Item By Type Of Customer (Excel) | Excel | Code: SalesByItemByTypeOfCustomer | Rpt Sales By Item By Type Of Customer |
| Sales By Item By Type Of Customer (Looker) | Looker | lookerstudio.google.com/...c2677979... | - |
| Sales By Item Line | Looker | lookerstudio.google.com/...7d4e9963... | Rpt Sales by Item Line |
| Sales By Item Theme | Looker | lookerstudio.google.com/...5dcfe2b9... | - |
| Sales By Line | Excel | Code: SalesByLine | Rpt Sales By Line |
| Sales By Line By Type Of Customer | Looker | lookerstudio.google.com/...3e3d070c... | - |
| Sales By Line With Ranking | Looker | lookerstudio.google.com/...3d7224c6... | Rpt Sales By Line With Ranking |
| Sales By Sales Group | Looker | lookerstudio.google.com/...50e808d8... | Rpt Sales By Sales Group |
| Sales By Sales Rep | Looker | lookerstudio.google.com/...6ff774af... | Rpt Sales By Sales Rep |
| Sales Rep Monthly Report | Looker | lookerstudio.google.com/...6a6bea54... | Rpt Sales Rep Monthly Report |

### IntExcelReport (Excel Templates)

| Template Name | ID | Root Schema |
|--------------|-----|-------------|
| Rpt Commission | 4ba4f203-7088-41dc-b86d-130c590b3594 | BGCommissionReportDataView |
| Rpt CustomersDidNotBuyOverAPeriodOfTime | 1f65a56a-d7f4-4ce2-b517-c633872ea545 | - |
| Rpt Sales By Customer | 62d81c91-13d2-4edf-9827-1f9e35ce03d9 | - |
| Rpt Sales By Customer (Collapsed) | ddb6bfa4-2c58-44b9-814d-91ee0c02c989 | - |
| Rpt Sales By Customer Type | 6e11dc16-df10-47c4-97be-9695f3feb77a | - |
| Rpt Sales by Customer Type (Collapsed) | 7592aced-1315-4475-bd13-da12e6c5750b | - |
| Rpt Sales by Customer Year Comparison | f7e2a69d-8a3e-4f1e-ba8a-d0cd8b3b1a53 | - |
| Rpt Sales By Customer Year Comparison (Collapsed) | f336165b-f6b7-4a55-bcf1-3f24bae73d26 | - |
| Rpt Sales By Item | c4f4e32c-376d-4b19-b04b-2129dba29d06 | - |
| Rpt Sales By Item By Type Of Customer | 53682214-a63c-407a-b3f1-79d8ab235f18 | - |
| Rpt Sales by Item Line | 1d009377-3cef-4199-9e38-7b47ddb27a0d | - |
| Rpt Sales By Line | 0b40d51d-4935-4918-97f2-45352aed341f | - |
| Rpt Sales By Line With Ranking | 384bf7f6-28fa-4f65-bd64-1a45d96a09e8 | - |
| Rpt Sales By Line With Ranking (Collapsed) | ba330b02-630e-4f5e-8d60-3e7c0560aa5b | - |
| Rpt Sales By Sales Group | a935a791-e2ff-4693-9b50-38a8596a3667 | - |
| Rpt Sales by Sales Group (Collapsed) | 6e9d462b-99ef-4e6c-9c7c-f425721be455 | - |
| Rpt Sales By Sales Rep | 50b59be9-1fab-449a-a257-11dce5ec1434 | - |
| Rpt Sales by Sales Rep (Collapsed) | 41afd5e9-7043-4bb8-a52f-0f927bc3505f | - |
| Rpt Sales Rep Monthly Report | 5b39f08f-3b55-4963-b74d-eddfb540bdba | - |
| Items by Customer | d213933b-093d-47fc-8da8-422c0d9bf715 | - |

**Note:** No IW_Commission template found in PROD.

---

## URL Building Logic

### Frontend Handler (UsrPage_ebkv9e8 v18)

```javascript
// Report Metadata Lookup
const metaUrl = "/0/odata/UsrReportesPampa(" + selectedReport.value + ")?$select=UsrURL,UsrCode";

// IntExcelReport Template Lookup
const odataUrl = "/0/odata/IntExcelReport?$filter=" +
    "(IntName eq '" + reportDisplayName + "' or IntName eq 'Rpt " + reportDisplayName + "'..." +
    "&$select=Id,IntName&$top=1";

// Excel Generation
const response = await fetch("/0/rest/UsrExcelReportService/Generate", {...});

// Excel Download
var downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" + result.key + "/" + encodeURIComponent(reportDisplayName);

// Looker Studio (if UsrURL populated)
window.open(reportUrl, "_blank");
```

### Backend Service (UsrExcelReportService)

```
POST /0/rest/UsrExcelReportService/Generate
  Body: { ReportId, YearMonthId, SalesRepId }

GET /0/rest/UsrExcelReportService/GetReport/{key}/{filename}
```

---

## Filter Handling Logic

### Commission Reports

| Filter | Attribute | Source |
|--------|-----------|--------|
| Year-Month | UsrYearMonth | BGYearMonth lookup |
| Sales Group | UsrSalesGroup (via SalesRepId) | BGSalesGroup lookup |

### Non-Commission Reports

| Filter | Container | Visibility |
|--------|-----------|------------|
| Date Range | GridContainer_xdy25v1 | UsrShowDateStatusFilters |
| Status | GridContainer_knkow5v | UsrShowDateStatusFilters |

### Visibility Logic

```
if (Looker URL exists) -> Hide all filters
else if (Commission report) -> Show Commission filters only
else -> Show Date+Status filters
```

---

## Cross-Package Dependencies

```
UsrPage_ebkv9e8 (BGApp_eykaguu) extends UsrPage_ebkv9e8 (BGlobalLookerStudio)
                    |
                    v
        UsrExcelReportService (BGApp_eykaguu)
                    |
                    v
        IntExcelReport templates -> BGCommissionReportDataView (PampaBayQuickBooks)
                                 -> Other report views (PampaBay)
```

### Package Load Order

1. BGlobalLookerStudio (base)
2. PampaBay (views, mixin)
3. PampaBayQuickBooks (commission data)
4. BGApp_eykaguu (frontend override, backend service)

---

## Issues Identified

### IW-001: IW_Commission Missing from PROD

**Finding:** No `IW_Commission` or `IW` related templates exist in PROD IntExcelReport.
**Impact:** IW_Commission column alignment issue may be DEV-only.
**Action:** Verify if IW_Commission is needed in PROD or if it's a DEV-specific feature.

### No IWQBIntegration Package

**Finding:** No package containing "IW" exists in PROD.
**Impact:** Confirms IWQBIntegration is DEV-only.

### Duplicate Report Names

**Finding:** "Sales By Item" and "Sales By Item By Type Of Customer" appear twice (Excel + Looker versions).
**Impact:** Frontend handler correctly distinguishes by checking UsrURL.

---

## Schema UIds Reference

| Schema | UId | Package |
|--------|-----|---------|
| UsrPage_ebkv9e8 (BGApp) | 561d9dd4-8bf2-4f63-a781-54ac48a74972 | BGApp_eykaguu |
| UsrPage_ebkv9e8 (BGlobal) | 4e6a5aa6-86b7-48c1-9147-7b09e96ee59e | BGlobalLookerStudio |
| UsrExcelReportService | 9ca2c720-734e-46f0-9944-3c139b57f810 | BGApp_eykaguu |
| BGIntExcelreportMixin | a589d29b-9da7-4f66-836b-8e39fe0ca376 | PampaBay |
| UsrIframe | 83116bac-139b-458f-8879-23b69c89b298 | BGlobalLookerStudio |
| BGPage_iaptpa6 | 4c777639-49df-4569-bd4e-adb72ce0ff56 | BGApp_eykaguu |

---

## Recommendations

1. **Verify IW_Commission Need** - Confirm if IW_Commission template is needed in PROD
2. **Template Naming Convention** - All Excel templates should follow "Rpt {ReportName}" pattern
3. **Commission Data Pipeline** - BGCommissionReportDataView is the critical view for commission reports
4. **Handler Consolidation** - Consider merging BGIntExcelReportService2 with UsrExcelReportService

---

*End of Audit*
