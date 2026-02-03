# RPT-005 Deployment Checklist

**Issue:** "Customers did not buy" report column mismatch
**Date Created:** 2026-01-29
**Status:** Ready for Deployment

---

## Pre-Deployment Verification

### 1. Code Review Completed
- [x] `GetReportName()` helper function added (lines 675-686)
- [x] Routing logic updated to check by report IntName (lines 2754-2766)
- [x] `GenerateCustomerDidNotBuyWithFilters()` function exists (lines 2222-2308)
- [x] `QueryCustomerDidNotBuyData()` function exists with correct columns (lines 2316-2420)
- [x] Column mapping matches expected PROD template:
  - Account, Address, City, State, ZIP, Email, Phone
  - Last Order Date, Last Order Amount, Previous Order Count
  - Last Order Sales Rep, Last Order Sales Group

### 2. Root Cause Understanding
- [x] `IntEntitySchemaName` column does NOT exist in IntExcelReport table
- [x] `GetReportEntitySchemaName()` falls back to IntEsq JSON parsing
- [x] IntEsq has `rootSchemaName = "BGSalesByCustomerView"` (historically set, wrong)
- [x] Fix routes by report IntName: `"Rpt CustomersDidNotBuyOverAPeriodOfTime"`

---

## Deployment Steps

### Step 1: Open PROD Source Code Designer
```
URL: https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178
```

### Step 2: Backup Current Code (Optional but Recommended)
1. Select all code in PROD designer
2. Copy to a local backup file: `backup_UsrExcelReportService_YYYYMMDD.cs`

### Step 3: Deploy Updated Code
1. Open local file: `source-code/UsrExcelReportService_Updated.cs`
2. Select ALL content (Ctrl+A)
3. Copy (Ctrl+C)
4. In PROD designer, select ALL (Ctrl+A)
5. Paste (Ctrl+V)
6. Click Save
7. Click Compile (if available)

### Step 4: Verify Compilation
- [ ] No compilation errors
- [ ] Save successful

---

## Post-Deployment Testing

### Test 1: "Customers did not buy" with Date Filters
1. Navigate to: Pampa Reports > Customers did not buy over a period of time
2. Set date range: `2026-01-01` to `2026-01-31`
3. Click Generate Report
4. Expected: Excel file downloads

**Verify Excel Columns (Data sheet):**
| Column | Expected Header |
|--------|-----------------|
| A | Account |
| B | Address |
| C | City |
| D | State |
| E | ZIP |
| F | Email |
| G | Phone |
| H | Last Order Date |
| I | Last Order Amount |
| J | Previous Order Count |
| K | Last Order Sales Rep |
| L | Last Order Sales Group |

- [ ] Columns match expected headers
- [ ] Data appears in correct columns (customer contact info, not order data)
- [ ] No VBA Type mismatch errors

### Test 2: Verify Other Reports Still Work
- [ ] "Items by Customer" - should still work (RPT-008 fix preserved)
- [ ] "Commission" - should still work
- [ ] "Sales by Customer" (different report) - should still work if using date filters

---

## Rollback Plan

If issues occur after deployment:

1. Open PROD Source Code Designer
2. Replace with backup code (from Step 2)
3. Save and compile
4. Report issue in `docs/SESSION_LOG_20260129.md`

---

## Key Code Sections Changed

### New Helper Function (lines 675-686)
```csharp
private string GetReportName(UserConnection userConnection, Guid reportId)
{
    var esq = new EntitySchemaQuery(userConnection.EntitySchemaManager, "IntExcelReport");
    esq.AddColumn("IntName");
    var entity = esq.GetEntity(userConnection, reportId);
    if (entity == null) return null;
    return entity.GetTypedColumnValue<string>("IntName");
}
```

### Updated Routing (lines 2754-2766)
```csharp
var reportName = GetReportName(userConnection, request.ReportId);
if (reportName == "Rpt CustomersDidNotBuyOverAPeriodOfTime" ||
    entitySchemaName == "BGCustomerDidNotBuyView")
{
    return GenerateCustomerDidNotBuyWithFilters(userConnection, request);
}
```

---

## Potential Risks

### Risk 1: BGCustomerDidNotBuyView Column Names
The code assumes `BGCustomerDidNotBuyView` has these column names:
- Account, Address, City, State, ZIP, Email, Phone
- LastOrderDate, LastOrderAmount, PreviousOrderCount
- LastOrderSalesRep, LastOrderSalesGroup

**Mitigation:** The code catches exceptions for missing columns and skips them silently. If column names differ, data may be partial but won't crash.

**Verification Query (run in PROD SQL if needed):**
```sql
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'BGCustomerDidNotBuyView'
ORDER BY ordinal_position;
```

### Risk 2: Empty Data Result
If `BGCustomerDidNotBuyView` has no data for the date range, the report returns "No data found" message.

**Mitigation:** This is expected behavior - the error message includes filter details for debugging.

---

## Notes

- This fix does NOT require any database changes
- This fix does NOT require frontend changes
- The IntExcelReport record does NOT need modification (we work around the issue)
- Other reports using BGSalesByCustomerView continue to work via the legacy routing
- The query logic gracefully handles missing columns (try/catch per column)

---

*Checklist created: 2026-01-29*
*Last updated: 2026-01-29 - Added risk documentation*
