# Report Filter Requirements

**Date:** 2026-01-29
**Purpose:** Map each downloadable Excel report to required filters and custom generator needs

---

## Summary

| Report | Schema | Custom Gen | Filters |
|--------|--------|------------|---------|
| Commission | BGCommissionReportDataView | Yes (via ExecutionId) | YearMonth, SalesGroup |
| Items by Customer | BGSalesByItemView | Yes (v54 fix) | Customer, Date, Status |
| Customers did not buy | BGSalesByCustomerView | **NEEDS** | Date, Status |
| Sales By Item | BGSalesByItemView | **NEEDS** | Date, Status |
| Sales By Line | BGSalesByItemLineView | **NEEDS** | Date, Status |
| Sales By Item By Type | BGSalesByItemView | **NEEDS** | Date, Status |

---

## View Column Analysis

### BGSalesByCustomerView
Used by: Customers did not buy, Sales By Customer
Columns: BGStatus, BGCustomer, BGShipDate, BGInvoiceDate, BGDeliveryDate, BGAmount, BGNumber, BGSalesRep, BGSalesGroup

### BGSalesByItemView
Used by: Items by Customer, Sales By Item, Sales By Item By Type
Columns: CreatedOn, BGShipDate, BGDeliveryDate, BGStatus, BGCustomer, BGItem, BGAmount, BGQuantity

### BGSalesByItemLineView
Used by: Sales By Line
Columns: TBD - likely similar to BGSalesByItemView

---

## Filter UI Mapping

| Report | Created | Shipping | Delivery | Status | Customer | YearMonth | SalesGroup |
|--------|---------|----------|----------|--------|----------|-----------|------------|
| Commission | - | - | - | - | - | **YES** | **YES** |
| Items by Customer | YES | YES | YES | YES | **YES** | - | - |
| Customers did not buy | YES | YES | YES | YES | - | - | - |
| Sales By Item | YES | YES | YES | YES | - | - | - |
| Sales By Line | YES | YES | YES | YES | - | - | - |
| Sales By Item By Type | YES | YES | YES | YES | - | - | - |

---

## Implementation Plan

### Backend Changes (UsrExcelReportService.cs)

1. **Add custom generator for BGSalesByCustomerView** - prevents OutOfMemoryException
2. **Extend BGSalesByItemView generator** - to handle all reports using this view
3. **Add custom generator for BGSalesByItemLineView** - if needed

### Frontend Changes (v55 handler)

1. **Report-specific filter visibility**:
   - Commission: Show YearMonth, SalesGroup
   - Items by Customer: Show Date filters, Status, Customer
   - Other Excel reports: Show Date filters, Status (no Customer)

---

*Created: 2026-01-29*
