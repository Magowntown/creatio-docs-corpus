# Shared Understanding - Creatio Reports & QB Integration

**Purpose:** Single comprehensive reference capturing our complete understanding of the system.
**Created:** 2026-02-01
**For:** AI assistants and team members picking up this project

---

## Quick Context

This project fixes Creatio (Bpmonline) Excel reports for PampaBay and prepares QuickBooks integration for go-live.

**Current State:**
- Reports work: ✅ COMPLETE (handed off to BGlobal for v8 rework)
- QB Integration: ✅ READY (pending go-live confirmation)

---

## 1. System Architecture

### Creatio Platform Overview

Creatio is a low-code CRM/BPM platform with:
- **Freedom UI** (v8+): New React-based frontend with schemas
- **Classic UI** (v7): Older ExtJS-based frontend
- **ORM/ESQ**: EntitySchemaQuery for database access
- **Packages**: Deployable units containing schemas, processes, views
- **WCF Services**: REST API endpoints

### BGlobal V7 Architecture (Critical Understanding)

BGlobal (the original implementer) designed **two distinct report patterns**:

#### Type A: Execution-Based Pattern

```
USER SELECTS FILTERS
        ↓
CREATE BGReportExecution RECORD
{
  Id: "exec-guid",
  BGCreatedFrom: 2026-01-01,
  BGCreatedTo: 2026-01-31
}
        ↓
SQL VIEW (with Cartesian JOIN)
SELECT ... FROM Account a
JOIN BGReportExecution re ON true  ← Cartesian product
WHERE NOT EXISTS (orders in date range)
        ↓
ESQ QUERY: WHERE BGExecutionId = 'exec-guid'
```

**Used by:** Commission, Customers Did Not Buy, Sales by Sales Group

**Key Insight:** The view only outputs foreign key IDs (e.g., `BGAccountId`). Customer details (Name, Address, City) must come via **ESQ relationship columns**:
```csharp
esq.AddColumn("BGAccount.Name");        // Joins to Account table
esq.AddColumn("BGAccount.City.Name");   // Joins to City lookup
```

#### Type B: Direct Pattern

```
USER SELECTS FILTERS
        ↓
DIRECT ESQ QUERY WITH FILTERS
esq.AddFilter("BGCustomer", Contains, "CustomerName")
esq.AddFilter("CreatedOn", GreaterOrEqual, startDate)
        ↓
RETURNS DATA DIRECTLY
```

**Used by:** Items by Customer, Sales by Item

**Key Insight:** All columns are directly available in the view. No execution record needed.

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND (v54 Handler)                                          │
│   - UsrPage_ebkv9e8                                             │
│   - Routes by IntName (report name)                             │
│   - Detects Looker vs Excel via UsrURL                          │
└───────────────────────────┬─────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND (UsrExcelReportService)                                 │
│   - 14 custom report generators                                 │
│   - Type A: CreateReportExecution() → Query by BGExecutionId    │
│   - Type B: Direct ESQ with filters                             │
│   - Populates Excel template                                    │
└───────────────────────────┬─────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ SQL VIEWS (12 defined)                                          │
│   - BGCustomerDidNotBuyView (Type A)                            │
│   - BGSalesByItemView (Type B)                                  │
│   - BGCommissionReportDataView (Type A)                         │
│   - IWCommissionReportDataView (Type B)                         │
└───────────────────────────┬─────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ EXCEL OUTPUT                                                    │
│   - Template from IntExcelReport.IntFile                        │
│   - Data populated to "Data" sheet                              │
│   - VBA macros process data → "Rpt" sheet                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Key Entities & Tables

### Report Configuration

| Entity | Purpose | Key Columns |
|--------|---------|-------------|
| **UsrReportesPampa** | Report dropdown menu | Name, UsrCode, UsrURL |
| **IntExcelReport** | Template definitions | IntName, IntEsq, IntFile |
| **BGReportExecution** | Filter storage (Type A) | BGCreatedFrom/To, BGYearMonthId, BGSalesGroupId |

