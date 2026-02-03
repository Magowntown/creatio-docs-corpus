# Handler Version History

**Document Purpose:** Track all iterations of the UsrPage_ebkv9e8 handler for the Pampa Reports page.

**Current Production Version:** v54 (Flat Object Fix) - deployed, Customer ID selection fixed
**Latest Development:** Backend column reorder fix - 🔴 DEPLOY NOW
**PROD Schema ID:** `873d9fd9-98ac-4ece-9f53-9f77c5f4ddf2` (BGApp_eykaguu package)
**Last Updated:** 2026-01-29

---

## Version Summary Table

| Version | File | Status | Key Feature | Issue Resolved |
|---------|------|--------|-------------|----------------|
| **v52** | `_v52_CustomerFix.js` | **🔴 DEPLOY NOW** | Extract .value from attribute objects + GUID validation | **FIXES Customer ID "value" bug** |
| v51 | `_v51_StableDialog.js` | **PROD** | Empty modelConfigDiff, Button+Dialog | Fixed infinite loading |
| v50 | `_v50_CorrectEmbedded.js` | **BROKEN** | modelConfigDiff with UsrCustomerEmbeddedDS | **CAUSED infinite loading** |
| v49 | `_v49_HybridCustomer.js` | Wrong syntax | Used modelConfig instead of modelConfigDiff | Superseded by v50 |
| v48 | `_v48_EmbeddedModel.js` | Backup | embeddedModel pattern (Creatio Academy) | PROPER ComboBox lookup to Account |
| v47 | `_v47_LookupDialog.js` | Backup | Button + crt.OpenLookupPageRequest | Works but user wanted ComboBox |
| v46 | `_v46_SdkModel.js` | Superseded | sdk.Model.create("Account") - WON'T WORK | ComboBox can't be populated programmatically |
| v45 | `_v45_RalphLoop.js` | Superseded | embeddedModel pattern | May not be supported |
| **v44** | `_v44_CustomerLookup.js` | Superseded | Account data source + Customer LOOKUP | Customer MUST be lookup |
| v43 | `_v43_CustomerText.js` | REJECTED | Customer as text | User rejected - must be lookup |
| v41 | `_v41_Complete.js` | USER MODIFIED | Proper lookups + parent UsrIframe | Best current approach |
| v42 | `_v42_Fixes.js` | Superseded | Wrong iframe approach | Superseded by user's v41 |
| v40 | `_v40_ProperLookups.js` | Partial | ComboBox lookups working | Commission filters |
| v39 | `_v39_FixedConfig.js` | Superseded | Text inputs, array format | Config format fix |
| **v22** | `_v22_Bare.js` | **PROD** | Absolute bare minimum - 80 lines | Troubleshooting null errors |
| v21 | `_v21_SafeFilters.js` | Superseded | Bulletproof null guards | Null pointer errors |
| v20 | `_v20_Minimal.js` | Superseded | BGlobal mixin pattern match | Architecture alignment |
| v19.18 | `_v19.18_CustomerInput.js` | Superseded | Text input for customer + CONTAINS filter | RPT-004: Items by Customer |
| v19.17 | `_v19.17_CustomerFromView.js` | Superseded | Custom dropdown from view | ComboBox binding issues |
| **v19.16** | `_v19.16_SyncDateFilters.js` | **✅ READY** | Sync date attribute access | **Date filters for Items by Customer** |
| **v19.13** | `_v19.13_ForcedReload.js` | **✅ VERIFIED** | modelConfig.path + HandlerChainService reload | **Issues 2+3 FIXED** |
| v19.12 | `_v19.12_Reload.js` | BROKEN | lookupListConfig pattern | Broke dropdown binding |
| v19.11 | `_v19.11_ClearCache.js` | FAILED | Clear list attribute | Didn't trigger reload |
| v19.10 | `_v19.10_CascadeFix.js` | FAILED | Readonly state during query | Didn't address caching |
| v19.9 | `_v19.9_Complete.js` | Superseded | Cascade filter + Customer filter | Missing force reload
| v19.8 | `_v19.8_CustomerOnly.js` | Superseded | Customer lookup ONLY | Issue 3 only |
| v19.7 | `_v19.7_Corrected.js` | BROKEN | Customer + Cascade filter | Broke Sales Group entirely |
| v19.6 | `_v19.6_CustomerLookup.js` | Wrong column | Attempted Customer lookup | Wrong column name |
| v19.5 | `_v19.5_ProperLookups.js` | Broken | Attempted proper lookups | Still broken |
| v19.4 | `_v19.4_CustomerFilter.js` | Rejected | Text input for Customer | User rejected approach |
| v19.3 | `_v19.3_CascadeFilters.js` | Broken | lookupListConfig for all | Broke YearMonth+SalesGroup |
| v10 | `_v10_Production.js` | Deprecated | Initial production handler | - |
| v10 | `_v10_Diagnostic.js` | Deprecated | Added diagnostics | - |
| v11 | `_v11_Programmatic.js` | Deprecated | Programmatic visibility | - |
| v12 | `_v12_DEVStyle.js` | Deprecated | DEV-style filtering | Broke non-Commission filters |
| v13 | `_v13_ThreeWay.js` | Deprecated | Three-way filter logic | Helper functions out of scope |
| v14 | `_v14_Fixed.js` | Deprecated | Fixed helper scope | DOM manipulation issues |
| v15 | `_v15_Iframe.js` | Deprecated | Iframe for Looker | X-Frame-Options blocked |
| v16 | `_v16_NewTab.js` | Deprecated | New tab for Looker | DOM selectors not finding elements |
| v17 | `_v17_CSSBased.js` | Deprecated | CSS/label-based finding | Schema `visible:false` prevents DOM finding |
| v18 | `_v18_AttrBinding.js` | Backup | Attribute binding for visibility | Works correctly |
| **v19.1** | `_v19_LookerFix.js` | **PROD** | Looker URL params + filter visibility + null guards | LOOKER-002, UI-002 |

