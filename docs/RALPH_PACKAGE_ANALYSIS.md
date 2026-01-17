# RALPH Package Analysis: Comprehensive QB Sync Investigation

**Date:** 2026-01-16
**Analyst:** Claude Code (Ralph Loop)
**Scope:** Complete analysis of Creatio packages, processes, and data flows affecting QuickBooks sync

---

## Executive Summary

This comprehensive analysis maps all Creatio packages, business processes, and source code schemas involved in the QuickBooks integration and Commission reporting system. Key findings:

1. **Two primary QB integration packages** work in tandem: `PampaBayQuickBooks` (sync operations) and `IWQBIntegration` (commission calculation)
2. **24 Order-related business processes** exist across multiple packages
3. **PaymentStatusId=Planned default** in IWQBIntegration's OrderPageV2 blocks 41% of December 2025 orders from QB sync
4. **December 2025 data gap** is NOT a technical issue - invoices exist in QB but await payment processing
5. **QB connectivity** depends on external service at 96.56.203.106:8080

---

## 1. Package Inventory

### 1.1 Primary Packages

| Package Name | Package ID | Purpose | Last Modified |
|--------------|------------|---------|---------------|
| **PampaBayQuickBooks** | `f63b797a-cff7-4fdc-9c73-000676e1d209` | QB sync (Orders, Invoices, Commissions) | 2026-01-15 |
| **IWQBIntegration** | `5af0c9b0-141b-4d3f-828e-a455a1705aed` | InterWeave QB Integration, Commission calculation | 2026-01-14 |
| **IntExcelExport** | (standard) | Excel report generation library | N/A |
| **PampaBayVer2** | (custom) | Pampa Bay customizations | 2025-05-20 |
| **PampaBay** | `8b0ef6b5-915e-4739-a779-9d54505f19df` | Main Pampa Bay package | Active |

### 1.2 Order Entity Extending Packages (12 total)

1. PampaBayWooCommerce
2. PRMOrder
3. PampaBayBrandwise
4. **IWQBIntegration** (most recent modification)
5. CrtOrder (system default)
6. PampaBayQuickBooks
7. Custom
8. Order
9. IWInterWeavePaymentApp
10. PampaBay
11. CrtOCMInLeadOppMgmt
12. Passport

---

## 2. Package Dependency Map

```
                    ┌─────────────────────────────────────┐
                    │           CREATIO CORE              │
                    │  (CrtOrder, BaseEntity, Order)      │
                    └─────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
            ┌───────▼───────┐ ┌───────▼───────┐ ┌───────▼───────┐
            │  PampaBay     │ │ Passport      │ │ Order (Crt)   │
            │  (8b0ef6b5)   │ │               │ │               │
            └───────┬───────┘ └───────┬───────┘ └───────────────┘
                    │                 │
            ┌───────▼─────────────────▼───────┐
            │      PampaBayQuickBooks         │
            │      (f63b797a)                 │
            │  - BGQuickBooksService.cs       │
            │  - BGBPGetQuickBooksCommissions │
            │  - BGBPRunQBCustomerOrderInteg  │
            └───────┬─────────────────────────┘
                    │
            ┌───────▼─────────────────────────┐
            │      IWQBIntegration            │
            │      (5af0c9b0)                 │
            │  - OrderPageV2 (PaymentStatus)  │
            │  - IWCalculateCommission*       │
            │  - 24 IW-prefixed Order columns │
            └───────┬─────────────────────────┘
                    │
            ┌───────▼─────────────────────────┐
            │      IntExcelExport             │
            │  - Report generation library    │
            │  - UsrExcelReportService uses   │
            └─────────────────────────────────┘
```

---

## 3. Business Process Inventory

### 3.1 QuickBooks/Sync-Related Processes (PampaBayQuickBooks)

