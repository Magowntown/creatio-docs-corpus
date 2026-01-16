# Package Comparison: IWQBIntegration vs PampaBayQuickBooks

**Date:** 2026-01-15
**Purpose:** Identify automation conflicts affecting Commission report data

---

## Executive Summary

**Root Cause:** IWQBIntegration's `OrderPageV2` client schema was modified on **2026-01-14** and is setting `PaymentStatusId = Planned` as default for UI-created orders. This prevents those orders from syncing to QuickBooks, causing them to be missing from commission reports.

---

## Package Comparison

### IWQBIntegration (New Package)

| Attribute | Value |
|-----------|-------|
| **Package ID** | 5af0c9b0-141b-4d3f-828e-a455a1705aed |
| **Purpose** | InterWeave QuickBooks Integration - Payment processing, commission calculation |
| **Order Schema Modified** | 2026-01-14T15:35:15Z (YESTERDAY) |
| **OrderPageV2 Modified** | 2026-01-14T15:35:15Z (MOST RECENT) |

**Processes (10):**
| Process | Caption |
|---------|---------|
| IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | IW Set Order and Product Tax Status by Order Sales Tax |
| IWCalculateCommissiononPayment | IW Calculate Commission on Payment |
| IWCalculateCommissiononPaymentV2 | IW Calculate Commission on Payment V2 |
| IWCalculateCommissiononPaymentIWQBIntegrationV3 | IW Calculate Commission on Payment V3 |
| IWCalculateCommissiononPaymentCustomV4 | IW Calculate Commission on Payment V4 |
| IWFillCommissionReportPaymentsFields | IW Fill Commission Report Payments Fields |
| IWFillCommissionReportPaymentsFieldsV2 | IW Fill Commission Report Payments Fields |
| IWUpdateInvoicePaymentAmountPayments | IW Update Invoice Payment Amount |
| IWUpdateInvoiceCreditedTotalandCheckbox | IW Update Invoice Credited Total and Checkbox |
| IWAccountCheckForInvoices | IW Account Check For Invoices |

**Columns Added to Order (24 IW-prefixed):**
- IWTaxStatus
- IWQBInvoiceNumber
- IWAuthNetTransactionId/Amount
- IWOrderCreditCardNumber, IWOrderCCExpDateMMYY, IWOrderCVMValue
- IWOrderBankAccountNumber, IWOrderBankRoutingInformation
- IWOrderRecurringMonthlyPaymentAmount
- ... and 14 more payment/billing fields

---

### PampaBayQuickBooks (Original Package)

| Attribute | Value |
|-----------|-------|
| **Package ID** | f63b797a-cff7-4fdc-9c73-000676e1d209 |
| **Purpose** | QuickBooks Integration - Order sync, commission download |
| **Order Schema Modified** | 2025-03-11T10:03:50Z |
| **OrderPageV2 Modified** | 2023-05-11T12:56:44Z |

**Processes (14):**
| Process | Caption |
|---------|---------|
| BGBPRunQBCustomerOrderIntegration | Run QB Customer Order Integration |
| BGBPGetQuickBooksCommissions | Get QuickBooks Commissions |
| BGBPQuickBooksCustomerOrderChangedLog | QuickBooks Customer Order Changed Log |
| BGBPQuickBooksFactoryOrderChangedLog | QuickBooks Factory Order Changed Log |
| BGBPRunQBFactoryOrderIntegration | Run QB Factory Order Integration |
| BGBPRunQBInventoryAdjustmentIntegration | Run QB Inventory Adjustment Integration |
| BGBPQBExportSchedule | Quickbooks export schedule |
| BGBPMarkCustomerOrdersReProcess | Mark Customer Orders to Re-Process |
| BGBPMarkFactoryOrdersReProcess | Mark Factory Orders to Re-Process |
| BGBPMarkQuickBooksLogReProcess | Mark QuickBooks Log to Re-Process |
| BGBPMarkInventoryAdjustmentReProcess | Mark Inventory Adjustment to Re-Process |
| BGQuickBooksCreateHeaderLog | QuickBooks Create Header Log |
| BGBPTestQuickBooks | Test QuickBooks |
| BGBPTestQBConnection | Test QB Connection |

