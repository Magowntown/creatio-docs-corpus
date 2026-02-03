# Creatio Support Email Draft

**Date:** 2026-01-28
**Environment:** dev-pampabay.creatio.com (Development), pampabay.creatio.com (Production)
**Creatio Version:** Freedom UI (v8)
**Package:** BGApp_eykaguu (extends BGlobalLookerStudio)

---

## Subject: Custom Reports Page Not Functioning After Freedom UI Migration - Request for Rollback/Fix Guidance

---

## Email Body

Dear Creatio/BGlobal Support Team,

We are experiencing critical issues with our custom reports page (`UsrPage_ebkv9e8`) after migrating from Classic UI (v7) to Freedom UI (v8). The reports functionality has been broken for approximately 3+ weeks, affecting business operations.

### Our Goals

We need the reports page to fully function with:

1. **Looker Studio Reports:**
   - Embedded in iframe on the page (not opening in new tab)
   - Date filters passed as URL parameters
   - Status filter passed as URL parameter

2. **Excel Reports (Commission, Items by Customer, etc.):**
   - Dynamic filter visibility based on selected report type
   - Commission reports: Year-Month (lookup) + Sales Group (lookup) filters
   - Items by Customer: Customer (lookup) + Date range filters
   - Other reports: Date range + Status filters
   - Excel file generation and download

### Summary of Issues

1. **"Items by Customer" Report Not Generating**
   - Error: `ArgumentNullException: Value cannot be null (Parameter 'value')`
   - Stack trace points to: `IntExcelExport.Utilities.ReportUtilities.GenerateReport`
   - This report has **0 records in BGReportExecution** - we believe it may have never worked properly

2. **Localized Resource String Errors**
   - Error: `Localized resource string not found. MainDS_Name`
   - Appears related to parent schema configuration (BGPage_iaptpa6)

3. **ComboBox Lookup Binding Issues**
   - Year-Month and Sales Group lookups work when bound to existing page data source
   - Customer lookup requires binding to Account entity, which requires adding a separate data source
   - Multiple approaches attempted without success

4. **Looker Studio Iframe Embedding**
   - SecurityError with cross-origin frames and sandboxed cookies
   - Parent schema has `UsrIframe` component but binding is problematic

### Technical Details

**Schema Hierarchy:**
```
UsrPage_ebkv9e8 (BGApp_eykaguu package)
  └── extends BGPage_iaptpa6 (BGlobalLookerStudio package)
      └── extends base page
```

**Key Schema Elements:**
- Report dropdown: `LookupAttribute_0as4io2`
- Date filters: `CreatedFrom`, `CreatedTo`
- Status filter: `LookupAttribute_tytkx09`
- Iframe container: `GridContainer_fh039aq` containing `UsrIframe`

**Working Filters (from v19.13 pattern):**
```javascript
"UsrYearMonth": {
    "modelConfig": {
        "path": "UsrEntity_e7ac661DS.BGYearMonth"
    }
}
```

**Non-Working Customer Lookup Attempt:**
```javascript
// Tried adding Account data source
modelConfigDiff: [{
    "operation": "merge",
    "path": [],
    "values": {
        "dataSources": {
            "UsrCustomerDS": {
                "type": "crt.EntityDataSource",
                "scope": "viewElement",
                "config": {
                    "entitySchemaName": "Account"
                }
            }
        }
    }
}]
```

### Approaches Attempted

| Approach | Result |
|----------|--------|
| viewModelConfigDiff array format with existing data source | Commission filters (YearMonth, SalesGroup) work |
| Adding Account entity data source for Customer lookup | Customer ComboBox doesn't populate |
| Iframe embedding with parent's UsrIframe component | SecurityError with cross-origin/sandboxed cookies |
| Various visibility binding patterns | Mixed results - some work, some don't |

### Backend Service

We created `UsrExcelReportService` to replace the missing original flow:
- Reads `IntExcelReport` templates
- Uses `ClosedXML` for Excel generation
- Creates `BGReportExecution` records for filtering
- Calls `IntExcelExport.Utilities.ReportUtilities.GenerateReport`

