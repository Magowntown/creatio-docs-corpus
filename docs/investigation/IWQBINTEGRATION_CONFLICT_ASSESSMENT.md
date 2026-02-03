# IWQBIntegration Package - Conflict Assessment Report

**Date:** 2026-01-30
**Package Version:** 8.3.2.4199
**Package UId:** 21e7eb4b-a41b-42f1-913a-41046da1cb86
**Status:** Pre-PROD Import Review

---

## Executive Summary

The IWQBIntegration package is a **deeply integrated customization** that extends 10 core Creatio entities and creates 21 new entities. **CRITICAL RISKS** identified:

1. **Multiple commission calculation versions (V1-V4)** - unclear which is active
2. **Tax status process duplication** - V1 and V2 both exist
3. **Order cascade to Payment** - V3 commission triggers on Order changes
4. **Invoice calculation race condition** - 3 processes modify same fields
5. **PCI-sensitive data** in Order columns (credit cards, bank routing)

**Recommendation:** Requires targeted testing and process cleanup before PROD import.

---

## Package Contents Summary

| Category | Count | Risk Level |
|----------|-------|------------|
| Entity Extensions | 10 | HIGH |
| New Entities | 21 | LOW |
| Business Processes | 11 | HIGH |
| Form Pages | 23 | MEDIUM |
| SQL Views | 1 | LOW |
| Source Code | 1 | MEDIUM |

---

## Order Entity - Custom Columns (20 Total)

### Payment/Banking Information (7 columns)

| Column | Type | Description | Risk |
|--------|------|-------------|------|
| IWOrderACH | Boolean | ACH payment enabled | LOW |
| IWOrderBankAccountNumber | Text | Bank account number | **PCI** |
| IWOrderBankAccountType | Lookup | Bank account type | LOW |
| IWOrderBankCCFirstName | Text | Cardholder first name | PII |
| IWOrderBankCCLastName | Text | Cardholder last name | PII |
| IWOrderBankRoutingInformation | Text | Routing number | **PCI** |
| IWOrderCreditCardNumber | Text | Credit card number | **PCI-DSS L1** |

### Card Details (3 columns)

| Column | Type | Description | Risk |
|--------|------|-------------|------|
| IWOrderCCExpDateMMYY | Integer | Card expiration MMYY | **PCI** |
| IWOrderCVMValue | Text | CVV/CVC value | **PCI-DSS L1** |
| IWOrderCCAmountToCharge | Decimal | Manual charge amount | LOW |

### Recurring Payment Configuration (5 columns)

| Column | Type | Description |
|--------|------|-------------|
| IWOrderCheckifRecurringMonthlyPaymentBoolean | Boolean | Recurring enabled |
| IWOrderDayofMonthtoBillOn | Lookup | Day of month |
| IWOrderRecurringMonthlyPaymentAmount | Decimal | Monthly amount |
| IWOrderRecurringPaymentsStartMonth | DateTime | Cycle start |
| IWOrderRecurringPaymentsEndMonth | DateTime | Cycle end |

### Payment Control & Status (2 columns)

| Column | Type | Description |
|--------|------|-------------|
| IWOrderDoNotAutoRRunCCACH | Boolean | Prevent auto-processing |
| IWOrderNumberofDeclines | Integer | Failed transaction counter |

### Customer Balance & Tracking (3 columns)

| Column | Type | Description |
|--------|------|-------------|
| IWOrderCustomerTotalBalance | Decimal | Running balance |
| IWOrderLastDateofAuthorizedPayment | DateTime | Last authorization |
| IWOrderManualECheckACHAmountToProcess | Decimal | ACH override amount |

### User-Mentioned Concern

**"Custom column removed linked to business process for ProductOrder"**

The user mentioned a removed column that was linked to a business process for ProductInOrder. Based on our analysis:

- **BGSetOrderProductTaxStatusByOrderSalesTax** - Triggers on Order AND OrderProduct changes
- **IWSetOrderandProductTaxStatusByOrderSalesTaxV2** - Enhanced version, same triggers

These processes read Order.SalesTax and write to OrderProduct.TaxStatus. If a column was removed from Order that these processes depended on, it could cause:
- Process execution failures
- TaxStatus not being set correctly on OrderProduct
- Cascading errors in Invoice/Commission calculations

**ACTION REQUIRED:** Verify the Order.SalesTax column exists and is properly mapped.

---

## Business Processes - Full Catalog

### Tax Calculation Processes

#### BGSetOrderProductTaxStatusByOrderSalesTax
- **Triggers:** Order Added/Modified/Deleted, Product In Order Added/Modified
- **Reads:** Order.SalesTax
- **Modifies:** OrderProduct.TaxStatus
- **Risk:** MODERATE - Frequent trigger, core functionality