| Process Name | Caption | UId | Last Modified | Function |
|--------------|---------|-----|---------------|----------|
| BGBPGetQuickBooksCommissions | Get QuickBooks Commissions | 7b1ac959-1726-4340-bc66-210b31f5f365 | 2026-01-15 | Downloads ReceivePayments/CreditMemos from QB |
| BGBPRunQBCustomerOrderIntegration | Run QB Customer Order Integration | 46126f18-8e44-4ebb-9d9a-85d2bb526152 | 2024-06-12 | Syncs Orders to QB Invoices |
| BGBPRunQBFactoryOrderIntegration | Run QB Factory Order Integration | be948e0a-8922-4d70-b5ce-7521790fbb97 | 2024-06-12 | Factory order sync |
| BGBPRunQBInventoryAdjustmentIntegration | Run QB Inventory Adjustment | 2cab22f3-f8bc-4688-a23c-e09a29dbd181 | 2024-06-12 | Inventory sync |
| BGBPQBExportSchedule | Quickbooks export schedule | 367b204a-7baa-43b5-9f26-cade1bd7d30c | 2024-05-29 | Scheduled sync trigger |
| BGBPQuickBooksCustomerOrderChangedLog | Customer Order Changed Log | 46f94312-a741-4c98-96e2-5aafa3765ce1 | 2024-09-05 | Order change logging |
| BGBPQuickBooksFactoryOrderChangedLog | Factory Order Changed Log | 0eb50b55-e06d-4a23-ab5f-f613726649ab | 2024-07-02 | Factory order logging |
| BGBPMarkQuickBooksLogReProcess | Mark QB Log to Re-Process | 6dfaf8e5-a1bc-4b5e-b6db-d7fb6c6087f7 | 2023-05-11 | Retry failed syncs |
| BGQuickBooksCreateHeaderLog | QB Create Header Log | f6b0da44-d60e-468c-a290-ed615dc466eb | 2023-04-13 | Log creation |
| BGBPTestQuickBooks | Test QuickBooks | 30405e40-20b8-4592-aaff-4161f23f873a | 2023-05-05 | Connection test |
| BGBPTestQBConnection | Test QB Connection | a5935161-a2f0-42f5-8ceb-1ee4ae054c99 | 2024-06-14 | Connection test |
| BGBPTestGetCompanyQBConnection | Test Get Company QB Connection | ba92d97f-ed51-479e-ae70-7a8c619e49a9 | 2025-05-20 | Connection test |
| BGBPRunQuickBooksIntegration | Run QuickBooks Integration | 21e2fb8f-209f-417a-b3a4-d67f3b679b0d | 2023-05-08 | Master integration trigger |

### 3.2 IWQBIntegration Processes (Commission Calculation)

| Process Name | Caption | UId | Last Modified |
|--------------|---------|-----|---------------|
| IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | Set Order and Product Tax Status | b1bd0482-dd1b-427e-909b-490ab989f768 | **2026-01-14** |
| IWCalculateCommissiononPaymentIWQBIntegrationV3 | Calculate Commission on Payment V3 | 9b615e60-1124-4dc1-8d70-607fcb1a9412 | **2026-01-14** |
| BGSetOrderProductTaxStatusByOrderSalesTax | Set OrderProduct Tax Status | 15cf23a4-3e07-42da-94cc-016ac6dd6185 | 2025-10-24 |
| IWCalculateCommissiononPayment | Calculate Commission on Payment | (in package) | - |
| IWCalculateCommissiononPaymentV2 | V2 | (in package) | - |
| IWCalculateCommissiononPaymentCustomV4 | V4 (has gateway error) | (in package) | - |
| IWFillCommissionReportPaymentsFields | Fill Commission Report Payments Fields | (in package) | - |
| IWUpdateInvoicePaymentAmountPayments | Update Invoice Payment Amount | (in package) | - |
| IWUpdateInvoiceCreditedTotalandCheckbox | Update Invoice Credited Total | (in package) | - |
| IWAccountCheckForInvoices | Account Check For Invoices | (in package) | - |

### 3.3 Order-Related Processes (Other Packages)

