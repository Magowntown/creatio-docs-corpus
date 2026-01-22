/**
 * UsrPage_ebkv9e8 - Child Schema with Report-Based Visibility (v1)
 * Package: BGApp_eykaguu
 *
 * PURPOSE:
 * Extends parent schema (BGlobalLookerStudio) to add:
 * 1. Commission-specific filters (Year-Month, Sales Group)
 * 2. Visibility toggling based on report selection
 * 3. Hybrid report generation (Looker Studio + Excel)
 *
 * VISIBILITY LOGIC:
 * - Commission reports: Show Year-Month, Sales Group, Warning; Hide date filters
 * - Non-Commission: Show date filters; Hide Commission filters
 * - Looker Studio reports: Opens in new tab (bypasses CSP issue)
 *
 * REPORT MAPPING (from UsrReportesPampa):
 * - Excel: Commission, Customers did not buy..., Items by Customer,
 *          Sales By Item, Sales By Item By Type, Sales By Line
 * - Looker: Sales By Customer, Sales By Sales Group, etc. (have UsrURL)
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // ============================================================
            // TOGGLE DATE FILTERS VISIBILITY (from parent schema)
            // When Commission selected, hide these; otherwise show
            // ============================================================
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": {
                    "visible": "$UsrShowDateFilters"
                }
            },
            // Also hide status order for Commission reports
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": {
                    "visible": "$UsrShowDateFilters"
                }
            },
            // Hide iframe container (blocked by CSP anyway)
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            },
            // Wire button to our hybrid handler instead of parent's OpenReport
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "clicked": {
                        "request": "usr.GenerateReportRequest"
                    }
                }
            },
            // ============================================================
            // COMMISSION FILTERS SECTION
            // Only visible when Commission report selected
            // ============================================================
            {
                "operation": "insert",
                "name": "CommissionWarningLabel",
                "values": {
                    "type": "crt.Label",
                    "caption": "Note: Date and transaction info for Commission reports is derived from QuickBooks synced data.",
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
                "index": 1
            },
            {
                "operation": "insert",
                "name": "CommissionFiltersContainer",
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
            {
                "operation": "insert",
                "name": "YearMonthCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Year-Month",
                    "labelPosition": "auto",
                    "control": "$UsrYearMonth",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select year-month...",
                    "layoutConfig": {
                        "column": 1,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": "",
                    "required": true
                },
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },
            {
                "operation": "insert",
                "name": "SalesGroupCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "auto",
                    "control": "$UsrSalesGroup",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select sales group...",
                    "layoutConfig": {
                        "column": 2,
                        "row": 1,
                        "colSpan": 1,
                        "rowSpan": 1
                    },
                    "visible": true,
                    "tooltip": "",
                    "required": true,
                    "mode": "List"
                },
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,
        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    // Visibility control attributes (declare as empty objects for Freedom UI reactivity)
                    "UsrShowCommissionFilters": {},
                    "UsrShowDateFilters": {},
                    // Commission filter lookups
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
                    // List config for Sales Group dropdown sorting
                    "UsrSalesGroup_List": {
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
            // Initialize visibility states on page load
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    // Default: Show date filters, hide Commission filters
                    request.$context.UsrShowCommissionFilters = false;
                    request.$context.UsrShowDateFilters = true;
                    console.log("[UsrPage_ebkv9e8] Page initialized - default visibility set");
                    return next?.handle(request);
                }
            },
            // Toggle visibility based on report selection
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    // React to the PARENT's report dropdown (LookupAttribute_0as4io2)
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_0as4io2;

                        let isCommissionReport = false;
                        if (selectedReport && selectedReport.displayValue) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            isCommissionReport = reportName.includes("commission");

                            // Clear Commission filter values when switching reports
                            if (isCommissionReport) {
                                // Keep values if switching TO Commission
                            } else {
                                // Clear Commission filters when switching AWAY from Commission
                                request.$context.UsrYearMonth = null;
                                request.$context.UsrSalesGroup = null;
                            }
                        }

                        // Toggle visibility
                        request.$context.UsrShowCommissionFilters = isCommissionReport;
                        request.$context.UsrShowDateFilters = !isCommissionReport;

                        console.log("[UsrPage_ebkv9e8] Report selected:",
                            selectedReport?.displayValue || "(none)",
                            "| Commission:", isCommissionReport,
                            "| ShowDateFilters:", !isCommissionReport);
                    }
                    return next?.handle(request);
                }
            },
            // Hybrid report generation handler
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    const context = request.$context;

                    // Get the selected report from PARENT's attribute
                    const selectedReport = await context.LookupAttribute_0as4io2;
                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const reportId = selectedReport.value;
                    let reportName = selectedReport.displayValue || "";

                    // Helper function to get BPMCSRF token
                    const getCookie = function(name) {
                        var value = "; " + document.cookie;
                        var parts = value.split("; " + name + "=");
                        if (parts.length === 2) return parts.pop().split(";").shift();
                        return "";
                    };
                    const bpmcsrf = getCookie("BPMCSRF");

                    // Fetch report metadata to check for Looker URL and get UsrCode
                    let reportUrl = "";
                    let reportCode = "";
                    try {
                        const metaUrl = "/0/odata/UsrReportesPampa(" + reportId + ")?$select=Id,Name,UsrURL,UsrCode";
                        const metaResp = await fetch(metaUrl, {
                            method: "GET",
                            headers: {"Content-Type": "application/json", "BPMCSRF": bpmcsrf}
                        });
                        if (metaResp.ok) {
                            const meta = await metaResp.json();
                            reportName = meta.Name || reportName;
                            reportUrl = meta.UsrURL || "";
                            reportCode = meta.UsrCode || "";
                            console.log("[UsrPage_ebkv9e8] Report metadata:", {name: reportName, code: reportCode, hasUrl: !!reportUrl});
                        }
                    } catch (e) {
                        console.log("[UsrPage_ebkv9e8] Metadata lookup error:", e);
                    }

                    // DECISION: Looker Studio (new tab) vs Excel (service)
                    if (reportUrl && reportUrl.length > 0) {
                        // LOOKER STUDIO PATH
                        // Convert embed URL to direct viewing URL
                        var viewUrl = reportUrl
                            .replace("/embed/u/0/", "/u/0/")
                            .replace("/embed/", "/u/0/");

                        console.log("[UsrPage_ebkv9e8] Opening Looker Studio:", viewUrl);
                        window.open(viewUrl, "_blank");
                        Terrasoft.showInformation("Opening report in new tab...");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[UsrPage_ebkv9e8] Using Excel service for:", reportName);

                    // Get Commission filter values
                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    let yearMonthId = emptyGuid;
                    let salesGroupId = emptyGuid;

                    try {
                        const yearMonth = await context.UsrYearMonth;
                        if (yearMonth && yearMonth.value) {
                            yearMonthId = yearMonth.value;
                        }
                    } catch (e) { /* Optional filter */ }

                    try {
                        const salesGroup = await context.UsrSalesGroup;
                        if (salesGroup && salesGroup.value) {
                            salesGroupId = salesGroup.value;
                        }
                    } catch (e) { /* Optional filter */ }

                    // Find matching IntExcelReport template
                    let intExcelReportId = null;
                    try {
                        const escapeName = function(s) { return s.replace(/'/g, "''"); };
                        // Try multiple name patterns
                        const odataUrl = "/0/odata/IntExcelReport?$filter=" +
                            "(IntName eq '" + escapeName(reportName) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportName) + "'" +
                            " or IntName eq '" + escapeName(reportCode) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportCode) + "')" +
                            "&$select=Id,IntName&$top=1";

                        const resp = await fetch(odataUrl, {
                            method: "GET",
                            headers: {"Content-Type": "application/json", "BPMCSRF": bpmcsrf}
                        });

                        const result = await resp.json();
                        if (result.value && result.value.length > 0) {
                            intExcelReportId = result.value[0].Id;
                            console.log("[UsrPage_ebkv9e8] Found template:", result.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    // Call UsrExcelReportService
                    try {
                        Terrasoft.showInformation("Generating report...");

                        const genResp = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: {"Content-Type": "application/json", "BPMCSRF": bpmcsrf},
                            body: JSON.stringify({
                                ReportId: intExcelReportId,
                                YearMonthId: yearMonthId,
                                SalesRepId: salesGroupId
                            })
                        });

                        const result = await genResp.json();
                        console.log("[UsrPage_ebkv9e8] Service response:", result);

                        if (result.success && result.key) {
                            // Download using hidden iframe
                            const downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" +
                                result.key + "/" + encodeURIComponent(reportName || "Report");

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
                            const errorMsg = result.message || result.errorMessage || "Unknown error";
                            Terrasoft.showErrorMessage("Report generation failed: " + errorMsg);
                        }
                    } catch (error) {
                        console.error("[UsrPage_ebkv9e8] Error:", error);
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
