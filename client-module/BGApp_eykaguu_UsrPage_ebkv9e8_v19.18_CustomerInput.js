/**
 * UsrPage_ebkv9e8 - v19.18 Customer Text Input Fix
 * Package: BGApp_eykaguu
 *
 * CHANGES FROM v19.17:
 * - Uses crt.Input for Customer instead of ComboBox (no entity binding needed)
 * - User types customer name directly (exact or partial)
 * - Backend uses CONTAINS filter instead of exact match
 * - Added "Search Customers" button to show available customers
 *
 * WHY THIS WORKS:
 * - BGSalesByItemView.BGCustomer is a VARCHAR column (not a lookup)
 * - Contains customer names like "Bay Country Shop", "Baytree Gift Company"
 * - User can type full or partial name, backend finds matches
 *
 * INCLUDES ALL v19.16 FEATURES:
 * - Date filters with sync attribute access
 * - Commission cascade filters (YearMonth -> SalesGroup)
 * - Looker Studio integration
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
                    "tooltip": "Filtered by Year-Month when data exists",
                    "mode": "List"
                },
                "parentName": "BGCommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // INSERT: Customer filter container (for "Items by Customer")
            // Uses text input instead of ComboBox - simpler and more flexible
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
                "name": "BGCustomerInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Customer Name",
                    "labelPosition": "auto",
                    "control": "$UsrCustomerName",
                    "placeholder": "Type customer name (e.g., Bay Country Shop)...",
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "visible": true,
                    "tooltip": "Type full or partial customer name. Use 'Show Customers' to see available names."
                },
                "parentName": "BGCustomerFilterContainer",
                "propertyName": "items",
                "index": 0
            },
            {
                "operation": "insert",
                "name": "BGShowCustomersBtn",
                "values": {
                    "type": "crt.Button",
                    "caption": "Show Customers",
                    "color": "outline",
                    "size": "medium",
                    "layoutConfig": { "column": 2, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "visible": true,
                    "clicked": { "request": "usr.ShowCustomersRequest" }
                },
                "parentName": "BGCustomerFilterContainer",
                "propertyName": "items",
                "index": 1
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
                    // Customer Name - simple text input (not a lookup)
                    "UsrCustomerName": {
                        "value": ""
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
                    console.log("[v19.18] Page init - Customer text input mode");
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
                    const isSalesGroupList = dsName.includes("SalesGroup") && dsName.includes("_List");

                    if (cascadeFilterEnabled && isSalesGroupList) {
                        console.log("[v19.18] Sales Group list load | validIds:",
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
                            console.log("[v19.18] Applied cascade filter for", validSalesGroupIds.length, "groups");
                        } else {
                            console.log("[v19.18] No cascade filter - showing all groups");
                        }
                    }

                    return next?.handle(request);
                }
            },

            // ================================================================
            // REPORT SELECTION
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    const bpmcsrf = getBpmcsrf();

                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_0as4io2;

                        if (selectedReport && selectedReport.displayValue && selectedReport.value) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission");
                            const isItemsByCustomer = reportName.includes("items by customer");

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
                                console.log("[v19.18] Error checking report URL:", e);
                            }

                            const isLookerReport = reportUrl && reportUrl.length > 0;

                            // Clear filters
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;
                            request.$context.UsrCustomerName = "";
                            validSalesGroupIds = null;

                            if (isCommissionReport) {
                                request.$context.UsrShowCommissionFilters = true;
                                request.$context.UsrShowDateStatusFilters = false;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = true;
                                console.log("[v19.18] COMMISSION report | Cascade: ENABLED");

                            } else if (isItemsByCustomer) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = true;
                                cascadeFilterEnabled = false;
                                console.log("[v19.18] ITEMS BY CUSTOMER report | Customer text input enabled");

                            } else if (isLookerReport) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = false;
                                console.log("[v19.18] LOOKER report | Date+Status filters");

                            } else {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                cascadeFilterEnabled = false;
                                console.log("[v19.18] OTHER EXCEL report | Date+Status filters");
                            }
                        } else {
                            request.$context.UsrShowCommissionFilters = false;
                            request.$context.UsrShowDateStatusFilters = false;
                            request.$context.UsrShowCustomerFilter = false;
                            cascadeFilterEnabled = false;
                            validSalesGroupIds = null;
                            console.log("[v19.18] No report selected");
                        }
                    }

                    // YearMonth cascade
                    if (request.attributeName === "UsrYearMonth" && !request.silent && cascadeFilterEnabled) {
                        const yearMonth = await request.$context.UsrYearMonth;

                        if (yearMonth && yearMonth.value) {
                            console.log("[v19.18] YearMonth changed to:", yearMonth.displayValue);
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
                                    console.log("[v19.18] Found", validSalesGroupIds.length, "groups for", yearMonth.displayValue);
                                } else {
                                    validSalesGroupIds = null;
                                }
                            } catch (e) {
                                validSalesGroupIds = null;
                            }

                            // Reload Sales Group dropdown
                            try {
                                await sdk.HandlerChainService.instance.process({
                                    type: "crt.LoadDataRequest",
                                    $context: request.$context,
                                    config: { loadType: "reload", useLastLoadParameters: false },
                                    dataSourceName: "UsrSalesGroup_List_DS",
                                    scopes: [...(request.scopes || [])]
                                });
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
            // SHOW CUSTOMERS - Display available customer names
            // ================================================================
            {
                request: "usr.ShowCustomersRequest",
                handler: async (request, next) => {
                    const bpmcsrf = getBpmcsrf();
                    console.log("[v19.18] Loading customer list from BGSalesByItemView...");

                    try {
                        // Query distinct customers from the view
                        const custUrl = "/0/odata/BGSalesByItemView?$apply=groupby((BGCustomer))&$orderby=BGCustomer&$top=100";
                        const resp = await fetch(custUrl, {
                            method: "GET",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });

                        if (resp.ok) {
                            const data = await resp.json();
                            const customers = (data.value || [])
                                .map(row => row.BGCustomer)
                                .filter(name => name && name.trim() !== "")
                                .sort();

                            if (customers.length > 0) {
                                // Show first 20 in an alert (user-friendly)
                                const display = customers.slice(0, 20).join("\n");
                                const more = customers.length > 20 ? "\n\n... and " + (customers.length - 20) + " more" : "";
                                alert("Available Customers:\n\n" + display + more + "\n\nType any of these names (or part of it) in the Customer field.");
                            } else {
                                alert("No customers found in the data view.");
                            }
                        } else {
                            alert("Failed to load customer list. Status: " + resp.status);
                        }
                    } catch (e) {
                        console.log("[v19.18] Error loading customers:", e);
                        alert("Error loading customer list: " + e.message);
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
                    } catch (e) {}

                    // LOOKER PATH
                    if (reportUrl && reportUrl.length > 0) {
                        var params = buildLookerParams(context);
                        var fullUrl = reportUrl + params;
                        console.log("[v19.18] Opening Looker:", reportDisplayName);
                        window.open(fullUrl, "_blank");
                        Terrasoft.showInformation("Report opened in new tab");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[v19.18] Generating Excel:", reportDisplayName);

                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;
                    var customerName = "";

                    // Commission filters
                    if (reportDisplayName.toLowerCase().includes("commission")) {
                        try {
                            const yearMonth = await context.UsrYearMonth;
                            if (yearMonth && yearMonth.value) {
                                yearMonthId = yearMonth.value;
                                console.log("[v19.18] Commission YearMonth:", yearMonth.displayValue);
                            }
                        } catch (e) {}
                        try {
                            const salesGroup = await context.UsrSalesGroup;
                            if (salesGroup && salesGroup.value) {
                                salesGroupId = salesGroup.value;
                                console.log("[v19.18] Commission SalesGroup:", salesGroup.displayValue);
                            }
                        } catch (e) {}
                    }

                    // Customer filter for "Items by Customer"
                    if (reportDisplayName.toLowerCase().includes("items by customer")) {
                        try {
                            const custName = await context.UsrCustomerName;
                            if (custName && typeof custName === 'string' && custName.trim() !== "") {
                                customerName = custName.trim();
                                console.log("[v19.18] Customer filter:", customerName);
                            }
                        } catch (e) {}
                    }

                    // Date and Status filters
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

                            console.log("[v19.18] Date attributes:", {
                                CreatedFrom: attrs.CreatedFrom,
                                CreatedTo: attrs.CreatedTo
                            });

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
                        } catch (e) {}
                    }

                    // Find template
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
                            console.log("[v19.18] Found template:", odataResult.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    // Generate
                    try {
                        Terrasoft.showInformation("Generating Excel report...");
                        const response = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify({
                                ReportId: intExcelReportId,
                                YearMonthId: yearMonthId,
                                SalesRepId: salesGroupId,
                                CustomerId: emptyGuid,
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
                        console.log("[v19.18] Service response:", result);

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
                        console.error("[v19.18] Error:", error);
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