| Process Name | Caption | Package | Last Modified |
|--------------|---------|---------|---------------|
| BGBPOrderCalculateFieldsV2 | ORDER: Calculated fields V2 | PampaBay | 2024-11-25 |
| BGBPOrderCalculateFields | ORDER: Calculated fields | PampaBay | 2024-08-02 |
| BGOrderSetMonth | Order Set Month | PampaBay | 2024-10-09 |
| BGProcessOrderInvoice | Customer Order: Invoice | PampaBay | 2024-11-08 |
| BGCopyOrderV2 | Copy Order V2 | PampaBay | 2024-12-12 |
| BGCopyOrder | BGCopyOrder | PampaBay | 2024-12-12 |
| CalculateOrderProductTotal | Calculate total in order product | CrtOrder | 2025-03-31 |
| SetTotalInOrder | Set total in order | CrtOrder | 2024-02-06 |
| CreateNewInvoiceFromOrder | Create new invoice from the order | CrtOrder | 2025-02-25 |
| OrderApprovalProcess | Order approval Freedom | CrtOrder | 2024-02-06 |

---

## 4. Source Code Schemas (C#)

### 4.1 PampaBayQuickBooks Package

| Schema Name | Purpose | Key Methods |
|-------------|---------|-------------|
| **BGQuickBooksService.cs** | Main QB integration service | `ProcessQuickBooksCommissions()`, `GetQuickBooksReceivedPayments()`, `GetQuickBooksCreditMemos()` |
| BGQuickBooksLogService | Log management | Sync logging |
| BGQuickBooksExportService | Export operations | Invoice/order export |

**Key Code Section - BGQuickBooksService.cs (lines 2053-2181):**
```csharp
// GetQuickBooksReceivedPayments - Queries QB for ReceivePayment records (NOT Invoices)
qSearch.QueryType = ObjsearchQueryTypes.qtReceivePaymentSearch;
// ...returns payments that are APPLIED to invoices

// GetQuickBooksCreditMemos - Queries QB for Credit Memo records
qSearch.QueryType = ObjsearchQueryTypes.qtCreditMemoSearch;
qSearch.SearchCriteria.PaidStatus = TPaidStatus.psPaid;
// ...returns credit memos with status = Paid
```

### 4.2 IWQBIntegration Package

| Schema Name | Purpose |
|-------------|---------|
| OrderPageV2 | Client schema - **sets PaymentStatusId=Planned as default** |
| IWPaymentsEventListener | Event handler for IWPayments entity |
| IWCommissionCalculator | Commission calculation logic |

### 4.3 Custom Schemas (PampaBayVer2)

| Schema Name | Purpose |
|-------------|---------|
| **UsrExcelReportService** | Report generation wrapper service |
| UsrPage_ebkv9e8 | Reports page client schema |

---

## 5. Entity Schemas and Views

### 5.1 Key Entities

| Entity | Package | Purpose |
|--------|---------|---------|
| Order | CrtOrder | Sales orders |
| BGCommissionReportQBDownload | PampaBayQuickBooks | QB payment data (10,020+ records) |
| BGCommissionReportDataView | PampaBayQuickBooks | PostgreSQL view for Commission report |
| IWPayments | IWQBIntegration | InterWeave payment data |
| IWCommissionReportDataView | IWQBIntegration | PostgreSQL view for IW_Commission report |
| IntExcelReport | IntExcelExport | Report template configuration |
| BGYearMonth | Custom | Year-Month lookup (filter) |
| BGSalesGroup | Custom | Sales Group lookup (filter) |
| BGReportExecution | Custom | Report execution context |

### 5.2 Database Views

**BGCommissionReportDataView** (PostgreSQL):
- JOINs: `BGCommissionReportQBDownload`, `Order`, `BGCommissionEarner`
- Filter columns: `BGInvoiceDate`, `BGSalesRep.BGSalesGroupLookup`
- Output: Commission data with resolved lookups