#### IWSetOrderandProductTaxStatusByOrderSalesTaxV2
- **Triggers:** Same as above
- **Reads:** Order.SalesTax
- **Modifies:** Order.TaxStatus, OrderProduct.TaxStatus
- **Risk:** HIGH - Enhanced version, possible duplicate with V1
- **CONFLICT:** Both V1 and V2 trigger on same events!

### Commission Calculation Processes

#### IWCalculateCommissiononPayment (Base)
- **Triggers:** Payment Added/Modified/Deleted
- **Modifies:** Commission fields
- **Risk:** HIGH - Core commission logic

#### IWCalculateCommissiononPaymentV2
- **Triggers:** Payment Added/Modified/Deleted
- **Parent:** IWCalculateCommissiononPayment
- **Risk:** HIGH - Unclear if active

#### IWCalculateCommissiononPaymentIWQBIntegrationV3
- **Triggers:** Payment Added/Modified/Deleted, **ORDER MODIFIED**
- **Risk:** VERY HIGH - Order changes trigger Payment recalculations!
- **WARNING:** This is the only version that listens to Order changes

#### IWCalculateCommissiononPaymentCustomV4
- **Triggers:** Payment Added/Modified/Deleted
- **Risk:** HIGH - Custom variant, unknown logic

### Invoice Processes

#### IWAccountCheckForInvoices
- **Triggers:** Invoice Added/Modified/Deleted
- **Modifies:** Invoice.IWInvoiceCheckbox
- **Risk:** MODERATE

#### IWUpdateInvoicePaymentAmountPayments
- **Triggers:** Payment Added/Modified/Deleted
- **Modifies:** Invoice.PaymentAmount, Invoice.IWCreditedTotal
- **Risk:** MODERATE-HIGH

#### IWUpdateInvoiceCreditedTotalandCheckbox
- **Triggers:** Payment Added/Modified/Deleted
- **Modifies:** Invoice.IWCreditedTotal, Invoice.IWInvoiceCheckbox
- **CONFLICT:** Overlaps with IWUpdateInvoicePaymentAmountPayments!

### Report Processes

#### IWFillCommissionReportPaymentsFields
- **Triggers:** Payment Added/Modified/Deleted
- **Modifies:** Payment report fields
- **Risk:** MODERATE

#### IWFillCommissionReportPaymentsFieldsV2
- **Triggers:** Payment Added/Modified/Deleted
- **Parent:** IWFillCommissionReportPaymentsFields
- **Risk:** MODERATE - Unclear if active

---

## Process Trigger Map

### Order Entity
| Event | Processes Triggered |
|-------|---------------------|
| Order Added | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2 |
| Order Modified | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2, **IWCalculateCommissiononPaymentIWQBIntegrationV3** |
| Order Deleted | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2 |

### OrderProduct Entity
| Event | Processes Triggered |
|-------|---------------------|
| Product In Order Added | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2 |
| Product In Order Modified | BGSetOrderProductTaxStatusByOrderSalesTax, IWSetOrderandProductTaxStatusByOrderSalesTaxV2 |

### Invoice Entity
| Event | Processes Triggered |
|-------|---------------------|
| Invoice Added | IWAccountCheckForInvoices |
| Invoice Modified | IWAccountCheckForInvoices |
| Invoice Deleted | IWAccountCheckForInvoices |

### Payment Entity
| Event | Processes Triggered |
|-------|---------------------|
| Payment Added | IWCalculateCommissiononPayment (ALL 4 VERSIONS), IWFillCommissionReportPaymentsFields (BOTH), IWUpdateInvoicePaymentAmountPayments, IWUpdateInvoiceCreditedTotalandCheckbox |
| Payment Modified | Same as above |
| Payment Deleted | Same as above |

---

## Entity Extensions Analysis

IWQBIntegration **EXTENDS** these 10 entities (not creates - modifies existing):

| Entity | Risk | Conflict Potential |
|--------|------|-------------------|
| Account | HIGH | BGApp_eykaguu, Custom may also extend |
| Activity | HIGH | BGApp_eykaguu may extend |
| BGSalesGroup | MEDIUM | PampaBay ownership |
| Contact | HIGH | BGApp_eykaguu may extend |
| Invoice | HIGH | Multiple invoice processes |
| InvoiceProduct | HIGH | Commission calculation dependencies |
| Opportunity | HIGH | Sales workflow dependencies |
| **Order** | **CRITICAL** | 20 new columns, tax process triggers |
| **OrderProduct** | **CRITICAL** | Tax status, commission cascades |
| Product | MEDIUM | Form page changes |

