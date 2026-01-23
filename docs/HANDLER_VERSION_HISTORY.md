# Handler Version History

**Document Purpose:** Track all iterations of the UsrPage_ebkv9e8 handler for the Pampa Reports page.

**Current Production Version:** v18 (Attribute Binding)
**Schema UID:** `561d9dd4-8bf2-4f63-a781-54ac48a74972` (BGApp_eykaguu package)
**Last Updated:** 2026-01-23

---

## Version Summary Table

| Version | File | Status | Key Feature | Issue Resolved |
|---------|------|--------|-------------|----------------|
| v10 | `_v10_Production.js` | Deprecated | Initial production handler | - |
| v10 | `_v10_Diagnostic.js` | Deprecated | Added diagnostics | - |
| v11 | `_v11_Programmatic.js` | Deprecated | Programmatic visibility | - |
| v12 | `_v12_DEVStyle.js` | Deprecated | DEV-style filtering | Broke non-Commission filters |
| v13 | `_v13_ThreeWay.js` | Deprecated | Three-way filter logic | Helper functions out of scope |
| v14 | `_v14_Fixed.js` | Deprecated | Fixed helper scope | DOM manipulation issues |
| v15 | `_v15_Iframe.js` | Deprecated | Iframe for Looker | X-Frame-Options blocked |
| v16 | `_v16_NewTab.js` | Deprecated | New tab for Looker | DOM selectors not finding elements |
| v17 | `_v17_CSSBased.js` | Deprecated | CSS/label-based finding | Schema `visible:false` prevents DOM finding |
| **v18** | `_v18_AttrBinding.js` | **CURRENT** | Attribute binding for visibility | Works correctly |

---

## Version Details

### v18 - Attribute Binding (CURRENT PRODUCTION)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v18_AttrBinding.js`
**Status:** Deployed to PROD
**Date:** 2026-01-23

**Key Innovation:**
Uses Freedom UI attribute binding to control parent schema element visibility dynamically.

```javascript
// Schema merge binds parent containers to child attribute
{
    "operation": "merge",
    "name": "GridContainer_xdy25v1",  // Date filters container
    "values": {
        "visible": "$UsrShowDateStatusFilters"
    }
},
{
    "operation": "merge",
    "name": "GridContainer_knkow5v",  // Status filter container
    "values": {
        "visible": "$UsrShowDateStatusFilters"
    }
}
```

**Visibility Logic:**
| Report Type | `UsrShowCommissionFilters` | `UsrShowDateStatusFilters` | Action |
|-------------|---------------------------|---------------------------|--------|
| None selected | `false` | `false` | - |
| Commission | `true` | `false` | Excel download |
| Non-Commission Excel | `false` | `true` | Excel download |
| Looker Studio | `false` | `false` | Opens new tab |

**What Works:**
- Dynamic filter visibility based on report selection
- Commission reports show Year-Month + Sales Group filters
- Non-Commission Excel reports show Date + Status filters
- Looker reports hide all filters, open in new browser tab
- Excel template resolution via IntExcelReport lookup
- Excel download via UsrExcelReportService

**Known Limitations:**
- Looker reports open in new tab (X-Frame-Options blocks iframe)
- Some Excel reports are slow (60+ seconds for large datasets)

---

### v17 - CSS-Based Finding (Deprecated)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v17_CSSBased.js`
**Issue:** Schema-level `visible: false` causes elements to not render at all, so DOM can't find them to show later.

---

### v16 - New Tab for Looker (Deprecated)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v16_NewTab.js`
**Issue:** `data-item-marker` attribute not used by Freedom UI on container elements. DOM selectors returned 0 matches.

---

### v15 - Iframe for Looker (Deprecated)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v15_Iframe.js`
**Issue:** Looker URLs in database point to `bglobalsolutions.com` which sets `X-Frame-Options: sameorigin`, blocking iframe embedding.

---

### v14 - Fixed Helper Scope (Deprecated)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v14_Fixed.js`
**Issue:** DOM manipulation approach doesn't reliably find elements.

---

### v13 - Three-Way Filter Logic (Deprecated)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v13_ThreeWay.js`
**Issue:** Helper functions defined outside `define()` scope, causing "function not defined" errors.

---

### v12 - DEV Style (Deprecated)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v12_DEVStyle.js`
**Issue:** Broke non-Commission Excel reports by hiding Date/Status filters permanently.

---

## Key Learnings

### Freedom UI Schema Inheritance
1. Parent schemas use `viewModelConfig` (base definition)
2. Child schemas use `viewModelConfigDiff` (extends parent)
3. Child can merge properties onto parent elements
4. Attribute bindings like `visible: "$Attribute"` work cross-schema if attribute is defined in merged viewModelConfigDiff

### DOM Manipulation vs Attribute Binding
- **DOM manipulation fails** when `visible: false` is set at schema level (elements don't render)
- **Attribute binding works** because Freedom UI handles reactivity internally
- Always prefer attribute binding for dynamic visibility in Freedom UI

### Element Discovery in Freedom UI
- `data-item-marker` is NOT consistently used on container elements
- Freedom UI uses CSS classes like `crt-input-label-container`, `crt-flex-item`
- Container elements from parent schema may not have predictable selectors

---

## Deployment

**Schema Designer URL:**
```
https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
```

**After deploying:**
1. Save and compile schema
2. Hard refresh browser (`Ctrl+Shift+R`)
3. Verify `[v18]` appears in console
4. Test report selection to verify filter visibility

---

## Related Files

| Purpose | Location |
|---------|----------|
| Parent schema reference | `client-module/BGlobalLookerStudio_UsrPage_ebkv9e8_Fixed.js` |
| Backend service | `source-code/UsrExcelReportService_Updated.cs` |
| Filter requirements | `docs/REPORT_FILTER_MAPPING.md` |
| Testing checklist | `docs/REPORT_TESTING_CHECKLIST.md` |
