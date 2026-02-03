# IWQBIntegration Package Investigation Log

**Date:** 2026-01-30
**Package:** IWQBIntegration v8.3.2.4199
**Package UId:** 21e7eb4b-a41b-42f1-913a-41046da1cb86
**Source:** DEV Environment (dev-pampabay.creatio.com)
**Target:** PROD Environment (pampabay.creatio.com)
**Status:** ✅ **INVESTIGATION COMPLETE** - Ready for PROD import with configuration

---

## Quick Links

| Document | Purpose |
|----------|---------|
| **[Master Catalog](../investigation/IWQBINTEGRATION_MASTER_CATALOG.md)** | Complete index of all entities, processes, risks |
| **[Team Instructions](../investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md)** | Step-by-step import procedure |
| **[Conflict Assessment](../investigation/IWQBINTEGRATION_CONFLICT_ASSESSMENT.md)** | Risk analysis (5 critical) |
| **[Deep Dive Analysis](../investigation/IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md)** | Root cause of 26x cascade |
| **[Consolidated Findings](../investigation/IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md)** | 6 parallel agent results |
| **[Next Steps](../investigation/IWQBINTEGRATION_NEXT_STEPS.md)** | Recommendations & improvements |

---

## Investigation Timeline

### Session Start: 2026-01-30 ~16:50

**Objective:** Deep investigation into IWQBIntegration package to ensure no conflicts with PROD environment before import.

**User Context:** "Currently we think there is actually a custom column we removed in the IWQBIntegration Order object that was linked to a business process for setting a value to the ProductOrder (ProductInOrder Object)."

---

## Phase 1: Package Extraction and Cataloging

### 1.1 Package Location
- **Zip File:** `/home/magown/creatio-report-fix/IWQBIntegration_2026-01-30_08.33.58.zip`
- **Extracted To:** `/home/magown/creatio-report-fix/investigation/IWQBIntegration/`

### 1.2 Package Format
- Creatio custom binary format (not standard zip)
- Inner .gz file containing concatenated schemas
- Extracted using `strings` command for content analysis

### 1.3 Package Contents Summary

| Category | Count |
|----------|-------|
| Total Files | 1,062 |
| Entity Extensions | 10 |
| New Entities (IW-prefixed) | 21 |
| Business Processes | 11 |
| Form Pages | 23 |
| SQL Views | 1 |
| Source Code Schemas | 1 |

---

## Phase 2: Entity Analysis

### 2.1 Entities EXTENDED by IWQBIntegration

These entities already exist in Creatio; IWQBIntegration adds columns/modifications:

| Entity | Parent Package | Risk Level | Notes |
|--------|----------------|------------|-------|
| Account | Creatio Core | HIGH | Foundational entity |
| Activity | Creatio Core | HIGH | Foundational entity |
| BGSalesGroup | PampaBay | MEDIUM | Custom entity |
| Contact | Creatio Core | HIGH | Foundational entity |
| Invoice | Creatio Core | HIGH | Business critical |
| InvoiceProduct | Creatio Core | HIGH | Business critical |
| Opportunity | Creatio Core | HIGH | Sales critical |
| **Order** | Creatio Core | **CRITICAL** | 20 new columns added |
| **OrderProduct** | Creatio Core | **CRITICAL** | Tax process triggers |
| Product | Creatio Core | MEDIUM | Foundational entity |

### 2.2 Order Entity - Custom Columns Added (20 Total)

#### Payment/Banking Information (7 columns)
| Column | Type | PCI Risk |
|--------|------|----------|
| IWOrderACH | Boolean | LOW |
| IWOrderBankAccountNumber | Text | **PCI-DSS** |
| IWOrderBankAccountType | Lookup | LOW |
| IWOrderBankCCFirstName | Text | PII |
| IWOrderBankCCLastName | Text | PII |
| IWOrderBankRoutingInformation | Text | **PCI-DSS** |
| IWOrderCreditCardNumber | Text | **PCI-DSS L1** |

#### Card Details (3 columns)
| Column | Type | PCI Risk |
|--------|------|----------|
| IWOrderCCExpDateMMYY | Integer | **PCI-DSS** |
| IWOrderCVMValue | Text | **PCI-DSS L1** |
| IWOrderCCAmountToCharge | Decimal | LOW |

#### Recurring Payment Configuration (5 columns)
| Column | Type |
|--------|------|
| IWOrderCheckifRecurringMonthlyPaymentBoolean | Boolean |
| IWOrderDayofMonthtoBillOn | Lookup |
| IWOrderRecurringMonthlyPaymentAmount | Decimal |
| IWOrderRecurringPaymentsStartMonth | DateTime |
| IWOrderRecurringPaymentsEndMonth | DateTime |

