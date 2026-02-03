# Creatio Support Request: Freedom UI Reports Page Issues

**To:** Creatio Support
**From:** [Customer/Partner Name]
**Subject:** Custom Reports Page Broken After Freedom UI (v8) Migration - IntExcelExport + Handler Issues
**Priority:** High
**Environment:** pampabay.creatio.com (PROD) / dev-pampabay.creatio.com (DEV)

---

## Executive Summary

After migrating from Creatio Classic UI (v7) to Freedom UI (v8), our custom Reports page has multiple issues related to:
1. **Frontend Handler** - Freedom UI schema changes break our custom handler
2. **IntExcelExport Package** - Integration issues with new data binding patterns
3. **Filter Visibility/Data Binding** - Freedom UI's reactive attribute system behaves differently
4. **Data View Resolution** - Backend code fails to resolve lookup column values correctly

We have invested significant effort (20+ handler versions) to resolve these issues. We are sharing our findings and requesting guidance on best practices for Freedom UI custom page development.

---

## Environment Details

| Component | Version/Details |
|-----------|-----------------|
| Creatio Version | Freedom UI (v8) |
| PROD URL | https://pampabay.creatio.com |
| DEV URL | https://dev-pampabay.creatio.com |
| Custom Package | BGApp_eykaguu |
| Parent Schema | BGlobalLookerStudio_UsrPage_ebkv9e8 |
| Child Handler Schema | UsrPage_ebkv9e8 (UID: 561d9dd4-8bf2-4f63-a781-54ac48a74972) |
| Backend Service | UsrExcelReportService (UID: a1e1ff91-d182-4339-ac79-dd011029be26) |
| Excel Export Package | IntExcelExport (third-party) |

---

## Issues Encountered

### Issue 1: Filter Visibility Not Working (RESOLVED)

**Problem:** After v8 migration, date/status filters were hidden for non-Commission reports. DOM manipulation approaches that worked in v7 failed in Freedom UI because:
- `visible: false` at schema level prevents DOM rendering entirely
- `data-item-marker` attributes not consistently applied to containers
- CSS selectors cannot find elements that aren't rendered

**Our Solution:** Use Freedom UI's attribute binding pattern:
```javascript
// viewConfigDiff - bind parent container to child attribute
{
    "operation": "merge",
    "name": "GridContainer_xdy25v1",  // Parent's date filter container
    "values": {
        "visible": "$UsrShowDateStatusFilters"  // Child's attribute
    }
}
```

**Request:** Is this the recommended pattern for controlling parent schema element visibility from a child schema? Are there better approaches?

---

### Issue 2: Asynchronous Attribute Access (RESOLVED)

**Problem:** Date and Status filter values were not being passed to our backend service. Code that worked in v7:
```javascript
const attrs = context.attributes || {};
if (attrs.CreatedFrom) { ... }  // Always undefined in Freedom UI
```

**Root Cause:** In Freedom UI, attributes bound to UI controls (DateTimePicker, ComboBox) must be accessed asynchronously:
```javascript
const dateCreatedFrom = await context.CreatedFrom;  // Correct in Freedom UI
```

**Our Solution (v19.16):** Changed all attribute access to use async/await pattern.

**Request:** Is there documentation on when to use `context.attributes.X` vs `await context.X`? The behavior is different from Classic UI.

---

### Issue 3: Cascade Filter (Sales Group by YearMonth) (PARTIALLY RESOLVED)

**Problem:** We need Sales Group dropdown to show only groups that have data for the selected YearMonth. Our attempts:

| Version | Approach | Result |
|---------|----------|--------|
| v19.3 | `lookupListConfig` pattern | Broke dropdown binding |
| v19.7 | `crt.LoadDataRequest` interceptor | Blocked all data when no match |
| v19.10 | Readonly state during async query | Didn't address caching |
| v19.11 | Clear list attribute | Didn't trigger reload |
| v19.12 | Combined approaches | Broke completely |
| **v19.13** | `modelConfig.path` + `HandlerChainService.process()` reload | **WORKS** |