### Filter Lookups

| Entity | Purpose |
|--------|---------|
| BGYearMonth | Year-month periods (Commission) |
| BGSalesGroup | Sales groups |
| Account | Customers |
| UsrStatus | Order statuses |

### QB Integration

| Entity | Purpose |
|--------|---------|
| BGQuickBooksIntegrationLogDetail | Sync status tracking |
| IWPayments | Payment records |
| IWCommissionReportDataView | Commission data |
| Order (extended) | 20 IW columns for payment/PCI |

---

## 3. Current Code Assets

### Backend Service

**File:** `source-code/UsrExcelReportService_Updated.cs`
**Size:** 4,387 lines
**Key Methods:**

| Method | Purpose |
|--------|---------|
| `Generate()` | Main entry point - routes to appropriate generator |
| `CreateReportExecution()` | Creates BGReportExecution for Type A |
| `QueryCustomerDidNotBuyData()` | ESQ with relationship columns |
| `GenerateSalesByItemWithFilters()` | Items by Customer generator |
| `GenerateIWCommissionWithDateFilter()` | Commission with date parsing |
| `PopulateExcelTemplate()` | Fills template with data |
| `GetReport()` | Download endpoint |

**Routing Logic (Critical):**
```
1. Get report name from IntExcelReport.IntName
2. Route by NAME first (not entity schema!)
3. Check for specific report handlers
4. Fall back to IntExcelExport library
```

### Frontend Handler

**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js`
**Size:** 858 lines
**Key Functions:**

| Function | Purpose |
|----------|---------|
| `getBpmcsrf()` | Extract CSRF token from cookies |
| `toWcfDate()` | Convert JS Date to WCF format `/Date(ms)/` |
| `setUsrIframeUrl()` | Set Looker iframe URL |
| `buildLookerParams()` | Build Looker filter parameters |

**Key Handlers:**

| Handler | Trigger | Purpose |
|---------|---------|---------|
| `crt.HandleViewModelInitRequest` | Page load | Reset state |
| `LookupAttribute_0as4io2` change | Report selected | Show/hide filters, detect Looker |
| `usr.OpenCustomerLookup` | Button click | Open Account lookup dialog |
| `usr.GenerateReportRequest` | Generate clicked | Route to Looker or Excel |

### VBA Macros

**File:** `vba/PMPSalesbySalesRep_FIXED_v2.bas`
**Fix:** Anchor variable reset pattern

**Problem:** BGlobal's nested While loops reset anchor inside loop → infinite loop
**Solution:** Reset anchor BEFORE the While, not inside

---

## 4. Packages (7 Total)

| Package | Size | Purpose |
|---------|------|---------|
| **PampaBay** | 2.2MB | Main app, SQL views, BGReportExecution |
| **IWQBIntegration** | 617KB | QB sync, commission, 31 entities |
| **IntExcelExport** | 636KB | Excel generation library |
| **BGApp_eykaguu** | 202KB | Frontend handler |
| **BGlobalLookerStudio** | 62KB | Looker iframe (UsrIframe) |
| **BpmonlineCloudIntegration** | 84KB | Platform SDK |
| **Custom** | 78KB | Misc customizations |

### IWQBIntegration (Critical for Go-Live)

**Configuration Required:**

| Setting | Value | Why |
|---------|-------|-----|
| `IWEnableCommissionV3` | **false** | Prevents 26x cascade bug |
| `IWEnableCommissionV4` | **false** | Disable experimental |
| Commission Process | **V2 only** | Tested, stable |
| Tax Process | **V2 only** | Avoid duplication |

**Risks Documented:**
1. Multiple commission versions active → duplicate calculations
2. V3 StartSignal4 triggers on ANY Order change → 26x cascade
3. Tax process duplication (V1 + V2)
4. Invoice field race condition (3 processes)
5. PCI-sensitive data in Order columns

---

## 5. Issues Resolved

### Reports (COMPLETE)

| ID | Issue | Fix |
|----|-------|-----|
| RPT-009 | VBA infinite loop | Anchor reset before While |
| RPT-010 | Wrong columns showing | Route by name first |
| RPT-005 | Customer columns missing | ESQ relationship columns |
| RPT-006/007/008 | Items by Customer | SQL JOIN fix, BGProductDescription |
| UI-007 | Customer ID flat object | v54 extraction fix |

### QB Sync

| ID | Issue | Status |
|----|-------|--------|
| SYNC-004 | QB Web Connector offline | ✅ Resolved |
| SYNC-005 | 637 false "Processed" | Pending reset |
| SYNC-003 | 20K batch limit (DEV) | Low priority |

---

## 6. Critical Lessons Learned

### Must Follow

1. **Route by report name FIRST** - `IntEsq.rootSchemaName` can be wrong (legacy data)
2. **WCF date format required** - Backend expects `/Date(milliseconds)/` not ISO 8601
3. **UsrIframe (not crt.IFrame)** - For Looker embedding
4. **Customer MUST be LOOKUP** - User rejected text input
5. **One data source per page** - Freedom UI limitation
6. **VBA anchor reset BEFORE loop** - Prevents infinite loop
7. **ESQ relationship columns** - For Type A view FK data access

### Never Do

1. Never edit Freedom UI schemas directly in system designer (strips helper functions)
2. Never use embeddedModel with large entities like Account (causes infinite loading)
3. Never assume IntEsq columns match actual view columns
4. Never use ComboBox for programmatic population (use Button + Dialog)

---

## 7. Deploy Locations

### Backend

**File:** `source-code/UsrExcelReportService_Updated.cs`
**URL:** https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178

### Frontend

**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js`
**URL:** https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2

