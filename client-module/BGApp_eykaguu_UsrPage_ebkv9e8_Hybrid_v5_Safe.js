/**
 * UsrPage_ebkv9e8 - Hybrid Handler v5 (Safe/Non-Destructive)
 *
 * DESIGN PRINCIPLE: Do NOT remove or hide any existing UI elements.
 * Only ADD Commission-specific filters and wire the Report button.
 *
 * For Commission reports: Show Year-Month and Sales Group filters
 * For other reports: Original filters (Status, dates) remain visible and functional
 *
 * v5 Changes from v4:
 * - Uses SAME attribute names as v2 (LookupAttribute_yubshr1, LookupAttribute_nt0mer7)
 * - Uses v2's report selector (LookupAttribute_bsixu8a) for consistency
 * - Removes the destructive "remove" operations from v2
 * - Keeps Status filter and date filters visible
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // ========================================
            // MINIMAL CHANGES - DON'T BREAK EXISTING UI
            // ========================================

            // Hide Looker Studio iframe (CSP blocks it anyway)
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            },

            // Wire report button to our hybrid handler
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "clicked": {
                        "request": "usr.GenerateReportRequest"
                    }
                }
            },

            // ========================================
            // COMMISSION-SPECIFIC FILTERS (Added, not replacing)
            // ========================================

            // Warning label for Commission reports
            {
                "operation": "insert",
                "name": "BGCommissionWarning",
                "values": {
                    "type": "crt.Label",
                    "caption": "Commission reports use QuickBooks synced data. Select Year-Month and Sales Group below.",
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
                "index": 3
            },

            // Commission filter container
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
                "index": 4
            },

            // Year-Month filter (Commission only) - uses v2 attribute name
            {
                "operation": "insert",
                "name": "BGYearMonth",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Year-Month",
                    "labelPosition": "auto",
                    "control": "$LookupAttribute_yubshr1",
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
                    "tooltip": ""
                },
                "parentName": "GridContainer_CommissionFilters",
                "propertyName": "items",
                "index": 0
            },

            // Sales Group filter (Commission only) - uses v2 attribute name
            {
                "operation": "insert",
                "name": "BGSalesGroup",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "auto",
                    "control": "$LookupAttribute_nt0mer7",
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
                    "tooltip": "",
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
                    // Commission filter visibility flag
                    "UsrShowCommissionFilters": {
                        "value": false
                    },
                    // Use SAME attribute names as v2 for compatibility
                    "LookupAttribute_nt0mer7": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGSalesGroup"
                        }
                    },
                    "LookupAttribute_yubshr1": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGYearMonth"
                        }
                    },
                    "LookupAttribute_nt0mer7_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [
                                    {
                                        "columnName": "BGSalesGroupName",
                                        "direction": "asc"
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        ]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // ========================================
            // REPORT SELECTION CHANGE HANDLER
            // Listen for the ORIGINAL report selector (from parent)
            // ========================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    // Listen for the original report selector attribute
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_0as4io2;

                        if (selectedReport && selectedReport.displayValue) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission");

                            // Show/hide Commission filters based on report type
                            request.$context.UsrShowCommissionFilters = isCommissionReport;

                            // Clear Commission filter values when switching reports
                            if (isCommissionReport) {
                                request.$context.LookupAttribute_yubshr1 = null;
                                request.$context.LookupAttribute_nt0mer7 = null;
                            }

                            console.log("[UsrPage_ebkv9e8] Report selected:", reportName,
                                "| Commission filters:", isCommissionReport ? "VISIBLE" : "HIDDEN");
                        } else {
                            request.$context.UsrShowCommissionFilters = false;
                        }
                    }

                    return next?.handle(request);
                }
            },

            // ========================================
            // HYBRID REPORT GENERATION HANDLER
            // ========================================
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    const context = request.$context;

                    // Get selected report from ORIGINAL selector (parent's)
                    const selectedReport = await context.LookupAttribute_0as4io2;
                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    let reportDisplayName = selectedReport.displayValue || "";

                    // Get BPMCSRF token
                    const getCookie = function(name) {
                        var value = "; " + document.cookie;
                        var parts = value.split("; " + name + "=");
                        if (parts.length === 2) return parts.pop().split(";").shift();
                        return "";
                    };
                    const bpmcsrf = getCookie("BPMCSRF");

                    // Fetch report metadata
                    let reportUrl = "";
                    let reportCode = "";
                    try {
                        const reportMetaUrl = "/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=Id,Name,UsrURL,UsrCode";
                        const reportMetaResp = await fetch(reportMetaUrl, {
                            method: "GET",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (reportMetaResp.ok) {
                            const reportMeta = await reportMetaResp.json();
                            reportDisplayName = reportMeta.Name || reportDisplayName;
                            reportUrl = reportMeta.UsrURL || "";
                            reportCode = reportMeta.UsrCode || "";
                        }
                    } catch (e) {
                        console.log("[UsrPage_ebkv9e8] Metadata lookup failed:", e);
                    }

                    // DECISION: Looker Studio (new tab) vs Excel (service)
                    if (reportUrl && reportUrl.length > 0) {
                        // ===== LOOKER STUDIO PATH =====
                        var viewUrl = reportUrl.replace("/embed/u/0/", "/u/0/").replace("/embed/", "/u/0/");
                        console.log("[UsrPage_ebkv9e8] Opening Looker Studio:", viewUrl);
                        window.open(viewUrl, "_blank");
                        Terrasoft.showInformation("Opening report in new tab...");
                        return next?.handle(request);
                    }

                    // ===== EXCEL PATH =====
                    console.log("[UsrPage_ebkv9e8] Using Excel service for:", reportDisplayName);

                    // Determine if this is a Commission report
                    const isCommissionReport = reportDisplayName.toLowerCase().includes("commission");

                    // Get filter values
                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;

                    if (isCommissionReport) {
                        // Commission reports use our custom filters (v2 attribute names)
                        try {
                            const yearMonth = await context.LookupAttribute_yubshr1;
                            if (yearMonth && yearMonth.value) {
                                yearMonthId = yearMonth.value;
                            }
                        } catch (e) {}

                        try {
                            const salesGroup = await context.LookupAttribute_nt0mer7;
                            if (salesGroup && salesGroup.value) {
                                salesGroupId = salesGroup.value;
                            }
                        } catch (e) {}
                    }

                    // Find IntExcelReport
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
                        } else {
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    // Call UsrExcelReportService
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
                        console.log("[UsrPage_ebkv9e8] Service response:", result);

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
                        console.error("[UsrPage_ebkv9e8] Error:", error);
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
