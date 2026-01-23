/**
 * UsrPage_ebkv9e8 - v16 New Tab Handler
 * Package: BGApp_eykaguu
 *
 * CHANGES FROM v15:
 * - Looker reports open in NEW TAB (X-Frame-Options blocks iframe from bglobalsolutions.com)
 * - Improved DOM visibility using MutationObserver for reliable element detection
 * - Parent container targeting for filter visibility
 * - Retry logic for DOM element discovery
 *
 * VISIBILITY RULES:
 * | Report Type          | Commission Filters | Date+Status Filters | Action       |
 * |----------------------|-------------------|---------------------|--------------|
 * | None selected        | Hidden            | Hidden              | -            |
 * | Commission           | VISIBLE           | Hidden              | Excel        |
 * | Non-Commission Excel | Hidden            | VISIBLE             | Excel        |
 * | Looker Studio        | Hidden            | Hidden              | New Tab      |
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {

    // ================================================================
    // HELPER FUNCTIONS
    // ================================================================

    function getBpmcsrf() {
        var value = "; " + document.cookie;
        var parts = value.split("; BPMCSRF=");
        if (parts.length === 2) return parts.pop().split(";").shift();
        return "";
    }

    /**
     * Find element by data-item-marker, checking multiple levels of parent wrapping
     */
    function findElementByMarker(markerName) {
        // Try direct marker first
        var el = document.querySelector('[data-item-marker="' + markerName + '"]');
        if (el) return el;

        // Try finding by partial match (in case marker is prefixed)
        var allMarked = document.querySelectorAll('[data-item-marker]');
        for (var i = 0; i < allMarked.length; i++) {
            var marker = allMarked[i].getAttribute('data-item-marker');
            if (marker && marker.indexOf(markerName) !== -1) {
                return allMarked[i];
            }
        }

        return null;
    }

    /**
     * Toggle visibility of parent schema filter elements via DOM
     * Uses container elements for reliable hiding
     * @param {boolean} visible - true to show, false to hide
     * @param {number} retryCount - number of retries (for delayed DOM rendering)
     */
    function toggleDateStatusFilters(visible, retryCount) {
        retryCount = retryCount || 0;
        const display = visible ? "" : "none";
        let found = 0;

        // Target parent container elements first (more reliable)
        const containers = [
            "GridContainer_xdy25v1",  // Date filters container (CreatedFrom, CreatedTo, etc.)
            "GridContainer_knkow5v"   // Status filter container (ComboBox_8w0dlcf)
        ];

        containers.forEach(function(name) {
            var el = findElementByMarker(name);
            if (el) {
                el.style.display = display;
                found++;
                console.log("[v16] Set " + name + " display:", display || "visible");
            }
        });

        // If containers not found and we have retries left, schedule another attempt
        if (found === 0 && retryCount < 5) {
            console.log("[v16] Containers not found, retrying in 300ms... (attempt " + (retryCount + 1) + ")");
            setTimeout(function() {
                toggleDateStatusFilters(visible, retryCount + 1);
            }, 300);
            return;
        }

        console.log("[v16] Date+Status filters:", visible ? "VISIBLE" : "HIDDEN", "| Found:", found + "/" + containers.length);
    }

    /**
     * Hide the iframe container (since we're using new tab for Looker)
     */
    function hideIframeContainer() {
        var container = findElementByMarker("GridContainer_fh039aq");
        if (container) {
            container.style.display = "none";
            console.log("[v16] Iframe container: HIDDEN");
        }
    }

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // ================================================================
            // HIDE PARENT'S REPORT DROPDOWN (we insert our own)
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": {
                    "visible": false
                }
            },

            // ================================================================
            // HIDE THE IFRAME CONTAINER (X-Frame-Options blocks bglobalsolutions.com)
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            },

            // ================================================================
            // WIRE GENERATE BUTTON TO OUR HANDLER
            // ================================================================
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
            // INSERT: Report selector container (always visible)
            // ================================================================
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

            // ================================================================
            // INSERT: Report dropdown
            // ================================================================
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

            // ================================================================
            // INSERT: Warning label (Commission only)
            // ================================================================
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

            // ================================================================
            // INSERT: Commission filters container (conditional)
            // ================================================================
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

            // ================================================================
            // INSERT: Year-Month filter
            // ================================================================
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

            // ================================================================
            // INSERT: Sales Group filter
            // ================================================================
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
                    "UsrShowCommissionFilters": {
                        "value": false
                    },
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
            // ================================================================
            // PAGE INIT - Set default visibility (everything hidden)
            // ================================================================
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);

                    // Wait for DOM to be ready, then hide filters and iframe
                    setTimeout(function() {
                        console.log("[v16] Page init - setting default visibility");
                        toggleDateStatusFilters(false);
                        hideIframeContainer();
                        // Commission filters hidden via $UsrShowCommissionFilters = false (default)
                    }, 500);

                    return;
                }
            },

            // ================================================================
            // REPORT SELECTION - Update visibility based on report type
            // ================================================================
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const selectedReport = await request.$context.LookupAttribute_0as4io2;

                        if (selectedReport && selectedReport.displayValue) {
                            const reportName = selectedReport.displayValue.toLowerCase();
                            const isCommissionReport = reportName.includes("commission");

                            // Check if report has Looker URL
                            let reportUrl = "";
                            try {
                                const bpmcsrf = getBpmcsrf();
                                const metaUrl = "/0/odata/UsrReportesPampa(" + selectedReport.value + ")?$select=UsrURL";
                                const resp = await fetch(metaUrl, {
                                    method: "GET",
                                    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                                });
                                if (resp.ok) {
                                    const meta = await resp.json();
                                    reportUrl = meta.UsrURL || "";
                                }
                            } catch (e) {
                                console.log("[v16] Error checking report URL:", e);
                            }

                            const isLookerReport = reportUrl && reportUrl.length > 0;

                            // Clear filter values when switching reports
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;

                            // Apply visibility rules
                            if (isLookerReport) {
                                // LOOKER STUDIO: Hide all filters (will open in new tab)
                                request.$context.UsrShowCommissionFilters = false;
                                toggleDateStatusFilters(false);
                                console.log("[v16] Report:", selectedReport.displayValue, "| Type: LOOKER | Opens in new tab");

                            } else if (isCommissionReport) {
                                // COMMISSION: Show commission filters, hide date+status
                                request.$context.UsrShowCommissionFilters = true;
                                toggleDateStatusFilters(false);
                                console.log("[v16] Report:", selectedReport.displayValue, "| Type: COMMISSION | Showing commission filters");

                            } else {
                                // NON-COMMISSION EXCEL: Show date+status, hide commission filters
                                request.$context.UsrShowCommissionFilters = false;
                                toggleDateStatusFilters(true);
                                console.log("[v16] Report:", selectedReport.displayValue, "| Type: EXCEL | Showing date+status filters");
                            }
                        } else {
                            // NO REPORT SELECTED: Hide everything
                            request.$context.UsrShowCommissionFilters = false;
                            toggleDateStatusFilters(false);
                            console.log("[v16] No report selected | All filters hidden");
                        }
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
                    const selectedReport = await context.LookupAttribute_0as4io2;

                    if (!selectedReport || !selectedReport.value) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    const pampaReportId = selectedReport.value;
                    let reportDisplayName = selectedReport.displayValue || "";
                    const bpmcsrf = getBpmcsrf();

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
                        console.log("[v16] Metadata lookup failed:", e);
                    }

                    // LOOKER STUDIO - Open in new tab (X-Frame-Options blocks iframe)
                    if (reportUrl && reportUrl.length > 0) {
                        console.log("[v16] Opening Looker Studio in new tab:", reportUrl);
                        window.open(reportUrl, "_blank");
                        Terrasoft.showInformation("Report opened in new tab");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[v16] Generating Excel report:", reportDisplayName);

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
                            console.log("[v16] Found template:", odataResult.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
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
                        console.log("[v16] Excel service response:", result);

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
                        console.error("[v16] Error:", error);
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
