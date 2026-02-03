/**
 * UsrPage_ebkv9e8 - v20 Embedded Looker
 * Package: BGApp_eykaguu
 *
 * CHANGES FROM v19:
 * - FIX: Looker reports now EMBED in iframe (was opening new tab)
 * - Uses shadow DOM to access UsrIframe component
 * - Shows/hides iframe container based on report type
 *
 * VISIBILITY RULES:
 * | Report Type          | Commission Filters | Date+Status Filters | Iframe  | Action         |
 * |----------------------|-------------------|---------------------|---------|----------------|
 * | None selected        | Hidden            | Hidden              | Hidden  | -              |
 * | Commission           | VISIBLE           | Hidden              | Hidden  | Excel          |
 * | Non-Commission Excel | Hidden            | VISIBLE             | Hidden  | Excel          |
 * | Looker Studio        | Hidden            | VISIBLE             | VISIBLE | Embed in iframe|
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

        // Status filter
        var status = attrs.LookupAttribute_tytkx09;
        if (status && status.displayValue && status.displayValue !== "All") {
            filters.push("contains(BGStatus, '" + status.displayValue + "')");
        }

        // Theme filter
        var theme = attrs.LookupAttribute_4ufq0og;
        if (theme && theme.displayValue) {
            filters.push("contains(BGTheme, '" + theme.displayValue + "')");
        }

        // Sales Rep filter
        var salesRep = attrs.LookupAttribute_houdnx9;
        if (salesRep && salesRep.displayValue) {
            filters.push("contains(BGSalesRep, '" + salesRep.displayValue + "')");
        }

        // Customer Type filter
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

    // Set iframe src via shadow DOM
    function setIframeSrc(url) {
        var usrIframe = document.getElementById('UsrIframe');
        if (usrIframe && usrIframe.shadowRoot) {
            var iframe = usrIframe.shadowRoot.querySelector('iframe');
            if (iframe) {
                iframe.src = url;
                console.log('[v20] Iframe src set to:', url);
                return true;
            }
        }
        console.log('[v20] Could not access iframe shadow root');
        return false;
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
            // IFRAME CONTAINER - Bind visibility to attribute (show for Looker)
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": "$UsrShowLookerIframe"
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
                    "UsrShowLookerIframe": {
                        "value": false
                    },
                    "UsrCurrentReportUrl": {
                        "value": ""
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
                    console.log("[v20] Page init - Embedded Looker handler");
                    // Hide iframe initially
                    request.$context.UsrShowLookerIframe = false;
                    return;
                }
            },

            // ================================================================
            // REPORT SELECTION - Update visibility and store URL
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    // Only handle report lookup changes, not other attributes
                    if (request.attributeName !== "LookupAttribute_0as4io2" || request.silent) {
                        return next?.handle(request);
                    }

                    let selectedReport = null;
                    try {
                        selectedReport = await request.$context.LookupAttribute_0as4io2;
                    } catch (e) {
                        // Lookup not ready yet (user still typing)
                        return next?.handle(request);
                    }

                    // Guard: Must have a valid GUID (not partial text from typing)
                    if (!selectedReport || !selectedReport.value ||
                        typeof selectedReport.value !== 'string' ||
                        !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(selectedReport.value)) {
                        // User is still typing or cleared selection
                        return next?.handle(request);
                    }

                    if (selectedReport.displayValue) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission");

                            // Check if report has Looker URL
                            let reportUrl = "";
                            try {
                                const bpmcsrf = getBpmcsrf();
                                const metaUrl = "/0/odata/UsrReportesPampa(" + selectedReport.value + ")?$select=UsrURL";
                                console.log("[v20] Fetching metadata from:", metaUrl);
                                const resp = await fetch(metaUrl, {
                                    method: "GET",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                });
                                console.log("[v20] Metadata response status:", resp.status);
                                if (resp.ok) {
                                    const responseText = await resp.text();
                                    console.log("[v20] Raw response:", responseText);
                                    try {
                                        const meta = JSON.parse(responseText);
                                        console.log("[v20] Parsed meta:", meta);
                                        // Defensive: handle various response structures
                                        if (meta) {
                                            if (typeof meta.UsrURL === 'string') {
                                                reportUrl = meta.UsrURL;
                                            } else if (meta.value && typeof meta.value.UsrURL === 'string') {
                                                reportUrl = meta.value.UsrURL;
                                            }
                                        }
                                    } catch (parseErr) {
                                        console.log("[v20] JSON parse error:", parseErr);
                                    }
                                }
                            } catch (e) {
                                console.log("[v20] Error checking report URL:", e);
                                reportUrl = ""; // Default to empty on error
                            }

                            const isLookerReport = reportUrl && reportUrl.length > 0;

                            // Store URL for later use
                            request.$context.UsrCurrentReportUrl = reportUrl;

                            // Clear filter values when switching reports
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;

                            // Apply visibility rules
                            if (isCommissionReport) {
                                request.$context.UsrShowCommissionFilters = true;
                                request.$context.UsrShowDateStatusFilters = false;
                                request.$context.UsrShowLookerIframe = false;
                                console.log("[v20] Report:", selectedReport.displayValue, "| Type: COMMISSION | URL:", reportUrl);

                            } else if (isLookerReport) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowLookerIframe = false; // Show after Generate click
                                console.log("[v20] Report:", selectedReport.displayValue, "| Type: LOOKER | URL:", reportUrl);

                            } else {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateStatusFilters = true;
                                request.$context.UsrShowLookerIframe = false;
                                console.log("[v20] Report:", selectedReport.displayValue, "| Type: EXCEL (no URL)");
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
                        console.log("[v20] Generate - fetching metadata:", reportMetaUrl);
                        const reportMetaResp = await fetch(reportMetaUrl, {
                            method: "GET",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (reportMetaResp.ok) {
                            const responseText = await reportMetaResp.text();
                            console.log("[v20] Generate - raw response:", responseText);
                            try {
                                const reportMeta = JSON.parse(responseText);
                                console.log("[v20] Generate - parsed meta:", reportMeta);
                                if (reportMeta) {
                                    reportDisplayName = reportMeta.Name || reportDisplayName;
                                    reportUrl = (reportMeta.UsrURL && typeof reportMeta.UsrURL === 'string') ? reportMeta.UsrURL : "";
                                    reportCode = (reportMeta.UsrCode && typeof reportMeta.UsrCode === 'string') ? reportMeta.UsrCode : "";
                                }
                            } catch (parseErr) {
                                console.log("[v20] Generate - JSON parse error:", parseErr);
                            }
                        }
                    } catch (e) {
                        console.log("[v20] Metadata lookup failed:", e);
                    }

                    // ================================================================
                    // LOOKER STUDIO - Embed in iframe
                    // ================================================================
                    if (reportUrl && reportUrl.length > 0) {
                        var params = buildLookerParams(context);
                        var fullUrl = reportUrl + params;
                        console.log("[v20] LOOKER DETECTED - URL:", fullUrl);

                        // Show iframe container
                        console.log("[v20] Setting UsrShowLookerIframe = true");
                        context.UsrShowLookerIframe = true;

                        // Use setTimeout to ensure DOM is updated before accessing shadow root
                        setTimeout(() => {
                            console.log("[v20] setTimeout fired - attempting to set iframe src");
                            var usrIframe = document.getElementById('UsrIframe');
                            console.log("[v20] UsrIframe element:", usrIframe);
                            if (usrIframe) {
                                console.log("[v20] UsrIframe.shadowRoot:", usrIframe.shadowRoot);
                                if (usrIframe.shadowRoot) {
                                    var iframe = usrIframe.shadowRoot.querySelector('iframe');
                                    console.log("[v20] iframe element:", iframe);
                                    if (iframe) {
                                        iframe.src = fullUrl;
                                        console.log("[v20] SUCCESS - iframe.src set to:", fullUrl);
                                    } else {
                                        console.log("[v20] ERROR - No iframe in shadow root");
                                    }
                                } else {
                                    console.log("[v20] ERROR - No shadow root on UsrIframe");
                                }
                            } else {
                                console.log("[v20] ERROR - UsrIframe element not found");
                            }
                        }, 500);

                        Terrasoft.showInformation("Loading report...");
                        return next?.handle(request);
                    }

                    // ================================================================
                    // EXCEL PATH
                    // ================================================================
                    console.log("[v20] Generating Excel report:", reportDisplayName);

                    // Hide iframe for Excel reports
                    context.UsrShowLookerIframe = false;

                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;

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
                            console.log("[v20] Found template:", odataResult.value[0].IntName);
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
                                SalesRepId: salesGroupId
                            })
                        });
                        const result = await response.json();
                        console.log("[v20] Excel service response:", result);

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
                        console.error("[v20] Error:", error);
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