---

## Conflict Analysis

### Schema Override Chain

```
Order Page Load Sequence (most specific wins):
1. BaseOrderPage [Order] - Base platform
2. OrderPageV2 [Order] - Platform extensions
3. OrderPageV2 [Passport] - Passport module
4. OrderPageV2 [PampaBayQuickBooks] - QB integration (2023-05-11)
5. OrderPageV2 [PampaBay] - Main customizations (2025-05-20)
6. OrderPageV2 [IWQBIntegration] - IW integration (2026-01-14) ← MOST RECENT, OVERRIDES ALL
```

### The Problem

1. **IWQBIntegration's OrderPageV2** overrides all previous page configurations
2. It was modified **yesterday** (2026-01-14)
3. It likely sets `PaymentStatusId = Planned` as default for new orders
4. **PampaBayQuickBooks' sync process** (`BGBPRunQBCustomerOrderIntegration`) filters out orders with certain PaymentStatus values
5. Result: Orders created via UI get "Planned" status → Not synced to QB → Missing from commission reports

### Process Overlap Analysis

| Function | IWQBIntegration | PampaBayQuickBooks |
|----------|-----------------|---------------------|
| Order sync to QB | ❌ | ✅ BGBPRunQBCustomerOrderIntegration |
| Commission download | ❌ | ✅ BGBPGetQuickBooksCommissions |
| Commission calculation | ✅ IWCalculateCommissiononPayment* | ❌ |
| Tax status setting | ✅ IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | ❌ |
| Payment processing | ✅ IWUpdateInvoicePaymentAmountPayments | ❌ |

**Observation:** IWQBIntegration handles payment-side processing, PampaBayQuickBooks handles QB sync. They should complement each other, but the page default is causing a disconnect.

---

## Process Execution Analysis

**Most Active IW Process:**
```
IW Set Order and Product Tax Status by Order Sales Tax: 30+ executions in recent logs
```

This process runs on EVERY order modification, but it sets `IWTaxStatus`, not `PaymentStatusId`.

**PaymentStatusId Source:** Most likely the OrderPageV2 client schema default, not a business process.

---

## Recommended Investigation

### To Confirm Root Cause

1. **Check IWQBIntegration OrderPageV2 source code** in Creatio Configuration:
   - Navigate to: Configuration → IWQBIntegration → OrderPageV2
   - Look for: `defValue`, `defaultValue`, or init method setting PaymentStatusId
   - Schema ID: `6c9e5e8b-9d0b-41b4-b24d-bec395eb68bf`

2. **Check PampaBayQuickBooks sync filter**:
   - Review BGBPRunQBCustomerOrderIntegration process
   - Identify what PaymentStatus values are excluded from sync

### Potential Fixes

| Option | Description | Risk |
|--------|-------------|------|
| A | Remove PaymentStatusId default from IWQBIntegration OrderPageV2 | Low - reverts to previous behavior |
| B | Update BGBPRunQBCustomerOrderIntegration to include "Planned" orders | Medium - may sync unintended orders |
| C | Add business process to clear PaymentStatusId for synced orders | Low - targeted fix |

---

## Timeline Correlation

| Date | Event |
|------|-------|
| 2023-05-11 | PampaBayQuickBooks OrderPageV2 last modified |
| 2025-03-11 | PampaBayQuickBooks Order schema modified |
| 2025-05-20 | PampaBay OrderPageV2 last modified |
| **2026-01-14** | **IWQBIntegration Order schema + OrderPageV2 modified** |
| 2026-01-15 | Commission report empty data issue reported |

The 1-day gap between IWQBIntegration modification and issue report strongly suggests causation.

---

## Files Created

| File | Purpose |
|------|---------|
| `scripts/investigation/compare_package_processes.py` | Package process comparison |
| `scripts/investigation/get_all_processes.py` | Process schema discovery |
| `scripts/investigation/analyze_process_triggers.py` | Process execution analysis |
| `scripts/investigation/check_page_defaults.py` | Page schema analysis |
