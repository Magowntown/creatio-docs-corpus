/**
 * UsrPage_ebkv9e8 - v19.9 Complete (Issues 2+3 Fixed)
 * Package: BGApp_eykaguu
 *
 * FIXES:
 * - Issue 2: Sales Group CASCADE FILTER - Only shows groups with data for selected Year-Month
 *            FIXED: When no groups match, shows ALL groups (graceful fallback)
 * - Issue 3: Customer filter for "Items by Customer" report
 *
 * v19.9 KEY FIX:
 * The v19.7 bug was: when validSalesGroupIds was empty [], it applied an impossible filter
 * that matched nothing, showing "no data" in the dropdown.
 *
 * The v19.9 fix: When no groups match the selected YearMonth, DON'T apply filter (show all).
 * This ensures the dropdown always has options - filtered when data exists, all when it doesn't.
 *
 * VISIBILITY RULES:
 * | Report Type          | Commission Filters | Date+Status Filters | Customer Filter | Action         |
 * |----------------------|-------------------|---------------------|-----------------|----------------|
 * | None selected        | Hidden            | Hidden              | Hidden          | -              |
 * | Commission           | VISIBLE           | Hidden              | Hidden          | Excel+Cascade  |
 * | Items by Customer    | Hidden            | VISIBLE             | VISIBLE         | Excel          |
 * | Non-Commission Excel | Hidden            | VISIBLE             | Hidden          | Excel          |
 * | Looker Studio        | Hidden            | VISIBLE             | Hidden          | New Tab+Params |
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
    // - cascadeFilterEnabled: true when Commission report is selected
    // - validSalesGroupIds: array of GUIDs, or null (no filter)
    // - KEY FIX: empty array [] means "no matches" -> show ALL (no filter)
    // ================================================================
    var cascadeFilterEnabled = false;
    var validSalesGroupIds = null;  // null = no filter, [] = no matches (show all), [...] = filter to these

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
                    "tooltip": "Filtered by Year-Month when data exists",
                    "mode": "List"
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
                    // YearMonth - bound to page entity
                    "UsrYearMonth": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGYearMonth"
                        }
                    },
                    // SalesGroup - bound to page entity
                    "UsrSalesGroup": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGSalesGroup"
                        }
                    },
                    "UsrSalesGroup_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{"columnName": "BGSalesGroupName", "direction": "asc"}]
                            }
                        }
                    },
                    // Customer - CORRECTED column name (BGCustomer, not Customer)
                    "UsrCustomer": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGCustomer"
                        }
                    },
                    "UsrCustomer_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{"columnName": "Name", "direction": "asc"}]
                            }
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
                    console.log("[v19.9] Page init - Issues 2+3 fixed");
                    cascadeFilterEnabled = false;
                    validSalesGroupIds = null;
                    return;
                }
            },

            // ================================================================
            // LOAD DATA REQUEST - CASCADE FILTER FOR SALES GROUP
            // KEY FIX: Only apply filter when validSalesGroupIds has items
            //          If empty array, DON'T filter (show all groups)
            // ================================================================
            {
                request: "crt.LoadDataRequest",
                handler: async (request, next) => {
                    const dsName = request.dataSourceName || "";

                    // Only intercept Sales Group list when cascade is enabled
                    const isSalesGroupList = dsName.includes("SalesGroup") && dsName.includes("_List");

                    if (cascadeFilterEnabled && isSalesGroupList) {
                        console.log("[v19.9] Sales Group list load | validIds:",
                            validSalesGroupIds === null ? "null (no filter)" :
                            validSalesGroupIds.length === 0 ? "[] (no matches - show all)" :
                            validSalesGroupIds.length + " groups");

                        // KEY FIX: Only apply filter if we have actual IDs to filter by
                        // If validSalesGroupIds is null OR empty [], don't filter (show all)
                        if (validSalesGroupIds !== null && validSalesGroupIds.length > 0) {
                            // Build filter for specific group IDs
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
                                    logicalOperation: 1,  // OR - match any of these IDs
                                    isEnabled: true,
                                    filterType: 6
                                }
                            }];
                            console.log("[v19.9] Applied cascade filter for", validSalesGroupIds.length, "groups");
                        } else {
                            // No filter to apply - show all groups (graceful fallback)
                            console.log("[v19.9] No cascade filter - showing all groups");
                        }
                    }

                    return next?.handle(request);
                }
            },

            // ================================================================
            // REPORT SELECTION - Visibility + cascade state
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
                                console.log("[v19.9] Error checking report URL:", e);
                            }

                            const isLookerReport = reportUrl && reportUrl.length > 0;

                            // Clear all filter values when switching reports
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;
                            request.$context.UsrCustomer = null;
                            validSalesGroupIds = null;

                            // Set visibility and cascade state based on report type
                            if (isCommissionReport) {
                                request.$context.UsrShowCommissionFilters = true;
                                request.$context.UsrShowDateStatusFilters = false;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = true;
                                console.log("[v19.9] COMMISSION report | Cascade: ENABLED | Filters: YearMonth+SalesGroup");

                            } else if (isItemsByCustomer) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = true;
                                cascadeFilterEnabled = false;
                                console.log("[v19.9] ITEMS BY CUSTOMER report | Filters: Date+Status+Customer");

                            } else if (isLookerReport) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = false;
                                console.log("[v19.9] LOOKER report | Filters: Date+Status");

                            } else {
                                // Other Excel reports
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = false;
                                console.log("[v19.9] OTHER EXCEL report | Filters: Date+Status");
                            }
                        } else {
                            // No report selected - hide everything
                            request.$context.UsrShowCommissionFilters = false;
                            request.$context.UsrShowDateStatusFilters = false;
                            request.$context.UsrShowCustomerFilter = false;
                            cascadeFilterEnabled = false;
                            validSalesGroupIds = null;
                            console.log("[v19.9] No report selected | All filters hidden");
                        }
                    }

                    // --------------------------------------------------------
                    // YEARMONTH CHANGE - Fetch valid Sales Groups (cascade)
                    // --------------------------------------------------------
                    if (request.attributeName === "UsrYearMonth" && !request.silent && cascadeFilterEnabled) {
                        const yearMonth = await request.$context.UsrYearMonth;

                        if (yearMonth && yearMonth.value) {
                            console.log("[v19.9] YearMonth changed to:", yearMonth.displayValue);

                            // Clear current sales group selection
                            request.$context.UsrSalesGroup = null;

                            // Query BGCommissionSalesGroupByYearMonth for valid groups
                            try {
                                // NOTE: Must use navigation property path BGYearMonth/Id (not BGYearMonthId)
                                const queryUrl = "/0/odata/BGCommissionSalesGroupByYearMonth?" +
                                    "$filter=BGYearMonth/Id eq " + yearMonth.value +
                                    "&$select=BGSalesGroupId";

                                console.log("[v19.9] Querying cascade data...");
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
                                        console.log("[v19.9] Found", validSalesGroupIds.length, "groups with data for", yearMonth.displayValue);
                                    } else {
                                        console.log("[v19.9] No groups found for", yearMonth.displayValue, "- will show ALL groups");
                                    }
                                } else {
                                    console.log("[v19.9] Cascade query failed:", resp.status);
                                    validSalesGroupIds = null;  // Error case - show all
                                }
                            } catch (e) {
                                console.log("[v19.9] Cascade query error:", e);
                                validSalesGroupIds = null;  // Error case - show all
                            }
                        } else {
                            // No YearMonth selected - clear cascade filter
                            validSalesGroupIds = null;
                            request.$context.UsrSalesGroup = null;
                            console.log("[v19.9] YearMonth cleared - cascade filter disabled");
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

                    // Fetch report metadata (URL, Code)
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
                        console.log("[v19.9] Metadata lookup failed:", e);
                    }

                    // --------------------------------------------------------
                    // LOOKER STUDIO - Open in new tab with params
                    // --------------------------------------------------------
                    if (reportUrl && reportUrl.length > 0) {
                        var params = buildLookerParams(context);
                        var fullUrl = reportUrl + params;
                        console.log("[v19.9] Opening Looker:", reportDisplayName);
                        window.open(fullUrl, "_blank");
                        Terrasoft.showInformation("Report opened in new tab");
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // EXCEL PATH
                    // --------------------------------------------------------
                    console.log("[v19.9] Generating Excel:", reportDisplayName);

                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;
                    var customerId = emptyGuid;

                    // Get Commission filter values
                    if (reportDisplayName.toLowerCase().includes("commission")) {
                        try {
                            const yearMonth = await context.UsrYearMonth;
                            if (yearMonth && yearMonth.value) {
                                yearMonthId = yearMonth.value;
                                console.log("[v19.9] Commission YearMonth:", yearMonth.displayValue);
                            }
                        } catch (e) {}
                        try {
                            const salesGroup = await context.UsrSalesGroup;
                            if (salesGroup && salesGroup.value) {
                                salesGroupId = salesGroup.value;
                                console.log("[v19.9] Commission SalesGroup:", salesGroup.displayValue);
                            }
                        } catch (e) {}
                    }

                    // Get Customer filter value for "Items by Customer"
                    if (reportDisplayName.toLowerCase().includes("items by customer")) {
                        try {
                            const customer = await context.UsrCustomer;
                            if (customer && customer.value) {
                                customerId = customer.value;
                                console.log("[v19.9] Customer filter:", customer.displayValue, "| ID:", customerId);
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
                            console.log("[v19.9] Found template:", odataResult.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    // Generate Excel via UsrExcelReportService
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
                        console.log("[v19.9] Service response:", result);

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
                        console.error("[v19.9] Error:", error);
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