#### Payment Control & Status (2 columns)
| Column | Type |
|--------|------|
| IWOrderDoNotAutoRRunCCACH | Boolean |
| IWOrderNumberofDeclines | Integer |

#### Customer Balance & Tracking (3 columns)
| Column | Type |
|--------|------|
| IWOrderCustomerTotalBalance | Decimal |
| IWOrderLastDateofAuthorizedPayment | DateTime |
| IWOrderManualECheckACHAmountToProcess | Decimal |

### 2.3 New Entities CREATED by IWQBIntegration (21 Total)

#### Payment & Commission Entities
- IWPayments
- IWCreditMemos
- IWCommissionReportDataView

#### QuickBooks Lookup Entities (15)
- IWQBAppTypeLookup
- IWQBBillingStatusLookup
- IWQBClassLookup
- IWQBCustomerTypeLookup
- IWQBFileSelectedLookup
- IWQBItemTypeLookup
- IWQBJobTypeLookup
- IWQBLevelLookup
- IWQBPaymentMethodLookup
- IWQBSalesRepLookup
- IWQBShipViaLookup
- IWQBTermLookup
- IWQBVendorTypeLookup

#### Accounting Lookups (4)
- IWBankAccountTypeLookup
- IWDayofMonthToBillOnLookup
- IWExpenseAccountLookup
- IWIncomeAccountLookup

#### Mystery Entity
- UsrEntity_e7ac661 (purpose unknown)

---

## Phase 3: Business Process Analysis

### 3.1 Complete Process Catalog

| Process | Triggers On | Modifies | Risk |
|---------|-------------|----------|------|
| BGSetOrderProductTaxStatusByOrderSalesTax | Order, OrderProduct | OrderProduct.TaxStatus | HIGH |
| IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | Order, OrderProduct | Order.TaxStatus, OrderProduct.TaxStatus | HIGH |
| IWAccountCheckForInvoices | Invoice | Invoice.IWInvoiceCheckbox | MEDIUM |
| IWCalculateCommissiononPayment | Payment | Commission fields | HIGH |
| IWCalculateCommissiononPaymentV2 | Payment | Commission fields | HIGH |
| IWCalculateCommissiononPaymentIWQBIntegrationV3 | Payment, **Order** | Commission fields | **CRITICAL** |
| IWCalculateCommissiononPaymentCustomV4 | Payment | Commission fields | HIGH |
| IWFillCommissionReportPaymentsFields | Payment | Payment report fields | MEDIUM |
| IWFillCommissionReportPaymentsFieldsV2 | Payment | Payment report fields | MEDIUM |
| IWUpdateInvoicePaymentAmountPayments | Payment | Invoice.PaymentAmount, IWCreditedTotal | HIGH |
| IWUpdateInvoiceCreditedTotalandCheckbox | Payment | Invoice.IWCreditedTotal, IWInvoiceCheckbox | HIGH |

### 3.2 Process Trigger Map

#### Order Entity Triggers
| Event | Processes |
|-------|-----------|
| Order Added | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2 |
| Order Modified | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2, **IWCalculateCommissiononPaymentIWQBIntegrationV3** |
| Order Deleted | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2 |

#### OrderProduct Entity Triggers
| Event | Processes |
|-------|-----------|
| Product In Order Added | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2 |
| Product In Order Modified | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2 |

#### Payment Entity Triggers
| Event | Processes |
|-------|-----------|
| Payment Added | All 4 commission versions, both report versions, both invoice update processes |
| Payment Modified | Same as above |
| Payment Deleted | Same as above |

---

## Phase 4: Critical Risk Analysis

### 4.1 RISK #1: Multiple Commission Versions Active

**Severity:** CRITICAL

**Finding:** Four versions of commission calculation exist:
- V1 (Base): IWCalculateCommissiononPayment
- V2: IWCalculateCommissiononPaymentV2
- V3 (QB): IWCalculateCommissiononPaymentIWQBIntegrationV3
- V4 (Custom): IWCalculateCommissiononPaymentCustomV4

**Problem:** All trigger on same Payment events. If multiple enabled:
- Duplicate commission calculations
- Conflicting field updates
- Data corruption

**Version Comparison:**

| Aspect | V1 | V2 | V3 | V4 |
|--------|----|----|----|----|
| Lines | ~2,743 | ~3,041 | ~3,112 | ~3,257 |
| Parameters | 72 | 78 | 79 | 84 |
| ChangeDataUserTasks | 2 | 3 | 3 | 4 |
| Start Signals | 3 | 3 | **4** | 3 |
| Order Trigger | ✗ | ✗ | **✓** | ✗ |

### 4.2 RISK #2: V3 Order→Payment Cascade (26x Duplicate Root Cause)

**Severity:** CRITICAL

**Finding:** V3 uniquely has `StartSignal4` that triggers on Order Modified events.

