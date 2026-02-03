/**
 * UsrPage_ebkv9e8 - v24 FIX (Safe Minimal)
 * Package: BGApp_eykaguu
 *
 * FIXES from v24:
 * - Removed crt.IFrame (may not be valid component type)
 * - Removed PDS paths (may not exist)
 * - Uses simple value attributes
 * - Looker opens in new tab (safer than iframe for now)
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/[]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/()/**SCHEMA_ARGS*/ {

    function getBpmcsrf() {
        var value = "; " + document.cookie;
        var parts = value.split("; BPMCSRF=");
        if (parts.length === 2) return parts.pop().split(";").shift();
        return "";
    }

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

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Wire Generate button
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "clicked": { "request": "usr.GenerateReportRequest" }
                }
            },

            // Commission Filters Container
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

            // Year-Month ComboBox
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
                    "visible": true
                },
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },

            // Sales Group ComboBox
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
                    "visible": true
                },
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // Customer Name Container
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

            // Customer Name Input
            {
                "operation": "insert",
                "name": "UsrCustomerNameInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Customer Name",
                    "labelPosition": "auto",
                    "control": "$UsrCustomerName",
                    "placeholder": "Enter customer name...",
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 2, "rowSpan": 1 },
                    "visible": true
                },
                "parentName": "CustomerNameContainer",
                "propertyName": "items",
                "index": 0
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/{
            "attributes": {
                "UsrShowCommissionFilters": { "value": false },
                "UsrShowCustomerNameFilter": { "value": false },
                "UsrYearMonth": {},
                "UsrSalesGroup": {},
                "UsrCustomerName": { "value": "" }
            }
        }/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/{}/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // Page init
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v24-fix] Page initialized");
                    return;
                }
            },

            // Report selection
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_bsixu8a" && !request.silent) {
                        const ctx = request.$context;
                        let selectedReport = null;

                        try {
                            selectedReport = await ctx.LookupAttribute_bsixu8a;
                        } catch (e) {
                            console.log("[v24-fix] Error getting report:", e);
                        }

                        // Reset visibility
                        ctx.UsrShowCommissionFilters = false;
                        ctx.UsrShowCustomerNameFilter = false;

                        if (!selectedReport || !selectedReport.value) {
                            return next?.handle(request);
                        }

                        const reportName = (selectedReport.displayValue || "").toLowerCase();

                        if (reportName.includes("commission")) {
                            ctx.UsrShowCommissionFilters = true;
                            console.log("[v24-fix] Commission filters visible");
                        } else if (reportName.includes("items by customer")) {
                            ctx.UsrShowCustomerNameFilter = true;
                            console.log("[v24-fix] Customer name filter visible");
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
                        selectedReport = await ctx.LookupAttribute_bsixu8a;
                    } catch (e) {
                        console.log("[v24-fix] Error getting report:", e);
                    }

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    const reportDisplayName = selectedReport.displayValue || "Report";

                    console.log("[v24-fix] Generate:", reportDisplayName);

                    // Check if Looker
                    let reportUrl = "";
                    let reportCode = "";
                    try {
                        const metaResp = await fetch("/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=UsrURL,UsrCode", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (metaResp.ok) {
                            const meta = await metaResp.json();
                            reportUrl = meta.UsrURL || "";
                            reportCode = meta.UsrCode || "";
                        }
                    } catch (e) {}

                    // LOOKER: Open in new tab (safer)
                    if (reportUrl) {
                        window.open(reportUrl, "_blank");
                        Terrasoft.showInformation("Looker report opened in new tab");
                        return next?.handle(request);
                    }

                    // EXCEL: Find template
                    let intExcelReportId = null;
                    let intEsq = "";
                    try {
                        const esc = (s) => (s || "").replace(/'/g, "''");
                        const terms = [];
                        if (reportDisplayName) {
                            terms.push("IntName eq '" + esc(reportDisplayName) + "'");
                            terms.push("IntName eq 'Rpt " + esc(reportDisplayName) + "'");
                        }
                        if (reportCode && reportCode !== reportDisplayName) {
                            terms.push("IntName eq '" + esc(reportCode) + "'");
                            terms.push("IntName eq 'Rpt " + esc(reportCode) + "'");
                        }

                        const resp = await fetch("/0/odata/IntExcelReport?$filter=(" + terms.join(" or ") + ")&$select=Id,IntName,IntEsq&$top=1", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        const data = await resp.json();

                        if (data.value && data.value[0]) {
                            intExcelReportId = data.value[0].Id;
                            intEsq = data.value[0].IntEsq || "";
                            console.log("[v24-fix] Template:", data.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Template not found: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error: " + e.message);
                        return next?.handle(request);
                    }

                    // Collect filters
                    const reportLower = reportDisplayName.toLowerCase();
                    let yearMonthId = "00000000-0000-0000-0000-000000000000";
                    let salesGroupId = "00000000-0000-0000-0000-000000000000";
                    let customerName = "";
                    let dateFrom = null;
                    let dateTo = null;
                    let statusName = "";

                    if (reportLower.includes("commission")) {
                        try {
                            const ym = await ctx.UsrYearMonth;
                            if (ym && ym.value) yearMonthId = ym.value;
                        } catch (e) {}
                        try {
                            const sg = await ctx.UsrSalesGroup;
                            if (sg && sg.value) salesGroupId = sg.value;
                        } catch (e) {}
                        console.log("[v24-fix] Commission | YearMonth:", yearMonthId, "| SalesGroup:", salesGroupId);

                    } else if (reportLower.includes("items by customer")) {
                        try {
                            customerName = (await ctx.UsrCustomerName) || "";
                        } catch (e) {}
                        try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                        try { dateTo = await ctx.CreatedTo; } catch (e) {}
                        console.log("[v24-fix] Items by Customer | Name:", customerName);

                    } else {
                        try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                        try { dateTo = await ctx.CreatedTo; } catch (e) {}
                        try {
                            const st = await ctx.LookupAttribute_tytkx09;
                            if (st && st.displayValue && st.displayValue !== "All") statusName = st.displayValue;
                        } catch (e) {}
                    }

                    // Generate
                    try {
                        Terrasoft.showInformation("Generating...");

                        const resp = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify({
                                EsqString: intEsq,
                                ReportId: intExcelReportId,
                                RecordCollection: [],
                                YearMonthId: yearMonthId,
                                SalesRepId: salesGroupId,
                                CustomerName: customerName,
                                CreatedFrom: toWcfDate(dateFrom),
                                CreatedTo: toWcfDate(dateTo),
                                StatusName: statusName
                            })
                        });

                        const result = await resp.json();
                        console.log("[v24-fix] Result:", result);

                        if (result.success && result.key) {
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
                            Terrasoft.showErrorMessage(result.message || result.errorMessage || "Failed");
                        }
                    } catch (e) {
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
