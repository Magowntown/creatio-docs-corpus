# IWQBIntegration Master Catalog

**Created:** 2026-01-30
**Package:** IWQBIntegration v8.3.2.4199
**Package UId:** 21e7eb4b-a41b-42f1-913a-41046da1cb86

---

## Document Index

### Primary Documents

| # | Document | Path | Purpose |
|---|----------|------|---------|
| 1 | **Master Catalog** | `docs/investigation/IWQBINTEGRATION_MASTER_CATALOG.md` | This index document |
| 2 | **Team Instructions** | `docs/investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` | Step-by-step procedures for team |
| 3 | **Investigation Log** | `docs/logs/IWQBINTEGRATION_INVESTIGATION_LOG.md` | Complete investigation timeline |
| 4 | **Conflict Assessment** | `docs/investigation/IWQBINTEGRATION_CONFLICT_ASSESSMENT.md` | Risk analysis (5 critical risks) |
| 5 | **PROD Import Checklist** | `docs/investigation/IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md` | 13-phase import procedure |
| 6 | **Deep Dive Analysis** | `docs/investigation/IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` | Root cause analyses |
| 7 | **Consolidated Findings** | `docs/investigation/IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md` | 6 parallel agent results |
| 8 | **Next Steps & Improvements** | `docs/investigation/IWQBINTEGRATION_NEXT_STEPS.md` | Recommendations |

### Working Files

| File | Path | Purpose |
|------|------|---------|
| Package Zip | `/home/magown/creatio-report-fix/IWQBIntegration_2026-01-30_08.33.58.zip` | Original exported package |
| Extracted Content | `investigation/IWQBIntegration/full_content.txt` | Strings extracted from binary |
| File Manifest | `investigation/IWQBIntegration/file_list.txt` | Package file listing |

---

## Entity Catalog

### Entities EXTENDED (10)

| Entity | Parent Package | Columns Added | Risk Level |
|--------|----------------|---------------|------------|
| Account | Creatio Core | QB sync fields | HIGH |
| Activity | Creatio Core | QB activity fields | HIGH |
| BGSalesGroup | PampaBay | Sales group extensions | MEDIUM |
| Contact | Creatio Core | QB vendor fields | HIGH |
| Invoice | Creatio Core | Payment tracking fields | HIGH |
| InvoiceProduct | Creatio Core | Commission fields | HIGH |
| Opportunity | Creatio Core | QB estimate fields | HIGH |
| **Order** | Creatio Core | **20 columns** (payment, PCI) | **CRITICAL** |
| **OrderProduct** | Creatio Core | Tax status, commission | **CRITICAL** |
| Product | Creatio Core | QB item fields | MEDIUM |

### Entities CREATED (21)

| Entity | Type | Purpose |
|--------|------|---------|
| IWPayments | Transaction | Payment records |
| IWCreditMemos | Transaction | Credit memo records |
| IWCommissionReportDataView | SQL View | Commission report data |
| IWQBAppTypeLookup | Lookup | QB application types |
| IWQBBillingStatusLookup | Lookup | Billing status codes |
| IWQBClassLookup | Lookup | QB class mapping |
| IWQBCustomerTypeLookup | Lookup | Customer type codes |
| IWQBFileSelectedLookup | Lookup | File selection options |
| IWQBItemTypeLookup | Lookup | Item type codes |
| IWQBJobTypeLookup | Lookup | Job type codes |
| IWQBLevelLookup | Lookup | Level codes |
| IWQBPaymentMethodLookup | Lookup | Payment methods |
| IWQBSalesRepLookup | Lookup | Sales rep mapping |
| IWQBShipViaLookup | Lookup | Shipping methods |
| IWQBTermLookup | Lookup | Payment terms |
| IWQBVendorTypeLookup | Lookup | Vendor type codes |
| IWBankAccountTypeLookup | Lookup | Bank account types |
| IWDayofMonthToBillOnLookup | Lookup | Billing day options |
| IWExpenseAccountLookup | Lookup | Expense account mapping |
| IWIncomeAccountLookup | Lookup | Income account mapping |
| UsrEntity_e7ac661 | Unknown | Purpose unknown |

