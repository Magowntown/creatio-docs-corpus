/**
 * UsrPage_ebkv9e8 - v36 DEBUG
 * Package: BGApp_eykaguu
 *
 * ALL FILTERS ALWAYS VISIBLE - Debug version to verify rendering
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
        if (date instanceof Date) return "/Date(" + date.getTime() + ")/";
        if (typeof date === "string") {
            var p = new Date(date);
            if (!isNaN(p.getTime())) return "/Date(" + p.getTime() + ")/";
        }
        return null;
    }

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Hide iframe
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": false }
            },

            // Show date filters always
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": true }
            },

            // Show status filter always
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": { "visible": true }
            },

            // Wire Generate button
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": { "clicked": { "request": "usr.GenerateReportRequest" } }
            },

            // YEAR-MONTH INPUT - insert directly into MainContainer
            {
                "operation": "insert",
                "name": "UsrYearMonthInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Year-Month (for Commission)",
                    "labelPosition": "above",
                    "control": "$UsrYearMonthText",
                    "placeholder": "e.g., 2025-12",
                    "visible": true
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 1
            },

            // SALES GROUP INPUT
            {
                "operation": "insert",
                "name": "UsrSalesGroupInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Sales Group (for Commission)",
                    "labelPosition": "above",
                    "control": "$UsrSalesGroupText",
                    "placeholder": "e.g., Group Name",
                    "visible": true
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 2
            },

            // CUSTOMER NAME INPUT
            {
                "operation": "insert",
                "name": "UsrCustomerNameInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Customer Name (for Items by Customer)",
                    "labelPosition": "above",
                    "control": "$UsrCustomerName",
                    "placeholder": "Enter customer name...",
                    "visible": true
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 3
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/{
            "attributes": {
                "UsrYearMonthText": { "value": "" },
                "UsrSalesGroupText": { "value": "" },
                "UsrCustomerName": { "value": "" }
            }
        }/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/{}/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v36] Page initialized - 3 inputs should be visible");
                    return;
                }
            },
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        try {
                            const r = await request.$context.LookupAttribute_0as4io2;
                            if (r && r.displayValue) console.log("[v36] Report:", r.displayValue);
                        } catch (e) {}
                    }
                    return next?.handle(request);
                }
            },
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    const ctx = request.$context;
                    const bpmcsrf = getBpmcsrf();
                    let selectedReport = null;
                    try { selectedReport = await ctx.LookupAttribute_0as4io2; } catch (e) {}

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    const reportDisplayName = selectedReport.displayValue || "Report";
                    console.log("[v36] Generate:", reportDisplayName);

                    // Check Looker
                    let reportUrl = "", reportCode = "";
                    try {
                        const r = await fetch("/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=UsrURL,UsrCode", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (r.ok) {
                            const m = await r.json();
                            if (m) { reportUrl = m.UsrURL || ""; reportCode = m.UsrCode || ""; }
                        }
                    } catch (e) {}

                    if (reportUrl) {
                        window.open(reportUrl, "_blank");
                        Terrasoft.showInformation("Looker opened");
                        return next?.handle(request);
                    }

                    // Find template
                    let intExcelReportId = null, intEsq = "";
                    try {
                        const esc = s => (s || "").replace(/'/g, "''");
                        const t = [];
                        if (reportDisplayName) { t.push("IntName eq '" + esc(reportDisplayName) + "'"); t.push("IntName eq 'Rpt " + esc(reportDisplayName) + "'"); }
                        if (reportCode && reportCode !== reportDisplayName) { t.push("IntName eq '" + esc(reportCode) + "'"); t.push("IntName eq 'Rpt " + esc(reportCode) + "'"); }
                        const r = await fetch("/0/odata/IntExcelReport?$filter=(" + t.join(" or ") + ")&$select=Id,IntName,IntEsq&$top=1", { headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf } });
                        const d = await r.json();
                        if (d && d.value && d.value[0]) { intExcelReportId = d.value[0].Id; intEsq = d.value[0].IntEsq || ""; console.log("[v36] Template:", d.value[0].IntName); }
                        else { Terrasoft.showErrorMessage("Template not found"); return next?.handle(request); }
                    } catch (e) { Terrasoft.showErrorMessage("Error: " + e.message); return next?.handle(request); }

                    // Filters
                    const rLower = reportDisplayName.toLowerCase();
                    let yearMonthId = "00000000-0000-0000-0000-000000000000", salesGroupId = "00000000-0000-0000-0000-000000000000", customerName = "", dateFrom = null, dateTo = null, statusName = "";

                    if (rLower.includes("commission")) {
                        const ym = await ctx.UsrYearMonthText || "";
                        const sg = await ctx.UsrSalesGroupText || "";
                        console.log("[v36] Commission | YM:", ym, "| SG:", sg);
                    } else if (rLower.includes("items by customer")) {
                        customerName = (await ctx.UsrCustomerName) || "";
                        try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                        try { dateTo = await ctx.CreatedTo; } catch (e) {}
                    } else {
                        try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                        try { dateTo = await ctx.CreatedTo; } catch (e) {}
                        try { const st = await ctx.LookupAttribute_tytkx09; if (st && st.displayValue && st.displayValue !== "All") statusName = st.displayValue; } catch (e) {}
                    }

                    // Generate
                    try {
                        Terrasoft.showInformation("Generating...");
                        const r = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify({ EsqString: intEsq, ReportId: intExcelReportId, RecordCollection: [], YearMonthId: yearMonthId, SalesRepId: salesGroupId, CustomerName: customerName, CreatedFrom: toWcfDate(dateFrom), CreatedTo: toWcfDate(dateTo), StatusName: statusName })
                        });
                        const res = await r.json();
                        console.log("[v36] Result:", res);
                        if (res && res.success && res.key) {
                            let iframe = document.getElementById("reportDownloadFrame");
                            if (!iframe) { iframe = document.createElement("iframe"); iframe.id = "reportDownloadFrame"; iframe.style.display = "none"; document.body.appendChild(iframe); }
                            iframe.src = "/0/rest/UsrExcelReportService/GetReport/" + res.key + "/" + encodeURIComponent(reportDisplayName);
                            Terrasoft.showInformation("Downloading: " + reportDisplayName);
                        } else { Terrasoft.showErrorMessage((res && res.message) || "Failed"); }
                    } catch (e) { Terrasoft.showErrorMessage("Error: " + e.message); }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
