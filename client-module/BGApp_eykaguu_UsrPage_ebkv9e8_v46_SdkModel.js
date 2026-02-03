/**
 * UsrPage_ebkv9e8 - v46 SDK MODEL APPROACH
 * Package: BGApp_eykaguu
 *
 * CORRECTED APPROACH based on Customer FX and Creatio Academy:
 *
 * The embeddedModel pattern in v45 may not be officially supported.
 * Instead, use sdk.Model.create("Account") in handlers to load Account data
 * programmatically, then populate the ComboBox list attribute.
 *
 * KEY PATTERNS:
 * 1. LOOKER REPORTS: User's v41 iframe fix (setUsrIframeUrl)
 * 2. COMMISSION FILTERS: v19.13 pattern (bound to UsrEntity_e7ac661DS)
 * 3. CUSTOMER FILTER: sdk.Model.create("Account") + populate list on page init
 *
 * SOURCES:
 * - https://customerfx.com/article/performing-a-model-load-query-on-a-creatio-freedom-ui-page-to-check-if-a-contact-is-a-user/
 * - https://community.creatio.com/questions/how-populate-virtual-lookup-data-creatio-freedom-ui
 * - https://academy.creatio.com/docs/8.x/dev/development-on-creatio-platform/front-end-development/freedom-ui/data-sources/crud-operations/crud-operations-with-data-sources
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {

    // ================================================================
    // HELPER FUNCTIONS
    // ================================================================

    function getBpmcsrf() {
        var value = "; " + document.cookie;
        var parts = value.split("; BPMCSRF=");
        if (parts.length === 2) return parts.pop().split(";").shift();
        return "";
    }

    function toWcfDate(date) {
        if (!date) return null;
        if (date instanceof Date) return "/Date(" + date.getTime() + ")/";
        if (typeof date === "string") {
            var p = new Date(date);
            if (!isNaN(p.getTime())) return "/Date(" + p.getTime() + ")/";
        }
        return null;
    }

    function formatDateForLooker(dateValue) {
        if (!dateValue) return null;
        var d = new Date(dateValue);
        if (isNaN(d.getTime())) return null;
        var year = d.getFullYear();
        var month = String(d.getMonth() + 1).padStart(2, '0');
        var day = String(d.getDate()).padStart(2, '0');
        return year + '-' + month + '-' + day;
    }

    // USER'S v41 FIX: Use parent's existing UsrIframe component
    function setUsrIframeUrl(url) {
        setTimeout(() => {
            try {
                const el = document.getElementById("UsrIframe");
                if (el) {
                    el.Url = url;
                    console.log("[v46] UsrIframe.Url set:", url);
                } else {
                    console.warn("[v46] UsrIframe element not found");
                }
            } catch (e) {
                console.log("[v46] Error setting UsrIframe Url:", e);
            }
        }, 500);
    }

    // ================================================================
    // CASCADE FILTER STATE (from v19.13)
    // ================================================================
    var cascadeFilterEnabled = false;
    var validSalesGroupIds = null;

    // ================================================================
    // CUSTOMER DATA CACHE
    // ================================================================
    var customerListLoaded = false;

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // ================================================================
            // PARENT ELEMENT MERGES
            // ================================================================

            // Looker iframe container - show only for Looker reports (USER'S v41 FIX)
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": "$UsrShowLookerFrame" }
            },

            // Date filters - bind visibility
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": "$UsrShowDateFilters" }
            },

            // Status filter - bind visibility
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": { "visible": "$UsrShowDateFilters" }
            },

            // Generate button - wire to handler
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "clicked": { "request": "usr.GenerateReportRequest" }
                }
            },

            // ================================================================
            // COMMISSION FILTERS CONTAINER
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrCommissionFiltersContainer",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)", "minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": { "columnGap": "large", "rowGap": "none" },
                    "items": [],
                    "fitContent": true,
                    "visible": "$UsrShowCommissionFilters",
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": { "top": "medium", "right": "none", "bottom": "medium", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 1
            },

            // Year-Month ComboBox
            {
                "operation": "insert",
                "name": "UsrYearMonthCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Year-Month",
                    "labelPosition": "auto",
                    "control": "$UsrYearMonth",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select month...",
                    "visible": true,
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "tooltip": "Required for Commission reports"
                },
                "parentName": "UsrCommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },

            // Sales Group ComboBox
            {
                "operation": "insert",
                "name": "UsrSalesGroupCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "auto",
                    "control": "$UsrSalesGroup",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select group (optional)...",
                    "visible": true,
                    "layoutConfig": { "column": 2, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "tooltip": "Filtered by Year-Month when data exists",
                    "mode": "List"
                },
                "parentName": "UsrCommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // CUSTOMER FILTER CONTAINER (for "Items by Customer")
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrCustomerFilterContainer",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": { "columnGap": "large", "rowGap": "none" },
                    "items": [],
                    "fitContent": true,
                    "visible": "$UsrShowCustomerFilter",
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": { "top": "medium", "right": "none", "bottom": "medium", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 2
            },

            // Customer ComboBox - LOOKUP TO ACCOUNT ENTITY (populated via sdk.Model)
            {
                "operation": "insert",
                "name": "UsrCustomerCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Customer",
                    "labelPosition": "auto",
                    "control": "$UsrCustomer",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select customer...",
                    "visible": true,
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "tooltip": "Select customer from Account entity"
                },
                "parentName": "UsrCustomerFilterContainer",
                "propertyName": "items",
                "index": 0
            }

        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    // ================================================================
                    // VISIBILITY FLAGS
                    // ================================================================
                    "UsrShowCommissionFilters": { "value": false },
                    "UsrShowCustomerFilter": { "value": false },
                    "UsrShowDateFilters": { "value": false },
                    "UsrShowLookerFrame": { "value": false },

                    // Looker URL storage
                    "UsrLookerUrl": { "value": "" },

                    // ================================================================
                    // YEARMONTH LOOKUP (bound to existing page data source)
                    // ================================================================
                    "UsrYearMonth": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGYearMonth"
                        }
                    },

                    // ================================================================
                    // SALESGROUP LOOKUP (bound to existing page data source)
                    // ================================================================
                    "UsrSalesGroup": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGSalesGroup"
                        }
                    },
                    "UsrSalesGroup_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{ "columnName": "BGSalesGroupName", "direction": "asc" }]
                            }
                        }
                    },

                    // ================================================================
                    // CUSTOMER LOOKUP (populated via sdk.Model in handler)
                    // NOT using embeddedModel - using programmatic population instead
                    // ================================================================
                    "UsrCustomer": {
                        "value": null
                    },
                    "UsrCustomer_List": {
                        "isCollection": true,
                        "value": []
                    }
                }
            }
        ]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // ================================================================
            // PAGE INIT - Load Account data for Customer dropdown
            // ================================================================
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v46] Page initialized - SDK Model approach");
                    console.log("[v46] Features: Looker iframe + Commission lookups + Customer Account lookup via sdk.Model");
                    cascadeFilterEnabled = false;
                    validSalesGroupIds = null;
                    customerListLoaded = false;
                    return;
                }
            },

            // ================================================================
            // LOAD CUSTOMER DATA - Triggered when "Items by Customer" selected
            // Uses sdk.Model.create("Account") pattern from Customer FX
            // ================================================================
            {
                request: "usr.LoadCustomerData",
                handler: async (request, next) => {
                    const ctx = request.$context;

                    if (customerListLoaded) {
                        console.log("[v46] Customer list already loaded, skipping");
                        return next?.handle(request);
                    }

                    console.log("[v46] Loading Account data for Customer dropdown...");

                    try {
                        // Use sdk.Model to query Account entity
                        const accountModel = await sdk.Model.create("Account");
                        const accounts = await accountModel.load({
                            attributes: ["Id", "Name"],
                            options: {
                                pagingConfig: {
                                    rowsOffset: 0,
                                    rowCount: 1000  // Load up to 1000 customers
                                },
                                sortingConfig: {
                                    columns: [{ columnName: "Name", direction: "asc" }]
                                }
                            }
                        });

                        console.log("[v46] Loaded", accounts.length, "accounts from Account entity");

                        // Convert to array format for ComboBox list
                        // Format: [{ value: "guid", displayValue: "Name" }, ...]
                        const customerList = accounts.map(acc => ({
                            value: acc.Id,
                            displayValue: acc.Name
                        }));

                        // Populate the UsrCustomer_List attribute
                        ctx.UsrCustomer_List = customerList;
                        customerListLoaded = true;

                        console.log("[v46] Customer dropdown populated with", customerList.length, "items");

                    } catch (e) {
                        console.error("[v46] Error loading Account data:", e);
                        // Don't fail silently - show error to user
                        Terrasoft.showErrorMessage("Error loading customer list: " + e.message);
                    }

                    return next?.handle(request);
                }
            },

            // ================================================================
            // LOAD DATA REQUEST - CASCADE FILTER FOR SALES GROUP (from v19.13)
            // ================================================================
            {
                request: "crt.LoadDataRequest",
                handler: async (request, next) => {
                    const dsName = request.dataSourceName || "";
                    const isSalesGroupList = dsName.includes("SalesGroup") && dsName.includes("_List");

                    if (cascadeFilterEnabled && isSalesGroupList) {
                        console.log("[v46] Sales Group list load | validIds:",
                            validSalesGroupIds === null ? "null (no filter)" :
                            validSalesGroupIds.length === 0 ? "[] (no matches - show all)" :
                            validSalesGroupIds.length + " groups");

                        if (validSalesGroupIds !== null && validSalesGroupIds.length > 0) {
                            const filterItems = {};
                            validSalesGroupIds.forEach((groupId, idx) => {
                                filterItems["SGFilter_" + idx] = {
                                    filterType: 1,
                                    comparisonType: 3,
                                    isEnabled: true,
                                    leftExpression: { expressionType: 0, columnPath: "Id" },
                                    rightExpression: {
                                        expressionType: 2,
                                        parameter: { dataValueType: 0, value: groupId }
                                    }
                                };
                            });

                            const existingParams = Array.isArray(request.parameters) ? request.parameters : [];
                            const keptParams = existingParams.filter(p => p && p.type !== "filter");

                            request.parameters = [...keptParams, {
                                type: "filter",
                                value: {
                                    items: filterItems,
                                    logicalOperation: 1,
                                    isEnabled: true,
                                    filterType: 6
                                }
                            }];
                            console.log("[v46] Applied cascade filter for", validSalesGroupIds.length, "groups");
                        }
                    }

                    return next?.handle(request);
                }
            },

            // ================================================================
            // REPORT SELECTION - Update visibility + trigger customer data load
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    const bpmcsrf = getBpmcsrf();

                    // --------------------------------------------------------
                    // REPORT SELECTION CHANGE
                    // --------------------------------------------------------
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const ctx = request.$context;
                        let selectedReport = null;

                        try {
                            selectedReport = await ctx.LookupAttribute_0as4io2;
                        } catch (e) {
                            console.log("[v46] Error getting report:", e);
                        }

                        // Reset all visibility and filter values
                        ctx.UsrShowCommissionFilters = false;
                        ctx.UsrShowCustomerFilter = false;
                        ctx.UsrShowDateFilters = false;
                        ctx.UsrShowLookerFrame = false;
                        ctx.UsrLookerUrl = "";
                        ctx.UsrYearMonth = null;
                        ctx.UsrSalesGroup = null;
                        ctx.UsrCustomer = null;
                        cascadeFilterEnabled = false;
                        validSalesGroupIds = null;

                        if (!selectedReport || !selectedReport.value) {
                            console.log("[v46] No report selected - all filters hidden");
                            return next?.handle(request);
                        }

                        const reportName = (selectedReport.displayValue || "").toLowerCase();
                        console.log("[v46] Report selected:", selectedReport.displayValue);

                        // Check if Looker report
                        let reportUrl = "";
                        try {
                            const r = await fetch("/0/odata/UsrReportesPampa(" + selectedReport.value + ")?$select=UsrURL", {
                                headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                            });
                            if (r.ok) {
                                const m = await r.json();
                                if (m && m.UsrURL) {
                                    reportUrl = m.UsrURL;
                                }
                            }
                        } catch (e) {}

                        // Set visibility based on report type
                        if (reportName.includes("commission")) {
                            ctx.UsrShowCommissionFilters = true;
                            ctx.UsrShowDateFilters = false;
                            ctx.UsrShowLookerFrame = false;
                            cascadeFilterEnabled = true;
                            console.log("[v46] -> COMMISSION: YearMonth + SalesGroup filters, cascade ENABLED");

                        } else if (reportName.includes("items by customer")) {
                            ctx.UsrShowCustomerFilter = true;
                            ctx.UsrShowDateFilters = true;
                            ctx.UsrShowLookerFrame = false;
                            cascadeFilterEnabled = false;
                            console.log("[v46] -> ITEMS BY CUSTOMER: Customer lookup + Date filters");

                            // TRIGGER CUSTOMER DATA LOAD via custom request
                            try {
                                await sdk.HandlerChainService.instance.process({
                                    type: "usr.LoadCustomerData",
                                    $context: ctx,
                                    scopes: [...(request.scopes || [])]
                                });
                            } catch (loadErr) {
                                console.log("[v46] Customer data load trigger error:", loadErr);
                            }

                        } else if (reportUrl) {
                            // LOOKER REPORT
                            ctx.UsrShowDateFilters = true;
                            ctx.UsrShowLookerFrame = true;
                            ctx.UsrLookerUrl = reportUrl;
                            cascadeFilterEnabled = false;
                            setUsrIframeUrl(reportUrl);
                            console.log("[v46] -> LOOKER: Iframe ENABLED, URL:", reportUrl);

                        } else {
                            // Other Excel reports
                            ctx.UsrShowDateFilters = true;
                            ctx.UsrShowLookerFrame = false;
                            cascadeFilterEnabled = false;
                            console.log("[v46] -> OTHER EXCEL: Date + Status filters");
                        }
                    }

                    // --------------------------------------------------------
                    // YEARMONTH CHANGE - Cascade filter for Sales Group (from v19.13)
                    // --------------------------------------------------------
                    if (request.attributeName === "UsrYearMonth" && !request.silent && cascadeFilterEnabled) {
                        const ctx = request.$context;
                        const yearMonth = await ctx.UsrYearMonth;

                        if (yearMonth && yearMonth.value) {
                            console.log("[v46] YearMonth changed to:", yearMonth.displayValue);
                            ctx.UsrSalesGroup = null;

                            try {
                                const queryUrl = "/0/odata/BGCommissionSalesGroupByYearMonth?" +
                                    "$filter=BGYearMonth/Id eq " + yearMonth.value +
                                    "&$select=BGSalesGroupId";

                                console.log("[v46] Querying cascade data...");
                                const resp = await fetch(queryUrl, {
                                    method: "GET",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                });

                                if (resp.ok) {
                                    const data = await resp.json();
                                    const groupIds = new Set();

                                    (data.value || []).forEach(row => {
                                        if (row.BGSalesGroupId) {
                                            groupIds.add(row.BGSalesGroupId);
                                        }
                                    });

                                    validSalesGroupIds = Array.from(groupIds);

                                    if (validSalesGroupIds.length > 0) {
                                        console.log("[v46] Found", validSalesGroupIds.length, "groups for", yearMonth.displayValue);
                                    } else {
                                        console.log("[v46] No groups found - will show ALL groups");
                                    }
                                } else {
                                    console.log("[v46] Cascade query failed:", resp.status);
                                    validSalesGroupIds = null;
                                }
                            } catch (e) {
                                console.log("[v46] Cascade query error:", e);
                                validSalesGroupIds = null;
                            }

                            // Force reload Sales Group dropdown (v19.13 key fix)
                            try {
                                console.log("[v46] Forcing Sales Group dropdown reload...");
                                const reloadRequest = {
                                    type: "crt.LoadDataRequest",
                                    $context: ctx,
                                    config: {
                                        loadType: "reload",
                                        useLastLoadParameters: false
                                    },
                                    dataSourceName: "UsrSalesGroup_List_DS",
                                    scopes: [...(request.scopes || [])]
                                };
                                await sdk.HandlerChainService.instance.process(reloadRequest);
                                console.log("[v46] Sales Group dropdown reloaded");
                            } catch (reloadError) {
                                console.log("[v46] Sales Group reload error (non-critical):", reloadError);
                            }

                        } else {
                            validSalesGroupIds = null;
                            ctx.UsrSalesGroup = null;
                            console.log("[v46] YearMonth cleared - cascade filter disabled");
                        }
                    }

                    return next?.handle(request);
                }
            },

            // ================================================================
            // REPORT GENERATION
            // ================================================================
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    const ctx = request.$context;
                    const bpmcsrf = getBpmcsrf();

                    let selectedReport = null;
                    try {
                        selectedReport = await ctx.LookupAttribute_0as4io2;
                    } catch (e) {}

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    const reportDisplayName = selectedReport.displayValue || "Report";
                    console.log("[v46] Generate:", reportDisplayName);

                    // Fetch report metadata
                    let reportUrl = "", reportCode = "";
                    try {
                        const r = await fetch("/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=UsrURL,UsrCode", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (r.ok) {
                            const m = await r.json();
                            if (m) {
                                reportUrl = m.UsrURL || "";
                                reportCode = m.UsrCode || "";
                            }
                        }
                    } catch (e) {}

                    // --------------------------------------------------------
                    // LOOKER REPORT - Update iframe with filter params
                    // --------------------------------------------------------
                    if (reportUrl) {
                        let params = "";
                        try {
                            const filters = [];
                            const createdFrom = await ctx.CreatedFrom;
                            const createdTo = await ctx.CreatedTo;
                            const status = await ctx.LookupAttribute_tytkx09;

                            if (createdFrom) {
                                const formatted = formatDateForLooker(createdFrom);
                                if (formatted) filters.push("CreatedOn ge datetime'" + formatted + "'");
                            }
                            if (createdTo) {
                                const formatted = formatDateForLooker(createdTo);
                                if (formatted) filters.push("CreatedOn le datetime'" + formatted + "'");
                            }
                            if (status && status.displayValue && status.displayValue !== "All") {
                                filters.push("contains(BGStatus, '" + status.displayValue + "')");
                            }

                            if (filters.length > 0) {
                                params = '?params=%7B"ds0.additionalFilters":"' + filters.join(" and ") + '","ds0.top":"1000000"%7D';
                            }
                        } catch (e) {
                            console.log("[v46] Looker params error:", e);
                        }

                        const fullUrl = reportUrl + params;
                        console.log("[v46] Looker URL with params:", fullUrl);

                        ctx.UsrLookerUrl = fullUrl;
                        ctx.UsrShowLookerFrame = true;
                        setUsrIframeUrl(fullUrl);
                        Terrasoft.showInformation("Looker report loaded in iframe");
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // EXCEL REPORT - Find template and generate
                    // --------------------------------------------------------
                    let intExcelReportId = null, intEsq = "";
                    try {
                        const esc = s => (s || "").replace(/'/g, "''");
                        const terms = [];
                        if (reportDisplayName) {
                            terms.push("IntName eq '" + esc(reportDisplayName) + "'");
                            terms.push("IntName eq 'Rpt " + esc(reportDisplayName) + "'");
                        }
                        if (reportCode && reportCode !== reportDisplayName) {
                            terms.push("IntName eq '" + esc(reportCode) + "'");
                            terms.push("IntName eq 'Rpt " + esc(reportCode) + "'");
                        }

                        const r = await fetch("/0/odata/IntExcelReport?$filter=(" + terms.join(" or ") + ")&$select=Id,IntName,IntEsq&$top=1", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        const d = await r.json();

                        if (d && d.value && d.value[0]) {
                            intExcelReportId = d.value[0].Id;
                            intEsq = d.value[0].IntEsq || "";
                            console.log("[v46] Template:", d.value[0].IntName, "| IntEsq:", intEsq ? "present" : "EMPTY");
                        } else {
                            Terrasoft.showErrorMessage("Template not found: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    // Collect filter values
                    const rLower = reportDisplayName.toLowerCase();
                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    let yearMonthId = emptyGuid;
                    let salesGroupId = emptyGuid;
                    let customerId = emptyGuid;
                    let customerName = "";
                    let dateFrom = null, dateTo = null, statusName = "";

                    // Always collect date filters
                    try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                    try { dateTo = await ctx.CreatedTo; } catch (e) {}
                    try {
                        const st = await ctx.LookupAttribute_tytkx09;
                        if (st && st.displayValue && st.displayValue !== "All") {
                            statusName = st.displayValue;
                        }
                    } catch (e) {}

                    console.log("[v46] Date filters | From:", dateFrom, "| To:", dateTo, "| Status:", statusName);

                    if (rLower.includes("commission")) {
                        try {
                            const ym = await ctx.UsrYearMonth;
                            if (ym && ym.value) {
                                yearMonthId = ym.value;
                                console.log("[v46] YearMonth:", ym.displayValue, "| ID:", yearMonthId);
                            }
                        } catch (e) {}

                        try {
                            const sg = await ctx.UsrSalesGroup;
                            if (sg && sg.value) {
                                salesGroupId = sg.value;
                                console.log("[v46] SalesGroup:", sg.displayValue, "| ID:", salesGroupId);
                            }
                        } catch (e) {}

                    } else if (rLower.includes("items by customer")) {
                        try {
                            const cust = await ctx.UsrCustomer;
                            if (cust && cust.value) {
                                customerId = cust.value;
                                customerName = cust.displayValue || "";
                                console.log("[v46] Customer:", customerName, "| ID:", customerId);
                            } else {
                                console.log("[v46] WARNING: No customer selected");
                            }
                        } catch (e) {
                            console.log("[v46] Customer lookup error:", e);
                        }
                    }

                    // Generate Excel
                    try {
                        Terrasoft.showInformation("Generating report...");

                        const requestBody = {
                            EsqString: intEsq,
                            ReportId: intExcelReportId,
                            RecordCollection: [],
                            YearMonthId: yearMonthId,
                            SalesRepId: salesGroupId,
                            CustomerId: customerId,
                            CustomerName: customerName,
                            CreatedFrom: toWcfDate(dateFrom),
                            CreatedTo: toWcfDate(dateTo),
                            StatusName: statusName
                        };

                        console.log("[v46] Request body:", JSON.stringify(requestBody, null, 2));

                        const r = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify(requestBody)
                        });

                        const result = await r.json();
                        console.log("[v46] Result:", result);

                        if (result && result.success && result.key) {
                            let iframe = document.getElementById("reportDownloadFrame");
                            if (!iframe) {
                                iframe = document.createElement("iframe");
                                iframe.id = "reportDownloadFrame";
                                iframe.style.display = "none";
                                document.body.appendChild(iframe);
                            }
                            iframe.src = "/0/rest/UsrExcelReportService/GetReport/" + result.key + "/" + encodeURIComponent(reportDisplayName);
                            Terrasoft.showInformation("Downloading: " + reportDisplayName);
                        } else {
                            const errorMsg = (result && result.message) || (result && result.errorMessage) || "Generation failed";
                            console.error("[v46] Generation failed:", errorMsg);
                            Terrasoft.showErrorMessage(errorMsg);
                        }
                    } catch (e) {
                        console.error("[v46] Error:", e);
                        Terrasoft.showErrorMessage("Error: " + e.message);
                    }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