---

## Business Process Catalog

### Commission Processes (4 versions)

| Process | Version | Order Trigger | Recommended State |
|---------|---------|---------------|-------------------|
| IWCalculateCommissiononPayment | V1 (Base) | ✗ | **DISABLE** |
| IWCalculateCommissiononPaymentV2 | V2 | ✗ | **ENABLE** (recommended) |
| IWCalculateCommissiononPaymentIWQBIntegrationV3 | V3 (QB) | **✓** | DISABLE (causes 26x cascade) |
| IWCalculateCommissiononPaymentCustomV4 | V4 (Custom) | ✗ | DISABLE (evaluate later) |

### Tax Status Processes (2 versions)

| Process | Version | Recommended State |
|---------|---------|-------------------|
| BGSetOrderProductTaxStatusByOrderSalesTax | V1 | **DISABLE** |
| IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | V2 | **ENABLE** |

### Invoice Processes (3)

| Process | Modifies | Conflict |
|---------|----------|----------|
| IWAccountCheckForInvoices | IWInvoiceCheckbox | Writes TRUE always |
| IWUpdateInvoicePaymentAmountPayments | PaymentAmount, IWCreditedTotal | |
| IWUpdateInvoiceCreditedTotalandCheckbox | IWCreditedTotal, IWInvoiceCheckbox | **RACE CONDITION** |

### Report Processes (2 versions)

| Process | Version |
|---------|---------|
| IWFillCommissionReportPaymentsFields | V1 |
| IWFillCommissionReportPaymentsFieldsV2 | V2 |

---

## Order Entity Column Catalog (20 columns)

### Payment/Banking (7)

| Column | Type | PCI Risk |
|--------|------|----------|
| IWOrderACH | Boolean | LOW |
| IWOrderBankAccountNumber | Text | **PCI-DSS** |
| IWOrderBankAccountType | Lookup | LOW |
| IWOrderBankCCFirstName | Text | PII |
| IWOrderBankCCLastName | Text | PII |
| IWOrderBankRoutingInformation | Text | **PCI-DSS** |
| IWOrderCreditCardNumber | Text | **PCI-DSS L1** |

### Card Details (3)

| Column | Type | PCI Risk |
|--------|------|----------|
| IWOrderCCExpDateMMYY | Integer | **PCI-DSS** |
| IWOrderCVMValue | Text | **PCI-DSS L1** |
| IWOrderCCAmountToCharge | Decimal | LOW |

### Recurring Payment (5)

| Column | Type |
|--------|------|
| IWOrderCheckifRecurringMonthlyPaymentBoolean | Boolean |
| IWOrderDayofMonthtoBillOn | Lookup |
| IWOrderRecurringMonthlyPaymentAmount | Decimal |
| IWOrderRecurringPaymentsStartMonth | DateTime |
| IWOrderRecurringPaymentsEndMonth | DateTime |

### Payment Control (2)

| Column | Type |
|--------|------|
| IWOrderDoNotAutoRRunCCACH | Boolean |
| IWOrderNumberofDeclines | Integer |

### Customer Balance (3)

| Column | Type |
|--------|------|
| IWOrderCustomerTotalBalance | Decimal |
| IWOrderLastDateofAuthorizedPayment | DateTime |
| IWOrderManualECheckACHAmountToProcess | Decimal |

---

## System Settings Catalog

| Setting Code | Type | Default | Controls |
|--------------|------|---------|----------|
| IWEnableCommissionV3 | Boolean | false | V3 Order→Payment cascade |
| IWEnableCommissionV4 | Boolean | false | V4 custom commission rules |
| IWEnableAutoPaymentProcessing | Boolean | true | Recurring CC/ACH processing |

