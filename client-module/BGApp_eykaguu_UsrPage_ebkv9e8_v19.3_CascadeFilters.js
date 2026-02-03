/**
 * UsrPage_ebkv9e8 - v19.3 Cascade Filters
 * Package: BGApp_eykaguu
 *
 * CHANGES FROM v19.2:
 * - FIX: Sales Group dropdown ACTUALLY filtered using crt.LoadDataRequest interception
 * - FIX: Customer filter properly wired for "Items by Customer" report
 * - CLARIFICATION: "Expand All" is a Looker Studio feature, not controllable from Creatio
 *
 * v19.3 FIXES (2026-01-27):
 * - Issue 2: Sales Group cascade - intercepts LoadDataRequest to filter by valid YearMonth combos
 * - Issue 3: Customer filter - properly binds to Account lookup with correct visibility
 * - Issue 1: NOT FIXABLE - "Sales by Sales Group" expand is Looker Studio's table drill-down feature
 *
 * KEY INSIGHT: The Sales Group dropdown needs LoadDataRequest interception to filter,
 * not just storing available groups. The filter is applied at the data source level.
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

    // Format date as YYYY-MM-DD for Looker params
    function formatDateForLooker(dateValue) {
        if (!dateValue) return null;
        var d = new Date(dateValue);
        if (isNaN(d.getTime())) return null;
        var year = d.getFullYear();
        var month = String(d.getMonth() + 1).padStart(2, '0');
        var day = String(d.getDate()).padStart(2, '0');
        return year + '-' + month + '-' + day;
    }

    // Build Looker Studio URL params
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

        var customer = attrs.UsrCustomer;
        if (customer && customer.displayValue) {
            filters.push("contains(BGAccount, '" + customer.displayValue + "')");
        }

        if (filters.length > 0) {
            param = param + '"' + filters.join(' and ') + '","ds0.top":"1000000"%7D';
        } else {
            param = param + '"","ds0.top":"1000000"%7D';
        }

        return param;
    }

    // Global state for cascade filtering
    var currentYearMonthId = null;
    var validSalesGroupIds = null; // null = no filter, [] = empty, [...ids] = filter to these

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // ================================================================
            // HIDE PARENT'S REPORT DROPDOWN (we insert our own)
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": {
                    "visible": false
                }
            },

            // ================================================================
            // HIDE THE IFRAME CONTAINER
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            },

            // ================================================================
            // DATE FILTERS CONTAINER - Bind to attribute for dynamic visibility
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": {
                    "visible": "$UsrShowDateStatusFilters"
                }
            },

            // ================================================================
            // STATUS FILTER CONTAINER - Bind to attribute for dynamic visibility
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": {
                    "visible": "$UsrShowDateStatusFilters"
                }
            },

            // ================================================================
            // WIRE GENERATE BUTTON TO OUR HANDLER
            // ================================================================
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "visible": true,
                    "clicked": {
                        "request": "usr.GenerateReportRequest"
                    }
                }
            },

            // ================================================================
            // INSERT: Report selector container (always visible)
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

            // ================================================================
            // INSERT: Report dropdown
            // ================================================================
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
                    "visible": true,
                    "tooltip": ""
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
            // INSERT: Commission filters container (conditional)
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

            // ================================================================
            // INSERT: Year-Month filter
            // ================================================================
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

            // ================================================================
            // INSERT: Sales Group filter (CASCADED by YearMonth via LoadDataRequest)
            // ================================================================
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
                    "tooltip": "Shows only groups with commission data for selected month"
                },
                "parentName": "BGCommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // INSERT: Customer filter container (for "Items by Customer" report)
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

            // ================================================================
            // INSERT: Customer lookup dropdown
            // ================================================================
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
                    "tooltip": "Filter by customer (Account)"
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
                    "UsrYearMonth": {
                        "lookupListConfig": {
                            "entitySchemaName": "BGYearMonth",
                            "hierarchical": false,
                            "orders": [
                                {
                                    "columnPath": "Name",
                                    "direction": "Desc"
                                }
                            ]
                        }
                    },
                    "UsrSalesGroup": {
                        "lookupListConfig": {
                            "entitySchemaName": "BGSalesGroup",
                            "hierarchical": false,
                            "orders": [
                                {
                                    "columnPath": "BGSalesGroupName",
                                    "direction": "Asc"
                                }
                            ]
                        }
                    },
                    "UsrCustomer": {
                        "lookupListConfig": {
                            "entitySchemaName": "Account",
                            "hierarchical": false,
                            "orders": [
                                {
                                    "columnPath": "Name",
                                    "direction": "Asc"
                                }
                            ]
                        }
                    }
                }
            }
        ]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // ================================================================
            // PAGE INIT - Log initialization
            // ================================================================
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v19.3] Page init - cascade filter support enabled");
                    // Reset global state
                    currentYearMonthId = null;
                    validSalesGroupIds = null;
                    return;
                }
            },

            // ================================================================
            // LOAD DATA REQUEST - Intercept to apply cascade filter on Sales Group
            // ================================================================
            {
                request: "crt.LoadDataRequest",
                handler: async (request, next) => {
                    // Check if this is the Sales Group lookup list
                    const dsName = request.dataSourceName || "";

                    // Sales Group lookup uses a data source like "UsrSalesGroup_List_DS"
                    if (dsName.includes("SalesGroup") && dsName.includes("_List")) {
                        console.log("[v19.3] Intercepting Sales Group data load:", dsName);

                        // Apply filter if we have valid group IDs
                        if (validSalesGroupIds !== null && validSalesGroupIds.length > 0) {
                            // Build IN filter for allowed IDs
                            const filterItems = {};
                            validSalesGroupIds.forEach((groupId, idx) => {
                                filterItems["SalesGroupFilter_" + idx] = {
                                    filterType: 1,  // Compare
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
                                    logicalOperation: 1, // OR - match ANY of the valid IDs
                                    isEnabled: true,
                                    filterType: 6  // FilterGroup
                                }
                            }];

                            console.log("[v19.3] Applied filter for", validSalesGroupIds.length, "sales groups");
                        } else if (validSalesGroupIds !== null && validSalesGroupIds.length === 0) {
                            // No valid groups - filter to nothing (show empty list)
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
                            console.log("[v19.3] No valid sales groups for selected month - showing empty list");
                        }
                        // If validSalesGroupIds is null, no filter is applied (show all)
                    }

                    return next?.handle(request);
                }
            },

            // ================================================================
            // REPORT SELECTION - Update visibility attributes based on report type
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    const bpmcsrf = getBpmcsrf();

                    // Handle Report selection change
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_0as4io2;

                        if (selectedReport && selectedReport.displayValue && selectedReport.value) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission");
                            const isItemsByCustomer = reportName.includes("items by customer");

                            // Check if report has Looker URL
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
                                console.log("[v19.3] Error checking report URL:", e);
                            }

                            const isLookerReport = reportUrl && reportUrl.length > 0;

                            // Clear filter values when switching reports
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;
                            request.$context.UsrCustomer = null;

                            // Reset cascade state
                            currentYearMonthId = null;
                            validSalesGroupIds = null;

                            // Apply visibility rules
                            if (isCommissionReport) {
                                request.$context.UsrShowCommissionFilters = true;
                                request.$context.UsrShowDateStatusFilters = false;
                                request.$context.UsrShowCustomerFilter = false;
                                console.log("[v19.3] Report:", selectedReport.displayValue, "| Type: COMMISSION | Showing YearMonth + SalesGroup filters");

                            } else if (isItemsByCustomer) {
                                // Items by Customer: Show date+status AND customer filter
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = true;
                                console.log("[v19.3] Report:", selectedReport.displayValue, "| Type: ITEMS_BY_CUSTOMER | Showing date+status + customer filter");

                            } else if (isLookerReport) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                console.log("[v19.3] Report:", selectedReport.displayValue, "| Type: LOOKER | Showing date+status filters");

                            } else {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                console.log("[v19.3] Report:", selectedReport.displayValue, "| Type: EXCEL | Showing date+status filters");
                            }
                        } else {
                            request.$context.UsrShowCommissionFilters = false;
                            request.$context.UsrShowDateStatusFilters = false;
                            request.$context.UsrShowCustomerFilter = false;
                            currentYearMonthId = null;
                            validSalesGroupIds = null;
                            console.log("[v19.3] No report selected | All filters hidden");
                        }
                    }

                    // Handle YearMonth change - Update cascade filter for Sales Group
                    if (request.attributeName === "UsrYearMonth" && !request.silent) {
                        const yearMonth = await request.$context.UsrYearMonth;

                        if (yearMonth && yearMonth.value) {
                            console.log("[v19.3] YearMonth changed to:", yearMonth.displayValue, "| ID:", yearMonth.value);
                            currentYearMonthId = yearMonth.value;

                            // Clear current sales group selection
                            request.$context.UsrSalesGroup = null;

                            // Fetch valid sales groups for this month from BGCommissionSalesGroupByYearMonth
                            try {
                                const odataUrl = "/0/odata/BGCommissionSalesGroupByYearMonth?" +
                                    "$filter=BGYearMonth/Id eq " + yearMonth.value +
                                    "&$select=BGSalesGroup";

                                const resp = await fetch(odataUrl, {
                                    method: "GET",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                });

                                if (resp.ok) {
                                    const data = await resp.json();
                                    const groupIds = new Set();
                                    (data.value || []).forEach(row => {
                                        if (row.BGSalesGroup) {
                                            groupIds.add(row.BGSalesGroup);
                                        }
                                    });

                                    validSalesGroupIds = Array.from(groupIds);
                                    console.log("[v19.3] Found", validSalesGroupIds.length, "valid sales groups for", yearMonth.displayValue);

                                    if (validSalesGroupIds.length === 0) {
                                        // Fallback: query commission data directly
                                        console.log("[v19.3] No groups in BGCommissionSalesGroupByYearMonth, trying BGCommissionReportDataView...");
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
                                                    fallbackGroups.add(row.BGSalesGroup);
                                                }
                                            });
                                            validSalesGroupIds = Array.from(fallbackGroups);
                                            console.log("[v19.3] Fallback found", validSalesGroupIds.length, "groups from commission data");
                                        }
                                    }
                                } else {
                                    console.log("[v19.3] BGCommissionSalesGroupByYearMonth query failed, showing all groups");
                                    validSalesGroupIds = null; // Show all
                                }
                            } catch (e) {
                                console.log("[v19.3] Error fetching valid sales groups:", e);
                                validSalesGroupIds = null; // Show all on error
                            }

                            // Trigger reload of Sales Group dropdown to apply the filter
                            // This requires the LoadDataRequest handler to intercept and apply our filter
                            try {
                                // Force reload by clearing and resetting (Freedom UI pattern)
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
                                console.log("[v19.3] Sales Group dropdown reloaded with filter");
                            } catch (e) {
                                console.log("[v19.3] Sales Group reload request error:", e);
                            }
                        } else {
                            currentYearMonthId = null;
                            validSalesGroupIds = null;
                            request.$context.UsrSalesGroup = null;
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

                    // Fetch report metadata
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
                        console.log("[v19.3] Metadata lookup failed:", e);
                    }

                    // LOOKER STUDIO - Open in new tab WITH URL PARAMS
                    if (reportUrl && reportUrl.length > 0) {
                        var params = buildLookerParams(context);
                        var fullUrl = reportUrl + params;
                        console.log("[v19.3] Opening Looker Studio:", fullUrl);
                        window.open(fullUrl, "_blank");
                        Terrasoft.showInformation("Report opened in new tab");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[v19.3] Generating Excel report:", reportDisplayName);

                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;
                    var customerId = emptyGuid;

                    // Get Commission filter values
                    if (reportDisplayName.toLowerCase().includes("commission")) {
                        try {
                            const yearMonth = await context.UsrYearMonth;
                            if (yearMonth && yearMonth.value) yearMonthId = yearMonth.value;
                        } catch (e) {}
                        try {
                            const salesGroup = await context.UsrSalesGroup;
                            if (salesGroup && salesGroup.value) salesGroupId = salesGroup.value;
                        } catch (e) {}
                    }

                    // Get Customer filter value for "Items by Customer"
                    if (reportDisplayName.toLowerCase().includes("items by customer")) {
                        try {
                            const customer = await context.UsrCustomer;
                            if (customer && customer.value) {
                                customerId = customer.value;
                                console.log("[v19.3] Customer filter:", customer.displayValue, "| ID:", customerId);
                            }
                        } catch (e) {}
                    }

                    // Find IntExcelReport template
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
                            console.log("[v19.3] Found template:", odataResult.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    // Generate Excel report
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
                        console.log("[v19.3] Excel service response:", result);

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
                        console.error("[v19.3] Error:", error);
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