The backend error occurs inside `IntExcelExport` library, not our custom code.

### Questions for Support

1. **Looker Studio Iframe Embedding:** What is the correct Freedom UI pattern to embed Looker Studio reports in an iframe on the page with dynamic URL parameters for filtering?

2. **External Entity Lookups:** What is the correct Freedom UI pattern to create a ComboBox lookup to an entity (like Account) that isn't in the page's primary data source?

3. **Items by Customer Report:** This report has 0 BGReportExecution records and throws `ArgumentNullException` in `IntExcelExport.Utilities.ReportUtilities`. Was it ever properly configured? What's missing?

4. **Original BGlobal Flow:** The original reports used `IntGenerateExcelReportUserTask` (GUID: `05c5265c-3f51-4114-9862-fc434abe1f6d`) business process. Can this be triggered from Freedom UI, or is there a recommended replacement?

5. **Rollback Option:** If a fix isn't feasible, is there a way to rollback to the Classic UI version of this reports page?

6. **Parent Schema Issues:** The `MainDS_Name` resource string error suggests configuration issues in parent schema (BGPage_iaptpa6). What should we check?

### Files Available

We can provide:
- Handler code iterations and approaches attempted
- Session logs documenting every approach
- Backend `UsrExcelReportService.cs` source code
- Browser console logs showing errors
- Database queries showing BGReportExecution configuration

### Current State vs Goals

| Feature | Goal | Current State |
|---------|------|---------------|
| Looker Studio reports | Embedded iframe with filter params | Opens in new tab only |
| Commission reports | YearMonth + SalesGroup lookups | Working |
| Items by Customer | Customer lookup + Date filters | Not generating (backend error) |
| Customer filter | ComboBox lookup to Account | Doesn't populate |
| Other Excel reports | Date + Status filters | Partially working |

**Business Impact:** Staff unable to generate critical business reports for 3+ weeks.

### Contact

Our ultimate goal is to have:
- **Looker Studio reports** fully embedded with filtering
- **Excel reports** (Commission, Items by Customer, etc.) generating with their respective lookup filters

Please advise on the best path forward - whether that's specific Freedom UI patterns, configuration fixes, or a rollback to Classic UI.

Thank you for your assistance.

Best regards,
[Your Name]
[Company]

---

## Attachments to Include

1. `docs/HANDLER_VERSION_HISTORY.md` - All version attempts
2. `docs/SESSION_LOG_20260128.md` - Detailed session notes
3. Console error screenshots
4. `source-code/UsrExcelReportService_Updated.cs` - Backend code

---

## Key Technical Notes for Call/Follow-up

### BGReportExecution Configuration
```sql
-- Check existing configuration
SELECT * FROM "BGReportExecution" WHERE "BGReportName" LIKE '%Items%Customer%';
-- Result: 0 records

-- Check IntExcelReport setup
SELECT "Id", "IntName", "IntEntitySchemaName", "IntEsq"
FROM "IntExcelReport"
WHERE "IntName" LIKE '%Items%Customer%';
```

### IntGenerateExcelReportUserTask
- GUID: `05c5265c-3f51-4114-9862-fc434abe1f6d`
- Status: Exists in PROD
- Issue: Classic UI mixin (`BGIntExcelreportMixin`) triggered it; mixins don't work in Freedom UI

### Working Pattern (v19.13)
```javascript
viewModelConfigDiff: [
    {
        "operation": "merge",
        "path": ["attributes"],
        "values": {
            "UsrYearMonth": {
                "modelConfig": {
                    "path": "UsrEntity_e7ac661DS.BGYearMonth"
                }
            }
        }
    }
]
```

### What We Need From Support
1. **Looker Studio iframe embedding pattern** - How to embed with dynamic filter parameters
2. **External entity lookup pattern** - How to bind ComboBox to Account entity
3. **Items by Customer fix** - Why IntExcelExport throws ArgumentNullException
4. **IntGenerateExcelReportUserTask guidance** - Can it work in Freedom UI?
5. **Parent schema resource string fix** - MainDS_Name error
6. **Rollback procedure** - If fixes aren't feasible