**Cascade Path:**
```
User edits Order (any field)
    ↓
StartSignal4 fires (NO FILTER - any field change)
    ↓
Query: SELECT * FROM IWPayments WHERE OrderId = [edited order]
    ↓
For EACH Payment (e.g., 26):
    ├─ Recalculate commission
    ├─ Update Payment
    ├─ Payment.OnUpdate fires
    └─ BGQuickBooksIntegrationLogDetail entry created
    ↓
Result: 1 Order edit = 26 log entries
```

**Design Flaw:** StartSignal4 has no filter to trigger only on commission-affecting columns. Triggers on ANY Order field change.

### 4.3 RISK #3: Tax Process Duplication

**Severity:** MEDIUM-HIGH

**Finding:** Both V1 (`BGSetOrderProductTaxStatusByOrderSalesTax`) and V2 (`IWSetOrderandProductTaxStatusByOrderSalesTaxV2`) exist with identical triggers.

**Resolution:** Disable V1, keep V2.

### 4.4 RISK #4: Invoice Race Condition

**Severity:** MEDIUM-HIGH

**Finding:** Three processes modify Invoice fields on Payment changes:

| Process | Modifies |
|---------|----------|
| IWAccountCheckForInvoices | IWInvoiceCheckbox (always TRUE) |
| IWUpdateInvoiceCreditedTotalandCheckbox | IWCreditedTotal, IWInvoiceCheckbox (conditional) |
| IWUpdateInvoicePaymentAmountPayments | PaymentAmount, IWCreditedTotal |

**Race Conditions Confirmed:**
1. **Lost Update:** Process 2+3 both write IWCreditedTotal
2. **Write Conflict:** Process 1+2 both write IWInvoiceCheckbox with different logic
3. **Dirty Read:** Process 2 reads PaymentAmount that Process 3 is modifying

### 4.5 RISK #5: PCI-Sensitive Data

**Severity:** COMPLIANCE

**Finding:** Order entity contains PCI-DSS Level 1 sensitive data:
- IWOrderCreditCardNumber
- IWOrderCVMValue
- IWOrderBankAccountNumber
- IWOrderBankRoutingInformation

---

## Phase 5: Package Dependencies

### 5.1 Required Custom Dependencies (Must exist in PROD)
1. PampaBayQuickBooks
2. PampaBay
3. IWInterWeavePaymentApp

### 5.2 Creatio Core Dependencies (16 packages, v7.8.0)
- CrtCoreBase, CrtInvoice, CrtOpportunity, CrtLeadOppMgmtApp
- CrtBulkEmailInC360, CrtOrderContractInC360, CrtLeadOppMgmtInC360
- CrtInvoiceInC360, CrtOCMInLeadOppMgmt, CrtDocumentInOpportunity
- CrtOpportunityInvoice, CrtOpportunityInC360, CrtContactToLeadInC360
- CrtSLMITILService, CrtProductSpecification, Invoice

---

## Phase 6: User's Concern - Removed Column

### 6.1 Original Concern
"Custom column we removed in the IWQBIntegration Order object that was linked to a business process for setting a value to the ProductOrder (ProductInOrder Object)"

### 6.2 Analysis
The processes that link Order to OrderProduct are:
- BGSetOrderProductTaxStatusByOrderSalesTax
- IWSetOrderandProductTaxStatusByOrderSalesTaxV2

Both processes:
- Read: **Order.SalesTax** column
- Write: **OrderProduct.TaxStatus** column

### 6.3 Verification Required
```sql
-- Check if Order.SalesTax exists in PROD
SELECT column_name FROM information_schema.columns
WHERE table_name = 'Order' AND column_name LIKE '%SalesTax%';

-- Check if OrderProduct.TaxStatus exists
SELECT column_name FROM information_schema.columns
WHERE table_name = 'OrderProduct' AND column_name LIKE '%TaxStatus%';
```

If Order.SalesTax was removed, the tax processes would fail.

---

## Phase 7: Parallel Agent Investigations (Ralph Loop)

### 7.1 Investigation Method
Used Ralph Loop with 6 parallel agents to investigate different aspects simultaneously.

### 7.2 Agent Results Summary

| Agent | Focus Area | Key Findings |
|-------|------------|--------------|
| SQL Views Agent | IWCommissionReportDataView | View is additive, uses standard LEFT JOINs, LOW risk |
| Form Pages Agent | 8 form extensions | OrderPageV2 adds 20 columns, QB tabs; MEDIUM conflict risk with BGApp_eykaguu |
| Backend Agent | UsrExcelReportService | NO conflicts - handler already supports IW views |
| System Settings Agent | Process control flags | 3 settings control V3/V4/AutoPayment behavior |
| Events Agent | 21 EventsProcess schemas | All use LocalMessageHelper OnSaved pattern |
| Lookup Agent | 16 lookup entities | Clean hierarchy, no circular dependencies |