---

## Critical Conflict Risks

### RISK 1: Multiple Commission Versions Active
**Severity:** CRITICAL

Four versions of commission calculation exist:
- V1 (Base), V2, V3 (QB), V4 (Custom)

All trigger on same Payment events. If multiple are enabled:
- Duplicate commission calculations
- Conflicting field updates
- Data corruption

**Mitigation:** Verify only ONE version is enabled in SysProcessSchemas.IsActualVersion

### RISK 2: Order Change Cascades to Payment
**Severity:** HIGH

IWCalculateCommissiononPaymentIWQBIntegrationV3 uniquely listens to Order Modified events.
- Modifying an Order could trigger payment recalculation
- May cause unexpected commission changes
- No other version has this behavior

**Mitigation:** Document this behavior; test Order modifications carefully

### RISK 3: Tax Process Duplication
**Severity:** MEDIUM-HIGH

BGSetOrderProductTaxStatusByOrderSalesTax AND IWSetOrderandProductTaxStatusByOrderSalesTaxV2 both exist.
- V2 is likely intended replacement
- Both may be active, causing duplicate writes

**Mitigation:** Disable V1 if V2 is authoritative

### RISK 4: Invoice Field Race Condition
**Severity:** MEDIUM-HIGH

Three processes modify Invoice fields on Payment changes:
1. IWAccountCheckForInvoices → IWInvoiceCheckbox
2. IWUpdateInvoicePaymentAmountPayments → PaymentAmount, IWCreditedTotal
3. IWUpdateInvoiceCreditedTotalandCheckbox → IWCreditedTotal, IWInvoiceCheckbox

Fields `IWCreditedTotal` and `IWInvoiceCheckbox` are modified by multiple processes!

**Mitigation:** Audit which process is authoritative for each field

### RISK 5: PCI Data in Order Columns
**Severity:** COMPLIANCE

Order entity contains PCI-DSS Level 1 sensitive data:
- IWOrderCreditCardNumber
- IWOrderCVMValue
- IWOrderBankAccountNumber
- IWOrderBankRoutingInformation

**Mitigation:** Ensure proper encryption, access controls, and audit logging

---

## Package Dependencies

### Critical Custom Dependencies (Must Pre-Exist in PROD)
1. **PampaBayQuickBooks** - QB integration backbone
2. **PampaBay** - Base customizations
3. **IWInterWeavePaymentApp** - Payment/commission infrastructure

### Creatio Core Dependencies (16 packages, v7.8.0)
- CrtCoreBase, CrtInvoice, CrtOpportunity, CrtLeadOppMgmtApp, etc.
- All standard Creatio modules, should already exist in PROD

---

## Pre-PROD Import Checklist

### Required Actions

- [ ] **Verify process versions** - Which commission version is active?
- [ ] **Disable duplicate processes** - V1 tax vs V2 tax
- [ ] **Test Order modification cascade** - V3 commission triggers on Order change
- [ ] **Audit Invoice processes** - Which owns IWCreditedTotal?
- [ ] **Verify Order.SalesTax column** - Required by tax processes
- [ ] **Check PCI compliance** - CC/bank data encryption
- [ ] **Confirm dependencies** - PampaBayQuickBooks, PampaBay, IWInterWeavePaymentApp exist

### Post-Import Testing

- [ ] Create new Order → Tax status set on OrderProduct
- [ ] Modify Order → No unexpected commission recalculation (unless V3 is desired)
- [ ] Add Payment → Commission calculated (only one version)
- [ ] Modify Payment → Invoice fields updated correctly
- [ ] Delete Payment → Invoice totals recalculated
- [ ] Commission Report generation works

---

## Recommendations

1. **Process Cleanup Required**
   - Disable V1 tax process if V2 is authoritative
   - Determine which commission version (V1-V4) should be active
   - Disable duplicate Invoice processes

2. **Documentation Required**
   - Document Order→Payment cascade behavior (V3)
   - Document Invoice field ownership

3. **Testing Required**
   - Full regression test of Order/OrderProduct workflows
   - Commission calculation end-to-end test
   - Invoice payment reconciliation test

4. **Security Review Required**
   - PCI compliance audit for CC/bank columns
   - Access control verification

---

## Files Reference

| File | Purpose |
|------|---------|
| `/home/magown/creatio-report-fix/IWQBIntegration_2026-01-30_08.33.58.zip` | Original package |
| `/home/magown/creatio-report-fix/investigation/IWQBIntegration/full_content.txt` | Extracted strings |
| `/home/magown/creatio-report-fix/investigation/IWQBIntegration/file_list.txt` | Package file manifest |

---

*Assessment prepared: 2026-01-30*
