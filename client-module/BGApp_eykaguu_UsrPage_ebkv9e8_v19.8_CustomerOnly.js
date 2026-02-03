/**
 * UsrPage_ebkv9e8 - v19.8 Customer Only
 * Package: BGApp_eykaguu
 *
 * BASED ON v19.1 (working PROD) + Customer filter ONLY
 *
 * v19.8 CHANGES:
 * - ADD: Customer dropdown filter for "Items by Customer" report
 * - KEEP: All v19.1 functionality intact (YearMonth, SalesGroup, Looker, Excel)
 * - REMOVED: Cascade filter logic (was breaking Sales Group in v19.7)
 *
 * WHY NO CASCADE FILTER:
 * The LoadDataRequest interceptor in v19.7 blocked ALL Sales Group data
 * when validSalesGroupIds was empty array. This caused "no data" in dropdown.
 * Better to show all Sales Groups than show none.
 *
 * VISIBILITY RULES (unchanged from v19.1):
 * | Report Type          | Commission Filters | Date+Status Filters | Action         |
 * |----------------------|-------------------|---------------------|----------------|
 * | None selected        | Hidden            | Hidden              | -              |
 * | Commission           | VISIBLE           | Hidden              | Excel          |
 * | Non-Commission Excel | Hidden            | VISIBLE             | Excel          |
 * | Looker Studio        | Hidden            | VISIBLE             | New Tab+Params |
 *
 * CUSTOMER FILTER:
 * - Bound to UsrEntity_e7ac661DS.BGCustomer (confirmed column name via OData $metadata)
 * - Shows in separate container after commission filters
 * - Used for "Items by Customer" report
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
        // If it's a Date object or ISO string
        var d = new Date(dateValue);
        if (isNaN(d.getTime())) return null;
        var year = d.getFullYear();
        var month = String(d.getMonth() + 1).padStart(2, '0');
        var day = String(d.getDate()).padStart(2, '0');
        return year + '-' + month + '-' + day;
    }

    // Build Looker Studio URL params (matches original parent schema logic)
    // NOTE: Uses context.attributes.X pattern to match parent schema's access pattern
    function buildLookerParams(context) {
        var param = '?params=%7B"ds0.additionalFilters":';
        var addedFirstFilter = false;
        var filters = [];
        var attrs = context.attributes || {};

        // Created date range
        if (attrs.CreatedFrom) {
            var createdfrom = formatDateForLooker(attrs.CreatedFrom);
            if (createdfrom) {
                filters.push('CreatedOn ge datetime' + "'" + createdfrom + "'");
            }
        }
        if (attrs.CreatedTo) {
            var createdto = formatDateForLooker(attrs.CreatedTo);
            if (createdto) {
                filters.push('CreatedOn le datetime' + "'" + createdto + "'");
            }
        }

        // Shipping date range
        if (attrs.ShippingFrom) {
            var shippingfrom = formatDateForLooker(attrs.ShippingFrom);
            if (shippingfrom) {
                filters.push('BGShipDate ge datetime' + "'" + shippingfrom + "'");
            }
        }
        if (attrs.ShippingTo) {
            var shippingto = formatDateForLooker(attrs.ShippingTo);
            if (shippingto) {
                filters.push('BGShipDate le datetime' + "'" + shippingto + "'");
            }
        }

        // Delivery date range
        if (attrs.DeliveryFrom) {
            var deliveryfrom = formatDateForLooker(attrs.DeliveryFrom);
            if (deliveryfrom) {
                filters.push('BGDeliveryDate ge datetime' + "'" + deliveryfrom + "'");
            }
        }
        if (attrs.DeliveryTo) {
            var deliveryto = formatDateForLooker(attrs.DeliveryTo);
            if (deliveryto) {
                filters.push('BGDeliveryDate le datetime' + "'" + deliveryto + "'");
            }
        }

        // Status filter - use attrs pattern to match parent schema
        var status = attrs.LookupAttribute_tytkx09;
        if (status && status.displayValue && status.displayValue !== "All") {
            filters.push("contains(BGStatus, '" + status.displayValue + "')");
        }

        // Theme filter (if UI element exists in PROD)
        var theme = attrs.LookupAttribute_4ufq0og;
        if (theme && theme.displayValue) {
            filters.push("contains(BGTheme, '" + theme.displayValue + "')");
        }

        // Sales Rep filter (if UI element exists in PROD)
        var salesRep = attrs.LookupAttribute_houdnx9;
        if (salesRep && salesRep.displayValue) {
            filters.push("contains(BGSalesRep, '" + salesRep.displayValue + "')");
        }

        // Customer Type filter (if UI element exists in PROD)
        var customerType = attrs.LookupAttribute_c4ubvuy;
        if (customerType && customerType.displayValue) {
            filters.push("contains(BGCustomerType, '" + customerType.displayValue + "')");
        }

        // Build the filter string
        if (filters.length > 0) {
            param = param + '"' + filters.join(' and ') + '","ds0.top":"1000000"%7D';
        } else {
            param = param + '"","ds0.top":"1000000"%7D';
        }

        return param;
    }

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
                    "gap": {
                        "columnGap": "large",
                        "rowGap": "none"
                    },
                    "items": [],
                    "fitContent": true,
                    "visible": true,
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": {
                        "top": "none",
                        "right": "none",
                        "bottom": "none",
                        "left": "none"
                    }
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
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
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
                    "gap": {
                        "columnGap": "large",
                        "rowGap": "none"
                    },
                    "items": [],
                    "fitContent": true,
                    "visible": "$UsrShowCommissionFilters",
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": {
                        "top": "none",
                        "right": "none",
                        "bottom": "none",
                        "left": "none"
                    }
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
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": "Required for Commission reports"
                },
                "parentName": "BGCommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },

            // ================================================================
            // INSERT: Sales Group filter
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
                    "layoutConfig": {
                        "column": 2,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": "Optional filter",
                    "mode": "List"
                },
                "parentName": "BGCommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // INSERT: Customer filter container (v19.8 NEW)
            // For "Items by Customer" report
            // ================================================================
            {
                "operation": "insert",
                "name": "BGCustomerFilterContainer",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)", "minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": {
                        "columnGap": "large",
                        "rowGap": "none"
                    },
                    "items": [],
                    "fitContent": true,
                    "visible": "$UsrShowCustomerFilter",
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": {
                        "top": "none",
                        "right": "none",
                        "bottom": "none",
                        "left": "none"
                    }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 3
            },

            // ================================================================
            // INSERT: Customer dropdown (v19.8 NEW)
            // ================================================================
            {
                "operation": "insert",
                "name": "BGCustomer",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Customer",
                    "labelPosition": "auto",
                    "control": "$UsrCustomer",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select customer...",
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": "Filter by customer"
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
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGYearMonth"
                        }
                    },
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
                    "UsrCustomer": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGCustomer"
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
                    console.log("[v19.8] Page init - visibility controlled by attribute binding");
                    console.log("[v19.8] UsrShowCommissionFilters:", request.$context.UsrShowCommissionFilters);
                    console.log("[v19.8] UsrShowDateStatusFilters:", request.$context.UsrShowDateStatusFilters);
                    console.log("[v19.8] UsrShowCustomerFilter:", request.$context.UsrShowCustomerFilter);
                    return;
                }
            },

            // ================================================================
            // REPORT SELECTION - Update visibility attributes based on report type
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_0as4io2;

                        // Guard: Ensure selectedReport has both displayValue AND value
                        if (selectedReport && selectedReport.displayValue && selectedReport.value) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission");
                            const isItemsByCustomer = reportName.includes("items by customer");

                            // Check if report has Looker URL
                            let reportUrl = "";
                            try {
                                const bpmcsrf = getBpmcsrf();
                                const metaUrl = "/0/odata/UsrReportesPampa(" + selectedReport.value + ")?$select=UsrURL";
                                const resp = await fetch(metaUrl, {
                                    method: "GET",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                });
                                if (resp.ok) {
                                    const meta = await resp.json();
                                    // Guard: Check meta exists and has UsrURL property
                                    if (meta && typeof meta.UsrURL !== 'undefined') {
                                        reportUrl = meta.UsrURL || "";
                                    }
                                }
                            } catch (e) {
                                console.log("[v19.8] Error checking report URL:", e);
                            }

                            const isLookerReport = reportUrl && reportUrl.length > 0;

                            // Clear filter values when switching reports
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;
                            request.$context.UsrCustomer = null;

                            // Apply visibility rules via attribute binding
                            if (isCommissionReport) {
                                // COMMISSION: Show commission filters, hide date+status and customer
                                request.$context.UsrShowCommissionFilters = true;
                                request.$context.UsrShowDateStatusFilters = false;
                                request.$context.UsrShowCustomerFilter = false;
                                console.log("[v19.8] Report:", selectedReport.displayValue, "| Type: COMMISSION | Showing commission filters");

                            } else if (isItemsByCustomer) {
                                // ITEMS BY CUSTOMER: Show customer filter + date+status filters
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = true;
                                console.log("[v19.8] Report:", selectedReport.displayValue, "| Type: ITEMS BY CUSTOMER | Showing customer + date filters");

                            } else if (isLookerReport) {
                                // LOOKER STUDIO: Show date+status filters (v19 FIX!)
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                console.log("[v19.8] Report:", selectedReport.displayValue, "| Type: LOOKER | Showing date+status filters");

                            } else {
                                // NON-COMMISSION EXCEL: Show date+status, hide commission filters
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                                console.log("[v19.8] Report:", selectedReport.displayValue, "| Type: EXCEL | Showing date+status filters");
                            }
                        } else {
                            // NO REPORT SELECTED: Hide everything
                            request.$context.UsrShowCommissionFilters = false;
                            request.$context.UsrShowDateStatusFilters = false;
                            request.$context.UsrShowCustomerFilter = false;
                            console.log("[v19.8] No report selected | All filters hidden");
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
                            // Guard: Check reportMeta exists before accessing properties
                            if (reportMeta) {
                                reportDisplayName = reportMeta.Name || reportDisplayName;
                                reportUrl = (typeof reportMeta.UsrURL !== 'undefined') ? (reportMeta.UsrURL || "") : "";
                                reportCode = (typeof reportMeta.UsrCode !== 'undefined') ? (reportMeta.UsrCode || "") : "";
                            }
                        }
                    } catch (e) {
                        console.log("[v19.8] Metadata lookup failed:", e);
                    }

                    // LOOKER STUDIO - Open in new tab WITH URL PARAMS (v19 FIX!)
                    if (reportUrl && reportUrl.length > 0) {
                        // Build URL params from date/status filters
                        var params = buildLookerParams(context);
                        var fullUrl = reportUrl + params;
                        console.log("[v19.8] Opening Looker Studio with params:", fullUrl);
                        window.open(fullUrl, "_blank");
                        Terrasoft.showInformation("Report opened in new tab");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[v19.8] Generating Excel report:", reportDisplayName);

                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;
                    var customerId = emptyGuid;

                    // Get Commission filter values if applicable
                    if (reportDisplayName.toLowerCase().includes("commission")) {
                        try {
                            const yearMonth = await context.UsrYearMonth;
                            if (yearMonth && yearMonth.value) {
                                yearMonthId = yearMonth.value;
                            }
                        } catch (e) {}
                        try {
                            const salesGroup = await context.UsrSalesGroup;
                            if (salesGroup && salesGroup.value) {
                                salesGroupId = salesGroup.value;
                            }
                        } catch (e) {}
                    }

                    // Get Customer filter value if applicable (v19.8 NEW)
                    if (reportDisplayName.toLowerCase().includes("items by customer")) {
                        try {
                            const customer = await context.UsrCustomer;
                            if (customer && customer.value) {
                                customerId = customer.value;
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
                            console.log("[v19.8] Found template:", odataResult.value[0].IntName);
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
                        console.log("[v19.8] Excel service response:", result);

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
                        console.error("[v19.8] Error:", error);
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