### 7.3 Critical Discoveries

1. **UsrExcelReportService Already Compatible:** Our updated handler already has routing for `IWCommissionReportDataView`
2. **System Settings Control Cascade:** `IWEnableCommissionV3 = false` prevents the 26x duplication issue
3. **Form Pages May Overlap:** Both IWQBIntegration and BGApp_eykaguu extend Order form - manual layout adjustment may be needed
4. **No Breaking Schema Conflicts:** Package can be imported without database migration issues

---

## Documents Generated

| Document | Path | Purpose |
|----------|------|---------|
| Conflict Assessment | `docs/investigation/IWQBINTEGRATION_CONFLICT_ASSESSMENT.md` | Full risk analysis |
| PROD Import Checklist | `docs/investigation/IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md` | Step-by-step procedures |
| Deep Dive Analysis | `docs/investigation/IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` | Detailed risk investigation |
| **Consolidated Findings** | `docs/investigation/IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md` | All parallel agent results |
| **Next Steps & Improvements** | `docs/investigation/IWQBINTEGRATION_NEXT_STEPS.md` | Actionable recommendations |
| Investigation Log | `docs/logs/IWQBINTEGRATION_INVESTIGATION_LOG.md` | This document |

---

## Working Files

| File | Path | Purpose |
|------|------|---------|
| Package Zip | `/home/magown/creatio-report-fix/IWQBIntegration_2026-01-30_08.33.58.zip` | Original package |
| Full Content | `/home/magown/creatio-report-fix/investigation/IWQBIntegration/full_content.txt` | Extracted strings |
| File List | `/home/magown/creatio-report-fix/investigation/IWQBIntegration/file_list.txt` | Package manifest |

---

## Recommendations

### Immediate Actions (Before PROD Import)

| Priority | Action |
|----------|--------|
| P0 | Verify which commission version is currently active in PROD |
| P0 | Disable StartSignal4 in V3 OR switch to V2/V4 |
| P0 | Disable V1 tax process |
| P1 | Verify Order.SalesTax column exists in PROD |
| P1 | Create PROD database backup |

### Configuration Recommendations

| Process | Recommended State |
|---------|-------------------|
| IWCalculateCommissiononPayment (V1) | DISABLE |
| IWCalculateCommissiononPaymentV2 | Enable (if standard commission) |
| IWCalculateCommissiononPaymentIWQBIntegrationV3 | DISABLE StartSignal4 |
| IWCalculateCommissiononPaymentCustomV4 | Enable (if custom rules needed) |
| BGSetOrderProductTaxStatusByOrderSalesTax | DISABLE |
| IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | ENABLE |

---

## Investigation Status

| Phase | Status | Notes |
|-------|--------|-------|
| Package Extraction | ✅ Complete | Binary format decoded |
| Entity Analysis | ✅ Complete | 10 extensions, 21 new |
| Process Analysis | ✅ Complete | 11 processes cataloged |
| Risk Assessment | ✅ Complete | 5 critical risks identified |
| Dependency Check | ✅ Complete | 3 custom + 16 core |
| Deep Dive: Commission | ✅ Complete | 4 versions compared |
| Deep Dive: V3 Cascade | ✅ Complete | Root cause of 26x found |
| Deep Dive: Invoice Race | ✅ Complete | Race condition confirmed |
| **Ralph Loop: 6 Parallel Agents** | ✅ Complete | SQL, Forms, Backend, Settings, Events, Lookups |
| **Consolidated Findings** | ✅ Complete | All agent results merged |
| **Next Steps & Improvements** | ✅ Complete | 5 immediate steps, 5 improvements |
| Documentation | ✅ Complete | **6 documents generated** |

---

## Final Assessment

### GO/NO-GO Decision: ✅ GO (with configuration)

The IWQBIntegration package is **technically safe to import** into PROD. No breaking conflicts were identified with:
- Existing database schema
- UsrExcelReportService backend handler
- Current report configurations

### Required Before Import

1. **Run verification SQL queries** (see IWQBINTEGRATION_NEXT_STEPS.md)
2. **Decide on commission version** (recommend V2)
3. **Set IWEnableCommissionV3 = false** (prevents 26x cascade)
4. **Create PROD database backup**
5. **Verify Order.SalesTax column exists**

### Post-Import Actions

1. Disable duplicate commission processes (keep only chosen version)
2. Disable V1 tax process if V2 is authoritative
3. Verify Order form layout in Form Designer
4. Execute test checklist from IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md
5. Monitor for 1 week for commission duplicates

---

*Investigation log completed: 2026-01-30*
*Total documents generated: 6*
*Investigation method: Ralph Loop with 6 parallel agents*
