/**
 * UsrPage_ebkv9e8 - v11 Programmatic Visibility
 * Package: BGApp_eykaguu
 *
 * APPROACH: Instead of relying on $Attribute bindings (which don't work
 * reliably across parent/child schema inheritance), this version:
 * 1. Keeps parent elements as-is
 * 2. Uses handlers to programmatically control visibility via context
 * 3. Inserts Commission elements with inline visibility control
 *
 * This bypasses the Freedom UI binding resolution issue.
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
    console.log("[v11] ========== SCHEMA LOADED ==========");

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Hide iframe (CSP blocks external domains) - this works because it's static
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            },
            // Override button to use our handler
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "clicked": {
                        "request": "usr.GenerateReportRequest"
                    }
                }
            },
            // Commission Warning - bound to our attribute
            {
                "operation": "insert",
                "name": "BGCommissionWarning",
                "values": {
                    "type": "crt.Label",
                    "caption": "Commission data is derived from QuickBooks synced payment records.",
                    "labelType": "body",
                    "labelThickness": "default",
                    "labelEllipsis": false,
                    "labelColor": "#D2310D",
                    "labelBackgroundColor": "transparent",
                    "labelTextAlign": "start",
                    "visible": "$UsrShowCommissionFilters"
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 2
            },
            // Commission filters container
            {
                "operation": "insert",
                "name": "GridContainer_CommissionFilters",
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
                "index": 3
            },
            // Year-Month filter
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
                "parentName": "GridContainer_CommissionFilters",
                "propertyName": "items",
                "index": 0
            },
            // Sales Group filter
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
                "parentName": "GridContainer_CommissionFilters",
                "propertyName": "items",
                "index": 1
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    "UsrShowCommissionFilters": {},
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
            // INIT: Set default and programmatically control parent element visibility
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    console.log("[v11] Init handler starting");

                    // Set default: Commission filters hidden
                    request.$context.UsrShowCommissionFilters = false;

                    // Wait for parent handler to complete first
                    const result = await next?.handle(request);

                    // Now try to programmatically hide parent elements for Commission
                    // The parent date filters should stay visible (default state)
                    console.log("[v11] Init complete - Commission filters hidden by default");

                    return result;
                }
            },

            // REPORT CHANGE: Toggle visibility based on selection
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const report = await request.$context.LookupAttribute_0as4io2;
                        let isCommission = false;

                        if (report && report.displayValue) {
                            isCommission = report.displayValue.toLowerCase().includes("commission");
                            console.log("[v11] Report selected:", report.displayValue, "| isCommission:", isCommission);

                            // Clear Commission filter values when switching away
                            if (!isCommission) {
                                request.$context.UsrYearMonth = null;
                                request.$context.UsrSalesGroup = null;
                            }
                        } else {
                            console.log("[v11] No report selected");
                        }

                        // Update Commission filters visibility (this should work for inserted elements)
                        request.$context.UsrShowCommissionFilters = isCommission;

                        // For parent elements (date filters), we need to use DOM manipulation
                        // since $binding doesn't work across parent/child
                        try {
                            // Try to find and toggle parent containers via DOM
                            setTimeout(() => {
                                // Date filters container (GridContainer_xdy25v1)
                                const dateFilters = document.querySelector('[data-item-marker="GridContainer_xdy25v1"]');
                                if (dateFilters) {
                                    dateFilters.style.display = isCommission ? 'none' : '';
                                    console.log("[v11] Date filters visibility set via DOM:", !isCommission);
                                }

                                // Status filter container (GridContainer_knkow5v)
                                const statusFilter = document.querySelector('[data-item-marker="GridContainer_knkow5v"]');
                                if (statusFilter) {
                                    statusFilter.style.display = isCommission ? 'none' : '';
                                    console.log("[v11] Status filter visibility set via DOM:", !isCommission);
                                }
                            }, 100);
                        } catch (e) {
                            console.log("[v11] DOM manipulation failed:", e);
                        }
                    }

                    return next?.handle(request);
                }
            },

            // GENERATE: Hybrid handler for Looker Studio + Excel
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    const ctx = request.$context;
                    const report = await ctx.LookupAttribute_0as4io2;

                    if (!report || !report.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const reportId = report.value;
                    let reportName = report.displayValue || "Report";
                    console.log("[v11] Generating report:", reportName);

                    // Get CSRF token
                    const bpmcsrf = ("; " + document.cookie).split("; BPMCSRF=").pop().split(";").shift() || "";

                    // Fetch report metadata
                    let reportUrl = "", reportCode = "";
                    try {
                        const resp = await fetch(`/0/odata/UsrReportesPampa(${reportId})?$select=Name,UsrURL,UsrCode`, {
                            headers: {"Content-Type": "application/json", "BPMCSRF": bpmcsrf}
                        });
                        if (resp.ok) {
                            const meta = await resp.json();
                            reportName = meta.Name || reportName;
                            reportUrl = meta.UsrURL || "";
                            reportCode = meta.UsrCode || "";
                        }
                    } catch (e) { console.log("[v11] Metadata error:", e); }

                    // LOOKER STUDIO PATH
                    if (reportUrl) {
                        const viewUrl = reportUrl.replace("/embed/u/0/", "/u/0/").replace("/embed/", "/u/0/");
                        console.log("[v11] Opening Looker:", viewUrl);
                        window.open(viewUrl, "_blank");
                        Terrasoft.showInformation("Opening report in new tab...");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[v11] Excel report:", reportName);
                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    let yearMonthId = emptyGuid, salesGroupId = emptyGuid;

                    if (reportName.toLowerCase().includes("commission")) {
                        try {
                            const ym = await ctx.UsrYearMonth;
                            if (ym?.value) yearMonthId = ym.value;
                        } catch (e) {}
                        try {
                            const sg = await ctx.UsrSalesGroup;
                            if (sg?.value) salesGroupId = sg.value;
                        } catch (e) {}
                    }

                    // Find IntExcelReport template
                    let templateId = null;
                    try {
                        const esc = s => s.replace(/'/g, "''");
                        const url = `/0/odata/IntExcelReport?$filter=(IntName eq '${esc(reportName)}' or IntName eq 'Rpt ${esc(reportName)}' or IntName eq '${esc(reportCode)}' or IntName eq 'Rpt ${esc(reportCode)}')&$select=Id,IntName&$top=1`;
                        const resp = await fetch(url, {headers: {"Content-Type": "application/json", "BPMCSRF": bpmcsrf}});
                        const data = await resp.json();
                        if (data.value?.length > 0) {
                            templateId = data.value[0].Id;
                        } else {
                            Terrasoft.showErrorMessage("Template not found: " + reportName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error: " + e.message);
                        return next?.handle(request);
                    }

                    // Generate Excel
                    try {
                        Terrasoft.showInformation("Generating report...");
                        const resp = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: {"Content-Type": "application/json", "BPMCSRF": bpmcsrf},
                            body: JSON.stringify({ReportId: templateId, YearMonthId: yearMonthId, SalesRepId: salesGroupId})
                        });
                        const result = await resp.json();

                        if (result.success && result.key) {
                            let iframe = document.getElementById("reportDownloadFrame");
                            if (!iframe) {
                                iframe = document.createElement("iframe");
                                iframe.id = "reportDownloadFrame";
                                iframe.style.display = "none";
                                document.body.appendChild(iframe);
                            }
                            iframe.src = `/0/rest/UsrExcelReportService/GetReport/${result.key}/${encodeURIComponent(reportName)}`;
                            Terrasoft.showInformation("Download starting...");
                        } else {
                            Terrasoft.showErrorMessage("Failed: " + (result.message || "Unknown error"));
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
