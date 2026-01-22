/**
 * UsrPage_ebkv9e8 - Child Schema with Report-Based Visibility (v2)
 * Package: BGApp_eykaguu
 *
 * EXTENDS: BGlobalLookerStudio parent schema
 *
 * PURPOSE:
 * 1. Add Commission-specific filters (Year-Month, Sales Group)
 * 2. Toggle filter visibility based on report selection
 * 3. Override report generation to support both Looker Studio and Excel
 *
 * PARENT SCHEMA ELEMENTS USED:
 * - LookupAttribute_0as4io2 → UsrReporte (report dropdown)
 * - GridContainer_xdy25v1 (date filters container)
 * - GridContainer_knkow5v (status order filter container)
 * - Button_vae0g6x (generate report button)
 * - GridContainer_fh039aq (iframe container - CSP blocked)
 *
 * VISIBILITY LOGIC:
 * - Commission reports: Show Year-Month, Sales Group, Warning; Hide date filters
 * - Non-Commission: Show date filters; Hide Commission filters
 * - Looker Studio reports: Open in new tab (bypass CSP)
 *
 * DEPLOYMENT: https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {
    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // ================================================================
            // PARENT ELEMENT MODIFICATIONS
            // ================================================================

            // Toggle date filters visibility (parent's container)
            // Hide for Commission, show for non-Commission
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": {
                    "visible": "$UsrShowDateFilters"
                }
            },
            // Toggle status order filter visibility
            // Hide for Commission, show for non-Commission
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": {
                    "visible": "$UsrShowDateFilters"
                }
            },
            // Hide iframe container (blocked by CSP in Freedom UI)
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            },
            // Override button to use our hybrid handler
            {
                "operation": "merge",
                "name": "Button_vae0g6x",
                "values": {
                    "clicked": {
                        "request": "usr.HybridGenerateReport"
                    }
                }
            },

            // ================================================================
            // NEW COMMISSION ELEMENTS
            // ================================================================

            // Warning label - shown only for Commission reports
            {
                "operation": "insert",
                "name": "CommissionWarningLabel",
                "values": {
                    "type": "crt.Label",
                    "caption": "Note: Commission report data is derived from QuickBooks synced payment records.",
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
            // Commission filters container
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
            // Year-Month filter
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
                    "tooltip": "Required for Commission reports"
                },
                "parentName": "CommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },
            // Sales Group filter
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
                    "tooltip": "Required for Commission reports",
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
                    // Visibility control attributes
                    // Empty object {} allows Freedom UI to track changes reactively
                    "UsrShowCommissionFilters": {},
                    "UsrShowDateFilters": {},

                    // Commission filter lookup bindings
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
                    // Sorting for Sales Group dropdown
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
            // ================================================================
            // INITIALIZATION HANDLER
            // Set default visibility states on page load
            // ================================================================
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    // Default: Show date filters, hide Commission filters
                    request.$context.UsrShowCommissionFilters = false;
                    request.$context.UsrShowDateFilters = true;

                    console.log("[UsrPage_ebkv9e8 v2] Initialized - Date filters visible, Commission filters hidden");
                    return next?.handle(request);
                }
            },

            // ================================================================
            // REPORT SELECTION CHANGE HANDLER
            // Toggle visibility based on selected report type
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    // React to parent's report dropdown changes
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_0as4io2;

                        let isCommissionReport = false;
                        let reportName = "(none)";

                        if (selectedReport && selectedReport.displayValue) {
                            reportName = selectedReport.displayValue;
                            // Check if this is a Commission report
                            isCommissionReport = reportName.toLowerCase().includes("commission");

                            // Clear Commission filter values when switching away from Commission
                            if (!isCommissionReport) {
                                request.$context.UsrYearMonth = null;
                                request.$context.UsrSalesGroup = null;
                            }
                        }

                        // Update visibility attributes
                        request.$context.UsrShowCommissionFilters = isCommissionReport;
                        request.$context.UsrShowDateFilters = !isCommissionReport;

                        console.log("[UsrPage_ebkv9e8 v2] Report selected:", reportName,
                            "| Commission:", isCommissionReport);
                    }

                    return next?.handle(request);
                }
            },

            // ================================================================
            // HYBRID REPORT GENERATION HANDLER
            // Routes to Looker Studio (new tab) or Excel service based on report config
            // ================================================================
            {
                request: "usr.HybridGenerateReport",
                handler: async (request, next) => {
                    const context = request.$context;

                    // Get selected report from parent's dropdown
                    const selectedReport = await context.LookupAttribute_0as4io2;
                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const reportId = selectedReport.value;
                    let reportName = selectedReport.displayValue || "Report";

                    console.log("[UsrPage_ebkv9e8 v2] Generating report:", reportName, "ID:", reportId);

                    // Get BPMCSRF token
                    const getCookie = function(name) {
                        var value = "; " + document.cookie;
                        var parts = value.split("; " + name + "=");
                        if (parts.length === 2) return parts.pop().split(";").shift();
                        return "";
                    };
                    const bpmcsrf = getCookie("BPMCSRF");

                    // Fetch report metadata (URL and Code)
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
                        }
                    } catch (e) {
                        console.log("[UsrPage_ebkv9e8 v2] Metadata error:", e);
                    }

                    // DECISION: Looker Studio vs Excel
                    if (reportUrl && reportUrl.length > 0) {
                        // ============================================
                        // LOOKER STUDIO PATH - Open in new tab
                        // ============================================

                        // Convert embed URL to direct viewing URL
                        var viewUrl = reportUrl
                            .replace("/embed/u/0/", "/u/0/")
                            .replace("/embed/", "/u/0/");

                        // Build filter parameters from date filters
                        var params = "";
                        var addedFilter = false;

                        const buildDateParam = function(attr, fieldName, op) {
                            const val = context.attributes[attr];
                            if (val) {
                                const dateStr = val.getFullYear() + "-" +
                                    String(val.getMonth() + 1).padStart(2, "0") + "-" +
                                    String(val.getDate()).padStart(2, "0") + "T00:00:00.0-00:00";
                                return (addedFilter ? " and " : "") + fieldName + " " + op + " " + dateStr;
                            }
                            return "";
                        };

                        // Add date filter params
                        var filterParts = [];
                        if (context.attributes.CreatedFrom) {
                            filterParts.push("CreatedOn ge " + buildDateParam("CreatedFrom", "CreatedOn", "ge").split(" ge ")[1]);
                        }
                        if (context.attributes.CreatedTo) {
                            filterParts.push("CreatedOn le " + buildDateParam("CreatedTo", "CreatedOn", "le").split(" le ")[1]);
                        }
                        // Add more date filters as needed...

                        if (filterParts.length > 0) {
                            params = '?params=%7B"ds0.additionalFilters":"' + filterParts.join(" and ") + '","ds0.top":"1000000"%7D';
                        }

                        console.log("[UsrPage_ebkv9e8 v2] Opening Looker Studio:", viewUrl);
                        window.open(viewUrl + params, "_blank");
                        Terrasoft.showInformation("Opening report in new browser tab...");

                        return next?.handle(request);
                    }

                    // ============================================
                    // EXCEL PATH - Use UsrExcelReportService
                    // ============================================

                    console.log("[UsrPage_ebkv9e8 v2] Using Excel service for:", reportName);

                    // Get Commission filter values
                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    let yearMonthId = emptyGuid;
                    let salesGroupId = emptyGuid;

                    try {
                        const yearMonth = await context.UsrYearMonth;
                        if (yearMonth && yearMonth.value) {
                            yearMonthId = yearMonth.value;
                        }
                    } catch (e) { /* Optional */ }

                    try {
                        const salesGroup = await context.UsrSalesGroup;
                        if (salesGroup && salesGroup.value) {
                            salesGroupId = salesGroup.value;
                        }
                    } catch (e) { /* Optional */ }

                    // Find IntExcelReport template by name
                    let intExcelReportId = null;
                    try {
                        const escapeName = function(s) { return s.replace(/'/g, "''"); };
                        const searchUrl = "/0/odata/IntExcelReport?$filter=" +
                            "(IntName eq '" + escapeName(reportName) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportName) + "'" +
                            " or IntName eq '" + escapeName(reportCode) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportCode) + "')" +
                            "&$select=Id,IntName&$top=1";

                        const searchResp = await fetch(searchUrl, {
                            method: "GET",
                            headers: {"Content-Type": "application/json", "BPMCSRF": bpmcsrf}
                        });

                        const searchResult = await searchResp.json();
                        if (searchResult.value && searchResult.value.length > 0) {
                            intExcelReportId = searchResult.value[0].Id;
                            console.log("[UsrPage_ebkv9e8 v2] Found template:", searchResult.value[0].IntName);
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
                        Terrasoft.showInformation("Generating Excel report...");

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
                        console.log("[UsrPage_ebkv9e8 v2] Service response:", result);

                        if (result.success && result.key) {
                            // Download via hidden iframe
                            const downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" +
                                result.key + "/" + encodeURIComponent(reportName);

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
                            const errMsg = result.message || result.errorMessage || "Unknown error";
                            Terrasoft.showErrorMessage("Report failed: " + errMsg);
                        }
                    } catch (error) {
                        console.error("[UsrPage_ebkv9e8 v2] Error:", error);
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