**IWCommissionReportDataView** (PostgreSQL):
- JOINs: `IWPayments`, `BGSalesGroup`, `Account`, `Order`
- Filter columns: `IWTransactionDate`, `IWSalesGroupId`
- Output: IW Commission data with resolved lookups

---

## 6. Data Flow Diagrams

### 6.1 Complete Order to Commission Report Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        ORDER CREATION                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  User creates Order in Creatio UI                                        │
│           │                                                              │
│           ▼                                                              │
│  IWQBIntegration.OrderPageV2                                             │
│  ┌─────────────────────────────────────┐                                 │
│  │ Sets PaymentStatusId = "Planned"    │ <-- PROBLEM: Blocks sync       │
│  │ (for non-Supervisor users)          │                                 │
│  └─────────────────────────────────────┘                                 │
│           │                                                              │
│           ▼                                                              │
│  Multiple processes trigger:                                             │
│  - IWSetOrderandProductTaxStatusByOrderSalesTaxV2                        │
│  - BGBPOrderCalculateFieldsV2                                            │
│  - BGOrderSetMonth                                                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     QB SYNC (ORDER → INVOICE)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  BGBPRunQBCustomerOrderIntegration                                       │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────────────────────────┐                                 │
│  │ Filter: PaymentStatusId != Planned  │ <-- Orders with "Planned" SKIP │
│  └─────────────────────────────────────┘                                 │
│           │                                                              │
│           ▼                                                              │
│  BGQuickBooksService.CreateOrUpdateInvoice()                             │
│           │                                                              │
│           ▼                                                              │
│  QuickBooks Desktop (96.56.203.106:8080)                                 │
│  - Invoice created                                                       │
│  - Order.BGQuickBooksId populated                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     QUICKBOOKS PROCESSING                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  [MANUAL STEP - QB Accounting Team]                                      │
│  Invoice must be marked as PAID to create ReceivePayment                 │
│           │                                                              │
│           ▼                                                              │
│  QB ReceivePayment record created (when invoice paid)                    │
│  QB CreditMemo record created (when return processed)                    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   QB COMMISSION SYNC                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  BGBPGetQuickBooksCommissions (auto or manual trigger)                   │
│           │                                                              │
│           ▼                                                              │
│  BGQuickBooksService.ProcessQuickBooksCommissions()                      │
│  - GetQuickBooksReceivedPayments() → qtReceivePaymentSearch              │
│  - GetQuickBooksCreditMemos() → qtCreditMemoSearch (psPaid)              │
│           │                                                              │
│           ▼                                                              │
│  BGCommissionReportQBDownload (table updated)                            │
│  - BGQuickBooksId, BGTransactionDate, BGAmount, BGInvoiceNumber          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   COMMISSION REPORT GENERATION                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  UsrPage_ebkv9e8 (Reports Page)                                          │
│  - User selects: Report, Year-Month, Sales Group                         │
│  - Calls UsrExcelReportService.Generate()                                │
│           │                                                              │
│           ▼                                                              │
│  UsrExcelReportService                                                   │
│  - Resolves IntExcelReport template                                      │
│  - Builds FiltersConfig (BGExecutionId for date/salesgroup)              │
│  - Calls IntExcelExport library                                          │
│           │                                                              │
│           ▼                                                              │
│  BGCommissionReportDataView (PostgreSQL view)                            │
│  - JOINs BGCommissionReportQBDownload with Order, BGCommissionEarner     │
│  - Filters: BGInvoiceDate, BGSalesRep.BGSalesGroupLookup                 │
│           │                                                              │
│           ▼                                                              │
│  Excel file (.xlsm) generated and downloaded                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 December 2025 Data Gap Visualization

