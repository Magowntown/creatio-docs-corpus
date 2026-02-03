/**
 * UsrPage_ebkv9e8 - v21 Safe Filters
 * Package: BGApp_eykaguu
 *
 * GOAL: Commission filters + Customer filter with BULLETPROOF null guards
 *
 * Features:
 * - Commission reports: Shows YearMonth + SalesGroup filters
 * - Items by Customer: Shows Customer text input
 * - Other reports: Uses parent's date/status filters
 * - Looker reports: Opens in new tab
 *
 * SAFETY: Every .value and .displayValue access is null-guarded
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {

    // ================================================================
    // SAFE HELPER FUNCTIONS
    // ================================================================

    function getBpmcsrf() {
        try {
            var value = "; " + document.cookie;
            var parts = value.split("; BPMCSRF=");
            if (parts.length === 2) return parts.pop().split(";").shift();
        } catch (e) {
            console.log("[v21] getBpmcsrf error:", e);
        }
        return "";
    }

    // SAFE: Get value from lookup with null guards
    function safeGetValue(lookup) {
        if (!lookup) return null;
        if (typeof lookup === 'string') return lookup;
        if (typeof lookup === 'object' && lookup.value !== undefined) return lookup.value;
        return null;
    }

    // SAFE: Get displayValue from lookup with null guards
    function safeGetDisplayValue(lookup) {
        if (!lookup) return "";
        if (typeof lookup === 'string') return lookup;
        if (typeof lookup === 'object' && lookup.displayValue !== undefined) return lookup.displayValue || "";
        return "";
    }

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Hide parent's report dropdown
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": { "visible": false }
            },
            // Hide iframe container
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": false }
            },
            // Date filters - visible based on report type
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": "$UsrShowDateFilters" }
            },
            // Status filter - visible based on report type
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
                    "visible": true,
                    "clicked": { "request": "usr.GenerateReportRequest" }
                }
            },

            // ================================================================
            // Report selector
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
            // Commission filters container
            // ================================================================
            {
                "operation": "insert",
                "name": "BGCommissionContainer",
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
                    "visible": true
                },
                "parentName": "BGCommissionContainer",
                "propertyName": "items",
                "index": 0
            },
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
                    "visible": true
                },
                "parentName": "BGCommissionContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // Customer filter container (for Items by Customer)
            // ================================================================
            {
                "operation": "insert",
                "name": "BGCustomerContainer",
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
                "index": 2
            },
            {
                "operation": "insert",
                "name": "BGCustomerInput",
                "values": {
                    "type": "crt.Input",
                    "label": "Customer Name",
                    "labelPosition": "auto",
                    "control": "$UsrCustomerName",
                    "placeholder": "Type customer name...",
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "visible": true
                },
                "parentName": "BGCustomerContainer",
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
                    "UsrShowDateFilters": { "value": false },
                    "UsrShowCustomerFilter": { "value": false },
                    "UsrYearMonth": {
                        "modelConfig": { "path": "UsrEntity_e7ac661DS.BGYearMonth" }
                    },
                    "UsrSalesGroup": {
                        "modelConfig": { "path": "UsrEntity_e7ac661DS.BGSalesGroup" }
                    },
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
                    try {
                        await next?.handle(request);
                        console.log("[v21] Page init - Safe Filters");
                    } catch (e) {
                        console.log("[v21] Init error:", e);
                    }
                    return;
                }
            },

            // ================================================================
            // REPORT SELECTION - Set filter visibility
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    try {
                        // Only handle report selection changes
                        if (request.attributeName !== "LookupAttribute_0as4io2" || request.silent) {
                            return next?.handle(request);
                        }

                        // SAFE: Get selected report with null guards
                        let selectedReport = null;
                        try {
                            selectedReport = await request.$context.LookupAttribute_0as4io2;
                        } catch (e) {
                            console.log("[v21] Error getting report:", e);
                        }

                        // SAFE: Get display value
                        const reportName = safeGetDisplayValue(selectedReport).toLowerCase();
                        const reportId = safeGetValue(selectedReport);

                        console.log("[v21] Report selected:", reportName || "(none)");

                        // Determine report type
                        const isCommission = reportName.includes("commission");
                        const isItemsByCustomer = reportName.includes("items by customer");

                        // Check if Looker report (has URL)
                        let isLooker = false;
                        if (reportId) {
                            try {
                                const bpmcsrf = getBpmcsrf();
                                const metaUrl = "/0/odata/UsrReportesPampa(" + reportId + ")?$select=UsrURL";
                                const resp = await fetch(metaUrl, {
                                    method: "GET",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                });
                                if (resp.ok) {
                                    const meta = await resp.json();
                                    isLooker = meta && meta.UsrURL && meta.UsrURL.length > 0;
                                }
                            } catch (e) {
                                console.log("[v21] Metadata check error:", e);
                            }
                        }

                        // SAFE: Set visibility flags
                        try {
                            if (isCommission) {
                                request.$context.UsrShowCommissionFilters = true;
                                request.$context.UsrShowDateFilters = false;
                                request.$context.UsrShowCustomerFilter = false;
                            } else if (isItemsByCustomer) {
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateFilters = true;
                                request.$context.UsrShowCustomerFilter = true;
                            } else if (reportId) {
                                // Other reports (Looker or Excel)
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateFilters = true;
                                request.$context.UsrShowCustomerFilter = false;
                            } else {
                                // No report selected
                                request.$context.UsrShowCommissionFilters = false;
                                request.$context.UsrShowDateFilters = false;
                                request.$context.UsrShowCustomerFilter = false;
                            }
                        } catch (e) {
                            console.log("[v21] Visibility set error:", e);
                        }

                    } catch (e) {
                        console.log("[v21] Attribute change error:", e);
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
                    const bpmcsrf = getBpmcsrf();

                    // --------------------------------------------------------
                    // SAFE: Get selected report
                    // --------------------------------------------------------
                    let selectedReport = null;
                    try {
                        selectedReport = await context.LookupAttribute_0as4io2;
                    } catch (e) {
                        console.log("[v21] Error getting report:", e);
                    }

                    const reportId = safeGetValue(selectedReport);
                    const reportDisplayName = safeGetDisplayValue(selectedReport) || "Report";

                    if (!reportId) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    console.log("[v21] Generating:", reportDisplayName);

                    // --------------------------------------------------------
                    // Fetch report metadata
                    // --------------------------------------------------------
                    let reportUrl = "";
                    let reportCode = "";
                    try {
                        const metaUrl = "/0/odata/UsrReportesPampa(" + reportId + ")?$select=Id,Name,UsrURL,UsrCode";
                        const metaResp = await fetch(metaUrl, {
                            method: "GET",
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
                        console.log("[v21] Metadata error:", e);
                    }

                    // --------------------------------------------------------
                    // LOOKER PATH
                    // --------------------------------------------------------
                    if (reportUrl && reportUrl.length > 0) {
                        console.log("[v21] Opening Looker:", reportDisplayName);
                        window.open(reportUrl, "_blank");
                        Terrasoft.showInformation("Report opened in new tab");
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // EXCEL PATH
                    // --------------------------------------------------------

                    // Find IntExcelReport template
                    let intExcelReportId = null;
                    try {
                        const escapeName = (s) => (s || "").replace(/'/g, "''");
                        const odataUrl = "/0/odata/IntExcelReport?$filter=" +
                            "(IntName eq '" + escapeName(reportDisplayName) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportDisplayName) + "'" +
                            " or IntName eq '" + escapeName(reportCode) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportCode) + "')" +
                            "&$select=Id,IntName&$top=1";

                        const odataResp = await fetch(odataUrl, {
                            method: "GET",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        const odataResult = await odataResp.json();

                        if (odataResult.value && odataResult.value.length > 0) {
                            intExcelReportId = odataResult.value[0].Id;
                            console.log("[v21] Found template:", odataResult.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Template not found: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error: " + e.message);
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // SAFE: Collect filter values
                    // --------------------------------------------------------
                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    let yearMonthId = emptyGuid;
                    let salesGroupId = emptyGuid;
                    let customerName = "";

                    // Commission filters
                    if (reportDisplayName.toLowerCase().includes("commission")) {
                        try {
                            const ym = await context.UsrYearMonth;
                            yearMonthId = safeGetValue(ym) || emptyGuid;
                            if (yearMonthId !== emptyGuid) {
                                console.log("[v21] YearMonth:", safeGetDisplayValue(ym));
                            }
                        } catch (e) {
                            console.log("[v21] YearMonth error:", e);
                        }

                        try {
                            const sg = await context.UsrSalesGroup;
                            salesGroupId = safeGetValue(sg) || emptyGuid;
                            if (salesGroupId !== emptyGuid) {
                                console.log("[v21] SalesGroup:", safeGetDisplayValue(sg));
                            }
                        } catch (e) {
                            console.log("[v21] SalesGroup error:", e);
                        }
                    }

                    // Customer filter
                    if (reportDisplayName.toLowerCase().includes("items by customer")) {
                        try {
                            const cn = await context.UsrCustomerName;
                            customerName = (typeof cn === 'string') ? cn.trim() : "";
                            if (customerName) {
                                console.log("[v21] Customer:", customerName);
                            }
                        } catch (e) {
                            console.log("[v21] Customer error:", e);
                        }
                    }

                    // --------------------------------------------------------
                    // Generate report
                    // --------------------------------------------------------
                    try {
                        Terrasoft.showInformation("Generating report...");

                        const response = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify({
                                ReportId: intExcelReportId,
                                YearMonthId: yearMonthId,
                                SalesRepId: salesGroupId,
                                CustomerName: customerName,
                                CustomerId: emptyGuid,
                                RecordCollection: []
                            })
                        });

                        const result = await response.json();
                        console.log("[v21] Response:", result);

                        if (result && result.success && result.key) {
                            const downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" +
                                result.key + "/" + encodeURIComponent(reportDisplayName);

                            let iframe = document.getElementById("reportDownloadFrame");
                            if (!iframe) {
                                iframe = document.createElement("iframe");
                                iframe.id = "reportDownloadFrame";
                                iframe.style.display = "none";
                                document.body.appendChild(iframe);
                            }
                            iframe.src = downloadUrl;
                            Terrasoft.showInformation("Download starting...");
                        } else {
                            const msg = (result && (result.message || result.errorMessage)) || "Unknown error";
                            Terrasoft.showErrorMessage("Failed: " + msg);
                        }
                    } catch (e) {
                        console.error("[v21] Error:", e);
                        Terrasoft.showErrorMessage("Error: " + (e.message || "Unknown"));
                    }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
