/**
 * UsrPage_ebkv9e8 - Hybrid Handler v7 (with initialization)
 *
 * v7 Changes from v6:
 * - Added crt.HandleViewModelInitRequest handler to initialize UsrShowCommissionFilters=false on page load
 * - This ensures Commission filters are hidden until a Commission report is selected
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Hide parent's original report container (we use our own)
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": {
                    "visible": false
                }
            },
            // Remove original report combo from parent (we create our own)
            {
                "operation": "remove",
                "name": "ComboBox_bo00lsk"
            },
            // Date filters VISIBLE for non-Commission reports
            {
                "operation": "merge",
                "name": "CreatedFrom",
                "values": {
                    "visible": true,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "CreatedTo",
                "values": {
                    "visible": true,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "ShippingFrom",
                "values": {
                    "visible": true,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "ShippingTo",
                "values": {
                    "visible": true,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "DeliveryFrom",
                "values": {
                    "visible": true,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "DeliveryTo",
                "values": {
                    "visible": true,
                    "layoutConfig": {}
                }
            },
            // Hide iframe container (Looker Studio - blocked by CSP anyway)
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
                    "visible": true,
                    "clicked": {
                        "request": "usr.GenerateReportRequest"
                    }
                }
            },
            // Add container for report selection
            {
                "operation": "insert",
                "name": "GridContainer_amm2zmo",
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
                    "visible": true,
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
                "index": 0
            },
            // Report selection combo
            {
                "operation": "insert",
                "name": "BGPampaReport",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Report",
                    "labelPosition": "auto",
                    "control": "$LookupAttribute_bsixu8a",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select a report...",
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": ""
                },
                "parentName": "GridContainer_amm2zmo",
                "propertyName": "items",
                "index": 0
            },
            // Warning label for Commission reports - CONDITIONAL
            {
                "operation": "insert",
                "name": "BGWarningLabel",
                "values": {
                    "type": "crt.Label",
                    "caption": "Date and transaction info derived from QuickBooks synced data.",
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
            // Filter fields container (for Commission reports) - CONDITIONAL
            {
                "operation": "insert",
                "name": "GridContainer_3asa01r",
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
                "index": 2
            },
            // Year-Month field
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
                    "placeholder": "",
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": ""
                },
                "parentName": "GridContainer_3asa01r",
                "propertyName": "items",
                "index": 0
            },
            // Sales Group field
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
                    "placeholder": "",
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
                "parentName": "GridContainer_3asa01r",
                "propertyName": "items",
                "index": 1
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,
        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    "UsrShowCommissionFilters": {
                        "value": false
                    },
                    "LookupAttribute_bsixu8a": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGPampaReport"
                        }
                    },
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
            // v7: Initialize Commission filters visibility on page load
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    // Ensure Commission filters are hidden by default
                    request.$context.UsrShowCommissionFilters = false;
                    console.log("[UsrPage_ebkv9e8] Page initialized - Commission filters HIDDEN");
                    return next?.handle(request);
                }
            },
            // Handle report selection change - show/hide Commission filters
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_bsixu8a" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_bsixu8a;

                        if (selectedReport && selectedReport.displayValue) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission");
                            request.$context.UsrShowCommissionFilters = isCommissionReport;
                            request.$context.LookupAttribute_yubshr1 = null;
                            request.$context.LookupAttribute_nt0mer7 = null;
                            console.log("[UsrPage_ebkv9e8] Report selected:", reportName,
                                "| Commission filters:", isCommissionReport ? "VISIBLE" : "HIDDEN");
                        } else {
                            request.$context.UsrShowCommissionFilters = false;
                        }
                    }

                    return next?.handle(request);
                }
            },
            // HYBRID Report generation handler
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    const context = request.$context;

                    // Get selected report
                    const selectedReport = await context.LookupAttribute_bsixu8a;
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
                        var viewUrl = reportUrl.replace("/embed/u/0/", "/u/0/").replace("/embed/", "/u/0/");
                        console.log("[UsrPage_ebkv9e8] Opening Looker Studio:", viewUrl);
                        window.open(viewUrl, "_blank");
                        Terrasoft.showInformation("Opening report in new tab...");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[UsrPage_ebkv9e8] Using Excel service for:", reportDisplayName);

                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;

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
