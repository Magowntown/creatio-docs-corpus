/**
 * UsrPage_ebkv9e8 - v21 Complete (v19.16 + Embedded Looker)
 * Package: BGApp_eykaguu
 *
 * COMBINES:
 * - v19.16: All working features (Commission, Items by Customer, Date filters, Cascade)
 * - v20: Embedded Looker iframe (instead of new tab)
 * - GUID validation to prevent TypeError during typing
 *
 * VISIBILITY RULES:
 * | Report Type          | Commission Filters | Date+Status | Customer | Iframe  |
 * |----------------------|-------------------|-------------|----------|---------|
 * | None selected        | Hidden            | Hidden      | Hidden   | Hidden  |
 * | Commission           | VISIBLE           | Hidden      | Hidden   | Hidden  |
 * | Items by Customer    | Hidden            | VISIBLE     | VISIBLE  | Hidden  |
 * | Non-Commission Excel | Hidden            | VISIBLE     | Hidden   | Hidden  |
 * | Looker Studio        | Hidden            | VISIBLE     | Hidden   | VISIBLE |
 *
 * Schema: UsrPage_ebkv9e8
 * PROD: https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
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

    // Convert date to WCF/Microsoft JSON format: /Date(milliseconds)/
    function formatDateForWcf(dateValue) {
        if (!dateValue) return null;
        var d = new Date(dateValue);
        if (isNaN(d.getTime())) return null;
        return "/Date(" + d.getTime() + ")/";
    }

    function buildLookerParams(context) {
        var param = '?params=%7B"ds0.additionalFilters":';
        var filters = [];
        var attrs = context.attributes || {};

        if (attrs.CreatedFrom != null) {
            var createdfrom = formatDateForLooker(attrs.CreatedFrom);
            if (createdfrom) filters.push('CreatedOn ge datetime' + "'" + createdfrom + "'");
        }
        if (attrs.CreatedTo != null) {
            var createdto = formatDateForLooker(attrs.CreatedTo);
            if (createdto) filters.push('CreatedOn le datetime' + "'" + createdto + "'");
        }
        if (attrs.ShippingFrom != null) {
            var shippingfrom = formatDateForLooker(attrs.ShippingFrom);
            if (shippingfrom) filters.push('BGShipDate ge datetime' + "'" + shippingfrom + "'");
        }
        if (attrs.ShippingTo != null) {
            var shippingto = formatDateForLooker(attrs.ShippingTo);
            if (shippingto) filters.push('BGShipDate le datetime' + "'" + shippingto + "'");
        }
        if (attrs.DeliveryFrom != null) {
            var deliveryfrom = formatDateForLooker(attrs.DeliveryFrom);
            if (deliveryfrom) filters.push('BGDeliveryDate ge datetime' + "'" + deliveryfrom + "'");
        }
        if (attrs.DeliveryTo != null) {
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

    // Validate GUID format (prevents errors during typing)
    function isValidGuid(str) {
        if (!str || typeof str !== 'string') return false;
        return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(str);
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
            // Iframe container - bind visibility to attribute (for Looker embedding)
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": "$UsrShowLookerIframe" }
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
                    "UsrShowCommissionFilters": { "value": false },
                    "UsrShowDateStatusFilters": { "value": false },
                    "UsrShowCustomerFilter": { "value": false },
                    "UsrShowLookerIframe": { "value": false },
                    "UsrYearMonth": {
                        "modelConfig": { "path": "UsrEntity_e7ac661DS.BGYearMonth" }
                    },
                    "UsrSalesGroup": {
                        "modelConfig": { "path": "UsrEntity_e7ac661DS.BGSalesGroup" }
                    },
                    "UsrSalesGroup_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{"columnName": "BGSalesGroupName", "direction": "asc"}]
                            }
                        }
                    },
                    "UsrCustomer": {
                        "modelConfig": { "path": "UsrEntity_e7ac661DS.BGCustomer" }
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
                    console.log("[v21] Page init - Complete handler (v19.16 + Embedded Looker)");
                    cascadeFilterEnabled = false;
                    validSalesGroupIds = null;
                    request.$context.UsrShowLookerIframe = false;
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
                    const isSalesGroupList = dsName.includes("SalesGroup") && dsName.includes("_List");

                    if (cascadeFilterEnabled && isSalesGroupList) {
                        console.log("[v21] Sales Group list load | validIds:",
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
                            console.log("[v21] Applied cascade filter for", validSalesGroupIds.length, "groups");
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
                        let selectedReport = null;
                        try {
                            selectedReport = await request.$context.LookupAttribute_0as4io2;
                        } catch (e) {
                            return next?.handle(request);
                        }

                        // GUID validation - prevents errors during typing
                        if (!selectedReport || !selectedReport.value || !isValidGuid(selectedReport.value)) {
                            return next?.handle(request);
                        }

                        if (selectedReport.displayValue) {
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
                                    const responseText = await resp.text();
                                    try {
                                        const meta = JSON.parse(responseText);
                                        if (meta && typeof meta.UsrURL === 'string') {
                                            reportUrl = meta.UsrURL;
                                        }
                                    } catch (e) {}
                                }
                            } catch (e) {
                                console.log("[v21] Error checking report URL:", e);
                            }

                            const isLookerReport = reportUrl && reportUrl.length > 0;

                            // Clear all filter values when switching reports
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;
                            request.$context.UsrCustomer = null;
                            request.$context.UsrShowLookerIframe = false;
                            validSalesGroupIds = null;

                            // Set visibility based on report type
                            if (isCommissionReport) {
                                request.$context.UsrShowCommissionFilters = true;
                                request.$context.UsrShowDateStatusFilters = false;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = true;
                                console.log("[v21] COMMISSION report | Cascade: ENABLED");

                            } else if (isItemsByCustomer) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = true;
                                cascadeFilterEnabled = false;
                                console.log("[v21] ITEMS BY CUSTOMER report | Filters: Date+Status+Customer");

                            } else if (isLookerReport) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = false;
                                console.log("[v21] LOOKER report | URL:", reportUrl);

                            } else {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = false;
                                console.log("[v21] OTHER EXCEL report");
                            }
                        }
                    }

                    // --------------------------------------------------------
                    // YEARMONTH CHANGE - Fetch valid Sales Groups (cascade)
                    // --------------------------------------------------------
                    if (request.attributeName === "UsrYearMonth" && !request.silent && cascadeFilterEnabled) {
                        const yearMonth = await request.$context.UsrYearMonth;

                        if (yearMonth && yearMonth.value) {
                            console.log("[v21] YearMonth changed to:", yearMonth.displayValue);
                            request.$context.UsrSalesGroup = null;

                            try {
                                const queryUrl = "/0/odata/BGCommissionSalesGroupByYearMonth?" +
                                    "$filter=BGYearMonth/Id eq " + yearMonth.value +
                                    "&$select=BGSalesGroupId";

                                const resp = await fetch(queryUrl, {
                                    method: "GET",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                });

                                if (resp.ok) {
                                    const data = await resp.json();
                                    const groupIds = new Set();
                                    (data.value || []).forEach(row => {
                                        if (row.BGSalesGroupId) groupIds.add(row.BGSalesGroupId);
                                    });
                                    validSalesGroupIds = Array.from(groupIds);
                                    console.log("[v21] Found", validSalesGroupIds.length, "groups for", yearMonth.displayValue);
                                } else {
                                    validSalesGroupIds = null;
                                }
                            } catch (e) {
                                validSalesGroupIds = null;
                            }

                            // Force reload Sales Group dropdown
                            try {
                                const reloadRequest = {
                                    type: "crt.LoadDataRequest",
                                    $context: request.$context,
                                    config: { loadType: "reload", useLastLoadParameters: false },
                                    dataSourceName: "UsrSalesGroup_List_DS",
                                    scopes: [...(request.scopes || [])]
                                };
                                await sdk.HandlerChainService.instance.process(reloadRequest);
                            } catch (e) {}

                        } else {
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
                            const responseText = await reportMetaResp.text();
                            try {
                                const reportMeta = JSON.parse(responseText);
                                if (reportMeta) {
                                    reportDisplayName = reportMeta.Name || reportDisplayName;
                                    reportUrl = (reportMeta.UsrURL && typeof reportMeta.UsrURL === 'string') ? reportMeta.UsrURL : "";
                                    reportCode = (reportMeta.UsrCode && typeof reportMeta.UsrCode === 'string') ? reportMeta.UsrCode : "";
                                }
                            } catch (e) {}
                        }
                    } catch (e) {
                        console.log("[v21] Metadata lookup failed:", e);
                    }

                    // --------------------------------------------------------
                    // LOOKER STUDIO - Embed in iframe
                    // --------------------------------------------------------
                    if (reportUrl && reportUrl.length > 0) {
                        var params = buildLookerParams(context);
                        var fullUrl = reportUrl + params;
                        console.log("[v21] LOOKER - Embedding in iframe:", fullUrl);

                        // Show iframe container
                        context.UsrShowLookerIframe = true;

                        // Set iframe src after DOM updates
                        setTimeout(() => {
                            var usrIframe = document.getElementById('UsrIframe');
                            if (usrIframe && usrIframe.shadowRoot) {
                                var iframe = usrIframe.shadowRoot.querySelector('iframe');
                                if (iframe) {
                                    iframe.src = fullUrl;
                                    console.log("[v21] Iframe src set successfully");
                                }
                            }
                        }, 500);

                        Terrasoft.showInformation("Loading report...");
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // EXCEL PATH
                    // --------------------------------------------------------
                    console.log("[v21] Generating Excel:", reportDisplayName);

                    // Hide iframe for Excel reports
                    context.UsrShowLookerIframe = false;

                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;
                    var customerId = emptyGuid;
                    var customerName = "";

                    // Get Commission filter values
                    if (reportDisplayName.toLowerCase().includes("commission")) {
                        try {
                            const yearMonth = await context.UsrYearMonth;
                            if (yearMonth && yearMonth.value) {
                                yearMonthId = yearMonth.value;
                                console.log("[v21] Commission YearMonth:", yearMonth.displayValue);
                            }
                        } catch (e) {}
                        try {
                            const salesGroup = await context.UsrSalesGroup;
                            if (salesGroup && salesGroup.value) {
                                salesGroupId = salesGroup.value;
                                console.log("[v21] Commission SalesGroup:", salesGroup.displayValue);
                            }
                        } catch (e) {}
                    }

                    // Get Customer filter value for "Items by Customer"
                    if (reportDisplayName.toLowerCase().includes("items by customer")) {
                        try {
                            const customer = await context.UsrCustomer;
                            if (customer && customer.value) {
                                customerId = customer.value;
                                customerName = customer.displayValue || "";
                                console.log("[v21] Customer filter:", customerName);
                            }
                        } catch (e) {}
                    }

                    // Get Date and Status filters for non-Commission reports
                    var createdFrom = null;
                    var createdTo = null;
                    var shippingFrom = null;
                    var shippingTo = null;
                    var deliveryFrom = null;
                    var deliveryTo = null;
                    var statusName = "";

                    if (!reportDisplayName.toLowerCase().includes("commission")) {
                        try {
                            const attrs = request.$context.attributes;

                            if (attrs.CreatedFrom != null) createdFrom = formatDateForWcf(attrs.CreatedFrom);
                            if (attrs.CreatedTo != null) createdTo = formatDateForWcf(attrs.CreatedTo);
                            if (attrs.ShippingFrom != null) shippingFrom = formatDateForWcf(attrs.ShippingFrom);
                            if (attrs.ShippingTo != null) shippingTo = formatDateForWcf(attrs.ShippingTo);
                            if (attrs.DeliveryFrom != null) deliveryFrom = formatDateForWcf(attrs.DeliveryFrom);
                            if (attrs.DeliveryTo != null) deliveryTo = formatDateForWcf(attrs.DeliveryTo);

                            const status = attrs.LookupAttribute_tytkx09;
                            if (status && status.displayValue && status.displayValue !== "All") {
                                statusName = status.displayValue;
                            }

                            console.log("[v21] Date filters:", { createdFrom, createdTo, statusName });
                        } catch (e) {
                            console.log("[v21] Error getting date filters:", e);
                        }
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
                            console.log("[v21] Found template:", odataResult.value[0].IntName);
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
                                CustomerId: customerId,
                                CustomerName: customerName,
                                CreatedFrom: createdFrom,
                                CreatedTo: createdTo,
                                ShippingFrom: shippingFrom,
                                ShippingTo: shippingTo,
                                DeliveryFrom: deliveryFrom,
                                DeliveryTo: deliveryTo,
                                StatusName: statusName
                            })
                        });
                        const result = await response.json();
                        console.log("[v21] Service response:", result);

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
                        console.error("[v21] Error:", error);
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
