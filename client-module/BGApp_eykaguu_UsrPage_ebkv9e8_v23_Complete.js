/**
 * UsrPage_ebkv9e8 - v23 COMPLETE
 * Package: BGApp_eykaguu
 *
 * COMBINES:
 * - v20's BGlobal backend pattern ({EsqString, ReportId, RecordCollection})
 * - v18's Commission filter UI (YearMonth, SalesGroup)
 * - v21's iframe embedding for Looker Studio
 * - Customer filter for "Items by Customer"
 * - Date + Status filters for other Excel reports
 *
 * VISIBILITY RULES:
 * | Report Type          | Commission | Date | Customer | Status | Iframe |
 * |----------------------|------------|------|----------|--------|--------|
 * | None                 | ❌         | ❌   | ❌       | ❌     | ❌     |
 * | Commission/IW_Comm   | ✅         | ❌   | ❌       | ❌     | ❌     |
 * | Items by Customer    | ❌         | ✅   | ✅       | ❌     | ❌     |
 * | Other Excel          | ❌         | ✅   | ❌       | ✅     | ❌     |
 * | Looker Studio        | ❌         | ❌   | ❌       | ❌     | ✅     |
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
     * Converts a JavaScript Date to WCF JSON format: /Date(milliseconds)/
     * WCF services require this format, not ISO 8601.
     */
    function toWcfDate(date) {
        if (!date) return null;
        // Handle Date objects
        if (date instanceof Date) {
            return "/Date(" + date.getTime() + ")/";
        }
        // Handle ISO string
        if (typeof date === "string") {
            var parsed = new Date(date);
            if (!isNaN(parsed.getTime())) {
                return "/Date(" + parsed.getTime() + ")/";
            }
        }
        return null;
    }

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // ================================================================
            // HIDE PARENT'S REPORT DROPDOWN (we use our own)
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": { "visible": false }
            },

            // ================================================================
            // IFRAME CONTAINER - For Looker Studio reports
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": "$UsrShowLookerIframe" }
            },

            // ================================================================
            // DATE FILTERS CONTAINER - Bind to attribute
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": "$UsrShowDateFilters" }
            },

            // ================================================================
            // STATUS FILTER CONTAINER - Bind to attribute
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": { "visible": "$UsrShowStatusFilter" }
            },

            // ================================================================
            // GENERATE BUTTON - Wire to our handler
            // ================================================================
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "visible": true,
                    "clicked": { "request": "usr.GenerateReportRequest" }
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
                    "visible": true
                },
                "parentName": "BGReportContainer",
                "propertyName": "items",
                "index": 0
            },

            // ================================================================
            // INSERT: Commission warning label
            // ================================================================
            {
                "operation": "insert",
                "name": "BGCommissionWarning",
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

            // ================================================================
            // INSERT: Year-Month filter (Commission)
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
            // INSERT: Sales Group filter (Commission)
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
                    "tooltip": "Optional filter",
                    "mode": "List"
                },
                "parentName": "BGCommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // INSERT: Customer filter container (Items by Customer)
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
            // INSERT: Customer Lookup (same pattern as v21)
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
                    "visible": true
                },
                "parentName": "BGCustomerFilterContainer",
                "propertyName": "items",
                "index": 0
            },
            // ================================================================
            // INSERT: Customer text override (optional - for partial name search)
            // ================================================================
            {
                "operation": "insert",
                "name": "BGCustomerTextOverride",
                "values": {
                    "type": "crt.Input",
                    "label": "Or enter name",
                    "labelPosition": "auto",
                    "control": "$UsrCustomerNameOverride",
                    "placeholder": "Partial name (overrides lookup)...",
                    "layoutConfig": { "column": 2, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "visible": true,
                    "tooltip": "Enter partial name to override lookup selection"
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
                    // Visibility attributes
                    "UsrShowCommissionFilters": { "value": false },
                    "UsrShowDateFilters": { "value": false },
                    "UsrShowCustomerFilter": { "value": false },
                    "UsrShowStatusFilter": { "value": false },
                    "UsrShowLookerIframe": { "value": false },

                    // Commission filter values (data source bound)
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
                                "default": [{ "columnName": "BGSalesGroupName", "direction": "asc" }]
                            }
                        }
                    },

                    // Customer filter - uses same pattern as v21
                    "UsrCustomer": {
                        "modelConfig": { "path": "UsrEntity_e7ac661DS.BGCustomer" }
                    },
                    "UsrCustomer_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{ "columnName": "Name", "direction": "asc" }]
                            }
                        }
                    },
                    // Customer name override (text input for partial search)
                    "UsrCustomerNameOverride": { "value": "" }
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
                    console.log("[v23] Page initialized - Complete handler with all filters");
                    return;
                }
            },

            // ================================================================
            // REPORT SELECTION - Update visibility based on report type
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const ctx = request.$context;
                        let selectedReport = null;

                        try {
                            selectedReport = await ctx.LookupAttribute_0as4io2;
                        } catch (e) {
                            console.log("[v23] Error getting report:", e);
                        }

                        if (!selectedReport || !selectedReport.displayValue) {
                            // No report selected - hide everything
                            ctx.UsrShowCommissionFilters = false;
                            ctx.UsrShowDateFilters = false;
                            ctx.UsrShowCustomerFilter = false;
                            ctx.UsrShowStatusFilter = false;
                            ctx.UsrShowLookerIframe = false;
                            console.log("[v23] No report selected - all filters hidden");
                            return next?.handle(request);
                        }

                        const reportName = (selectedReport.displayValue || "").toLowerCase();
                        const reportId = selectedReport.value;

                        // Check if Looker report (has UsrURL)
                        let isLooker = false;
                        let lookerUrl = "";
                        try {
                            const bpmcsrf = getBpmcsrf();
                            const metaResp = await fetch("/0/odata/UsrReportesPampa(" + reportId + ")?$select=UsrURL", {
                                headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                            });
                            if (metaResp.ok) {
                                const meta = await metaResp.json();
                                lookerUrl = meta.UsrURL || "";
                                isLooker = lookerUrl.length > 0;
                            }
                        } catch (e) {
                            console.log("[v23] Error checking Looker URL:", e);
                        }

                        // Determine report type
                        const isCommission = reportName.includes("commission");
                        const isItemsByCustomer = reportName.includes("items by customer");

                        // Reset all filters
                        ctx.UsrShowCommissionFilters = false;
                        ctx.UsrShowDateFilters = false;
                        ctx.UsrShowCustomerFilter = false;
                        ctx.UsrShowStatusFilter = false;
                        ctx.UsrShowLookerIframe = false;

                        // Apply visibility rules
                        if (isLooker) {
                            // LOOKER: Show iframe container
                            ctx.UsrShowLookerIframe = true;

                            console.log("[v23] Report:", selectedReport.displayValue, "| Type: LOOKER | URL:", lookerUrl);

                            // Set iframe src after DOM updates (Freedom UI needs time to render)
                            setTimeout(() => {
                                try {
                                    // Try Freedom UI component (UsrIframe with shadowRoot)
                                    var usrIframe = document.getElementById("UsrIframe");
                                    if (usrIframe && usrIframe.shadowRoot) {
                                        var iframe = usrIframe.shadowRoot.querySelector("iframe");
                                        if (iframe) {
                                            iframe.src = lookerUrl;
                                            console.log("[v23] Looker iframe src set via shadowRoot:", lookerUrl);
                                            return;
                                        }
                                    }

                                    // Fallback: Try to find iframe in container
                                    var container = document.querySelector("[data-item-marker='GridContainer_fh039aq']") ||
                                                    document.getElementById("GridContainer_fh039aq");
                                    if (container) {
                                        var iframeEl = container.querySelector("iframe");
                                        if (iframeEl) {
                                            iframeEl.src = lookerUrl;
                                            console.log("[v23] Looker iframe src set via container:", lookerUrl);
                                            return;
                                        }
                                    }

                                    // Last resort: Find any iframe that might be for Looker
                                    var iframes = document.querySelectorAll("iframe");
                                    for (var i = 0; i < iframes.length; i++) {
                                        var f = iframes[i];
                                        if (f.id !== "reportDownloadFrame" && !f.src.includes("/0/rest/")) {
                                            f.src = lookerUrl;
                                            console.log("[v23] Looker iframe src set via fallback:", lookerUrl);
                                            return;
                                        }
                                    }

                                    console.log("[v23] WARNING: Could not find iframe element to set src");
                                } catch (e) {
                                    console.log("[v23] Error setting iframe src:", e);
                                }
                            }, 500);

                            console.log("[v23] Report:", selectedReport.displayValue, "| Type: LOOKER | Iframe visible");

                        } else if (isCommission) {
                            // COMMISSION: Show commission filters only
                            ctx.UsrShowCommissionFilters = true;
                            console.log("[v23] Report:", selectedReport.displayValue, "| Type: COMMISSION | Commission filters visible");

                        } else if (isItemsByCustomer) {
                            // ITEMS BY CUSTOMER: Show date filters + customer filter
                            ctx.UsrShowDateFilters = true;
                            ctx.UsrShowCustomerFilter = true;
                            console.log("[v23] Report:", selectedReport.displayValue, "| Type: ITEMS BY CUSTOMER | Date + Customer filters visible");

                        } else {
                            // OTHER EXCEL: Show date filters + status filter
                            ctx.UsrShowDateFilters = true;
                            ctx.UsrShowStatusFilter = true;
                            console.log("[v23] Report:", selectedReport.displayValue, "| Type: OTHER EXCEL | Date + Status filters visible");
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

                    // Get selected report
                    let selectedReport = null;
                    try {
                        selectedReport = await ctx.LookupAttribute_0as4io2;
                    } catch (e) {
                        console.log("[v23] Error getting report:", e);
                    }

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    const reportDisplayName = selectedReport.displayValue || "Report";

                    console.log("[v23] Generate clicked | Report:", reportDisplayName, "| ID:", pampaReportId);

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
                        console.log("[v23] Metadata fetch error:", e);
                    }

                    // --------------------------------------------------------
                    // LOOKER PATH - Embed in iframe
                    // --------------------------------------------------------
                    if (reportUrl && reportUrl.length > 0) {
                        console.log("[v23] Looker report - setting iframe src:", reportUrl);

                        // Ensure iframe container is visible
                        ctx.UsrShowLookerIframe = true;

                        // Set iframe src (with delay for DOM update)
                        setTimeout(() => {
                            try {
                                // Try Freedom UI component
                                var usrIframe = document.getElementById("UsrIframe");
                                if (usrIframe && usrIframe.shadowRoot) {
                                    var iframe = usrIframe.shadowRoot.querySelector("iframe");
                                    if (iframe) {
                                        iframe.src = reportUrl;
                                        console.log("[v23] Generate: Iframe src set via shadowRoot");
                                        return;
                                    }
                                }

                                // Fallback: container search
                                var container = document.querySelector("[data-item-marker='GridContainer_fh039aq']") ||
                                                document.getElementById("GridContainer_fh039aq");
                                if (container) {
                                    var iframeEl = container.querySelector("iframe");
                                    if (iframeEl) {
                                        iframeEl.src = reportUrl;
                                        console.log("[v23] Generate: Iframe src set via container");
                                    }
                                }
                            } catch (e) {
                                console.log("[v23] Generate: Error setting iframe:", e);
                            }
                        }, 300);

                        Terrasoft.showInformation("Loading Looker report in iframe...");
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // EXCEL PATH - BGlobal pattern
                    // --------------------------------------------------------
                    console.log("[v23] Excel report generation starting...");

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
                        console.log("[v23] Template search URL:", odataUrl);

                        const odataResp = await fetch(odataUrl, {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        const odataResult = await odataResp.json();

                        if (odataResult.value && odataResult.value.length > 0) {
                            intExcelReportId = odataResult.value[0].Id;
                            intEsq = odataResult.value[0].IntEsq || "";
                            console.log("[v23] Found template:", odataResult.value[0].IntName, "| ID:", intExcelReportId);
                        } else {
                            console.log("[v23] Template not found for:", reportDisplayName, "/", reportCode);
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        console.error("[v23] Template search error:", e);
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    // Collect filter values based on report type
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
                        // Get Commission filters
                        try {
                            const ym = await ctx.UsrYearMonth;
                            if (ym && ym.value) yearMonthId = ym.value;
                        } catch (e) {}
                        try {
                            const sg = await ctx.UsrSalesGroup;
                            if (sg && sg.value) salesGroupId = sg.value;
                        } catch (e) {}
                        console.log("[v23] Commission filters | YearMonth:", yearMonthId, "| SalesGroup:", salesGroupId);

                    } else if (isItemsByCustomer) {
                        // Get Customer filter - prefer text override, then lookup displayValue
                        try {
                            const textOverride = await ctx.UsrCustomerNameOverride;
                            if (textOverride && textOverride.trim()) {
                                customerName = textOverride.trim();
                            } else {
                                const customerLookup = await ctx.UsrCustomer;
                                if (customerLookup && customerLookup.displayValue) {
                                    customerName = customerLookup.displayValue;
                                }
                            }
                        } catch (e) {
                            console.log("[v23] Error getting customer:", e);
                        }

                        // Get Date filters from parent's controls
                        try {
                            dateFrom = await ctx.CreatedFrom; // Parent's date filter attribute
                        } catch (e) {}
                        try {
                            dateTo = await ctx.CreatedTo; // Parent's date filter attribute
                        } catch (e) {}
                        console.log("[v23] Items by Customer filters | CustomerName:", customerName, "| CreatedFrom:", dateFrom, "| CreatedTo:", dateTo);

                    } else {
                        // Get Date + Status filters (parent's attributes)
                        try {
                            dateFrom = await ctx.CreatedFrom;
                        } catch (e) {}
                        try {
                            dateTo = await ctx.CreatedTo;
                        } catch (e) {}
                        try {
                            const status = await ctx.LookupAttribute_tytkx09; // Parent's status lookup
                            if (status && status.displayValue && status.displayValue !== "All") {
                                statusName = status.displayValue;
                            }
                        } catch (e) {}
                        console.log("[v23] Other Excel filters | CreatedFrom:", dateFrom, "| CreatedTo:", dateTo, "| Status:", statusName);
                    }

                    // --------------------------------------------------------
                    // CALL BACKEND SERVICE - BGlobal pattern
                    // {EsqString, ReportId, RecordCollection} + our filter extensions
                    // Field names MUST match UsrExcelReportRequest DataContract
                    // --------------------------------------------------------
                    try {
                        Terrasoft.showInformation("Generating report...");

                        const requestBody = {
                            // BGlobal's original fields
                            EsqString: intEsq,
                            ReportId: intExcelReportId,
                            RecordCollection: [],

                            // Commission filters
                            YearMonthId: yearMonthId,
                            SalesRepId: salesGroupId,  // Backend uses SalesRepId for SalesGroup (legacy naming)

                            // Items by Customer filters
                            CustomerName: customerName,
                            CreatedFrom: toWcfDate(dateFrom),  // WCF requires /Date(ms)/ format
                            CreatedTo: toWcfDate(dateTo),      // WCF requires /Date(ms)/ format

                            // Status filter (Other Excel reports)
                            StatusName: statusName
                        };

                        console.log("[v23] Calling UsrExcelReportService/Generate with:", JSON.stringify(requestBody, null, 2));

                        const response = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify(requestBody)
                        });

                        console.log("[v23] Response status:", response.status);
                        const resultText = await response.text();
                        console.log("[v23] Response text:", resultText);

                        let result;
                        try {
                            result = JSON.parse(resultText);
                        } catch (e) {
                            console.error("[v23] JSON parse error:", e);
                            Terrasoft.showErrorMessage("Invalid response from server");
                            return next?.handle(request);
                        }

                        if (result.success && result.key) {
                            // Download via hidden iframe
                            const downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" +
                                result.key + "/" + encodeURIComponent(reportDisplayName);

                            console.log("[v23] Download URL:", downloadUrl);

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
                            console.error("[v23] Generation failed:", errorMsg);
                            Terrasoft.showErrorMessage("Failed: " + errorMsg);
                        }
                    } catch (error) {
                        console.error("[v23] Exception:", error);
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
