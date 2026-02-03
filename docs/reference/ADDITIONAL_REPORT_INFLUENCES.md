# Additional Report Page Influences

**Date:** 2026-01-23
**Last Updated:** 2026-01-23 (Business Rule Duplicate Debunked)
**Purpose:** Document ALL schema types beyond ClientUnit/Entity/SourceCode that could influence the Reports page

---

## Summary

Beyond the schemas documented in `PROD_PACKAGE_AUDIT.md`, the following additional schema types were found:

| Schema Type | Count | Impact on Reports | Investigation Status |
|-------------|-------|-------------------|----------------------|
| **Business Rules (AddonSchemaManager)** | **1** | Direct - Page behavior | ✅ **VERIFIED - No duplicate** |
| **Business Processes (ProcessSchemaManager)** | 10+ | Data population | Documented |
| **DCM Schemas** | 2 | Low - Case management | Documented |
| **System Settings** | 11 | Configuration | Documented |

---

## 1. Business Rules (AddonSchemaManager)

### BGUsrPage_ebkv9e8BusinessRule

| Property | Value |
|----------|-------|
| **UId** | `60ed3410-ca3e-4423-9cf5-8cc0ccc616b2` |
| **Package** | BGApp_eykaguu |
| **Modified** | 2025-07-14 |
| **ExtendParent** | false |

**Impact:** This business rule applies to the Reports page (`UsrPage_ebkv9e8`). It could contain:
- Field validation rules
- Visibility rules for UI elements
- Required field enforcement
- Conditional logic

### ✅ Investigation Complete (2026-01-23)

**Previously Documented Duplicate:** A second business rule with UId `e42d1bec-59a1-46d1-968b-8efd41a0afe6` was documented in the Custom package.

**Investigation Result:** The duplicate **DOES NOT EXIST** in PROD.

| Search | Result |
|--------|--------|
| By UId `60ed3410-ca3e-4423-9cf5-8cc0ccc616b2` | ✅ Found in BGApp_eykaguu |
| By UId `e42d1bec-59a1-46d1-968b-8efd41a0afe6` | ❌ **NOT FOUND** |
| All schemas in Custom package | ❌ **EMPTY** - No schemas |
| All AddonSchemaManager schemas | Only 1 for Reports page |

**Verified via:** `scripts/investigation/fetch_business_rule_v2.py`

**Conclusion:** v19 handler deployment has **NO RISK** of business rule conflicts.
Only one `BGUsrPage_ebkv9e8BusinessRule` exists, in the same package as the handler override.

---

## 2. Business Processes (ProcessSchemaManager)

### Commission-Related Processes

| Process Name | Caption | Modified | Impact |
|-------------|---------|----------|--------|
| **BGBPGetQuickBooksCommissions** | Get QuickBooks Commissions | 2026-01-15 | **HIGH** - Populates commission data |
| BGAddCommissionEarners | Add Commission Earners | 2024-06-07 | Creates commission earner records |
| BGAddCommissionEarnersManager | Add Commission Earner Managers | 2024-03-14 | Creates manager records |

### Report Infrastructure Processes

| Process Name | Caption | Impact |
|-------------|---------|--------|
| IntChangeAccessRightsExcelReport | Change access rights to Excel report | Report permissions |
| IntGenerateDefaultReportRights | Generate default report rights | Report permissions |
| ImportExcelDataProcess | Import Excel data | Data import |
| ImportExcelLookupProcess | Adding values to lookup during Excel import | Lookup population |

### BGBPGetQuickBooksCommissions Details

**Critical Process** - Runs regularly to pull commission data from QuickBooks.

**Recent Executions:**
| Date | Duration |
|------|----------|
| 2026-01-22 08:51 | ~51 seconds |
| 2026-01-20 19:44 | ~47 seconds |
| 2026-01-20 16:02 | ~32 seconds |

