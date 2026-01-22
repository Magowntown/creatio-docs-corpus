# Report Filter Mapping

**Date:** 2026-01-22
**Purpose:** Define filter requirements for each report in UsrReportesPampa lookup

---

## Summary

The Reports page has **18 reports** with different filter requirements:
- **12 Looker Studio reports** - Use date/status/lookup filters passed as URL parameters
- **6 Excel-only reports** - Use UsrExcelReportService with IntExcelReport templates

### The Problem

The Hybrid_v2 handler (deployed to PROD) incorrectly:
1. **REMOVES** `GridContainer_knkow5v` (Status filter container) - breaks non-Commission reports
2. **REMOVES** `ComboBox_8w0dlcf` (Status dropdown) - breaks non-Commission reports
3. **HIDES** all date filters unconditionally - breaks non-Commission reports
4. **SHOWS** Year-Month and Sales Group filters for ALL reports - wrong for non-Commission

### The Solution

The v4 Minimal handler:
1. Does NOT remove any existing UI elements
2. Only ADDS Commission-specific filters (Year-Month, Sales Group)
3. Controls visibility via `$UsrShowCommissionFilters` attribute
4. Detects Commission reports by name pattern (`reportName.includes("commission")`)

---

## Filter Elements Inventory

### Original Page Filters (Parent Schema)

| Element Name | Type | Attribute | Purpose | Used By |
|-------------|------|-----------|---------|---------|
| `ComboBox_8w0dlcf` | crt.ComboBox | `LookupAttribute_tytkx09` | Status Order filter | Looker Studio reports |
| `GridContainer_knkow5v` | crt.GridContainer | - | Container for Status filter | Looker Studio reports |
| `CreatedFrom` | Date | `CreatedFrom` | Created date range start | Looker Studio reports |
| `CreatedTo` | Date | `CreatedTo` | Created date range end | Looker Studio reports |
| `ShippingFrom` | Date | `ShippingFrom` | Ship date range start | Looker Studio reports |
| `ShippingTo` | Date | `ShippingTo` | Ship date range end | Looker Studio reports |
| `DeliveryFrom` | Date | `DeliveryFrom` | Delivery date range start | Looker Studio reports |
| `DeliveryTo` | Date | `DeliveryTo` | Delivery date range end | Looker Studio reports |
| `LookupAttribute_4ufq0og` | Lookup | Theme | Theme filter | Some Looker reports |
| `LookupAttribute_houdnx9` | Lookup | Sales Rep | Sales Rep filter | Some Looker reports |
| `LookupAttribute_c4ubvuy` | Lookup | Customer Type | Customer Type filter | Some Looker reports |

### Commission-Specific Filters (Added by v4 Handler)

| Element Name | Type | Attribute | Purpose | Used By |
|-------------|------|-----------|---------|---------|
| `BGYearMonth` | crt.ComboBox | `LookupAttribute_YearMonth` | Year-Month filter | Commission, IW_Commission |
| `BGSalesGroup` | crt.ComboBox | `LookupAttribute_SalesGroup` | Sales Group filter | Commission, IW_Commission |
| `BGCommissionWarning` | crt.Label | - | Warning about QB data | Commission, IW_Commission |
| `GridContainer_CommissionFilters` | crt.GridContainer | - | Container for Commission filters | Commission, IW_Commission |

---

## Report-by-Report Analysis

### Excel-Only Reports (No Looker URL)

| Report Name | Filter Needs | Notes |
|-------------|--------------|-------|
| **Commission** | Year-Month, Sales Group | QB-synced data, uses BGCommissionReportDataView |
| **IW_Commission** | Year-Month, Sales Group | InterWeave payments data, uses IWCommissionReportDataView |
| **Customers did not buy over period** | Date filters (CreatedFrom/To) | Order entity data |
| **Items by Customer** | Date filters | Order entity data, has template issues (RPT-004) |
| **Sales By Item** | Date filters | Order entity data |
| **Sales By Item By Type Of Customer** | Date filters, Customer Type | Order entity data |

### Looker Studio Reports (Have UsrURL)

| Report Name | Filter Needs | Notes |
|-------------|--------------|-------|
| Sales By Customer | Status, Dates, Customer Type | Opens in new tab |
| Sales By Sales Group | Status, Dates, Sales Group | Opens in new tab |
| Sales By Customer Type | Status, Dates, Customer Type | Opens in new tab |
| Sales Rep Monthly Report | Status, Dates, Sales Rep | Opens in new tab |
| Sales By Sales Rep | Status, Dates, Sales Rep | Opens in new tab |
| Sales By Line With Ranking | Status, Dates | Opens in new tab |
| Sales By Line | Status, Dates | Opens in new tab |
| (And 5 more similar reports) | Status, Dates, various lookups | Opens in new tab |

---

## Filter Visibility Rules

### Decision Logic

