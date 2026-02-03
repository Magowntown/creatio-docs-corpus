# BGSalesByItemLineView Schema Analysis

**Date:** 2026-01-29
**Source:** PROD pgAdmin query

---

## Column Structure

| Column | Data Type | Notes |
|--------|-----------|-------|
| BGAmount | numeric | Order line amount |
| BGCustomer | character varying | Customer name |
| BGCustomerType | character varying | Customer type lookup |
| BGDeliveryDate | date | Delivery date |
| BGDescription | text | **Product description** (different from BGProductDescription) |
| BGExecutionId | uuid | **Type A view** - requires BGReportExecution |
| BGFilters | text | Execution filter metadata |
| BGItem | character varying | Product code/name |
| BGLine | character varying | Product line grouping |
| BGNumber | character varying | Order number |
| BGNumberInvoice | character varying | Invoice number |
| BGPONumber | character varying | PO number |
| BGPrice | numeric | Unit price |
| BGQuantity | integer | Quantity |
| BGReportEndDate | timestamp without time zone | Execution end date filter |
| BGReportStartDate | timestamp without time zone | Execution start date filter |
| BGSalesGroup | character varying | Sales group name |
| BGSalesRep | character varying | Sales rep name |
| BGShipDate | date | Ship date |
| BGStatus | character varying | Order status |
| CreatedById | uuid | Creatio audit |
| CreatedOn | timestamp without time zone | Order creation date |
| Id | uuid | Primary key |
| ModifiedById | uuid | Creatio audit |
| ModifiedOn | timestamp without time zone | Creatio audit |
| ProcessListeners | integer | Creatio internal |

---

## Key Findings

### 1. This is a Type A (Execution-Based) View

The presence of these columns indicates execution-based filtering:
- `BGExecutionId` - Links to BGReportExecution table
- `BGFilters` - Stores filter metadata
- `BGReportStartDate` / `BGReportEndDate` - Date range from execution

**Implication:** Reports using this view require BGReportExecution records to be created before generating data.

### 2. Product Description Column Name

- Uses `BGDescription` (not `BGProductDescription`)
- Backend code may need to map to correct column name

### 3. Additional Columns vs BGSalesByItemView

| Column | BGSalesByItemLineView | BGSalesByItemView |
|--------|----------------------|-------------------|
| BGDescription | ✅ Yes (text) | ❌ No (added BGProductDescription) |
| BGExecutionId | ✅ Yes | ❌ No |
| BGFilters | ✅ Yes | ❌ No |
| BGReportStartDate | ✅ Yes | ❌ No |
| BGReportEndDate | ✅ Yes | ❌ No |
| BGLine | ✅ Yes | ❌ No |
| BGCustomerType | ✅ Yes | ❌ No |
| BGNumberInvoice | ✅ Yes | ❌ No |

### 4. Employee JOIN Status

Previously verified: Uses correct pattern
```sql
JOIN "Employee" e ON o."BGSalesRepLookupId" = e."Id"
```
No duplicate row issue.

---

## PROD Report Configuration

These reports use BGSalesByItemLineView (confirmed 2026-01-29):

| Report | View | Type |
|--------|------|------|
| Rpt Sales by Item Line | BGSalesByItemLineView | Execution-Based |
| Rpt Sales By Item | BGSalesByItemLineView | Execution-Based |
| Rpt Sales By Item By Type Of Customer | BGSalesByItemLineView | Execution-Based |

---

## VBA Type Mismatch Analysis

Possible causes for VBA Runtime Error '13' Type mismatch:

1. **BGExecutionId filtering** - If no execution record exists, view returns no/wrong data
2. **Column order mismatch** - IntExcelExport may return columns in different order than VBA expects
3. **NULL values** - Some columns may have NULL where VBA expects numbers
4. **Data type difference** - `BGQuantity` is `integer`, `BGAmount`/`BGPrice` are `numeric`

---

## Recommended Investigation

1. Check if BGReportExecution records exist for these reports
2. Compare IntExcelExport column output order vs VBA expectations
3. Test report with sample data to capture actual Excel output

---

*Created: 2026-01-29*
