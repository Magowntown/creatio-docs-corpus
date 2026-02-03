/**
 * UsrPage_ebkv9e8 - v24 PARENT-DRIVEN (Minimal)
 * Package: BGApp_eykaguu
 *
 * APPROACH:
 * - DO NOT hide parent dropdown container (GridContainer_oshnwh8)
 * - DO NOT insert our own dropdown - use parent's LookupAttribute_bsixu8a
 * - Let parent business rules control date/status filter visibility
 * - INSERT Commission filters (YearMonth, SalesGroup) - parent doesn't have these
 * - INSERT Looker iframe for embedding
 *
 * PARENT ATTRIBUTES (BGPage_iaptpa6):
 * - Report: LookupAttribute_bsixu8a
 * - Dates: CreatedFrom, CreatedTo, ShippingFrom, ShippingTo, DeliveryFrom, DeliveryTo, BGFrom, BGTo, BGDate
 * - Status: LookupAttribute_tytkx09
 * - Customer type: LookupAttribute_bjjaqun
 * - Sales rep: LookupAttribute_z2lixqt
 * - Theme: LookupAttribute_pacf0nb
 *
 * OUR ATTRIBUTES (inserted by this handler):
 * - UsrYearMonth: For Commission reports
 * - UsrSalesGroup: For Commission reports
 * - UsrCustomerName: For "Items by Customer" report (text input, CONTAINS match)
 * - UsrShowCommissionFilters: Visibility control
 * - UsrShowCustomerNameFilter: Visibility control
 * - UsrShowLookerIframe: Visibility control
 *
 * Looker: Embedded in crt.IFrame component
 * Excel: UsrExcelReportService/Generate + GetReport
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

    /**
     * Converts JavaScript Date to WCF JSON format: /Date(milliseconds)/
     */
    function toWcfDate(date) {
        if (!date) return null;
        if (date instanceof Date) {
            return "/Date(" + date.getTime() + ")/";
        }
        if (typeof date === "string") {
            var parsed = new Date(date);
            if (!isNaN(parsed.getTime())) {
                return "/Date(" + parsed.getTime() + ")/";
            }
        }
        return null;
    }

    /**
     * Sets Looker iframe src via crt.IFrame component or shadowRoot
     */
    function setLookerIframeSrc(url) {
        setTimeout(() => {
            try {
                // Try 1: Our inserted UsrLookerIframe component
                var usrLookerIframe = document.getElementById("UsrLookerIframe");
                if (usrLookerIframe) {
                    if (usrLookerIframe.shadowRoot) {
                        var iframe = usrLookerIframe.shadowRoot.querySelector("iframe");
                        if (iframe) {
                            iframe.src = url;
                            console.log("[v24] Iframe src set via UsrLookerIframe shadowRoot:", url);
                            return;
                        }
                    }
                    // If no shadowRoot, try setting src attribute directly
                    if (typeof usrLookerIframe.src !== "undefined") {
                        usrLookerIframe.src = url;
                        console.log("[v24] Iframe src set directly on UsrLookerIframe:", url);
                        return;
                    }
                }

                // Try 2: Original UsrIframe from BGlobalLookerStudio package
                var usrIframe = document.getElementById("UsrIframe");
                if (usrIframe && usrIframe.shadowRoot) {
                    var iframe = usrIframe.shadowRoot.querySelector("iframe");
                    if (iframe) {
                        iframe.src = url;
                        console.log("[v24] Iframe src set via UsrIframe shadowRoot:", url);
                        return;
                    }
                }

                // Try 3: Find iframe by data-item-marker
                var markedElement = document.querySelector("[data-item-marker='UsrLookerIframe']");
                if (markedElement) {
                    var iframe = markedElement.querySelector("iframe") || markedElement;
                    if (iframe.tagName === "IFRAME" || iframe.shadowRoot) {
                        var actualIframe = iframe.shadowRoot ? iframe.shadowRoot.querySelector("iframe") : iframe;
                        if (actualIframe) {
                            actualIframe.src = url;
                            console.log("[v24] Iframe src set via data-item-marker:", url);
                            return;
                        }
                    }
                }

                // Try 4: Find any iframe in GridContainer_fh039aq
                var container = document.querySelector("[data-item-marker='GridContainer_fh039aq']");
                if (container) {
                    var iframeEl = container.querySelector("iframe");
                    if (iframeEl) {
                        iframeEl.src = url;
                        console.log("[v24] Iframe src set via GridContainer_fh039aq:", url);
                        return;
                    }
                }

                console.log("[v24] WARNING: Could not find iframe element to set src");
            } catch (e) {
                console.log("[v24] Error setting iframe src:", e);
            }
        }, 500);
    }

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // ================================================================
            // WIRE GENERATE BUTTON TO OUR HANDLER
            // ================================================================
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "clicked": { "request": "usr.GenerateReportRequest" }
                }
            },

            // ================================================================
            // INSERT: Commission Filters Container (Parent doesn't have YearMonth/SalesGroup)
            // ================================================================
            {
                "operation": "insert",
                "name": "CommissionFiltersContainer",
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

            // ================================================================
            // INSERT: Year-Month filter (Commission only)
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrYearMonthFilter",
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
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },

            // ================================================================
            // INSERT: Sales Group filter (Commission only)
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrSalesGroupFilter",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "auto",
                    "control": "$UsrSalesGroup",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select group (optional)...",
                    "layoutConfig": { "column": 2, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "visible": true,
                    "tooltip": "Optional filter"
                },
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // INSERT: Customer Name Container (Items by Customer only)
            // ================================================================
            {
                "operation": "insert",
                "name": "CustomerNameContainer",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)", "minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": { "columnGap": "large", "rowGap": "none" },
                    "items": [],
                    "fitContent": true,
                    "visible": "$UsrShowCustomerNameFilter",
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": { "top": "none", "right": "none", "bottom": "none", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 2
            },

            // ================================================================
            // INSERT: Customer Name text input (Items by Customer)
            // Backend filters BGSalesByItemView.BGCustomer (varchar) with CONTAINS
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrCustomerNameInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Customer Name",
                    "labelPosition": "auto",
                    "control": "$UsrCustomerName",
                    "placeholder": "Enter customer name (partial match)...",
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 2, "rowSpan": 1 },
                    "visible": true,
                    "tooltip": "Filters by customer name using CONTAINS match"
                },
                "parentName": "CustomerNameContainer",
                "propertyName": "items",
                "index": 0
            },

            // ================================================================
            // INSERT: UsrIframe for Looker embedding (hidden by default)
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrLookerIframe",
                "values": {
                    "type": "crt.IFrame",
                    "src": "",
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 2, "rowSpan": 1 },
                    "visible": "$UsrShowLookerIframe",
                    "styles": {
                        "width": "100%",
                        "height": "600px",
                        "border": "none"
                    }
                },
                "parentName": "GridContainer_fh039aq",
                "propertyName": "items",
                "index": 0
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    // Visibility controls
                    "UsrShowLookerIframe": { "value": false },
                    "UsrShowCommissionFilters": { "value": false },
                    "UsrShowCustomerNameFilter": { "value": false },

                    // Commission filter attributes (parent doesn't have these)
                    "UsrYearMonth": {
                        "modelConfig": {
                            "path": "PDS.UsrYearMonth"
                        }
                    },
                    "UsrSalesGroup": {
                        "modelConfig": {
                            "path": "PDS.UsrSalesGroup"
                        }
                    },

                    // Customer Name for "Items by Customer" (parent doesn't have this)
                    "UsrCustomerName": { "value": "" }
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
                    console.log("[v24] Parent-driven handler initialized");
                    console.log("[v24] Using parent's LookupAttribute_bsixu8a for report selection");
                    console.log("[v24] Parent business rules control filter visibility");
                    return;
                }
            },

            // ================================================================
            // REPORT SELECTION - Handle Looker iframe + Commission filters visibility
            // (Parent business rules handle date/status filter visibility)
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    // Listen to PARENT's dropdown attribute
                    if (request.attributeName === "LookupAttribute_bsixu8a" && !request.silent) {
                        const ctx = request.$context;
                        let selectedReport = null;

                        try {
                            selectedReport = await ctx.LookupAttribute_bsixu8a;
                        } catch (e) {
                            console.log("[v24] Error getting report:", e);
                        }

                        if (!selectedReport || !selectedReport.value) {
                            ctx.UsrShowLookerIframe = false;
                            ctx.UsrShowCommissionFilters = false;
                            return next?.handle(request);
                        }

                        const reportId = selectedReport.value;
                        const reportName = selectedReport.displayValue || "";
                        const reportNameLower = reportName.toLowerCase();

                        // Check if Looker report (has UsrURL)
                        let lookerUrl = "";
                        try {
                            const bpmcsrf = getBpmcsrf();
                            const metaResp = await fetch("/0/odata/UsrReportesPampa(" + reportId + ")?$select=UsrURL", {
                                headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                            });
                            if (metaResp.ok) {
                                const meta = await metaResp.json();
                                lookerUrl = meta.UsrURL || "";
                            }
                        } catch (e) {
                            console.log("[v24] Error checking Looker URL:", e);
                        }

                        // Determine report type
                        const isLooker = lookerUrl && lookerUrl.length > 0;
                        const isCommission = reportNameLower.includes("commission");
                        const isItemsByCustomer = reportNameLower.includes("items by customer");

                        // Reset visibility
                        ctx.UsrShowLookerIframe = false;
                        ctx.UsrShowCommissionFilters = false;
                        ctx.UsrShowCustomerNameFilter = false;

                        if (isLooker) {
                            // LOOKER: Show iframe and set src
                            ctx.UsrShowLookerIframe = true;
                            setLookerIframeSrc(lookerUrl);
                            console.log("[v24] Report:", reportName, "| Type: LOOKER | Iframe visible");
                        } else if (isCommission) {
                            // COMMISSION: Show our YearMonth/SalesGroup filters
                            ctx.UsrShowCommissionFilters = true;
                            console.log("[v24] Report:", reportName, "| Type: COMMISSION | Commission filters visible");
                        } else if (isItemsByCustomer) {
                            // ITEMS BY CUSTOMER: Show Customer Name filter (parent shows date filters)
                            ctx.UsrShowCustomerNameFilter = true;
                            console.log("[v24] Report:", reportName, "| Type: ITEMS BY CUSTOMER | Customer name filter visible");
                        } else {
                            // OTHER EXCEL: Parent rules control date/status filters
                            console.log("[v24] Report:", reportName, "| Type: EXCEL | Parent controls filters");
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

                    // Get selected report from PARENT's dropdown
                    let selectedReport = null;
                    try {
                        selectedReport = await ctx.LookupAttribute_bsixu8a;
                    } catch (e) {
                        console.log("[v24] Error getting report:", e);
                    }

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    const reportDisplayName = selectedReport.displayValue || "Report";

                    console.log("[v24] Generate clicked | Report:", reportDisplayName, "| ID:", pampaReportId);

                    // Fetch report metadata
                    let reportUrl = "";
                    let reportCode = "";
                    try {
                        const metaResp = await fetch("/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=Id,Name,UsrURL,UsrCode", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (metaResp.ok) {
                            const meta = await metaResp.json();
                            reportUrl = meta.UsrURL || "";
                            reportCode = meta.UsrCode || "";
                        }
                    } catch (e) {
                        console.log("[v24] Metadata fetch error:", e);
                    }

                    // --------------------------------------------------------
                    // LOOKER PATH - Iframe embedding
                    // --------------------------------------------------------
                    if (reportUrl && reportUrl.length > 0) {
                        console.log("[v24] Looker report - refreshing iframe:", reportUrl);
                        ctx.UsrShowLookerIframe = true;
                        setLookerIframeSrc(reportUrl);
                        Terrasoft.showInformation("Looker report loaded in iframe");
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // EXCEL PATH
                    // --------------------------------------------------------
                    console.log("[v24] Excel report generation starting...");

                    // Find IntExcelReport template
                    let intExcelReportId = null;
                    let intEsq = null;
                    try {
                        const escapeName = (s) => (s || "").replace(/'/g, "''");
                        const searchTerms = [];
                        if (reportDisplayName) {
                            searchTerms.push("IntName eq '" + escapeName(reportDisplayName) + "'");
                            searchTerms.push("IntName eq 'Rpt " + escapeName(reportDisplayName) + "'");
                        }
                        if (reportCode && reportCode !== reportDisplayName) {
                            searchTerms.push("IntName eq '" + escapeName(reportCode) + "'");
                            searchTerms.push("IntName eq 'Rpt " + escapeName(reportCode) + "'");
                        }

                        const odataUrl = "/0/odata/IntExcelReport?$filter=(" + searchTerms.join(" or ") + ")&$select=Id,IntName,IntEsq&$top=1";
                        console.log("[v24] Template search:", odataUrl);

                        const odataResp = await fetch(odataUrl, {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        const odataResult = await odataResp.json();

                        if (odataResult.value && odataResult.value.length > 0) {
                            intExcelReportId = odataResult.value[0].Id;
                            intEsq = odataResult.value[0].IntEsq || "";
                            console.log("[v24] Found template:", odataResult.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        console.error("[v24] Template search error:", e);
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // Collect filter values from attributes
                    // Commission: Our UsrYearMonth/UsrSalesGroup (we insert these)
                    // Other: Parent's date/status attributes
                    // --------------------------------------------------------
                    const reportNameLower = reportDisplayName.toLowerCase();
                    const isCommission = reportNameLower.includes("commission");
                    const isItemsByCustomer = reportNameLower.includes("items by customer");

                    let yearMonthId = "00000000-0000-0000-0000-000000000000";
                    let salesGroupId = "00000000-0000-0000-0000-000000000000";
                    let customerName = "";
                    let dateFrom = null;
                    let dateTo = null;
                    let statusName = "";

                    if (isCommission) {
                        // Commission filters (OUR inserted attributes - parent doesn't have these)
                        try {
                            const ym = await ctx.UsrYearMonth;
                            if (ym && ym.value) yearMonthId = ym.value;
                        } catch (e) {}
                        try {
                            const sg = await ctx.UsrSalesGroup;
                            if (sg && sg.value) salesGroupId = sg.value;
                        } catch (e) {}
                        console.log("[v24] Commission filters | YearMonth:", yearMonthId, "| SalesGroup:", salesGroupId);

                    } else if (isItemsByCustomer) {
                        // Customer Name (OUR input) + Date filters (PARENT's attributes)
                        try {
                            customerName = await ctx.UsrCustomerName || "";
                            if (typeof customerName === "string") {
                                customerName = customerName.trim();
                            }
                        } catch (e) {}
                        try {
                            dateFrom = await ctx.CreatedFrom;
                        } catch (e) {}
                        try {
                            dateTo = await ctx.CreatedTo;
                        } catch (e) {}
                        console.log("[v24] Items by Customer | CustomerName:", customerName, "| From:", dateFrom, "| To:", dateTo);

                    } else {
                        // Other Excel: Date + Status filters (PARENT's attributes)
                        try {
                            dateFrom = await ctx.CreatedFrom;
                        } catch (e) {}
                        try {
                            dateTo = await ctx.CreatedTo;
                        } catch (e) {}
                        try {
                            const status = await ctx.LookupAttribute_tytkx09; // Status Order
                            if (status && status.displayValue && status.displayValue !== "All") {
                                statusName = status.displayValue;
                            }
                        } catch (e) {}
                        console.log("[v24] Other Excel | From:", dateFrom, "| To:", dateTo, "| Status:", statusName);
                    }

                    // --------------------------------------------------------
                    // CALL BACKEND SERVICE
                    // --------------------------------------------------------
                    try {
                        Terrasoft.showInformation("Generating report...");

                        const requestBody = {
                            EsqString: intEsq,
                            ReportId: intExcelReportId,
                            RecordCollection: [],
                            YearMonthId: yearMonthId,
                            SalesRepId: salesGroupId,
                            CustomerName: customerName,
                            CreatedFrom: toWcfDate(dateFrom),
                            CreatedTo: toWcfDate(dateTo),
                            StatusName: statusName
                        };

                        console.log("[v24] Calling UsrExcelReportService/Generate");

                        const response = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify(requestBody)
                        });

                        const resultText = await response.text();
                        console.log("[v24] Response:", response.status, resultText);

                        let result;
                        try {
                            result = JSON.parse(resultText);
                        } catch (e) {
                            Terrasoft.showErrorMessage("Invalid response from server");
                            return next?.handle(request);
                        }

                        if (result.success && result.key) {
                            // Download via hidden iframe
                            const downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" +
                                result.key + "/" + encodeURIComponent(reportDisplayName);

                            console.log("[v24] Download URL:", downloadUrl);

                            let iframe = document.getElementById("reportDownloadFrame");
                            if (!iframe) {
                                iframe = document.createElement("iframe");
                                iframe.id = "reportDownloadFrame";
                                iframe.style.display = "none";
                                document.body.appendChild(iframe);
                            }
                            iframe.src = downloadUrl;
                            Terrasoft.showInformation("Download starting: " + reportDisplayName);
                        } else {
                            const errorMsg = result.message || result.errorMessage || "Unknown error";
                            Terrasoft.showErrorMessage("Failed: " + errorMsg);
                        }
                    } catch (error) {
                        console.error("[v24] Exception:", error);
                        Terrasoft.showErrorMessage("Error: " + (error.message || "Unknown error"));
                    }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
