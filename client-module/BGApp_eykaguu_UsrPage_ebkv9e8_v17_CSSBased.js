/**
 * UsrPage_ebkv9e8 - v17 CSS-Based Visibility
 * Package: BGApp_eykaguu
 *
 * CHANGES FROM v16:
 * - Uses CSS class and label text to find elements (data-item-marker not used by Freedom UI)
 * - Finds elements by label content then navigates to parent grid containers
 * - More robust element discovery
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
     * Find the nearest ancestor with a specific class pattern
     */
    function findAncestorWithClass(element, classPattern) {
        var current = element;
        var maxDepth = 15;  // Don't go too far up
        var depth = 0;
        while (current && current !== document.body && depth < maxDepth) {
            if (current.className && typeof current.className === 'string') {
                if (current.className.includes(classPattern)) {
                    return current;
                }
            }
            current = current.parentElement;
            depth++;
        }
        return null;
    }

    /**
     * Find form field containers by their label text
     * Returns array of grid row containers that hold these fields
     */
    function findFieldContainersByLabels(labelTexts) {
        var containers = new Set();
        var labels = document.querySelectorAll('label');

        labels.forEach(function(label) {
            var labelText = label.textContent.trim();
            for (var i = 0; i < labelTexts.length; i++) {
                if (labelText.includes(labelTexts[i])) {
                    // Find the grid row or container ancestor
                    // Freedom UI structure: label -> input-container -> grid-item -> grid-row
                    var gridContainer = findAncestorWithClass(label, 'grid');
                    if (gridContainer) {
                        containers.add(gridContainer);
                    }
                    // Also try finding by crt- prefixed classes
                    var crtContainer = findAncestorWithClass(label, 'crt-');
                    if (crtContainer && crtContainer.className.includes('container')) {
                        containers.add(crtContainer);
                    }
                    break;
                }
            }
        });

        return Array.from(containers);
    }

    /**
     * Find the main filter sections by looking for specific layout patterns
     */
    function findFilterSections() {
        var sections = {
            dateFilters: [],
            statusFilter: []
        };

        // Find all labels that match our filter fields
        var dateLabels = ['Created From', 'Created To', 'Shipping From', 'Shipping To', 'Delivery From', 'Delivery To'];
        var statusLabels = ['Status Order'];

        var labels = document.querySelectorAll('label');
        var processedParents = new Set();

        labels.forEach(function(label) {
            var labelText = label.textContent.trim();

            // Check if this is a date filter label
            for (var i = 0; i < dateLabels.length; i++) {
                if (labelText === dateLabels[i] || labelText.includes(dateLabels[i])) {
                    // Go up to find the grid-item level (usually the field wrapper)
                    var fieldWrapper = label.closest('.crt-flex-item') ||
                                      label.closest('[class*="grid-item"]') ||
                                      label.parentElement?.parentElement?.parentElement;
                    if (fieldWrapper && !processedParents.has(fieldWrapper)) {
                        sections.dateFilters.push(fieldWrapper);
                        processedParents.add(fieldWrapper);
                    }
                    break;
                }
            }

            // Check if this is a status filter label
            for (var j = 0; j < statusLabels.length; j++) {
                if (labelText === statusLabels[j] || labelText.includes(statusLabels[j])) {
                    var statusWrapper = label.closest('.crt-flex-item') ||
                                       label.closest('[class*="grid-item"]') ||
                                       label.parentElement?.parentElement?.parentElement;
                    if (statusWrapper && !processedParents.has(statusWrapper)) {
                        sections.statusFilter.push(statusWrapper);
                        processedParents.add(statusWrapper);
                    }
                    break;
                }
            }
        });

        return sections;
    }

    /**
     * Toggle visibility of date and status filter elements
     * @param {boolean} visible - true to show, false to hide
     * @param {number} retryCount - number of retries
     */
    function toggleDateStatusFilters(visible, retryCount) {
        retryCount = retryCount || 0;
        var display = visible ? "" : "none";
        var sections = findFilterSections();
        var foundCount = sections.dateFilters.length + sections.statusFilter.length;

        console.log("[v17] Found filter elements - Date:", sections.dateFilters.length, "Status:", sections.statusFilter.length);

        if (foundCount === 0 && retryCount < 8) {
            console.log("[v17] No filters found, retrying in 400ms... (attempt " + (retryCount + 1) + ")");
            setTimeout(function() {
                toggleDateStatusFilters(visible, retryCount + 1);
            }, 400);
            return;
        }

        // Hide/show date filter elements
        sections.dateFilters.forEach(function(el) {
            el.style.display = display;
        });

        // Hide/show status filter elements
        sections.statusFilter.forEach(function(el) {
            el.style.display = display;
        });

        // Also try to find and hide the parent grid containers
        // Look for grid containers that hold multiple date fields
        if (!visible && sections.dateFilters.length > 0) {
            var firstDateEl = sections.dateFilters[0];
            var parentGrid = firstDateEl.parentElement;
            // Go up to find a container that holds all 6 date fields
            var attempts = 0;
            while (parentGrid && attempts < 5) {
                var childCount = parentGrid.querySelectorAll('label').length;
                if (childCount >= 4) {  // Found a container with multiple fields
                    parentGrid.style.display = display;
                    console.log("[v17] Found parent grid with", childCount, "labels, setting display:", display || "visible");
                    break;
                }
                parentGrid = parentGrid.parentElement;
                attempts++;
            }
        }

        console.log("[v17] Date+Status filters:", visible ? "VISIBLE" : "HIDDEN", "| Found:", foundCount, "elements");
    }

    /**
     * Alternative approach: Hide by injecting CSS rules
     */
    function injectFilterHidingCSS(hide) {
        var styleId = 'v17-filter-visibility';
        var existingStyle = document.getElementById(styleId);

        if (existingStyle) {
            existingStyle.remove();
        }

        if (hide) {
            var style = document.createElement('style');
            style.id = styleId;
            // This CSS will hide elements based on their label content
            // We use the :has() selector where supported, with fallback
            style.textContent = `
                /* Hide date filter fields by targeting their container structure */
                .crt-input-label-container:has(label[title*="Created"]),
                .crt-input-label-container:has(label[title*="Shipping"]),
                .crt-input-label-container:has(label[title*="Delivery"]),
                .crt-input-label-container:has(label[title*="Status Order"]) {
                    display: none !important;
                }
            `;
            document.head.appendChild(style);
            console.log("[v17] Injected CSS to hide filters");
        } else {
            console.log("[v17] Removed CSS filter hiding");
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
            // HIDE THE IFRAME CONTAINER
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": {
                    "visible": false
                }
            },

            // ================================================================
            // HIDE DATE FILTERS CONTAINER BY DEFAULT
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": {
                    "visible": false
                }
            },

            // ================================================================
            // HIDE STATUS FILTER CONTAINER BY DEFAULT
            // ================================================================
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
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
                    "UsrShowDateStatusFilters": {
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
            // PAGE INIT - Set default visibility
            // ================================================================
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);

                    console.log("[v17] Page init - hiding date/status filters by default");

                    // The schema merge should hide GridContainer_xdy25v1 and GridContainer_knkow5v
                    // But as backup, also use DOM manipulation after a delay
                    setTimeout(function() {
                        toggleDateStatusFilters(false);
                    }, 800);

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
                                console.log("[v17] Error checking report URL:", e);
                            }

                            const isLookerReport = reportUrl && reportUrl.length > 0;

                            // Clear filter values when switching reports
                            request.$context.UsrYearMonth = null;
                            request.$context.UsrSalesGroup = null;

                            // Apply visibility rules
                            if (isLookerReport) {
                                // LOOKER STUDIO: Hide all filters
                                request.$context.UsrShowCommissionFilters = false;
                                toggleDateStatusFilters(false);
                                console.log("[v17] Report:", selectedReport.displayValue, "| Type: LOOKER | Opens in new tab");

                            } else if (isCommissionReport) {
                                // COMMISSION: Show commission filters, hide date+status
                                request.$context.UsrShowCommissionFilters = true;
                                toggleDateStatusFilters(false);
                                console.log("[v17] Report:", selectedReport.displayValue, "| Type: COMMISSION | Showing commission filters");

                            } else {
                                // NON-COMMISSION EXCEL: Show date+status, hide commission filters
                                request.$context.UsrShowCommissionFilters = false;
                                toggleDateStatusFilters(true);
                                console.log("[v17] Report:", selectedReport.displayValue, "| Type: EXCEL | Showing date+status filters");
                            }
                        } else {
                            // NO REPORT SELECTED: Hide everything
                            request.$context.UsrShowCommissionFilters = false;
                            toggleDateStatusFilters(false);
                            console.log("[v17] No report selected | All filters hidden");
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
                        console.log("[v17] Metadata lookup failed:", e);
                    }

                    // LOOKER STUDIO - Open in new tab
                    if (reportUrl && reportUrl.length > 0) {
                        console.log("[v17] Opening Looker Studio in new tab:", reportUrl);
                        window.open(reportUrl, "_blank");
                        Terrasoft.showInformation("Report opened in new tab");
                        return next?.handle(request);
                    }

                    // EXCEL PATH
                    console.log("[v17] Generating Excel report:", reportDisplayName);

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
                            console.log("[v17] Found template:", odataResult.value[0].IntName);
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
                        console.log("[v17] Excel service response:", result);

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
                        console.error("[v17] Error:", error);
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
