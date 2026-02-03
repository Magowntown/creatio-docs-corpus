/**
 * UsrPage_ebkv9e8 - v19.12 Reload Pattern (Based on v19.3)
 * Package: BGApp_eykaguu
 *
 * KEY FIX: Uses sdk.HandlerChainService.instance.process() to force reload
 * of Sales Group dropdown AFTER cascade query completes.
 *
 * This was the WORKING pattern from v19.3 that was lost in later versions.
 *
 * DIFFERENCES FROM v19.9/v19.10/v19.11:
 * 1. Uses lookupListConfig instead of modelConfig.path for dropdowns
 * 2. Explicitly triggers crt.LoadDataRequest to reload the Sales Group list
 * 3. Uses correct column $select=BGSalesGroup (not BGSalesGroupId)
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

    function formatDateForLooker(dateValue) {
        if (!dateValue) return null;
        var d = new Date(dateValue);
        if (isNaN(d.getTime())) return null;
        var year = d.getFullYear();
        var month = String(d.getMonth() + 1).padStart(2, '0');
        var day = String(d.getDate()).padStart(2, '0');
        return year + '-' + month + '-' + day;
    }

    function buildLookerParams(context) {
        var param = '?params=%7B"ds0.additionalFilters":';
        var filters = [];
        var attrs = context.attributes || {};

        if (attrs.CreatedFrom) {
            var createdfrom = formatDateForLooker(attrs.CreatedFrom);
            if (createdfrom) filters.push('CreatedOn ge datetime' + "'" + createdfrom + "'");
        }
        if (attrs.CreatedTo) {
            var createdto = formatDateForLooker(attrs.CreatedTo);
            if (createdto) filters.push('CreatedOn le datetime' + "'" + createdto + "'");
        }
        if (attrs.ShippingFrom) {
            var shippingfrom = formatDateForLooker(attrs.ShippingFrom);
            if (shippingfrom) filters.push('BGShipDate ge datetime' + "'" + shippingfrom + "'");
        }
        if (attrs.ShippingTo) {
            var shippingto = formatDateForLooker(attrs.ShippingTo);
            if (shippingto) filters.push('BGShipDate le datetime' + "'" + shippingto + "'");
        }
        if (attrs.DeliveryFrom) {
            var deliveryfrom = formatDateForLooker(attrs.DeliveryFrom);
            if (deliveryfrom) filters.push('BGDeliveryDate ge datetime' + "'" + deliveryfrom + "'");
        }
        if (attrs.DeliveryTo) {
            var deliveryto = formatDateForLooker(attrs.DeliveryTo);
            if (deliveryto) filters.push('BGDeliveryDate le datetime' + "'" + deliveryto + "'");
        }

        var status = attrs.LookupAttribute_tytkx09;
        if (status && status.displayValue && status.displayValue !== "All") {
            filters.push("contains(BGStatus, '" + status.displayValue + "')");
        }

        var theme = attrs.LookupAttribute_4ufq0og;
        if (theme && theme.displayValue) {
            filters.push("contains(BGTheme, '" + theme.displayValue + "')");
        }

        var salesRep = attrs.LookupAttribute_houdnx9;
        if (salesRep && salesRep.displayValue) {
            filters.push("contains(BGSalesRep, '" + salesRep.displayValue + "')");
        }

        var customerType = attrs.LookupAttribute_c4ubvuy;
        if (customerType && customerType.displayValue) {
            filters.push("contains(BGCustomerType, '" + customerType.displayValue + "')");
        }

        if (filters.length > 0) {
            param = param + '"' + filters.join(' and ') + '","ds0.top":"1000000"%7D';
        } else {
            param = param + '"","ds0.top":"1000000"%7D';
        }

        return param;
    }

    // ================================================================
    // CASCADE FILTER STATE
    // ================================================================
    var cascadeFilterEnabled = false;
    var validSalesGroupIds = null;

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Hide parent's report dropdown
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": { "visible": false }
            },
            // Hide iframe container
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": false }
            },
            // Date filters - bind visibility
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": "$UsrShowDateStatusFilters" }
            },
            // Status filter - bind visibility
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": { "visible": "$UsrShowDateStatusFilters" }
            },
            // Generate button
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "visible": true,
                    "clicked": { "request": "usr.GenerateReportRequest" }
                }
            },

            // ================================================================
            // INSERT: Report selector container
            // ================================================================
            {
                "operation": "insert",
                "name": "BGReportContainer",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)", "minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": { "columnGap": "large", "rowGap": "none" },
                    "items": [],
                    "fitContent": true,
                    "visible": true,
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": { "top": "none", "right": "none", "bottom": "none", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 0
            },
            {
                "operation": "insert",
                "name": "BGPampaReport",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Report",
                    "labelPosition": "auto",
                    "control": "$LookupAttribute_0as4io2",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select a report...",
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "visible": true
                },
                "parentName": "BGReportContainer",
                "propertyName": "items",
                "index": 0
            },

            // ================================================================
            // INSERT: Warning label (Commission only)
            // ================================================================
            {
                "operation": "insert",
                "name": "BGWarningLabel",
                "values": {
                    "type": "crt.Label",
                    "caption": "Commission data is derived from QuickBooks synced payment records.",
                    "labelType": "placeholder",
                    "labelThickness": "default",
                    "labelEllipsis": false,
                    "labelColor": "#D2310D",
                    "labelBackgroundColor": "transparent",
                    "labelTextAlign": "center",
                    "visible": "$UsrShowCommissionFilters"
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // INSERT: Commission filters container
            // ================================================================
            {
                "operation": "insert",
                "name": "BGCommissionFiltersContainer",
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
                    "padding": { "top": "none", "right": "none", "bottom": "none", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 2
            },
            {
                "operation": "insert",
                "name": "BGYearMonth",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Year-Month",
                    "labelPosition": "auto",
                    "control": "$UsrYearMonth",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select month...",
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "visible": true,
                    "tooltip": "Required for Commission reports"
                },
                "parentName": "BGCommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },
            {
                "operation": "insert",
                "name": "BGSalesGroup",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "auto",
                    "control": "$UsrSalesGroup",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select group...",
                    "layoutConfig": { "column": 2, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "visible": true,
                    "tooltip": "Filtered by Year-Month selection"
                },
                "parentName": "BGCommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // INSERT: Customer filter container (for "Items by Customer")
            // ================================================================
            {
                "operation": "insert",
                "name": "BGCustomerFilterContainer",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)", "minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": { "columnGap": "large", "rowGap": "none" },
                    "items": [],
                    "fitContent": true,
                    "visible": "$UsrShowCustomerFilter",
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": { "top": "none", "right": "none", "bottom": "none", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 3
            },
            {
                "operation": "insert",
                "name": "BGCustomerLookup",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Customer",
                    "labelPosition": "auto",
                    "control": "$UsrCustomer",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select customer...",
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "visible": true,
                    "tooltip": "Filter report by customer"
                },
                "parentName": "BGCustomerFilterContainer",
                "propertyName": "items",
                "index": 0
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    "UsrShowCommissionFilters": {
                        "value": false
                    },
                    "UsrShowDateStatusFilters": {
                        "value": false
                    },
                    "UsrShowCustomerFilter": {
                        "value": false
                    },
                    // v19.12: Use lookupListConfig pattern (like v19.3)
                    "UsrYearMonth": {
                        "lookupListConfig": {
                            "entitySchemaName": "BGYearMonth",
                            "hierarchical": false,
                            "orders": [
                                { "columnPath": "Name", "direction": "Desc" }
                            ]
                        }
                    },
                    "UsrSalesGroup": {
                        "lookupListConfig": {
                            "entitySchemaName": "BGSalesGroup",
                            "hierarchical": false,
                            "orders": [
                                { "columnPath": "BGSalesGroupName", "direction": "Asc" }
                            ]
                        }
                    },
                    // Customer lookup - uses Account entity
                    "UsrCustomer": {
                        "lookupListConfig": {
                            "entitySchemaName": "Account",
                            "hierarchical": false,
                            "orders": [
                                { "columnPath": "Name", "direction": "Asc" }
                            ]
                        }
                    }
                }
            }
        ]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // ================================================================
            // PAGE INIT
            // ================================================================
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v19.12] Page init - Using v19.3 reload pattern");
                    cascadeFilterEnabled = false;
                    validSalesGroupIds = null;
                    return;
                }
            },

            // ================================================================
            // LOAD DATA REQUEST - CASCADE FILTER FOR SALES GROUP
            // ================================================================
            {
                request: "crt.LoadDataRequest",
                handler: async (request, next) => {
                    const dsName = request.dataSourceName || "";

                    // Intercept Sales Group list
                    const isSalesGroupList = dsName.includes("SalesGroup") && dsName.includes("_List");

                    if (cascadeFilterEnabled && isSalesGroupList) {
                        console.log("[v19.12] LoadDataRequest for Sales Group list");

                        if (validSalesGroupIds !== null && validSalesGroupIds.length > 0) {
                            // Build OR filter for valid group IDs
                            const filterItems = {};
                            validSalesGroupIds.forEach((groupId, idx) => {
                                filterItems["SGFilter_" + idx] = {
                                    filterType: 1,
                                    comparisonType: 3,  // Equals
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
                                    logicalOperation: 1,  // OR
                                    isEnabled: true,
                                    filterType: 6
                                }
                            }];
                            console.log("[v19.12] ✓ Applied cascade filter for", validSalesGroupIds.length, "groups");

                        } else if (validSalesGroupIds !== null && validSalesGroupIds.length === 0) {
                            // No valid groups - filter to impossible GUID (show empty)
                            const existingParams = Array.isArray(request.parameters) ? request.parameters : [];
                            const keptParams = existingParams.filter(p => p && p.type !== "filter");

                            request.parameters = [...keptParams, {
                                type: "filter",
                                value: {
                                    items: {
                                        "NoGroupsFilter": {
                                            filterType: 1,
                                            comparisonType: 3,
                                            isEnabled: true,
                                            leftExpression: { expressionType: 0, columnPath: "Id" },
                                            rightExpression: {
                                                expressionType: 2,
                                                parameter: { dataValueType: 0, value: "00000000-0000-0000-0000-000000000000" }
                                            }
                                        }
                                    },
                                    logicalOperation: 0,
                                    isEnabled: true,
                                    filterType: 6
                                }
                            }];
                            console.log("[v19.12] No groups for this month - showing empty list");
                        } else {
                            console.log("[v19.12] validSalesGroupIds is null - showing all groups");
                        }
                    }

                    return next?.handle(request);
                }
            },

            // ================================================================
            // REPORT SELECTION & YEARMONTH CHANGE
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    const bpmcsrf = getBpmcsrf();

                    // --------------------------------------------------------
                    // REPORT SELECTION CHANGE
                    // --------------------------------------------------------
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_0as4io2;

                        if (selectedReport && selectedReport.displayValue && selectedReport.value) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission");
                            const isItemsByCustomer = reportName.includes("items by customer");

                            // Check for Looker URL
                            let reportUrl = "";
                            try {
                                const metaUrl = "/0/odata/UsrReportesPampa(" + selectedReport.value + ")?$select=UsrURL";
                                const resp = await fetch(metaUrl, {
                                    method: "GET",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                });
                                if (resp.ok) {
                                    const meta = await resp.json();
                                    if (meta && typeof meta.UsrURL !== 'undefined') {
                                        reportUrl = meta.UsrURL || "";
                                    }
                                }
                            } catch (e) {
                                console.log("[v19.12] Error checking report URL:", e);
                            }

                            const isLookerReport = reportUrl && reportUrl.length > 0;

                            // Clear filters
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;
                            request.$context.UsrCustomer = null;
                            validSalesGroupIds = null;

                            if (isCommissionReport) {
                                request.$context.UsrShowCommissionFilters = true;
                                request.$context.UsrShowDateStatusFilters = false;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = true;
                                console.log("[v19.12] COMMISSION report | Cascade ENABLED");

                            } else if (isItemsByCustomer) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = true;
                                cascadeFilterEnabled = false;
                                console.log("[v19.12] ITEMS BY CUSTOMER report");

                            } else if (isLookerReport) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = false;
                                console.log("[v19.12] LOOKER report");

                            } else {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = false;
                                console.log("[v19.12] OTHER EXCEL report");
                            }
                        } else {
                            request.$context.UsrShowCommissionFilters = false;
                            request.$context.UsrShowDateStatusFilters = false;
                            request.$context.UsrShowCustomerFilter = false;
                            cascadeFilterEnabled = false;
                            validSalesGroupIds = null;
                            console.log("[v19.12] No report selected");
                        }
                    }

                    // --------------------------------------------------------
                    // YEARMONTH CHANGE - Fetch cascade data + FORCE RELOAD
                    // --------------------------------------------------------
                    if (request.attributeName === "UsrYearMonth" && !request.silent && cascadeFilterEnabled) {
                        const yearMonth = await request.$context.UsrYearMonth;

                        // Clear current selection
                        request.$context.UsrSalesGroup = null;

                        if (yearMonth && yearMonth.value) {
                            console.log("[v19.12] YearMonth changed to:", yearMonth.displayValue);

                            // Fetch valid sales groups
                            try {
                                // v19.12: Use BGSalesGroup column (not BGSalesGroupId) like v19.3
                                const queryUrl = "/0/odata/BGCommissionSalesGroupByYearMonth?" +
                                    "$filter=BGYearMonth/Id eq " + yearMonth.value +
                                    "&$select=BGSalesGroup";

                                console.log("[v19.12] Fetching cascade data...");
                                const resp = await fetch(queryUrl, {
                                    method: "GET",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                });

                                if (resp.ok) {
                                    const data = await resp.json();
                                    const groupIds = new Set();

                                    (data.value || []).forEach(row => {
                                        // v19.3 uses BGSalesGroup, might be an object with Id
                                        if (row.BGSalesGroup) {
                                            // Could be direct GUID or object
                                            const gid = typeof row.BGSalesGroup === 'object'
                                                ? row.BGSalesGroup.Id
                                                : row.BGSalesGroup;
                                            if (gid) groupIds.add(gid);
                                        }
                                        // Also check BGSalesGroupId in case it's there
                                        if (row.BGSalesGroupId) {
                                            groupIds.add(row.BGSalesGroupId);
                                        }
                                    });

                                    validSalesGroupIds = Array.from(groupIds);
                                    console.log("[v19.12] Found", validSalesGroupIds.length, "groups for", yearMonth.displayValue);

                                    // Fallback if no results
                                    if (validSalesGroupIds.length === 0) {
                                        console.log("[v19.12] Trying fallback query to BGCommissionReportDataView...");
                                        const fallbackUrl = "/0/odata/BGCommissionReportDataView?" +
                                            "$filter=BGYearMonth/Id eq " + yearMonth.value +
                                            "&$select=BGSalesGroup&$top=1000";

                                        const fallbackResp = await fetch(fallbackUrl, {
                                            method: "GET",
                                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                        });

                                        if (fallbackResp.ok) {
                                            const fallbackData = await fallbackResp.json();
                                            const fallbackGroups = new Set();
                                            (fallbackData.value || []).forEach(row => {
                                                if (row.BGSalesGroup) {
                                                    const gid = typeof row.BGSalesGroup === 'object'
                                                        ? row.BGSalesGroup.Id
                                                        : row.BGSalesGroup;
                                                    if (gid) fallbackGroups.add(gid);
                                                }
                                            });
                                            validSalesGroupIds = Array.from(fallbackGroups);
                                            console.log("[v19.12] Fallback found", validSalesGroupIds.length, "groups");
                                        }
                                    }
                                } else {
                                    console.log("[v19.12] Cascade query failed:", resp.status);
                                    validSalesGroupIds = null;
                                }
                            } catch (e) {
                                console.log("[v19.12] Cascade query error:", e);
                                validSalesGroupIds = null;
                            }

                            // ========================================================
                            // KEY FIX FROM v19.3: Force reload of Sales Group dropdown
                            // This triggers LoadDataRequest which applies our filter
                            // ========================================================
                            try {
                                console.log("[v19.12] Forcing Sales Group dropdown reload...");
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
                                console.log("[v19.12] ✓ Sales Group dropdown reloaded with filter!");
                            } catch (e) {
                                console.log("[v19.12] Reload request error:", e);
                                // Try alternative method
                                try {
                                    console.log("[v19.12] Trying alternative reload method...");
                                    await request.$context.executeRequest({
                                        type: "crt.LoadDataRequest",
                                        config: { loadType: "reload" },
                                        dataSourceName: "UsrSalesGroup_List_DS"
                                    });
                                    console.log("[v19.12] ✓ Alternative reload succeeded");
                                } catch (e2) {
                                    console.log("[v19.12] Alternative reload also failed:", e2);
                                }
                            }

                        } else {
                            validSalesGroupIds = null;
                            console.log("[v19.12] YearMonth cleared");
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
                    const context = request.$context;
                    const selectedReport = await context.LookupAttribute_0as4io2;

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    let reportDisplayName = selectedReport.displayValue || "";
                    const bpmcsrf = getBpmcsrf();

                    let reportUrl = "";
                    let reportCode = "";
                    try {
                        const reportMetaUrl = "/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=Id,Name,UsrURL,UsrCode";
                        const reportMetaResp = await fetch(reportMetaUrl, {
                            method: "GET",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (reportMetaResp.ok) {
                            const reportMeta = await reportMetaResp.json();
                            if (reportMeta) {
                                reportDisplayName = reportMeta.Name || reportDisplayName;
                                reportUrl = (typeof reportMeta.UsrURL !== 'undefined') ? (reportMeta.UsrURL || "") : "";
                                reportCode = (typeof reportMeta.UsrCode !== 'undefined') ? (reportMeta.UsrCode || "") : "";
                            }
                        }
                    } catch (e) {
                        console.log("[v19.12] Metadata lookup failed:", e);
                    }

                    // LOOKER PATH
                    if (reportUrl && reportUrl.length > 0) {
                        var params = buildLookerParams(context);
                        var fullUrl = reportUrl + params;
                        console.log("[v19.12] Opening Looker:", reportDisplayName);
                        window.open(fullUrl, "_blank");
                        Terrasoft.showInformation("Report opened in new tab");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[v19.12] Generating Excel:", reportDisplayName);

                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;
                    var customerId = emptyGuid;

                    if (reportDisplayName.toLowerCase().includes("commission")) {
                        try {
                            const yearMonth = await context.UsrYearMonth;
                            if (yearMonth && yearMonth.value) {
                                yearMonthId = yearMonth.value;
                                console.log("[v19.12] YearMonth:", yearMonth.displayValue);
                            }
                        } catch (e) {}
                        try {
                            const salesGroup = await context.UsrSalesGroup;
                            if (salesGroup && salesGroup.value) {
                                salesGroupId = salesGroup.value;
                                console.log("[v19.12] SalesGroup:", salesGroup.displayValue);
                            }
                        } catch (e) {}
                    }

                    if (reportDisplayName.toLowerCase().includes("items by customer")) {
                        try {
                            const customer = await context.UsrCustomer;
                            if (customer && customer.value) {
                                customerId = customer.value;
                                console.log("[v19.12] Customer:", customer.displayValue);
                            }
                        } catch (e) {}
                    }

                    var intExcelReportId = null;
                    try {
                        var escapeName = function(s) { return s.replace(/'/g, "''"); };
                        var odataUrl = "/0/odata/IntExcelReport?$filter=" +
                            "(IntName eq '" + escapeName(reportDisplayName) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportDisplayName) + "'" +
                            " or IntName eq '" + escapeName(reportCode) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportCode) + "')" +
                            "&$select=Id,IntName&$top=1";
                        const odataResponse = await fetch(odataUrl, {
                            method: "GET",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        const odataResult = await odataResponse.json();
                        if (odataResult.value && odataResult.value.length > 0) {
                            intExcelReportId = odataResult.value[0].Id;
                            console.log("[v19.12] Template:", odataResult.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    try {
                        Terrasoft.showInformation("Generating Excel report...");
                        const response = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify({
                                ReportId: intExcelReportId,
                                YearMonthId: yearMonthId,
                                SalesRepId: salesGroupId,
                                CustomerId: customerId
                            })
                        });
                        const result = await response.json();
                        console.log("[v19.12] Service response:", result);

                        if (result.success && result.key) {
                            var downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" +
                                result.key + "/" + encodeURIComponent(reportDisplayName || "Report");
                            var iframe = document.getElementById("reportDownloadFrame");
                            if (!iframe) {
                                iframe = document.createElement("iframe");
                                iframe.id = "reportDownloadFrame";
                                iframe.style.display = "none";
                                document.body.appendChild(iframe);
                            }
                            iframe.src = downloadUrl;
                            Terrasoft.showInformation("Download starting...");
                        } else {
                            var errorMsg = result.message || result.errorMessage || "Unknown error";
                            Terrasoft.showErrorMessage("Failed: " + errorMsg);
                        }
                    } catch (error) {
                        console.error("[v19.12] Error:", error);
                        Terrasoft.showErrorMessage("Error: " + error.message);
                    }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
