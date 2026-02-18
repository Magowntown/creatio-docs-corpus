# SQL Directory

> SQL view definitions and fixes for the Creatio reporting system.

## Files

| File | Purpose | Status |
|------|---------|--------|
| `VwBGSalesByItemView_ORIGINAL.sql` | Original view from PampaBay PROD | Reference |
| `VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql` | Fixed employee JOIN (26x duplicate fix) | ✅ Fix |
| `VwBGSalesByItemView_FIXED_MULTILINE.sql` | Multiline formatting | Reference |
| `VwBGSalesByItemView_FINAL.sql` | Final consolidated fix | ✅ Deployed |
| `VwBGSalesByItemView_REPLACE.sql` | REPLACE variant | Reference |
| `VwBGSalesByItemView_DEV_DEPLOY.sql` | DEV deployment variant | Reference |
| `VwBGSalesByItemView_SQLSCRIPT_FINAL.sql` | Final SQL script | Reference |
| `BGSalesByItemView_fix.sql` | Consolidated fix | Reference |
| `ALL_VIEWS_ADD_PRODUCT_DESCRIPTION.sql` | Add BGProductDescription across views | Enhancement |
| `BGCommissionReportDataView.sql` | Commission report data source | Reference |
| `BGCustomerDidNotBuyView_ORIGINAL.sql` | Customers Did Not Buy view | Reference |

## Fix History

### RPT-007: 26x Duplicate Rows
**File:** `VwBGSalesByItemView_FIXED_EMPLOYEE_JOIN.sql`

**Problem:** Employee JOIN caused 26x row multiplication
**Fix:** Corrected JOIN conditions to eliminate duplicates

### RPT-006: Missing Product Description
**File:** `ALL_VIEWS_ADD_PRODUCT_DESCRIPTION.sql`

**Problem:** DESCRIPCION column showing wrong data
**Fix:** Added BGProductDescription column to multiple views

## Usage

```sql
-- Deploy view fix to Creatio
-- 1. Connect to Creatio database
-- 2. Run the appropriate SQL file
-- 3. Verify with SELECT COUNT(*) queries
```

## Related Documentation

- `docs/reference/MASTER_CATALOG.md` - View catalog
- `docs/investigation/BGLOBAL_V7_ARCHITECTURE_COMPLETE.md` - V7 architecture
- `docs/issues/RPT007_*.md` - Specific issue documentation
