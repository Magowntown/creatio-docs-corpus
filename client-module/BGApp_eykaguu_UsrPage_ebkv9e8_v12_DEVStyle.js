/**
 * UsrPage_ebkv9e8 - v12 DEV-Style Handler
 * Package: BGApp_eykaguu
 *
 * APPROACH: Follow DEV's IWQBIntegration pattern exactly:
 * 1. Hide/Remove parent elements (no dynamic binding on parent elements)
 * 2. Insert new elements with bindings declared in THIS schema
 * 3. Use handler to toggle UsrShowCommissionFilters
 *
 * VISIBILITY RULES:
 * - Date filters: HIDDEN permanently (not needed for current reports)
 * - Status filter: REMOVED permanently
 * - Commission filters: Conditional via $UsrShowCommissionFilters
 * - Warning label: Conditional via $UsrShowCommissionFilters
 *
 * NOTE: Uses LookupAttribute_0as4io2 (PROD's attribute name, not DEV's LookupAttribute_bsixu8a)
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // ================================================================
            // HIDE/REMOVE PARENT ELEMENTS (hard-coded, no dynamic binding)
            // ================================================================

            // Hide parent's report dropdown container
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": {
                    "visible": false
                }
            },
            // Hide parent's date filters
            {
                "operation": "merge",
                "name": "CreatedFrom",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "CreatedTo",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "ShippingFrom",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "ShippingTo",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "DeliveryFrom",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            {
                "operation": "merge",
                "name": "DeliveryTo",
                "values": {
                    "visible": false,
                    "layoutConfig": {}
                }
            },
            // Remove status filter container
            {
                "operation": "remove",
                "name": "GridContainer_knkow5v"
            },
            // Hide iframe container (CSP blocks external domains)
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            },
            // Wire Generate button to our handler
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

            // ================================================================
            // INSERT NEW ELEMENTS (with bindings in THIS schema)
            // ================================================================

            // New report selector container (always visible)
            {
                "operation": "insert",
                "name": "BGReportContainer",
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
            // New report dropdown
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
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": ""
                },
                "parentName": "BGReportContainer",
                "propertyName": "items",
                "index": 0
            },
            // Warning label (conditional - Commission only)
            {
                "operation": "insert",
                "name": "BGWarningLabel",
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
            // Commission filters container (conditional)
            {
                "operation": "insert",
                "name": "BGCommissionFiltersContainer",
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
                "parentName": "BGCommissionFiltersContainer",
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
                "parentName": "BGCommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    // Visibility attribute - matches DEV's pattern
                    "UsrShowCommissionFilters": {
                        "value": false
                    },
                    // Commission filter bindings
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
            // Report selection handler - toggle Commission filters
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_0as4io2;
                        if (selectedReport && selectedReport.displayValue) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission");
                            request.$context.UsrShowCommissionFilters = isCommissionReport;
                            // Clear filter values when switching reports
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;
                            console.log("[v12] Report:", selectedReport.displayValue, "| Commission:", isCommissionReport);
                        } else {
                            request.$context.UsrShowCommissionFilters = false;
                        }
                    }
                    return next?.handle(request);
                }
            },
            // Hybrid report generation handler (Looker Studio + Excel)
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    const context = request.$context;
                    const selectedReport = await context.LookupAttribute_0as4io2;

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    let reportDisplayName = selectedReport.displayValue || "";

                    // Get CSRF token
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
                            console.log("[v12] Report metadata:", reportDisplayName, "URL:", reportUrl ? "YES" : "NO");
                        }
                    } catch (e) {
                        console.log("[v12] Metadata lookup failed:", e);
                    }

                    // LOOKER STUDIO PATH
                    if (reportUrl && reportUrl.length > 0) {
                        var viewUrl = reportUrl.replace("/embed/u/0/", "/u/0/").replace("/embed/", "/u/0/");
                        console.log("[v12] Opening Looker Studio in new tab:", viewUrl);
                        window.open(viewUrl, "_blank");
                        Terrasoft.showInformation("Opening report in new tab...");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[v12] No Looker URL, using Excel service for:", reportDisplayName);

                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    var yearMonthId = emptyGuid;
                    var salesGroupId = emptyGuid;

                    // Get Commission filter values if applicable
                    if (reportDisplayName.toLowerCase().includes("commission")) {
                        try {
                            const yearMonth = await context.UsrYearMonth;
                            if (yearMonth && yearMonth.value) {
                                yearMonthId = yearMonth.value;
                            }
                        } catch (e) {}
                        try {
                            const salesGroup = await context.UsrSalesGroup;
                            if (salesGroup && salesGroup.value) {
                                salesGroupId = salesGroup.value;
                            }
                        } catch (e) {}
                    }

                    // Find IntExcelReport template
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
                            console.log("[v12] Found IntExcelReport:", odataResult.value[0].IntName, "->", intExcelReportId);
                        } else {
                            Terrasoft.showErrorMessage("Excel report template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding report template: " + e.message);
                        return next?.handle(request);
                    }

                    // Generate Excel report
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
                        console.log("[v12] UsrExcelReportService response:", result);

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
                            Terrasoft.showInformation("Report generated - download starting...");
                        } else {
                            var errorMsg = result.message || result.errorMessage || "Unknown error";
                            Terrasoft.showErrorMessage("Failed to generate report: " + errorMsg);
                        }
                    } catch (error) {
                        console.error("[v12] Error:", error);
                        Terrasoft.showErrorMessage("Error generating report: " + error.message);
                    }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