### Test Commands

```bash
# API tests
source .env && python3 scripts/testing/test_report_service.py

# Specific report
source .env && CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py
```

---

## 8. Current Focus

### QB Integration Go-Live

| Task | Priority | Status |
|------|----------|--------|
| Confirm QB Web Connector stable (24-48h) | HIGH | Monitoring |
| SYNC-005: Reset 637 false-processed | LOW | After stability |
| Set go-live date with Carlos | PENDING | After confirmation |
| IWQBIntegration PROD import | PENDING | After go-live decision |

### Reports (Handed Off)

All reports work has been handed off to BGlobal/Rommel for v8 rework.

---

## 9. Navigation Guide

| Need | Document |
|------|----------|
| Current status | `CLAUDE.md` |
| Find docs by scenario | `docs/AI_NAVIGATION.md` |
| Complete doc listing | `docs/DOCUMENT_INDEX.md` |
| V7 architecture | `docs/investigation/BGLOBAL_V7_ARCHITECTURE_COMPLETE.md` |
| All reports/views | `docs/reference/MASTER_CATALOG.md` |
| IWQBIntegration | `docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md` |
| Handler versions | `docs/reference/HANDLER_VERSION_HISTORY.md` |
| Session history | `docs/logs/SESSION_LOG_20260201.md` (latest) |

---

## 10. Status GUIDs Reference

### QB Integration Log Status

| Status | GUID |
|--------|------|
| Pending | `c97db3bc-634d-4c90-8432-ec7141c87640` |
| Processed | `e7428193-4cf1-4d1b-abae-00e93ab5e1c5` |
| Error | `bdfc60c7-55fd-4cbd-9a2c-dca2def46d80` |
| Processing | `fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef` |
| Re-Process | `ff92e20c-da27-4255-96bc-57e32f0944f4` |

### Order Types

| Type | GUID |
|------|------|
| Customer Order | `154d3407-9d8c-49c2-84cd-e85afeb8d55a` |
| Factory Order | (different GUID) |

### Account Types

| Type | GUID |
|------|------|
| Customer | `03a75490-53e6-df11-971b-001d60e938c6` |

---

*Shared Understanding - Created 2026-02-01*
*This document captures our complete collective knowledge of the system.*
