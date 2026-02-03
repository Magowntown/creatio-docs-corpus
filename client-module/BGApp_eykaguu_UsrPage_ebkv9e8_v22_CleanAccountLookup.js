/**
 * UsrPage_ebkv9e8 - v22 Clean Account Lookup
 * Package: BGApp_eykaguu
 *
 * CHANGES FROM v21:
 * - Customer lookup now uses Account entity directly (standard Creatio pattern)
 * - Added AccountDS data source for customer selection
 * - Removed dependency on UsrEntity_e7ac661.BGCustomer
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
                "values": { "caption": "Generate Report" }
            },

            // ================================================================
            // INSERT: Report selector
            // ================================================================
            {
                "operation": "insert",
                "name": "BGReportSelectorContainer",
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
                "name": "BGReportLookup",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Report",
                    "labelPosition": "auto",
                    "control": "$UsrReport",
                    "listActions": [],
                    "showValueAsLink": false,
                    "controlActions": [],
                    "placeholder": "Select a report...",
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 2, "rowSpan": 1 },
                    "visible": true,
                    "tooltip": "Select the report to generate"
                },
                "parentName": "BGReportSelectorContainer",
                "propertyName": "items",
                "index": 0
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
                "index": 1
            },
            {
                "operation": "insert",
                "name": "BGYearMonthLookup",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Year-Month",
                    "labelPosition": "auto",
                    "control": "$UsrYearMonth",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select year-month...",
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
                "name": "BGSalesGroupLookup",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "auto",
                    "control": "$UsrSalesGroup",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "All sales groups",
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
            // Uses Account entity directly for proper customer lookup
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
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 2, "rowSpan": 1 },
                    "visible": true,
                    "tooltip": "Select a customer from the Account list"
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
                    // Report lookup - uses UsrReportesPampa
                    "UsrReport": {
                        "modelConfig": {
                            "path": "UsrReportesPampaDS.Id"
                        }
                    },
                    "UsrReport_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{"columnName": "Name", "direction": "asc"}]
                            }
                        }
                    },
                    // Commission filters
                    "UsrYearMonth": {
                        "modelConfig": { "path": "BGYearMonthDS.Id" }
                    },
                    "UsrYearMonth_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{"columnName": "BGYearMonth", "direction": "desc"}]
                            }
                        }
                    },
                    "UsrSalesGroup": {
                        "modelConfig": { "path": "BGSalesGroupDS.Id" }
                    },
                    "UsrSalesGroup_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{"columnName": "BGSalesGroupName", "direction": "asc"}]
                            }
                        }
                    },
                    // Customer lookup - uses Account entity directly
                    "UsrCustomer": {
                        "modelConfig": { "path": "AccountDS.Id" }
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

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["dataSources"],
                "values": {
                    // Report lookup data source
                    "UsrReportesPampaDS": {
                        "type": "crt.EntityDataSource",
                        "scope": "viewElement",
                        "config": {
                            "entitySchemaName": "UsrReportesPampa"
                        }
                    },
                    // Year-Month lookup data source
                    "BGYearMonthDS": {
                        "type": "crt.EntityDataSource",
                        "scope": "viewElement",
                        "config": {
                            "entitySchemaName": "BGYearMonth"
                        }
                    },
                    // Sales Group lookup data source
                    "BGSalesGroupDS": {
                        "type": "crt.EntityDataSource",
                        "scope": "viewElement",
                        "config": {
                            "entitySchemaName": "BGSalesGroup"
                        }
                    },
                    // Customer lookup data source - Account entity
                    "AccountDS": {
                        "type": "crt.EntityDataSource",
                        "scope": "viewElement",
                        "config": {
                            "entitySchemaName": "Account"
                        }
                    }
                }
            }
        ]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // ================================================================
            // PAGE INIT
            // ================================================================
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v22] Page init - Clean Account Lookup handler");
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
                        console.log("[v22] Sales Group list load | validIds:",
                            validSalesGroupIds === null ? "null (no filter)" :
                            validSalesGroupIds.length + " groups available");

                        if (validSalesGroupIds !== null && validSalesGroupIds.length > 0) {
                            const comparisonType = Terrasoft.ComparisonType.EQUAL;
                            const filter = Terrasoft.createColumnInFilterWithParameters(
                                "Id", validSalesGroupIds);
                            request.parameters = request.parameters || [];
                            request.parameters.push({
                                type: "filter",
                                value: filter
                            });
                        }
                    }
                    return next?.handle(request);
                }
            },

            // ================================================================
            // REPORT SELECTION CHANGE
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "UsrReport" && !request.silent) {
                        const lookupVal = await request.$context.UsrReport;
                        console.log("[v22] Report selection changed:", lookupVal);

                        // Reset all filters
                        request.$context.UsrShowCommissionFilters = false;
                        request.$context.UsrShowDateStatusFilters = false;
                        request.$context.UsrShowCustomerFilter = false;
                        request.$context.UsrShowLookerIframe = false;

                        if (!lookupVal || !lookupVal.value) {
                            console.log("[v22] No report selected");
                            return next?.handle(request);
                        }

                        if (!isValidGuid(lookupVal.value)) {
                            console.log("[v22] Invalid GUID (user typing)");
                            return next?.handle(request);
                        }

                        // Load report details from UsrReportesPampa
                        try {
                            const model = await sdk.Model.create("UsrReportesPampa");
                            const results = await model.load({
                                attributes: ["Id", "Name", "UsrCode", "UsrURL"],
                                parameters: [{
                                    type: sdk.ModelParameterType.PrimaryColumnValue,
                                    value: lookupVal.value
                                }]
                            });

                            if (results && results.length > 0) {
                                const report = results[0];
                                const reportName = (report.Name || "").toLowerCase();
                                const hasUsrURL = report.UsrURL && report.UsrURL.trim() !== "";

                                console.log("[v22] Report:", report.Name, "| HasURL:", hasUsrURL);

                                // Store for later use
                                request.$context.UsrReportDetails = report;

                                // Determine report type and show appropriate filters
                                const isCommission = reportName.includes("commission");
                                const isItemsByCustomer = reportName.includes("items by customer");
                                const isLooker = hasUsrURL;

                                // Reset filter values
                                request.$context.UsrYearMonth = null;
                                request.$context.UsrSalesGroup = null;
                                request.$context.UsrCustomer = null;

                                if (isCommission) {
                                    // Commission: Show YearMonth + SalesGroup
                                    request.$context.UsrShowCommissionFilters = true;
                                    request.$context.UsrShowDateStatusFilters = false;
                                    request.$context.UsrShowCustomerFilter = false;
                                    cascadeFilterEnabled = true;
                                    validSalesGroupIds = null;
                                    console.log("[v22] COMMISSION report | Filters: YearMonth + SalesGroup");
                                } else if (isItemsByCustomer) {
                                    // Items by Customer: Show Date+Status+Customer
                                    request.$context.UsrShowCommissionFilters = false;
                                    request.$context.UsrShowDateStatusFilters = true;
                                    request.$context.UsrShowCustomerFilter = true;
                                    cascadeFilterEnabled = false;
                                    console.log("[v22] ITEMS BY CUSTOMER report | Filters: Date+Status+Customer");
                                } else if (isLooker) {
                                    // Looker: Show Date+Status, embed iframe
                                    request.$context.UsrShowCommissionFilters = false;
                                    request.$context.UsrShowDateStatusFilters = true;
                                    request.$context.UsrShowCustomerFilter = false;
                                    cascadeFilterEnabled = false;
                                    console.log("[v22] LOOKER report | Filters: Date+Status");
                                } else {
                                    // Other Excel: Show Date+Status
                                    request.$context.UsrShowCommissionFilters = false;
                                    request.$context.UsrShowDateStatusFilters = true;
                                    request.$context.UsrShowCustomerFilter = false;
                                    cascadeFilterEnabled = false;
                                    console.log("[v22] EXCEL report | Filters: Date+Status");
                                }
                            }
                        } catch (e) {
                            console.error("[v22] Error loading report details:", e);
                        }
                    }

                    // CASCADE: YearMonth selection -> filter Sales Groups
                    if (request.attributeName === "UsrYearMonth" && cascadeFilterEnabled) {
                        const yearMonth = await request.$context.UsrYearMonth;
                        console.log("[v22] YearMonth changed:", yearMonth ? yearMonth.displayValue : "null");

                        if (yearMonth && yearMonth.value) {
                            try {
                                const bpmcsrf = getBpmcsrf();
                                const esqUrl = "/0/DataService/json/SyncReply/SelectQuery";
                                const esqBody = {
                                    rootSchemaName: "BGCommissionReportDataView",
                                    operationType: 0,
                                    columns: {
                                        items: {
                                            BGSalesGroup: { expression: { columnPath: "BGSalesGroup" } }
                                        }
                                    },
                                    filters: {
                                        items: {
                                            ymFilter: {
                                                filterType: 1,
                                                comparisonType: 3,
                                                leftExpression: { columnPath: "BGYearMonthId" },
                                                rightExpression: { parameter: { value: yearMonth.value } }
                                            }
                                        }
                                    },
                                    isDistinct: true
                                };

                                const response = await fetch(esqUrl, {
                                    method: "POST",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                                    body: JSON.stringify(esqBody)
                                });
                                const result = await response.json();

                                if (result && result.rows) {
                                    validSalesGroupIds = result.rows
                                        .filter(r => r.BGSalesGroup && r.BGSalesGroup.value)
                                        .map(r => r.BGSalesGroup.value);
                                    console.log("[v22] Found", validSalesGroupIds.length, "sales groups for YearMonth");
                                }
                            } catch (e) {
                                console.error("[v22] Error loading sales groups:", e);
                                validSalesGroupIds = null;
                            }
                        } else {
                            validSalesGroupIds = null;
                        }

                        // Clear and reload sales group list
                        request.$context.UsrSalesGroup = null;
                        try {
                            await request.$context.executeRequest({
                                type: "crt.LoadDataRequest",
                                $context: request.$context,
                                config: { loadType: "reload" },
                                dataSourceName: "BGSalesGroupDS_List"
                            });
                        } catch (e) {}
                    }

                    return next?.handle(request);
                }
            },

            // ================================================================
            // OPEN REPORT HANDLER
            // ================================================================
            {
                request: "OpenReport",
                handler: async (request, next) => {
                    const context = request.$context;
                    const bpmcsrf = getBpmcsrf();

                    // Get report details
                    const reportDetails = context.UsrReportDetails;
                    if (!reportDetails) {
                        Terrasoft.showErrorMessage("Please select a report first");
                        return next?.handle(request);
                    }

                    const reportId = reportDetails.Id;
                    const reportCode = reportDetails.UsrCode || "";
                    const reportDisplayName = reportDetails.Name || "";
                    const usrURL = reportDetails.UsrURL || "";

                    console.log("[v22] Generate:", reportDisplayName, "| Code:", reportCode);

                    // --------------------------------------------------------
                    // LOOKER PATH - Embed in iframe
                    // --------------------------------------------------------
                    if (usrURL && usrURL.trim() !== "") {
                        console.log("[v22] Looker report - embedding iframe");

                        const params = buildLookerParams(context);
                        const fullUrl = usrURL + params;
                        console.log("[v22] Looker URL:", fullUrl);

                        // Show the iframe container and set source
                        context.UsrShowLookerIframe = true;

                        // Set iframe src via custom element or DOM
                        setTimeout(() => {
                            const iframeContainer = document.querySelector('[data-name="UsrIframe"]');
                            if (iframeContainer) {
                                let iframe = iframeContainer.querySelector('iframe');
                                if (!iframe) {
                                    iframe = document.createElement('iframe');
                                    iframe.style.width = '100%';
                                    iframe.style.height = '800px';
                                    iframe.style.border = 'none';
                                    iframeContainer.appendChild(iframe);
                                }
                                iframe.src = fullUrl;
                                console.log("[v22] Iframe src set successfully");
                            }
                        }, 100);

                        Terrasoft.showInformation("Loading report...");
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // EXCEL PATH
                    // --------------------------------------------------------
                    console.log("[v22] Generating Excel:", reportDisplayName);

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
                                console.log("[v22] Commission YearMonth:", yearMonth.displayValue);
                            }
                        } catch (e) {}
                        try {
                            const salesGroup = await context.UsrSalesGroup;
                            if (salesGroup && salesGroup.value) {
                                salesGroupId = salesGroup.value;
                                console.log("[v22] Commission SalesGroup:", salesGroup.displayValue);
                            }
                        } catch (e) {}
                    }

                    // Get Customer filter value for "Items by Customer"
                    // UsrCustomer is now bound to Account entity
                    if (reportDisplayName.toLowerCase().includes("items by customer")) {
                        try {
                            const customer = await context.UsrCustomer;
                            if (customer && customer.value) {
                                customerId = customer.value;
                                // displayValue will be Account.Name
                                customerName = customer.displayValue || "";
                                console.log("[v22] Customer filter (from Account):", customerName);
                            } else {
                                console.log("[v22] WARNING: No customer selected for Items by Customer report");
                                Terrasoft.showWarningMessage("Please select a customer");
                                return next?.handle(request);
                            }
                        } catch (e) {
                            console.error("[v22] Error getting customer:", e);
                        }
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

                            console.log("[v22] Date filters:", { createdFrom, createdTo, statusName });
                        } catch (e) {
                            console.log("[v22] Error getting date filters:", e);
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
                            console.log("[v22] Found template:", odataResult.value[0].IntName);
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
                        console.log("[v22] Service response:", result);

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
                        console.error("[v22] Error:", error);
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