---

## Version Details

### v50 - Correct Embedded Model (RECOMMENDED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v50_CorrectEmbedded.js`
**Status:** READY FOR DEPLOYMENT
**Date:** 2026-01-28

**Critical Fix:** Use EXACT Academy syntax with `modelConfigDiff` (not `modelConfig`) for embedded data sources.

**Discovery:** v48 and v49 used `modelConfig` instead of `modelConfigDiff` for the embeddedModel paths. The Academy documentation clearly shows `modelConfigDiff` is required.

**Academy Pattern (EXACT):**
```javascript
"UsrCustomer_List": {
    "isCollection": true,
    "modelConfigDiff": {                           // <-- NOTE: "Diff" suffix
        "path": "UsrCustomerEmbeddedDS"
    },
    "embeddedModel": {
        "name": "UsrCustomerEmbeddedDS",
        "config": {
            "type": "crt.EntityDataSource",
            "config": { "entitySchemaName": "Account" }
        }
    },
    "viewModelConfigDiff": {
        "attributes": {
            "value": {
                "modelConfigDiff": {               // <-- NOTE: "Diff" suffix
                    "path": "UsrCustomerEmbeddedDS.Id"
                }
            },
            "displayValue": {
                "modelConfigDiff": {               // <-- NOTE: "Diff" suffix
                    "path": "UsrCustomerEmbeddedDS.Name"
                }
            }
        }
    }
}
```

**Why v50 over v49:**
| Aspect | v49 (WRONG) | v50 (CORRECT) |
|--------|-------------|---------------|
| Path config | `modelConfig` | `modelConfigDiff` |
| Value mapping | `modelConfig` | `modelConfigDiff` |
| Main attr type | Missing | `dataValueType: 10` (LOOKUP) |
| Sorting config | Missing | Added |
| Academy match | No | Yes |

---

### v49 - Hybrid Customer (WRONG SYNTAX)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v49_HybridCustomer.js`
**Status:** READY FOR DEPLOYMENT
**Date:** 2026-01-28

**Strategy:** Primary ComboBox with embeddedModel, fallback "Browse..." button if ComboBox fails.

**Key Discovery:** Freedom UI officially supports only ONE data source per page. The embeddedModel pattern is documented but may have edge cases where it doesn't populate.

