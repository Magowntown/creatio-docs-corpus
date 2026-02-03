# BGReportExecution Entity Schema

**Entity:** BGReportExecution  
**UId:** `9467fd8d-64ad-40bf-8da8-8496c3392a7c`  
**Caption:** Report Execution  
**Queried:** 2026-01-23 from PROD (pampabay.creatio.com)

---

## Overview

The `BGReportExecution` entity stores filter parameters for report generation. When a user requests a report, a record is created with the selected filter values, which are then used by the backend Excel report service.

**Total Records:** 117  
**Used by Reports:** Commission, Sales By Sales Group, Sales By Customer, Sales Rep Monthly Report, Sales By Customer Type, Sales By Item By Type Of Customer, Customers did not buy over a period of time

---

## Column Schema

| Column Name | Data Type | Lookup Entity | Required | Description |
|-------------|-----------|---------------|----------|-------------|
| **Id** | GUID (0) | - | Yes | Primary key |
| **CreatedOn** | DateTime (7) | - | Yes | Record creation timestamp |
| **CreatedBy** | Lookup (10) | Contact | Yes | User who created the record |
| **ModifiedOn** | DateTime (7) | - | Yes | Last modification timestamp |
| **ModifiedBy** | Lookup (10) | Contact | Yes | User who last modified |
| **ProcessListeners** | Integer (4) | - | No | Process listeners count |
| **BGUserId** | GUID (0) | - | No | User executing the report |
| **BGReportName** | Text (1) | - | Yes | Report identifier/name |
| **BGCreatedFrom** | DateTime (7) | - | No | Order created date range start |
| **BGCreatedTo** | DateTime (7) | - | No | Order created date range end |
| **BGShippingFrom** | DateTime (7) | - | No | Shipping date range start |
| **BGShippingTo** | DateTime (7) | - | No | Shipping date range end |
| **BGDeliveryFrom** | DateTime (7) | - | No | Delivery date range start |
| **BGDeliveryTo** | DateTime (7) | - | No | Delivery date range end |
| **BGDate** | DateTime (7) | - | No | Single date filter |
| **BGOrderStatus** | Lookup (10) | UsrStatus | No | Order status filter |
| **BGSalesGroup** | Lookup (10) | BGSalesGroup | No | Sales group filter |
| **BGYearMonth** | Lookup (10) | BGYearMonth | No | Year-month period filter |
| **BGTheme** | Lookup (10) | BGProductThemeLookup | No | Product theme filter |
| **BGCustomerType** | Lookup (10) | BGCustomerTypeLookup | No | Customer type filter |
| **BGSalesRep** | Lookup (10) | Employee | No | Sales representative filter |
| **BGCustomer** | Lookup (10) | Account | No | Customer account filter |

---

## Commission Report Usage

For **Commission** reports, the key filters are:

| Filter | Column | Required |
|--------|--------|----------|
| Year-Month | `BGYearMonth` | **Yes** |
| Sales Group | `BGSalesGroup` | Optional |

### Sample Commission Record

```json
{
  "Id": "428c36fa-8fc9-4f07-880e-5364a34b282a",
  "BGReportName": "Commission",
  "BGUserId": "7f3b869f-34f3-4f20-ab4d-7480a5fdf647",
  "BGYearMonth": {
    "value": "72314c1e-8740-4384-b7e1-62c5d07ff7eb",
    "displayValue": "2024-11"
  },
  "BGSalesGroup": "",
  "BGCreatedFrom": "",
  "BGCreatedTo": "",
  // ... other filters empty
}
```

### Sample Commission with Sales Group Filter

```json
{
  "Id": "2c3c672a-6e01-49ef-9997-6aaa6d6bc7ea",
  "BGReportName": "Commission",
  "BGYearMonth": {
    "value": "98dd7c3b-3a38-47a2-8670-219748699ac2",
    "displayValue": "2024-12"
  },
  "BGSalesGroup": {
    "value": "edfefb79-77b6-43fe-932b-c012d9a2fc9d",
    "displayValue": "RDGZ & Consulting LLC"
  }
}
```

---

## Data Value Types Reference

| Type Code | Type Name |
|-----------|-----------|
| 0 | GUID |
| 1 | Text |
| 4 | Integer |
| 7 | DateTime |
| 10 | Lookup |

---

## Lookup Entity References

| Column | Entity | Notes |
|--------|--------|-------|
| BGOrderStatus | UsrStatus | Custom order status lookup |
| BGSalesGroup | BGSalesGroup | Sales group/team |
| BGYearMonth | BGYearMonth | Period lookup (YYYY-MM format) |
| BGTheme | BGProductThemeLookup | Product theme categories |
| BGCustomerType | BGCustomerTypeLookup | Customer classification |
| BGSalesRep | Employee | System employee entity |
| BGCustomer | Account | System account entity |

---

## Notes

1. **IW_Commission** reports do not yet have records in this table (0 records found)
2. Commission reports primarily use `BGYearMonth` filter (required)
3. `BGSalesGroup` is optional for Commission reports
4. Date range filters (`BGCreatedFrom/To`, `BGShippingFrom/To`, `BGDeliveryFrom/To`) are used by non-Commission reports
5. The `BGUserId` stores the SysAdminUnit ID of the user executing the report
