/**
 * UsrPage_ebkv9e8 - v38 WITH LOOKUPS
 * Package: BGApp_eykaguu
 *
 * Proper ComboBox lookups for Year-Month and Sales Group
 * Customer Name stays as text input (search filter)
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

            // Date filters - conditional
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": "$UsrShowDateFilters" }
            },

            // Status filter - conditional
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": { "visible": "$UsrShowDateFilters" }
            },

            // Generate button
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": { "clicked": { "request": "usr.GenerateReportRequest" } }
            },

            // YEAR-MONTH COMBOBOX (Lookup)
            {
                "operation": "insert",
                "name": "UsrYearMonthCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Year-Month",
                    "labelPosition": "above",
                    "control": "$UsrYearMonth",
                    "listActions": [],
                    "showValueAsLink": false,
                    "controlActions": [],
                    "placeholder": "Select month...",
                    "visible": "$UsrShowCommissionFilters"
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 1
            },

            // SALES GROUP COMBOBOX (Lookup)
            {
                "operation": "insert",
                "name": "UsrSalesGroupCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "above",
                    "control": "$UsrSalesGroup",
                    "listActions": [],
                    "showValueAsLink": false,
                    "controlActions": [],
                    "placeholder": "Select group (optional)...",
                    "visible": "$UsrShowCommissionFilters"
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 2
            },

            // CUSTOMER NAME INPUT (Text search)
            {
                "operation": "insert",
                "name": "UsrCustomerNameInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Customer Name",
                    "labelPosition": "above",
                    "control": "$UsrCustomerName",
                    "placeholder": "Enter customer name...",
                    "visible": "$UsrShowCustomerFilter"
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 3
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/{
            "attributes": {
                "UsrShowCommissionFilters": { "value": false },
                "UsrShowCustomerFilter": { "value": false },
                "UsrShowDateFilters": { "value": true },
                "UsrYearMonth": {
                    "modelConfig": {
                        "path": "UsrYearMonthDS.UsrYearMonth"
                    }
                },
                "UsrSalesGroup": {
                    "modelConfig": {
                        "path": "UsrSalesGroupDS.UsrSalesGroup"
                    }
                },
                "UsrCustomerName": { "value": "" }
            }
        }/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/{
            "dataSources": {
                "UsrYearMonthDS": {
                    "type": "crt.EntityDataSource",
                    "scope": "page",
                    "config": {
                        "entitySchemaName": "BGYearMonth"
                    }
                },
                "UsrSalesGroupDS": {
                    "type": "crt.EntityDataSource",
                    "scope": "page",
                    "config": {
                        "entitySchemaName": "BGSalesGroup"
                    }
                }
            }
        }/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v38] Page initialized with lookup ComboBoxes");
                    return;
                }
            },

            // Report selection - update filter visibility
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const ctx = request.$context;
                        let selectedReport = null;

                        try {
                            selectedReport = await ctx.LookupAttribute_0as4io2;
                        } catch (e) {
                            console.log("[v38] Error:", e);
                        }

                        // Reset
                        ctx.UsrShowCommissionFilters = false;
                        ctx.UsrShowCustomerFilter = false;
                        ctx.UsrShowDateFilters = true;

                        if (!selectedReport || !selectedReport.value) {
                            console.log("[v38] No report selected");
                            return next?.handle(request);
                        }

                        const reportName = (selectedReport.displayValue || "").toLowerCase();
                        console.log("[v38] Report selected:", selectedReport.displayValue);

                        if (reportName.includes("commission")) {
                            ctx.UsrShowCommissionFilters = true;
                            ctx.UsrShowDateFilters = false;
                            console.log("[v38] → Commission filters ON");
                        } else if (reportName.includes("items by customer")) {
                            ctx.UsrShowCustomerFilter = true;
                            ctx.UsrShowDateFilters = true;
                            console.log("[v38] → Customer filter ON");
                        } else {
                            ctx.UsrShowDateFilters = true;
                            console.log("[v38] → Date filters ON");
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
                    console.log("[v38] Generate:", reportDisplayName);

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
                        Terrasoft.showInformation("Looker report opened in new tab");
                        return next?.handle(request);
                    }

                    // Find template
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
                            console.log("[v38] Template:", d.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Template not found: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error: " + e.message);
                        return next?.handle(request);
                    }

                    // Collect filters
                    const rLower = reportDisplayName.toLowerCase();
                    let yearMonthId = "00000000-0000-0000-0000-000000000000";
                    let salesGroupId = "00000000-0000-0000-0000-000000000000";
                    let customerName = "";
                    let dateFrom = null, dateTo = null, statusName = "";

                    if (rLower.includes("commission")) {
                        // Get lookup values
                        try {
                            const ym = await ctx.UsrYearMonth;
                            if (ym && ym.value) yearMonthId = ym.value;
                            console.log("[v38] YearMonth selected:", ym);
                        } catch (e) {}

                        try {
                            const sg = await ctx.UsrSalesGroup;
                            if (sg && sg.value) salesGroupId = sg.value;
                            console.log("[v38] SalesGroup selected:", sg);
                        } catch (e) {}

                        console.log("[v38] Commission | YearMonthId:", yearMonthId, "| SalesGroupId:", salesGroupId);

                    } else if (rLower.includes("items by customer")) {
                        customerName = (await ctx.UsrCustomerName) || "";
                        try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                        try { dateTo = await ctx.CreatedTo; } catch (e) {}
                        console.log("[v38] Items by Customer | Name:", customerName);

                    } else {
                        try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                        try { dateTo = await ctx.CreatedTo; } catch (e) {}
                        try {
                            const st = await ctx.LookupAttribute_tytkx09;
                            if (st && st.displayValue && st.displayValue !== "All") {
                                statusName = st.displayValue;
                            }
                        } catch (e) {}
                    }

                    // Generate
                    try {
                        Terrasoft.showInformation("Generating report...");

                        const r = await fetch("/0/rest/UsrExcelReportService/Generate", {
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

                        const result = await r.json();
                        console.log("[v38] Result:", result);

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
                            Terrasoft.showErrorMessage((result && result.message) || (result && result.errorMessage) || "Generation failed");
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