**Features:**
- ✅ Customer ComboBox using embeddedModel pattern (primary)
- ✅ "Browse..." button fallback (appears if ComboBox empty after 2s)
- ✅ Both methods store value in `ctx.UsrCustomer` with same format
- ✅ Looker Studio iframe (user's v41 fix)
- ✅ YearMonth/SalesGroup with cascade filter (v19.13 pattern)
- ✅ Frontend validation prevents Generate without customer

**embeddedModel Configuration:**
```javascript
"UsrCustomer_List": {
    "isCollection": true,
    "modelConfig": {
        "path": "UsrCustomerDS",
        "sortingConfig": { "default": [{ "columnName": "Name", "direction": "asc" }] }
    },
    "embeddedModel": {
        "name": "UsrCustomerDS",
        "config": {
            "type": "crt.EntityDataSource",
            "config": { "entitySchemaName": "Account" }
        }
    },
    "viewModelConfigDiff": {
        "attributes": {
            "value": { "modelConfig": { "path": "UsrCustomerDS.Id" } },
            "displayValue": { "modelConfig": { "path": "UsrCustomerDS.Name" } }
        }
    }
}
```

**Fallback Handler:**
```javascript
{
    request: "usr.OpenCustomerLookup",
    handler: async (request, next) => {
        await ctx.executeRequest({
            type: "crt.OpenLookupPageRequest",
            entitySchemaName: "Account",
            caption: "Select Customer",
            // ... selection dialog opens
        });
    }
}
```

---

### v48 - Embedded Model Pattern (RECOMMENDED - Creatio Academy)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v48_EmbeddedModel.js`
**Status:** READY FOR DEPLOYMENT
**Date:** 2026-01-28

**Solution:** Uses official `embeddedModel` pattern from Creatio Academy documentation.

**Source:** https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/front-end-development/freedom-ui/data-sources/data-handling

**Customer ComboBox Configuration:**
```javascript
"UsrCustomer_List": {
    "isCollection": true,
    "modelConfigDiff": { "path": "UsrCustomerEmbeddedDS" },
    "embeddedModel": {
        "name": "UsrCustomerEmbeddedDS",
        "config": {
            "type": "crt.EntityDataSource",
            "config": { "entitySchemaName": "Account" }
        }
    },
    "viewModelConfigDiff": {
        "attributes": {
            "value": { "modelConfigDiff": { "path": "UsrCustomerEmbeddedDS.Id" } },
            "displayValue": { "modelConfigDiff": { "path": "UsrCustomerEmbeddedDS.Name" } }
        }
    }
}
```

**Features:**
- ✅ Looker Studio iframe (user's v41 fix)
- ✅ YearMonth ComboBox (v19.13 pattern)
- ✅ SalesGroup ComboBox with cascade filter (v19.13 pattern)
- ✅ **Customer ComboBox → Account entity** (embeddedModel pattern)
- ✅ Frontend validation prevents Generate without customer
- ✅ Routes to `GenerateSalesByItemWithFilters` (bypasses broken IntExcelExport)

**Why v48 over v47:**
- User explicitly demanded ComboBox lookup ("THE CUSTOMER FILTER HAS TO BE A FUCKING LOOKUP")
- v47 used Button+Dialog which works but isn't a proper dropdown
- v48 uses official Creatio Academy pattern

---

### v47 - Lookup Dialog Approach (BACKUP)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v47_LookupDialog.js`
**Status:** Backup - use v48 instead
**Date:** 2026-01-28

**Discovery:** ComboBox cannot be programmatically populated in Freedom UI!

From [Creatio Community](https://community.creatio.com/questions/how-populate-virtual-lookup-data-creatio-freedom-ui):
> "Currently it's not possible to achieve using handlers or basic Freedom UI wizard."

**Solution: Button + crt.OpenLookupPageRequest**

Instead of a ComboBox, use a Button that opens the Account lookup dialog:

```javascript
{
    request: "usr.OpenCustomerLookup",
    handler: async (request, next) => {
        await ctx.executeRequest({
            type: "crt.OpenLookupPageRequest",
            $context: ctx,
            entitySchemaName: "Account",
            caption: "Select Customer",
            features: {
                select: { multiple: false, resultType: "lookupValues" },
                create: { enabled: false }
            },
            afterClosed: function(selectedItems) {
                if (selectedItems && Object.keys(selectedItems).length > 0) {
                    const firstKey = Object.keys(selectedItems)[0];
                    const selected = selectedItems[firstKey];
                    ctx.UsrCustomerId = selected.value || firstKey;
                    ctx.UsrCustomerName = selected.displayValue;
                    ctx.UsrSelectedCustomerDisplay = "Customer: " + selected.displayValue;
                }
            }
        });
    }
}
```

**UI Elements:**
- `UsrSelectCustomerButton` (crt.Button): Opens Account lookup dialog
- `UsrSelectedCustomerLabel` (crt.Label): Displays "Customer: [Name]"
- `UsrCustomerId` (attribute): Stores Account GUID
- `UsrCustomerName` (attribute): Stores Account Name

**Features:**
- Commission filters: YearMonth + SalesGroup (ComboBox lookups)
- Customer filter: **Button opens Account lookup dialog**
- Looker iframe: User's v41 fix preserved
- Date/Status filters: Standard pattern
- Cascade filter: v19.13 pattern for Sales Group filtering

**Sources:**
- https://customerfx.com/article/invoking-a-multi-select-lookup-dialog-on-a-creatio-freedom-ui-page/
- https://community.creatio.com/questions/how-populate-virtual-lookup-data-creatio-freedom-ui

---

### v46 - SDK Model Approach (SUPERSEDED - WON'T WORK)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v46_SdkModel.js`
**Status:** SUPERSEDED - ComboBox cannot be programmatically populated
**Date:** 2026-01-28

**Discovery:** The embeddedModel pattern in v45 may not be officially supported. According to Creatio Community:
> "Currently, the system's basic tools allow you to add only one data source."

**Solution: sdk.Model.create("Account") in handler**

Uses the officially documented pattern from Customer FX and Creatio Academy:

```javascript
// Custom request handler to load Account data
{
    request: "usr.LoadCustomerData",
    handler: async (request, next) => {
        const accountModel = await sdk.Model.create("Account");
        const accounts = await accountModel.load({
            attributes: ["Id", "Name"],
            options: {
                pagingConfig: { rowsOffset: 0, rowCount: 1000 },
                sortingConfig: { columns: [{ columnName: "Name", direction: "asc" }] }
            }
        });

        // Convert to array format for ComboBox
        const customerList = accounts.map(acc => ({
            value: acc.Id,
            displayValue: acc.Name
        }));

        // Populate the list attribute
        ctx.UsrCustomer_List = customerList;
        customerListLoaded = true;
        return next?.handle(request);
    }
}
```

**Customer attribute configuration:**
```javascript
"UsrCustomer": {
    "value": null  // Simple value attribute
},
"UsrCustomer_List": {
    "isCollection": true,
    "value": []  // Populated programmatically by handler
}
```

**Features:**
- Commission filters: YearMonth + SalesGroup (ComboBox lookups)
- Customer filter: **LOOKUP to Account entity** via sdk.Model
- Looker iframe: User's v41 fix preserved
- Date/Status filters: Standard pattern
- Cascade filter: v19.13 pattern for Sales Group filtering

**Sources:**
- https://customerfx.com/article/performing-a-model-load-query-on-a-creatio-freedom-ui-page-to-check-if-a-contact-is-a-user/
- https://community.creatio.com/questions/how-populate-virtual-lookup-data-creatio-freedom-ui
- https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/front-end-development/freedom-ui/data-sources/crud-operations/crud-operations-with-data-sources

---

### v45 - Ralph Loop Solution (embeddedModel - SUPERSEDED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v45_RalphLoop.js`
**Status:** Superseded by v46 - embeddedModel may not be officially supported
**Date:** 2026-01-28

Used embeddedModel pattern for Customer lookup. Research found this may not be supported by Creatio.

---

### v44 - Customer Lookup (SUPERSEDED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v44_CustomerLookup.js`
**Status:** Ready for testing
**Date:** 2026-01-28

**User Requirement:** "THE CUSTOMER FILTER HAS TO BE A FUCKING LOOKUP" - explicit rejection of text input.

**Solution: Account Entity Data Source**

Added `modelConfigDiff` with Account data source:
```javascript
modelConfigDiff: [
    {
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
    }
]
```

**Customer attribute bindings:**
```javascript
"UsrCustomer": {
    "modelConfig": {
        "path": "UsrCustomerDS.Id"
    }
},
"UsrCustomer_List": {
    "isCollection": true,
    "modelConfig": {
        "path": "UsrCustomerDS",
        "sortingConfig": {
            "default": [{ "columnName": "Name", "direction": "asc" }]
        }
    }
}
```

**Features:**
- Commission filters: YearMonth + SalesGroup (ComboBox lookups)
- Customer filter: **LOOKUP to Account entity** (NOT text input)
- Looker reports: Embedded in parent's UsrIframe
- Excel reports: Download via hidden iframe

---

### v43 - Customer Text (USER REJECTED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v43_CustomerText.js`
**Status:** REJECTED - User explicitly required Customer as LOOKUP, not text
**Date:** 2026-01-28

**Builds on user's v41 modifications:**
1. `setUsrIframeUrl()` - Uses parent's UsrIframe component
2. `UsrShowLookerFrame` - Visibility binding for GridContainer_fh039aq
3. ComboBox lookups for YearMonth, SalesGroup

**Key Fix:**
- Customer changed from ComboBox to TEXT INPUT
- Reason: `BGCustomer` in `BGSalesByItemView` is VARCHAR, not entity lookup
- ComboBox requires entity binding - won't populate from varchar column

**Features:**
- Commission filters: YearMonth + SalesGroup (ComboBox lookups)
- Items by Customer: Customer name text input + Date filters
- Looker reports: Embedded in parent's UsrIframe
- Excel reports: Download via hidden iframe

---

### v41 - Complete (USER MODIFIED - BEST APPROACH)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v41_Complete.js`
**Status:** ✅ USER MODIFIED - Current best approach
**Date:** 2026-01-28

**User's Critical Modifications:**
1. Added `setUsrIframeUrl()` function to use parent's existing UsrIframe component:
```javascript
function setUsrIframeUrl(url) {
    setTimeout(() => {
        try {
            const el = document.getElementById("UsrIframe");
            if (el) {
                el.Url = url;
                console.log("[v41] UsrIframe.Url set:", url);
            }
        } catch (e) {
            console.log("[v41] Error setting UsrIframe Url:", e);
        }
    }, 500);
}
```
2. `GridContainer_fh039aq` visibility bound to `$UsrShowLookerFrame`

**Key Features:**
- Proper ComboBox lookups for YearMonth, SalesGroup
- Customer as ComboBox lookup (BUT: BGCustomer is VARCHAR - binding won't populate)
- Looker iframe using parent's UsrIframe component (CORRECT approach)
- viewModelConfigDiff array format (correct pattern)

**Remaining Issues:**
1. Customer lookup won't populate - BGCustomer is varchar, not entity lookup
2. "Report false*" label - parent schema issue
3. Items by Customer - backend error in BGlobal's IntExcelExport code

---

### v42 - Fixes (SUPERSEDED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v42_Fixes.js`
**Status:** ❌ Superseded - Used wrong iframe approach
**Date:** 2026-01-28

**Why Superseded:** Used DOM manipulation for iframe instead of user's correct approach using parent's UsrIframe component.

---

### v40 - Proper Lookups
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v40_ProperLookups.js`
**Status:** Partial success
**Date:** 2026-01-28

**Key Changes:**
- ComboBox lookups bound to existing page data source (`UsrEntity_e7ac661DS.BGYearMonth`)
- Commission filters working
- Uses v19.13 viewModelConfigDiff array pattern

**Test Results:**
- Commission reports: ✅ Working
- "Report false*" still showing
- Customer lookup: Shows but doesn't populate
- Items by Customer: ArgumentNullException (backend error)

---

### v39 - Fixed Config (TEXT INPUTS)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v39_FixedConfig.js`
**Status:** Superseded by v40+ (uses text inputs, user wanted lookups)
**Date:** 2026-01-28

**Root Cause Analysis of v36-v38 Failures:**
| Version | What Worked | What Failed | Root Cause |
|---------|------------|-------------|------------|
| v36 | Text inputs showed up (always visible) | - | `visible: true` works |
| v37 | Visibility binding syntax | Filters didn't show | Container wrapper missing |
| v38 | ComboBox syntax | Filters didn't show | Wrong `viewModelConfigDiff` format + wrong data source binding |

**Key Fixes in v39:**
1. **viewModelConfigDiff format**: Changed from plain object to array with `"operation": "merge"` and `"path": ["attributes"]` (v19.13 pattern)
2. **Don't hide parent's report dropdown**: Removed merge on `GridContainer_oshnwh8` - was causing "Report false*" label issue
3. **GridContainer wrapper with visibility binding**: Inputs are always visible but their CONTAINER is bound to `$UsrShowCommissionFilters`
4. **Text inputs with ID lookup**: Uses proven-to-work text inputs, looks up actual IDs by name when generating

**Visibility Logic:**
| Report Type | Commission Filters | Date+Status | Customer |
|-------------|-------------------|-------------|----------|
| None selected | hidden | visible (default) | hidden |
| Commission | visible | hidden | hidden |
| Items by Customer | hidden | visible | visible |
| Looker/Other | hidden | visible | hidden |

**ID Lookup for Commission:**
When generating Commission reports, v39 looks up IDs from text input:
```javascript
// Look up YearMonth ID by name
const ymResp = await fetch("/0/odata/BGYearMonth?$filter=BGYearMonthName eq '" + ymText + "'&$select=Id&$top=1");
```

---

### v22 - Bare Minimum (CURRENT PRODUCTION)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v22_Bare.js`
**Status:** ✅ **PROD** - Deployed 2026-01-28
**Date:** 2026-01-28

**Purpose:**
Absolute bare minimum handler to isolate issues. Previous versions (v20, v21) caused:
- "Cannot read properties of null (reading 'value')" errors
- "Localized resource string not found. MainDS_Name" errors
- Page slowness/unresponsiveness

**Key Characteristics:**
- ~80 lines total (vs 300+ in v21)
- NO sdk dependency (`@creatio-devkit/common`)
- NO attribute change handlers (HandleViewModelAttributeChangeRequest)
- NO complex filter visibility logic
- NO LoadDataRequest interceptors
- Just ONE handler for Generate button click

**What It Does:**
1. Hides parent's GridContainer_oshnwh8 (parent's dropdown)
2. Adds simple Report ComboBox bound to `$LookupAttribute_0as4io2`
3. On Generate:
   - Checks if Looker (UsrURL) → opens new tab
   - Otherwise finds IntExcelReport template → calls UsrExcelReportService

**Theory:**
Testing if issues stem from our handlers or from the parent schema itself. If v22 still has problems, the issue is in:
- Parent schema (BGPage_iaptpa6)
- Missing resource strings
- ExtendParent schema configuration

---

### v21 - Safe Filters (SUPERSEDED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v21_SafeFilters.js`
**Status:** Superseded by v22
**Date:** 2026-01-28

**Purpose:**
Added bulletproof null guards after v20 caused null pointer errors in PROD.

**Key Additions:**
```javascript
// Helper functions with aggressive null checking
function safeGetValue(obj) {
    if (!obj) return null;
    if (typeof obj === 'string' || typeof obj === 'number') return obj;
    if (obj.value !== undefined) return obj.value;
    return null;
}

function safeGetDisplayValue(obj) {
    if (!obj) return null;
    if (typeof obj === 'string') return obj;
    if (obj.displayValue !== undefined) return obj.displayValue;
    if (obj.value !== undefined) return String(obj.value);
    return null;
}
```

**Why Superseded:**
Even with null guards, page was slow/unresponsive. Issues likely from the volume of attribute change handlers, not just null values.

---

### v20 - Minimal BGlobal Pattern (SUPERSEDED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v20_Minimal.js`
**Status:** Superseded by v21→v22
**Date:** 2026-01-28

**Purpose:**
Match BGlobal's BGIntExcelreportMixin as closely as possible.

**BGlobal's Mixin Interface:**
- Sends: `{EsqString, ReportId, RecordCollection}`
- EsqString = serialized ESQ with filters already embedded (from IntExcelReport.IntEsq)
- RecordCollection = array of record IDs (can be empty for section reports)
- Downloads via UsrExcelReportService/GetReport/{key}/{filename}

**Key Approach:**
- Reads IntEsq from IntExcelReport template
- Passes it as EsqString to backend (let backend handle filtering)
- NO complex filter visibility logic
- NO cascade filters

**Error Encountered:**
`Cannot read properties of null (reading 'value')` at line 533 in PROD

**Root Cause:**
Lookup attribute access returned null when accessed without await or proper null checking.

---

### v19.18 - Customer Text Input (SUPERSEDED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.18_CustomerInput.js`
**Status:** Superseded by v20→v21→v22
**Date:** 2026-01-28

**Root Cause of "No data found" Issue:**
The Customer dropdown in v19.16 was bound to Account entity via `UsrEntity_e7ac661DS.BGCustomer`.
Users selected "Pampa Bay" (company account) which doesn't exist in BGSalesByItemView.
The view contains actual customers like "Bay Country Shop", "Baytree Gift Company", etc.

**v19.18 Fix:**
1. Changed Customer control from ComboBox to text Input
2. User types customer name directly (full or partial)
3. Backend uses CONTAINS filter (comparisonType 11) instead of exact match
4. Added "Show Customers" button to display available customer names

**Backend Changes Required:**
```csharp
// Added new method to UsrExcelReportService:
private string BuildStringContainsFilterJson(string columnPath, string value)
// Changed CustomerFilter to use CONTAINS instead of Equals
BuildStringContainsFilterJson("BGCustomer", request.CustomerName)
```

**All Features:**
- ✅ Customer text input for "Items by Customer"
- ✅ "Show Customers" button to display available options
- ✅ CONTAINS filtering on backend (partial name matching)
- ✅ All v19.16 features (dates, cascade, Looker)

---

### v19.17 - Customer From View (SUPERSEDED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.17_CustomerFromView.js`
**Status:** Superseded by v19.18
**Date:** 2026-01-28

**Approach:**
Tried to populate ComboBox dropdown dynamically from DISTINCT BGCustomer values in BGSalesByItemView.

**Why It Failed:**
Freedom UI ComboBox requires proper entity data source binding. Custom data via LoadDataRequest
interception doesn't work reliably for ComboBox controls.

**Superseded by:** v19.18 with text input approach

---

### v19.16 - Sync Date Filters (READY TO DEPLOY)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.16_AsyncDateFilters.js`
**Status:** ✅ **READY** - Date filters now properly collected and passed to backend
**Date:** 2026-01-27
**Based on:** v19.15 (Complete Filters)

**Root Cause of v19.15 Failure:**
Date and Status filters were not being passed to the backend. The code used:
```javascript
const attrs = context.attributes || {};
if (attrs.CreatedFrom) { ... }  // WRONG - always undefined
```

In Freedom UI, attributes bound to UI controls (like DateTimePicker) must be accessed asynchronously:
```javascript
const dateCreatedFrom = await context.CreatedFrom;  // CORRECT
```

The `context.attributes.X` pattern only works for simple value attributes, not for parent schema attributes with control bindings.

**v19.16 Fix:**
Changed all date and status filter access to use async pattern:
```javascript
// BEFORE (v19.15 - broken):
const attrs = context.attributes || {};
if (attrs.CreatedFrom) {
    createdFrom = formatDateForWcf(attrs.CreatedFrom);
}

// AFTER (v19.16 - working):
const dateCreatedFrom = await context.CreatedFrom;
if (dateCreatedFrom) {
    createdFrom = formatDateForWcf(dateCreatedFrom);
}
```

**Also Fixed:**
- `buildLookerParams()` function is now async
- All lookup attribute access (Status, Theme, SalesRep, CustomerType) uses await

**All Features:**
- ✅ Date filters passed to backend (CreatedFrom/To, ShippingFrom/To, DeliveryFrom/To)
- ✅ Status filter passed to backend
- ✅ Customer filter for "Items by Customer"
- ✅ Cascade filter for Commission reports
- ✅ Looker reports with URL params

---

### v19.13 - Forced Reload (VERIFIED WORKING)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.13_ForcedReload.js`
**Status:** ✅ **VERIFIED** - Cascade filter works, persists after report switching
**Date:** 2026-01-27
**Tested:** 2026-01-27 - Confirmed 14 groups shown for 2025-12, filter persists after switching reports

**Why Previous Versions Failed:**
| Version | Approach | Failure Reason |
|---------|----------|----------------|
| v19.9 | `modelConfig.path` + LoadDataRequest interceptor | Missing force reload - cached dropdown not refreshed |
| v19.10 | Added readonly state during async query | Didn't address caching - just prevented clicking |
| v19.11 | Clear `UsrSalesGroup_List = null` | Clearing attribute doesn't trigger reload |
| v19.12 | Used `lookupListConfig` pattern from v19.3 | Broke dropdown binding - no `modelConfig.path` |

**v19.13 Solution:**
Combines TWO key patterns:
1. **From v19.9**: `modelConfig.path` for dropdown binding (ensures dropdowns have data)
2. **From v19.3**: `sdk.HandlerChainService.instance.process()` to force reload after cascade query

```javascript
// After cascade query completes and validSalesGroupIds is set:
const reloadRequest = {
    type: "crt.LoadDataRequest",
    $context: request.$context,
    config: {
        loadType: "reload",
        useLastLoadParameters: false
    },
    dataSourceName: "UsrSalesGroup_List_DS",
    scopes: [...(request.scopes || [])]
};
await sdk.HandlerChainService.instance.process(reloadRequest);
```

**Key Insight:**
- `modelConfig.path` tells Freedom UI WHERE to store the selected value
- `lookupListConfig` tells Freedom UI WHERE to get the list options
- Using ONLY `lookupListConfig` (v19.12) breaks the binding
- The force reload via `HandlerChainService` ensures the `crt.LoadDataRequest` interceptor fires AFTER `validSalesGroupIds` is populated

**All Features:**
- ✅ Dynamic filter visibility based on report type
- ✅ Working dropdowns with data (YearMonth, SalesGroup, Customer)
- ✅ Cascade filter: Sales Group filtered by YearMonth
- ✅ Customer filter for "Items by Customer" report
- ✅ Looker reports with URL params
- ✅ Excel report downloads

---

### v19.10 - Cascade Race Condition Fix (FAILED)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.10_CascadeFix.js`
**Status:** ❌ FAILED - Readonly state doesn't address caching
**Date:** 2026-01-27

**Root Cause of v19.9 Failure (Incorrect Analysis):**
The cascade filter appeared to work initially but broke when switching between reports. The issue:
1. When YearMonth changes, the cascade query is **async** (`await fetch(...)`)
2. User can click Sales Group dropdown **before** the fetch completes
3. When LoadDataRequest fires, `validSalesGroupIds` is still `null`
4. No filter is applied → all 76 groups show instead of filtered list

**v19.10 Fix:**
Added `UsrSalesGroupLoading` attribute that **disables** the Sales Group dropdown during the async cascade query:

```javascript
// When YearMonth changes (BEFORE async query)
request.$context.UsrSalesGroupLoading = true;  // Disable dropdown

// After cascade query completes (in finally block)
request.$context.UsrSalesGroupLoading = false;  // Re-enable dropdown
```

**Schema Changes:**
```javascript
// viewModelConfigDiff - new attribute
"UsrSalesGroupLoading": { "value": false }

// viewConfigDiff - bind to dropdown
"BGSalesGroup": {
    "readonly": "$UsrSalesGroupLoading"
}
```

**Behavior Timeline:**
| Step | State | Dropdown |
|------|-------|----------|
| 1. Select YearMonth | `UsrSalesGroupLoading = true` | **Disabled** |
| 2. Cascade query running | `validSalesGroupIds = null` | **Disabled** |
| 3. Query completes | `validSalesGroupIds = [14 groups]` | Still disabled |
| 4. Finally block | `UsrSalesGroupLoading = false` | **Enabled** |
| 5. User opens dropdown | LoadDataRequest fires | Shows 14 groups ✓ |

---

### v19.9 - Complete (SUPERSEDED by v19.13)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.9_Complete.js`
**Status:** ⚠️ Missing force reload - Use v19.13 instead
**Date:** 2026-01-27

**Fixes:**
1. **Issue 2 (Cascade Filter):** Sales Group dropdown now filtered by YearMonth selection
2. **Issue 3 (Customer Filter):** Customer dropdown added for "Items by Customer" report

**Key Fix for Issue 2:**
The v19.7 bug was: when `validSalesGroupIds` was empty `[]`, it applied a filter matching nothing.
The v19.9 fix: When no groups match, DON'T apply filter (show all groups as graceful fallback).

```javascript
// v19.7 BUG - showed empty dropdown
if (validSalesGroupIds.length === 0) {
    // Applied filter for impossible GUID = no results
}

// v19.9 FIX - graceful fallback
if (validSalesGroupIds !== null && validSalesGroupIds.length > 0) {
    // Only apply filter when we have actual IDs
} else {
    // Don't filter - show all groups
}
```

**Visibility Rules (unchanged):**
| Report Type | Commission Filters | Date+Status | Customer | Cascade |
|-------------|-------------------|-------------|----------|---------|
| None selected | hidden | hidden | hidden | - |
| Commission | visible | hidden | hidden | **active** |
| Items by Customer | hidden | visible | **visible** | - |
| Looker Studio | hidden | visible | hidden | - |
| Other Excel | hidden | visible | hidden | - |

---

### v19.1 - Looker Fix (PRODUCTION)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19_LookerFix.js`
**Status:** ✅ Deployed to DEV and PROD (2026-01-23)
**Date:** 2026-01-23

**Key Fixes from v18:**
1. **Looker reports now show Date+Status filters** (v18 incorrectly hid all filters)
2. **Looker reports now build URL params** from filter values (v18 just opened base URL)

**v19.1 Additional Fixes (from DEV testing):**
| Bug | Symptom | Fix |
|-----|---------|-----|
| Missing `selectedReport.value` check | `Cannot read properties of null` | Added `&& selectedReport.value` to condition |
| Missing `meta` null check | `Cannot read properties of undefined` | Added `if (meta && typeof meta.UsrURL !== 'undefined')` |
| Missing `reportMeta` null check | Potential null reference | Added `if (reportMeta)` guard |

**Bugs Fixed Before Deployment:**
| Bug | Issue | Fix |
|-----|-------|-----|
| Attribute access | Used `context.X` | Changed to `context.attributes.X` (parent pattern) |
| Field name | Used `BGShippingDate` | Changed to `BGShipDate` (parent pattern) |

**Visibility Logic (CORRECTED):**
| Report Type | `UsrShowCommissionFilters` | `UsrShowDateStatusFilters` | Action |
|-------------|---------------------------|---------------------------|--------|
| None selected | `false` | `false` | - |
| Commission | `true` | `false` | Excel download |
| Non-Commission Excel | `false` | `true` | Excel download |
| **Looker Studio** | `false` | **`true`** ✓ | Opens new tab + URL params |

**URL Param Format (restored from original parent):**
```
?params=%7B"ds0.additionalFilters":"CreatedOn ge datetime'2025-01-01' and CreatedOn le datetime'2025-12-31' and contains(BGStatus, 'Shipped')","ds0.top":"1000000"%7D
```

**What Changed:**
```javascript
// v18 (WRONG):
if (isLookerReport) {
    request.$context.UsrShowDateStatusFilters = false;  // Hides filters!
}
window.open(reportUrl, "_blank");  // No params!

// v19 (CORRECT):
if (isLookerReport) {
    request.$context.UsrShowDateStatusFilters = true;   // Shows filters
}
var params = buildLookerParams(context);
window.open(reportUrl + params, "_blank");  // With params!
```

---

### v19.8 - Customer Only (READY TO DEPLOY)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.8_CustomerOnly.js`
**Status:** ✅ Ready for deployment
**Date:** 2026-01-27

**Based on:** v19.1 (working PROD) + Customer filter ONLY

**Why v19.8 exists:**
v19.7's LoadDataRequest interceptor broke Sales Group entirely. When the cascade filter query returned empty results, the interceptor blocked ALL Sales Group data instead of showing all options.

**Issues Addressed:**
| Issue | Status | Approach |
|-------|--------|----------|
| Issue 3 (Customer filter) | ✅ FIXED | Added `UsrCustomer` bound to `BGCustomer` column |
| Issue 2 (Cascade filter) | ❌ DEFERRED | Removed - needs different approach |
| Issue 1 (Expand all) | ❌ NOT FIXABLE | Looker Studio feature |

**Key Changes from v19.1:**
1. Added `UsrShowCustomerFilter` visibility attribute
2. Added `BGCustomerFilterContainer` with Customer dropdown
3. Added `UsrCustomer` attribute bound to `UsrEntity_e7ac661DS.BGCustomer`
4. Added "Items by Customer" report detection to show customer filter
5. Added `CustomerId` parameter to Excel service request

**What was NOT added (intentionally):**
- NO `crt.LoadDataRequest` interceptor (this broke v19.7)
- NO cascade filter logic
- Sales Group shows ALL groups (working behavior from v19.1)

**Visibility Rules:**
| Report Type | Commission | Date+Status | Customer |
|-------------|------------|-------------|----------|
| None selected | hidden | hidden | hidden |
| Commission | visible | hidden | hidden |
| Items by Customer | hidden | visible | **visible** |
| Looker Studio | hidden | visible | hidden |
| Other Excel | hidden | visible | hidden |

---

### v19.7 - Corrected Customer + Cascade (BROKEN)
**File:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v19.7_Corrected.js`
**Status:** ❌ BROKEN - Sales Group shows no data
**Date:** 2026-01-27

**Root Cause of Failure:**
The `crt.LoadDataRequest` interceptor blocked ALL Sales Group data. When cascade query returned empty array `[]`, the filter condition `validSalesGroupIds !== null` was true but the array was empty, causing the Id filter to match nothing.

```javascript
// PROBLEMATIC CODE in v19.7:
if (cascadeFilterEnabled && isSalesGroupList && validSalesGroupIds !== null) {
    // When validSalesGroupIds = [], this filter matches NOTHING
    request.filters = [..., { "comparisonType": 4, "leftExpression": {..., "columnPath": "Id"},
                              "rightExpression": {..., "parameter": {"value": validSalesGroupIds}}}];
}
```

**Lesson Learned:**
LoadDataRequest interception is too aggressive for optional cascade filtering. Need to either:
1. Use server-side filtering in the data source
2. Use a different approach that doesn't block the default behavior

---

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