```javascript
if (report.name.toLowerCase().includes("commission")) {
    // Commission reports (Commission, IW_Commission)
    showCommissionFilters = true;  // Year-Month, Sales Group
    // Original filters remain visible (no removal)
    // Note: Original filters are irrelevant for Commission
    //       but removing them breaks other reports
} else {
    // All other reports
    showCommissionFilters = false; // Hide Year-Month, Sales Group
    // Original filters remain visible and functional
}
```

### Filter Visibility Matrix

| Report Type | Status | Date Filters | Theme/SalesRep/CustType | Year-Month | Sales Group |
|-------------|--------|--------------|-------------------------|------------|-------------|
| **Commission** | Visible (ignored) | Visible (ignored) | Visible (ignored) | **VISIBLE** | **VISIBLE** |
| **IW_Commission** | Visible (ignored) | Visible (ignored) | Visible (ignored) | **VISIBLE** | **VISIBLE** |
| **Looker Reports** | **ACTIVE** | **ACTIVE** | **ACTIVE** | Hidden | Hidden |
| **Other Excel** | **ACTIVE** | **ACTIVE** | **ACTIVE** | Hidden | Hidden |

---

## Implementation in v4 Minimal Handler

### Key Design Principles

1. **Non-Destructive:** Never remove or hide existing UI elements
2. **Additive Only:** Only add Commission-specific filters
3. **Conditional Visibility:** Use attribute binding for Commission filters
4. **Original Selector:** Use existing `LookupAttribute_0as4io2` (not a new one)

### viewConfigDiff Operations

```javascript
// ONLY these operations - no removal!
[
    // Hide Looker iframe (CSP blocks it anyway)
    { "operation": "merge", "name": "GridContainer_fh039aq", "values": { "visible": false } },

    // Wire report button to hybrid handler
    { "operation": "merge", "name": "Button_vae0g6x", "values": { "clicked": { "request": "usr.GenerateReportRequest" } } },

    // INSERT Commission warning label (conditional visibility)
    { "operation": "insert", "name": "BGCommissionWarning", "values": { "visible": "$UsrShowCommissionFilters" } },

    // INSERT Commission filter container (conditional visibility)
    { "operation": "insert", "name": "GridContainer_CommissionFilters", "values": { "visible": "$UsrShowCommissionFilters" } },

    // INSERT Year-Month filter (inside Commission container)
    { "operation": "insert", "name": "BGYearMonth", "parentName": "GridContainer_CommissionFilters" },

    // INSERT Sales Group filter (inside Commission container)
    { "operation": "insert", "name": "BGSalesGroup", "parentName": "GridContainer_CommissionFilters" }
]
```

### Handler Logic

```javascript
// crt.HandleViewModelAttributeChangeRequest handler
if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
    const selectedReport = await request.$context.LookupAttribute_0as4io2;
    if (selectedReport && selectedReport.displayValue) {
        const reportName = selectedReport.displayValue.toLowerCase();
        const isCommissionReport = reportName.includes("commission");

        // Only toggle Commission filter visibility
        request.$context.UsrShowCommissionFilters = isCommissionReport;

        // Clear Commission filters when switching
        if (isCommissionReport) {
            request.$context.LookupAttribute_YearMonth = null;
            request.$context.LookupAttribute_SalesGroup = null;
        }
    }
}
```

---

## Handler Version Comparison

| Feature | v2 (Hybrid) | v3 (Conditional) | v4 (Minimal) |
|---------|-------------|------------------|--------------|
| Removes Status filter | ✅ YES (broken) | ❌ NO | ❌ NO |
| Removes Status dropdown | ✅ YES (broken) | ❌ NO | ❌ NO |
| Hides date filters | ✅ YES (broken) | Conditional | ❌ NO |
| Commission filters | Always visible | Conditional | Conditional |
| Uses original selector | ❌ NO (new one) | ✅ YES | ✅ YES |
| Non-destructive | ❌ NO | ⚠️ Partial | ✅ YES |

**Recommendation:** Deploy v4 Minimal handler to fix the issue.

---

## Files Reference

| File | Purpose |
|------|---------|
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js` | Current PROD (broken) |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v3.js` | Conditional visibility approach |
| `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v4_Minimal.js` | **RECOMMENDED** - Minimal non-destructive |
| `client-module/BGlobalLookerStudio_UsrPage_ebkv9e8_Fixed.js` | Original parent schema (reference) |

---

## Testing Checklist

### Commission Reports
- [ ] Commission report shows Year-Month and Sales Group filters
- [ ] Commission report filters work correctly
- [ ] Commission Excel downloads successfully

### Looker Studio Reports
- [ ] Sales By Line shows Status filter
- [ ] Sales By Line shows date filters
- [ ] Sales By Line does NOT show Year-Month filter
- [ ] Sales By Line does NOT show Sales Group filter
- [ ] Report opens in new tab correctly

### Other Excel Reports
- [ ] Items by Customer shows appropriate filters
- [ ] Customers did not buy shows date filters
- [ ] All Excel downloads work

---

*Created: 2026-01-22*