**Our Solution:** Combine `modelConfig.path` for binding with explicit `HandlerChainService.instance.process()` to force reload:
```javascript
const reloadRequest = {
    type: "crt.LoadDataRequest",
    $context: request.$context,
    config: { loadType: "reload", useLastLoadParameters: false },
    dataSourceName: "UsrSalesGroup_List_DS"
};
await sdk.HandlerChainService.instance.process(reloadRequest);
```

**Request:** Is there a documented pattern for cascade/dependent dropdowns in Freedom UI? We found this through extensive trial and error.

---

### Issue 4: Backend Lookup Resolution (RESOLVED)

**Problem:** Our `GetReportEntitySchemaName()` function queries IntExcelReport and needs the `IntEntitySchemaName` (lookup to SysSchema) resolved to a string. In Freedom UI, ESQ returns the GUID, not the display value.

**Code that failed:**
```csharp
esq.AddColumn("IntEntitySchemaName");
var name = entity.GetTypedColumnValue<string>("IntEntitySchemaName");  // Returns GUID
```

**Our Solution:** Multiple fallback approaches:
1. `esq.AddColumn("IntEntitySchemaName.Name")` with column reference alias
2. GUID resolution via separate SysSchema query
3. Parse IntEsq JSON for `rootSchemaName`

**Request:** What is the correct pattern for resolving lookup column display values in server-side code?

---

### Issue 5: IntExcelExport Filter Application (ONGOING)

**Problem:** The IntExcelExport library's `GenerateReport()` function doesn't properly apply our `FiltersConfig` to the ESQ for certain views. For large views like `BGSalesByItemView` (4.8M rows), this causes "Row out of range" errors.

**Our Workaround:** Created custom generator functions that build ESQ directly with proper filters:
```csharp
if (entitySchemaName == "BGSalesByItemView" && !string.IsNullOrEmpty(request.CustomerName))
{
    return GenerateSalesByItemWithFilters(userConnection, request);
}
```

**Request:** Can you review the IntExcelExport package and confirm the correct way to pass filters to the report generation? The `FiltersConfig` parameter doesn't seem to work for all entity schemas.

---

## Files We Can Provide

| File | Purpose | Size |
|------|---------|------|
| `UsrPage_ebkv9e8.js` (current v19.1) | Frontend handler | ~800 lines |
| `UsrPage_ebkv9e8.js` (v19.13) | Cascade filter fix | ~1000 lines |
| `UsrPage_ebkv9e8.js` (v19.16) | Async attribute fix | ~1050 lines |
| `UsrExcelReportService.cs` | Backend service | ~2300 lines |
| Handler Version History | 20+ versions documented | - |
| Filter Mapping Document | Report-to-filter requirements | - |

---

## Questions for Creatio Support

1. **Attribute Access Pattern:** When should we use `context.attributes.X` vs `await context.X` in Freedom UI handlers?

2. **Cascade Dropdowns:** Is there a documented pattern for dependent/cascade dropdowns (e.g., filter dropdown B based on dropdown A selection)?

3. **Parent Schema Manipulation:** Is our `viewConfigDiff` merge pattern the recommended way to control parent schema element visibility?

4. **Lookup Resolution:** What is the server-side pattern for getting lookup column display values instead of GUIDs?

5. **IntExcelExport Filters:** How should `FiltersConfig` be structured to properly filter large views during report generation?

6. **Handler Chain:** Is `HandlerChainService.instance.process()` the correct way to programmatically trigger data reloads?

---

## Timeline

| Date | Milestone |
|------|-----------|
| 2026-01-06 | Started migration investigation |
| 2026-01-20 | v18 (Attribute Binding) deployed to PROD |
| 2026-01-23 | v19.1 (Looker Fix) deployed to PROD |
| 2026-01-27 | v19.13 (Cascade Filter) verified working |
| 2026-01-28 | v19.16 (Async Attributes) ready |
| 2026-01-28 | Items by Customer backend fix deployed to PROD |

---

## Contact Information

**Technical Contact:** [Your Name]
**Email:** [Your Email]
**Phone:** [Your Phone]

---

*Prepared: 2026-01-28*