```
                        Creatio Orders              QuickBooks
                        ─────────────              ───────────
Dec 2025 Orders  ────────────────────────────────►  Invoices
(ORD-15159,                                        (EXIST - have
 ORD-15299, etc.)                                   BGQuickBooksId)
      │
      │                                                  │
      │                                                  ▼
      │                                           [AWAITING
      │                                            PAYMENT]
      │                                                  │
      │                                                  ▼
      │                                            ReceivePayments
      │                                            (DON'T EXIST)
      │
      │                                                  │
      ▼                                                  ▼
BGCommissionReportQBDownload  ◄─────────────────  (NO DATA TO SYNC)
(Dec 2025: 39 CreditMemos,
 0 Sales)

RESULT: Commission report shows ONLY returns, no sales
ROOT CAUSE: QB accounting team hasn't marked Dec invoices as paid
```

---

## 7. Conflict Analysis

### 7.1 Identified Conflicts

| # | Conflict | Packages | Impact |
|---|----------|----------|--------|
| 1 | PaymentStatusId default | IWQBIntegration vs PampaBayQuickBooks | 41% of orders blocked from QB sync |
| 2 | Multiple OrderPageV2 schemas | 6 packages override | Last modifier (IWQBIntegration) wins |
| 3 | V4 Commission process gateway | IWQBIntegration | ArgumentException on parameter type |

### 7.2 Schema Override Chain (Order Page)

```
BaseOrderPage [Order] ← Base platform
      ↓
OrderPageV2 [Order] ← Platform extensions
      ↓
OrderPageV2 [Passport] ← Passport module
      ↓
OrderPageV2 [PampaBayQuickBooks] ← QB integration (2023-05-11)
      ↓
OrderPageV2 [PampaBay] ← Main customizations (2025-05-20)
      ↓
OrderPageV2 [IWQBIntegration] ← IW integration (2026-01-14) ← OVERRIDES ALL
```

### 7.3 PaymentStatusId Distribution Analysis

**December 2025 Orders:**
| PaymentStatusId | Count | Percentage | Synced to QB? |
|-----------------|-------|------------|---------------|
| NULL/Empty | 294 | 59% | YES |
| **Planned (bfe38d3d...)** | **206** | **41%** | **NO** |

**By Creator (Last 50 Orders):**
| Creator | NULL (Synced) | Planned (Not Synced) |
|---------|---------------|----------------------|
| Supervisor | 37 | 0 |
| Maria Victoria | 0 | 7 |
| Pamela Murphy | 0 | 4 |
| Krutika | 0 | 2 |

**Observation:** Supervisor orders sync correctly; other users' orders get "Planned" status from IWQBIntegration's OrderPageV2 default.

---

## 8. Recent Modifications Timeline

| Date | Package | Schema | Change |
|------|---------|--------|--------|
| **2026-01-15** | PampaBayQuickBooks | BGBPGetQuickBooksCommissions | Added AutoStartDate/AutoEndDate parameters, Phase 1 automation |
| **2026-01-14** | IWQBIntegration | OrderPageV2 | Modified (set PaymentStatusId default) |
| **2026-01-14** | IWQBIntegration | IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | Modified |
| **2026-01-14** | IWQBIntegration | IWCalculateCommissiononPaymentIWQBIntegrationV3 | Modified |
| 2025-05-20 | PampaBayQuickBooks | BGBPTestGetCompanyQBConnection | Modified |
| 2025-03-11 | PampaBayQuickBooks | Order schema | Modified |
| 2023-05-11 | PampaBayQuickBooks | OrderPageV2 | Last stable modification |

**Critical Correlation:**
- IWQBIntegration modifications on **2026-01-14**
- Commission report issues reported on **2026-01-15**
- 1-day gap strongly suggests causation

---

## 9. Known Issues Summary