**Data Flow:**
```
QuickBooks → BGBPGetQuickBooksCommissions → BGCommissionReportQBDownload → BGCommissionReportDataView → Commission Report
```

---

## 3. DCM Schemas (DcmSchemaManager)

| Schema | Caption |
|--------|---------|
| BGCase_d945e21 | (Case process) |
| BGCustomerOrderCase | Customer Order Case |

**Impact:** Low - These manage case/order workflows, not directly related to report generation.

---

## 4. System Settings

### Report-Related Settings

| Setting Code | Type | Purpose |
|-------------|------|---------|
| ExcelExportBatchSize | Integer | Batch size for Excel exports |
| MaxImportExcelRecordCount | Integer | Max records for Excel import |
| UseExportToExcelLog | Boolean | Enable export logging |
| HasIntExcelReportMiniPageAddMode | Boolean | Excel report mini page mode |
| ReportDecimalSeparator | ShortText | Decimal symbol in printables |
| SaveWordReportAsRecordAttachment | Boolean | Save Word as attachment |

### FastReport Settings

| Setting Code | Type | Purpose |
|-------------|------|---------|
| BnzOpenFastReportFile | Boolean | Open FastReport vs download |
| BnzFastReportDataProvider | MediumText | Custom data provider |

**Impact:** These are global Creatio settings, not Pampa-specific. May affect Excel generation behavior.

---

## 5. NOT Found in Report Packages

The following schema types were checked but NOT found in the report-related packages:

| Schema Type | Manager | Status |
|-------------|---------|--------|
| Service Schemas | ServiceSchemaManager | None found |
| Classic Page Schemas | PageSchemaManager | None found |
| CSS Stylesheets | StyleSheetSchemaManager | None found |
| Process User Tasks | ProcessUserTaskSchemaManager | None found |
| Image Lists | ImageListSchemaManager | None found |
| Value Lists | ValueListSchemaManager | None found |

---

## 6. Data Dependencies

### Lookup Data (Not Schemas, but Critical)

| Entity | Records | Purpose |
|--------|---------|---------|
| UsrReportesPampa | 18 | Report definitions |
| IntExcelReport | 33 | Excel templates |
| BGYearMonth | Multiple | Year-Month filter options |
| BGSalesGroup | Multiple | Sales group filter options |
| BGReportExecution | 117 | Report execution context |

### View Dependencies (SQL-backed)

| View | Data Source | Used By |
|------|-------------|---------|
| BGCommissionReportDataView | BGCommissionReportQBDownload + Order | Commission report |
| BGSalesBySalesGroupView | Order entity | Sales by Group report |
| BGSalesByCustomerView | Order entity | Sales by Customer report |

---

## Recommendations

### ~~Immediate Actions~~ ✅ COMPLETED

1. ~~**Review BGUsrPage_ebkv9e8BusinessRule**~~
   - ✅ **COMPLETE** (2026-01-23) - No duplicate exists
   - ✅ No visibility rule conflicts detected
   - Location: BGApp_eykaguu package (same as handler)

2. **Verify BGBPGetQuickBooksCommissions**
   - Ensure this process runs successfully
   - It populates commission data needed for reports
   - ⚠️ Blocked by SYNC-004 (QB Web Connector offline)

### Before PROD Deployment

1. ~~Check that business rule doesn't override handler visibility~~ ✅ **VERIFIED - No conflict**
2. Verify IntExcelReport templates haven't changed
3. Confirm BGReportExecution records are created properly

---

## Schema UIds for Reference

| Schema | UId | Type |
|--------|-----|------|
| BGUsrPage_ebkv9e8BusinessRule | 60ed3410-ca3e-4423-9cf5-8cc0ccc616b2 | Business Rule |
| BGBPGetQuickBooksCommissions | 7b1ac959-1726-4340-bc66-210b31f5f365 | Process |
| BGAddCommissionEarners | (check SysSchema) | Process |

---

*End of Document*