---

## Risk Catalog

| Risk ID | Severity | Description | Mitigation |
|---------|----------|-------------|------------|
| RISK-001 | CRITICAL | Multiple commission versions active | Enable only ONE version |
| RISK-002 | CRITICAL | V3 Order→Payment cascade (26x) | Set IWEnableCommissionV3=false |
| RISK-003 | MEDIUM-HIGH | Tax process duplication | Disable V1, keep V2 |
| RISK-004 | MEDIUM-HIGH | Invoice race condition | Audit field ownership |
| RISK-005 | COMPLIANCE | PCI-sensitive data in Order | Verify encryption/access |

---

## Dependency Catalog

### Custom Package Dependencies (must exist in PROD)

| Package | Purpose | Required |
|---------|---------|----------|
| PampaBayQuickBooks | QB integration backbone | ✓ |
| PampaBay | Base customizations | ✓ |
| IWInterWeavePaymentApp | Payment/commission infrastructure | ✓ |

### Creatio Core Dependencies (16 packages, v7.8.0)

- CrtCoreBase
- CrtInvoice
- CrtOpportunity
- CrtLeadOppMgmtApp
- CrtBulkEmailInC360
- CrtOrderContractInC360
- CrtLeadOppMgmtInC360
- CrtInvoiceInC360
- CrtOCMInLeadOppMgmt
- CrtDocumentInOpportunity
- CrtOpportunityInvoice
- CrtOpportunityInC360
- CrtContactToLeadInC360
- CrtSLMITILService
- CrtProductSpecification
- Invoice

---

## Investigation Method Catalog

| Phase | Method | Agents Used |
|-------|--------|-------------|
| Package Extraction | Binary format decode | gunzip + strings |
| Entity Analysis | Schema parsing | Manual + grep |
| Process Analysis | Flow diagram extraction | Manual |
| Risk Assessment | Cross-reference analysis | Manual |
| Parallel Investigation | Ralph Loop | 6 agents |

### Ralph Loop Agents (6)

| Agent | Focus | Result |
|-------|-------|--------|
| SQL Views Agent | IWCommissionReportDataView | LOW risk, additive only |
| Form Pages Agent | 8 form extensions | MEDIUM conflict risk |
| Backend Agent | UsrExcelReportService | NO conflicts |
| System Settings Agent | Process control flags | 3 settings identified |
| Events Agent | EventsProcess schemas | 21 OnSaved handlers |
| Lookup Agent | Lookup dependencies | No circular deps |

---

## Quick Reference

### Verification SQL (Run Before Import)

```sql
-- Check Order.SalesTax exists
SELECT column_name FROM information_schema.columns
WHERE table_name = 'Order' AND column_name LIKE '%SalesTax%';

-- Check dependencies exist
SELECT "Name", "Version" FROM "SysPackage"
WHERE "Name" IN ('PampaBayQuickBooks', 'PampaBay', 'IWInterWeavePaymentApp');

-- Check current commission processes
SELECT "Name", "Enabled" FROM "SysSchema"
WHERE "Name" LIKE 'IWCalculateCommission%';
```

### Key Decisions Required

| Decision | Options | Recommended |
|----------|---------|-------------|
| Commission Version | V1, V2, V3, V4 | V2 |
| Tax Process | V1, V2 | V2 |
| IWEnableCommissionV3 | true/false | false |
| IWEnableCommissionV4 | true/false | false |

### Document Links

- **Start Here:** `IWQBINTEGRATION_TEAM_INSTRUCTIONS.md`
- **Full Checklist:** `IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md`
- **Risk Details:** `IWQBINTEGRATION_CONFLICT_ASSESSMENT.md`
- **Root Cause Analysis:** `IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md`

---

*Master catalog compiled: 2026-01-30*
*Total investigation documents: 8*
*Total entities cataloged: 31 (10 extended + 21 created)*
*Total processes cataloged: 11*
*Total risks identified: 5*
