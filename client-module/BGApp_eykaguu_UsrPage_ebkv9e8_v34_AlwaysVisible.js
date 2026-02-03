/**
 * UsrPage_ebkv9e8 - v34 ALWAYS VISIBLE
 * Package: BGApp_eykaguu
 *
 * DEBUG VERSION: All filters always visible to verify they render
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
            // Hide parent's iframe container
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": false }
            },

            // Ensure the parent report dropdown stays visible and has a proper label/placeholder
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": { "visible": true }
            },
            {
                "operation": "merge",
                "name": "ComboBox_bo00lsk",
                "values": {
                    "label": "Report",
                    "placeholder": "Select a report...",
                    "control": "$LookupAttribute_0as4io2",
                    "visible": true
                }
            },

            // Keep date filters visible for now
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": true }
            },

            // Keep status filter visible
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": { "visible": true }
            },

            // Wire Generate button
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "clicked": { "request": "usr.GenerateReportRequest" }
                }
            },

            // Debug inputs container - ALWAYS VISIBLE (so we can verify rendering)
            {
                "operation": "insert",
                "name": "CommissionFiltersContainer",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": [
                        "minmax(32px, 1fr)",
                        "minmax(32px, 1fr)",
                        "minmax(32px, 1fr)"
                    ],
                    "rows": "minmax(max-content, 32px)",
                    "gap": { "columnGap": "large", "rowGap": "none" },
                    "items": [],
                    "fitContent": true,
                    "visible": true,
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": { "top": "medium", "right": "none", "bottom": "medium", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 1
            },

            // Year-Month Input (debug text)
            {
                "operation": "insert",
                "name": "UsrYearMonthInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Year-Month",
                    "labelPosition": "above",
                    "control": "$UsrYearMonthText",
                    "placeholder": "e.g., 2025-12",
                    "visible": true,
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 }
                },
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },

            // Sales Group Input (debug text)
            {
                "operation": "insert",
                "name": "UsrSalesGroupInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Sales Group",
                    "labelPosition": "above",
                    "control": "$UsrSalesGroupText",
                    "placeholder": "e.g., Group Name",
                    "visible": true,
                    "layoutConfig": { "column": 2, "row": 1, "colSpan": 1, "rowSpan": 1 }
                },
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // Customer Name Input (debug text)
            {
                "operation": "insert",
                "name": "UsrCustomerNameInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Customer Name",
                    "labelPosition": "above",
                    "control": "$UsrCustomerName",
                    "placeholder": "Enter customer name...",
                    "visible": true,
                    "layoutConfig": { "column": 3, "row": 1, "colSpan": 1, "rowSpan": 1 }
                },
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 2
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    "UsrYearMonthText": { "value": "" },
                    "UsrSalesGroupText": { "value": "" },
                    "UsrCustomerName": { "value": "" }
                }
            }
        ]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/{}/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // Page init
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v34] Page initialized - filters should be visible");
                    return;
                }
            },

            // Report selection - just log
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const ctx = request.$context;
                        let selectedReport = null;

                        try {
                            selectedReport = await ctx.LookupAttribute_0as4io2;
                        } catch (e) {
                            console.log("[v34] Error getting report:", e);
                        }

                        if (selectedReport && selectedReport.displayValue) {
                            console.log("[v34] Report selected:", selectedReport.displayValue);
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
                    } catch (e) {
                        console.log("[v34] Error getting report:", e);
                    }

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    const reportDisplayName = selectedReport.displayValue || "Report";

                    console.log("[v34] Generate:", reportDisplayName);

                    // Check if Looker (with null safety)
                    let reportUrl = "";
                    let reportCode = "";
                    try {
                        const metaResp = await fetch("/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=UsrURL,UsrCode", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (metaResp.ok) {
                            const meta = await metaResp.json();
                            if (meta) {
                                reportUrl = meta.UsrURL || "";
                                reportCode = meta.UsrCode || "";
                            }
                        }
                    } catch (e) {
                        console.log("[v34] Metadata error:", e);
                    }

                    // LOOKER: Open in new tab
                    if (reportUrl) {
                        window.open(reportUrl, "_blank");
                        Terrasoft.showInformation("Looker report opened");
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

                        if (data && data.value && data.value[0]) {
                            intExcelReportId = data.value[0].Id;
                            intEsq = data.value[0].IntEsq || "";
                            console.log("[v34] Found template:", data.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Template not found: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error: " + e.message);
                        return next?.handle(request);
                    }

                    // Collect filters - use text inputs for now
                    const reportLower = reportDisplayName.toLowerCase();
                    let yearMonthId = "00000000-0000-0000-0000-000000000000";
                    let salesGroupId = "00000000-0000-0000-0000-000000000000";
                    let customerName = "";
                    let dateFrom = null;
                    let dateTo = null;
                    let statusName = "";

                    // For commission, we need to lookup YearMonth and SalesGroup IDs
                    // For now, just log the text values
                    if (reportLower.includes("commission")) {
                        const ymText = await ctx.UsrYearMonthText || "";
                        const sgText = await ctx.UsrSalesGroupText || "";
                        console.log("[v34] Commission | YearMonth text:", ymText, "| SalesGroup text:", sgText);
                        // TODO: Lookup IDs from text values
                    } else if (reportLower.includes("items by customer")) {
                        customerName = (await ctx.UsrCustomerName) || "";
                        try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                        try { dateTo = await ctx.CreatedTo; } catch (e) {}
                        console.log("[v34] Items by Customer | Name:", customerName);
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
                        console.log("[v34] Result:", result);

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
                            Terrasoft.showErrorMessage((result && result.message) || "Failed");
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
