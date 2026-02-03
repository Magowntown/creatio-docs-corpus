/**
 * UsrPage_ebkv9e8 - v41 COMPLETE
 * Package: BGApp_eykaguu
 *
 * FIXES:
 * 1. Customer as LOOKUP (ComboBox bound to BGCustomer)
 * 2. Looker reports EMBEDDED in iframe (not new tab)
 * 3. Better error handling for null EsqString
 * 4. Date filters properly collected and passed to backend
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {

    function getBpmcsrf() {
        var value = "; " + document.cookie;
        var parts = value.split("; BPMCSRF=");
        if (parts.length === 2) return parts.pop().split(";").shift();
        return "";
    }

    function toWcfDate(date) {
        if (!date) return null;
        if (date instanceof Date) return "/Date(" + date.getTime() + ")/";
        if (typeof date === "string") {
            var p = new Date(date);
            if (!isNaN(p.getTime())) return "/Date(" + p.getTime() + ")/";
        }
        return null;
    }

    // Set Looker URL on the parent package's UsrIframe custom element.
    // (The parent Freedom UI schema already contains GridContainer_fh039aq + UsrIframe.)
    function setUsrIframeUrl(url) {
        setTimeout(() => {
            try {
                const el = document.getElementById("UsrIframe");
                if (el) {
                    // UsrIframe defines an input named "Url".
                    el.Url = url;
                    console.log("[v41] UsrIframe.Url set:", url);
                } else {
                    console.log("[v41] WARNING: UsrIframe element not found");
                }
            } catch (e) {
                console.log("[v41] Error setting UsrIframe Url:", e);
            }
        }, 500);
    }

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Parent iframe container (BGlobalLookerStudio). Show only for Looker reports.
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": "$UsrShowLookerFrame" }
            },

            // Date filters - bind visibility
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": "$UsrShowDateFilters" }
            },

            // Status filter - bind visibility
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": { "visible": "$UsrShowDateFilters" }
            },

            // Generate button
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "clicked": { "request": "usr.GenerateReportRequest" }
                }
            },

            // ================================================================
            // COMMISSION FILTERS CONTAINER
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrCommissionFiltersContainer",
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
                    "padding": { "top": "medium", "right": "none", "bottom": "medium", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 1
            },

            // Year-Month COMBOBOX (Lookup)
            {
                "operation": "insert",
                "name": "UsrYearMonthCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Year-Month",
                    "labelPosition": "auto",
                    "control": "$UsrYearMonth",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select month...",
                    "visible": true,
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "tooltip": "Required for Commission reports"
                },
                "parentName": "UsrCommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },

            // Sales Group COMBOBOX (Lookup)
            {
                "operation": "insert",
                "name": "UsrSalesGroupCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "auto",
                    "control": "$UsrSalesGroup",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select group (optional)...",
                    "visible": true,
                    "layoutConfig": { "column": 2, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "tooltip": "Optional filter",
                    "mode": "List"
                },
                "parentName": "UsrCommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // CUSTOMER FILTER CONTAINER (for "Items by Customer")
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrCustomerFilterContainer",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": { "columnGap": "large", "rowGap": "none" },
                    "items": [],
                    "fitContent": true,
                    "visible": "$UsrShowCustomerFilter",
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": { "top": "medium", "right": "none", "bottom": "medium", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 2
            },

            // Customer COMBOBOX (LOOKUP - not text input!)
            {
                "operation": "insert",
                "name": "UsrCustomerCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Customer",
                    "labelPosition": "auto",
                    "control": "$UsrCustomer",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select customer...",
                    "visible": true,
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "tooltip": "Filter by customer"
                },
                "parentName": "UsrCustomerFilterContainer",
                "propertyName": "items",
                "index": 0
            },

        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        // v19.13 PATTERN: Array with operation merge
        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    // Visibility flags
                    "UsrShowCommissionFilters": { "value": false },
                    "UsrShowCustomerFilter": { "value": false },
                    "UsrShowDateFilters": { "value": true },
                    "UsrShowLookerFrame": { "value": false },

                    // Looker URL for iframe
                    "UsrLookerUrl": { "value": "" },

                    // YearMonth - LOOKUP
                    "UsrYearMonth": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGYearMonth"
                        }
                    },

                    // SalesGroup - LOOKUP
                    "UsrSalesGroup": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGSalesGroup"
                        }
                    },

                    // SalesGroup list
                    "UsrSalesGroup_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{ "columnName": "BGSalesGroupName", "direction": "asc" }]
                            }
                        }
                    },

                    // Customer - LOOKUP (bound to BGCustomer entity)
                    "UsrCustomer": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGCustomer"
                        }
                    },

                    // Customer list
                    "UsrCustomer_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{ "columnName": "Name", "direction": "asc" }]
                            }
                        }
                    }
                }
            }
        ]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // Page init
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v41] Page initialized - Lookups + Iframe embedding");
                    return;
                }
            },

            // Report selection - update filter visibility
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    const bpmcsrf = getBpmcsrf();

                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const ctx = request.$context;
                        let selectedReport = null;

                        try {
                            selectedReport = await ctx.LookupAttribute_0as4io2;
                        } catch (e) {
                            console.log("[v41] Error getting report:", e);
                        }

                        // Reset all visibility
                        ctx.UsrShowCommissionFilters = false;
                        ctx.UsrShowCustomerFilter = false;
                        ctx.UsrShowDateFilters = true;
                        ctx.UsrShowLookerFrame = false;
                        ctx.UsrLookerUrl = "";

                        // Clear filter values
                        ctx.UsrYearMonth = null;
                        ctx.UsrSalesGroup = null;
                        ctx.UsrCustomer = null;

                        if (!selectedReport || !selectedReport.value) {
                            console.log("[v41] No report selected");
                            return next?.handle(request);
                        }

                        const reportName = (selectedReport.displayValue || "").toLowerCase();
                        console.log("[v41] Report selected:", selectedReport.displayValue);

                        // Check if Looker
                        let reportUrl = "";
                        try {
                            const r = await fetch("/0/odata/UsrReportesPampa(" + selectedReport.value + ")?$select=UsrURL", {
                                headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                            });
                            if (r.ok) {
                                const m = await r.json();
                                if (m && m.UsrURL) {
                                    reportUrl = m.UsrURL;
                                }
                            }
                        } catch (e) {}

                        if (reportName.includes("commission")) {
                            ctx.UsrShowCommissionFilters = true;
                            ctx.UsrShowDateFilters = false;
                            ctx.UsrShowLookerFrame = false;
                            console.log("[v41] → Commission filters ON");

                        } else if (reportName.includes("items by customer")) {
                            ctx.UsrShowCustomerFilter = true;
                            ctx.UsrShowDateFilters = true;
                            ctx.UsrShowLookerFrame = false;
                            console.log("[v41] → Customer lookup + Date filters ON");

                        } else if (reportUrl) {
                            // LOOKER: Show parent iframe and set URL (filters added on Generate)
                            ctx.UsrShowDateFilters = true;  // Keep date filters for Looker params
                            ctx.UsrShowLookerFrame = true;
                            ctx.UsrLookerUrl = reportUrl;
                            setUsrIframeUrl(reportUrl);
                            console.log("[v41] → Looker iframe ENABLED:", reportUrl);

                        } else {
                            ctx.UsrShowDateFilters = true;
                            ctx.UsrShowLookerFrame = false;
                            console.log("[v41] → Date filters ON (Excel report)");
                        }
                    }

                    return next?.handle(request);
                }
            },

            // Generate report
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    const ctx = request.$context;
                    const bpmcsrf = getBpmcsrf();

                    let selectedReport = null;
                    try {
                        selectedReport = await ctx.LookupAttribute_0as4io2;
                    } catch (e) {}

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    const reportDisplayName = selectedReport.displayValue || "Report";
                    console.log("[v41] Generate:", reportDisplayName);

                    // Check if Looker
                    let reportUrl = "", reportCode = "";
                    try {
                        const r = await fetch("/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=UsrURL,UsrCode", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (r.ok) {
                            const m = await r.json();
                            if (m) {
                                reportUrl = m.UsrURL || "";
                                reportCode = m.UsrCode || "";
                            }
                        }
                    } catch (e) {}

                    // LOOKER: Update iframe with filter params
                    if (reportUrl) {
                        // Build Looker params from date filters
                        let params = "";
                        try {
                            const filters = [];
                            const createdFrom = await ctx.CreatedFrom;
                            const createdTo = await ctx.CreatedTo;
                            const status = await ctx.LookupAttribute_tytkx09;

                            if (createdFrom) {
                                const d = new Date(createdFrom);
                                filters.push("CreatedOn ge datetime'" + d.toISOString().split("T")[0] + "'");
                            }
                            if (createdTo) {
                                const d = new Date(createdTo);
                                filters.push("CreatedOn le datetime'" + d.toISOString().split("T")[0] + "'");
                            }
                            if (status && status.displayValue && status.displayValue !== "All") {
                                filters.push("contains(BGStatus, '" + status.displayValue + "')");
                            }

                            if (filters.length > 0) {
                                params = '?params=%7B"ds0.additionalFilters":"' + filters.join(" and ") + '","ds0.top":"1000000"%7D';
                            }
                        } catch (e) {
                            console.log("[v41] Looker params error:", e);
                        }

                        const fullUrl = reportUrl + params;
                        console.log("[v41] Looker URL with params:", fullUrl);

                        // Update iframe (parent UsrIframe)
                        ctx.UsrLookerUrl = fullUrl;
                        ctx.UsrShowLookerFrame = true;
                        setUsrIframeUrl(fullUrl);
                        Terrasoft.showInformation("Looker report loaded in iframe");
                        return next?.handle(request);
                    }

                    // EXCEL: Find template
                    let intExcelReportId = null, intEsq = "";
                    try {
                        const esc = s => (s || "").replace(/'/g, "''");
                        const terms = [];
                        if (reportDisplayName) {
                            terms.push("IntName eq '" + esc(reportDisplayName) + "'");
                            terms.push("IntName eq 'Rpt " + esc(reportDisplayName) + "'");
                        }
                        if (reportCode && reportCode !== reportDisplayName) {
                            terms.push("IntName eq '" + esc(reportCode) + "'");
                            terms.push("IntName eq 'Rpt " + esc(reportCode) + "'");
                        }

                        const r = await fetch("/0/odata/IntExcelReport?$filter=(" + terms.join(" or ") + ")&$select=Id,IntName,IntEsq&$top=1", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        const d = await r.json();

                        if (d && d.value && d.value[0]) {
                            intExcelReportId = d.value[0].Id;
                            intEsq = d.value[0].IntEsq || "";
                            console.log("[v41] Template:", d.value[0].IntName, "| IntEsq:", intEsq ? "present" : "NULL/EMPTY");
                        } else {
                            Terrasoft.showErrorMessage("Template not found: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error: " + e.message);
                        return next?.handle(request);
                    }

                    // Warn if IntEsq is empty (will cause backend error)
                    if (!intEsq || intEsq.trim() === "") {
                        console.warn("[v41] WARNING: IntEsq is empty for template - backend may fail");
                    }

                    // Collect filters
                    const rLower = reportDisplayName.toLowerCase();
                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    let yearMonthId = emptyGuid;
                    let salesGroupId = emptyGuid;
                    let customerId = emptyGuid;
                    let customerName = "";
                    let dateFrom = null, dateTo = null, statusName = "";

                    // Always collect date filters (they're always visible for non-Commission)
                    try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                    try { dateTo = await ctx.CreatedTo; } catch (e) {}
                    try {
                        const st = await ctx.LookupAttribute_tytkx09;
                        if (st && st.displayValue && st.displayValue !== "All") {
                            statusName = st.displayValue;
                        }
                    } catch (e) {}

                    console.log("[v41] Date filters | From:", dateFrom, "| To:", dateTo, "| Status:", statusName);

                    if (rLower.includes("commission")) {
                        // Get LOOKUP values
                        try {
                            const ym = await ctx.UsrYearMonth;
                            if (ym && ym.value) {
                                yearMonthId = ym.value;
                                console.log("[v41] YearMonth:", ym.displayValue, "| ID:", yearMonthId);
                            }
                        } catch (e) {}

                        try {
                            const sg = await ctx.UsrSalesGroup;
                            if (sg && sg.value) {
                                salesGroupId = sg.value;
                                console.log("[v41] SalesGroup:", sg.displayValue, "| ID:", salesGroupId);
                            }
                        } catch (e) {}

                    } else if (rLower.includes("items by customer")) {
                        // Get Customer LOOKUP value
                        try {
                            const cust = await ctx.UsrCustomer;
                            if (cust && cust.value) {
                                customerId = cust.value;
                                customerName = cust.displayValue || "";
                                console.log("[v41] Customer:", customerName, "| ID:", customerId);
                            } else {
                                console.log("[v41] WARNING: No customer selected for Items by Customer report");
                            }
                        } catch (e) {
                            console.log("[v41] Customer lookup error:", e);
                        }
                    }

                    // Generate
                    try {
                        Terrasoft.showInformation("Generating report...");

                        const requestBody = {
                            EsqString: intEsq,
                            ReportId: intExcelReportId,
                            RecordCollection: [],
                            YearMonthId: yearMonthId,
                            SalesRepId: salesGroupId,
                            CustomerId: customerId,
                            CustomerName: customerName,
                            CreatedFrom: toWcfDate(dateFrom),
                            CreatedTo: toWcfDate(dateTo),
                            StatusName: statusName
                        };

                        console.log("[v41] Request body:", JSON.stringify(requestBody, null, 2));

                        const r = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify(requestBody)
                        });

                        const result = await r.json();
                        console.log("[v41] Result:", result);

                        if (result && result.success && result.key) {
                            let iframe = document.getElementById("reportDownloadFrame");
                            if (!iframe) {
                                iframe = document.createElement("iframe");
                                iframe.id = "reportDownloadFrame";
                                iframe.style.display = "none";
                                document.body.appendChild(iframe);
                            }
                            iframe.src = "/0/rest/UsrExcelReportService/GetReport/" + result.key + "/" + encodeURIComponent(reportDisplayName);
                            Terrasoft.showInformation("Downloading: " + reportDisplayName);
                        } else {
                            const errorMsg = (result && result.message) || (result && result.errorMessage) || "Generation failed";
                            console.error("[v41] Generation failed:", errorMsg);
                            Terrasoft.showErrorMessage(errorMsg);
                        }
                    } catch (e) {
                        console.error("[v41] Error:", e);
                        Terrasoft.showErrorMessage("Error: " + e.message);
                    }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