| ID | Issue | Root Cause | Status | Fix |
|----|-------|------------|--------|-----|
| **DATA-001** | PaymentStatusId=Planned blocks QB sync | IWQBIntegration OrderPageV2 default | Business Decision Required | A) Remove default, B) Include in sync |
| **DATA-002** | Dec 2025 missing sales | Invoices awaiting payment in QB | QB Workflow | QB team must process payments |
| **SYNC-001** | QB sync process blocked | Required manual date input | **RESOLVED** | Phase 1 automation deployed |
| **FLT-004** | Commission view date mismatch | WHERE vs SELECT column mismatch | **RESOLVED** | Fixed SQL view |
| **FLT-002** | IW_Commission filters | Library limitation with DateTime | **RESOLVED** | Custom generator bypass |
| **PROC-001** | V4 Commission process error | Gateway condition type mismatch | Dormant | Fix when IWPayments has data |
| **ENV-001** | Template lookup in DEV | Unknown | Not Reproducible | Monitor |

---

## 10. Recommendations

### 10.1 Immediate Actions

1. **Decision Required: DATA-001**
   - Meet with business stakeholders to decide if "Planned" orders should sync to QB
   - Options: Remove default, include in sync, or keep current behavior (intentional workflow)

2. **Verify DATA-002 Resolution**
   - Confirm with QB accounting team that Dec 2025 invoices have been paid
   - Monitor next commission sync for Dec 2025 sales data

### 10.2 Short-Term Improvements

1. **Complete QB Sync Automation (Phase 2)**
   - Replace 30-day window with dynamic ESQ query
   - Query `MAX(CreatedOn)` from BGCommissionReportQBDownload
   - Guide: `docs/QB_SYNC_AUTOMATION.md`

2. **Add Monitoring**
   - Create dashboard for QB sync status
   - Alert when sync fails or has no data

### 10.3 Long-Term Architecture

1. **Consolidate OrderPageV2 Schemas**
   - Too many packages overriding same schema (6+)
   - Creates maintenance nightmare
   - Recommend single "OrderPageExtensions" package

2. **Document Package Dependencies**
   - Create official dependency map
   - Prevent accidental conflicts

3. **Fix V4 Commission Process**
   - When IWPayments starts receiving data
   - Gateway condition expects numeric, receives incompatible type

---

## 11. File References

| Purpose | Path |
|---------|------|
| QB Integration Service | `/home/magown/creatio-report-fix/BGQuickBooksService.cs` |
| Report Service | `/home/magown/creatio-report-fix/source-code/UsrExcelReportService_Updated.cs` |
| Reports Page Handler | `/home/magown/creatio-report-fix/client-module/UsrPage_ebkv9e8_Hybrid.js` |
| Process Metadata | `/home/magown/creatio-report-fix/BGBPGetQuickBooksCommissions.metadata` |
| Package Comparison | `/home/magown/creatio-report-fix/docs/PACKAGE_COMPARISON.md` |
| Payment Status Investigation | `/home/magown/creatio-report-fix/docs/INVESTIGATION_PAYMENT_STATUS.md` |
| QB Sync Automation Guide | `/home/magown/creatio-report-fix/docs/QB_SYNC_AUTOMATION.md` |
| Test Log | `/home/magown/creatio-report-fix/docs/TEST_LOG.md` |

---

## 12. Appendix: Package UIds Quick Reference

```
PampaBayQuickBooks:        f63b797a-cff7-4fdc-9c73-000676e1d209
IWQBIntegration:           5af0c9b0-141b-4d3f-828e-a455a1705aed
PampaBay:                  8b0ef6b5-915e-4739-a779-9d54505f19df
CrtOrder:                  faa74024-7a36-4e60-b36a-86c6192eb452
Passport:                  (varies)
CrtLandingPageAnalytics:   969b67c3-c386-4546-aa67-5bb643aaff3e
Exchange:                  83b14f73-99f2-443e-963e-8258176a86dd
LDAP:                      e5764112-2fcf-43ec-9949-28285e9beaf5
Campaigns:                 a4f9ce9c-dc4a-4c14-aeb3-cf1edf857562

Planned PaymentStatusId:   bfe38d3d-bd57-48d7-a2d7-82435cd274ca
```

---

**Report Generated:** 2026-01-16
**Analysis Method:** Ralph Loop comprehensive investigation
**Data Sources:** Codebase files, investigation scripts, Creatio API queries
