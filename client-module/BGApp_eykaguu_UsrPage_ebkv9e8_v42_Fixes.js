/**
 * UsrPage_ebkv9e8 - v42 FIXES
 * Package: BGApp_eykaguu
 *
 * FIXES from v41:
 * 1. Customer lookup bound to Account entity (not BGCustomer)
 * 2. Looker iframe via DOM manipulation (not crt.IFrame) - no sandbox restrictions
 * 3. Better logging for customer selection
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {

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

    // Create Looker iframe via DOM (no sandbox restrictions)
    function showLookerInPage(url) {
        // Find or create container
        let container = document.getElementById("usrLookerContainer");
        if (!container) {
            container = document.createElement("div");
            container.id = "usrLookerContainer";
            container.style.cssText = "width:100%;margin-top:20px;";

            // Find MainContainer in DOM and append
            const mainContainer = document.querySelector('[data-item-marker="MainContainer"]') ||
                                  document.querySelector('.main-container') ||
                                  document.querySelector('[class*="MainContainer"]');
            if (mainContainer) {
                mainContainer.appendChild(container);
            } else {
                // Fallback: append to body
                document.body.appendChild(container);
            }
        }

        // Clear existing content
        while (container.firstChild) {
            container.removeChild(container.firstChild);
        }

        // Create iframe using safe DOM methods
        const iframe = document.createElement("iframe");
        iframe.id = "usrLookerFrame";
        iframe.src = url;
        iframe.style.cssText = "width:100%;height:800px;border:1px solid #ddd;border-radius:4px;";
        iframe.setAttribute("allowfullscreen", "true");
        // Note: NO sandbox attribute - Looker needs full access
        container.appendChild(iframe);

        container.style.display = "block";
        console.log("[v42] Looker iframe created via DOM:", url);
    }

    function hideLookerFrame() {
        const container = document.getElementById("usrLookerContainer");
        if (container) {
            container.style.display = "none";
            while (container.firstChild) {
                container.removeChild(container.firstChild);
            }
        }
    }

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Hide parent's iframe container
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": false }
            },

            // Date filters - bind visibility
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": "$UsrShowDateFilters" }
            },

            // Status filter - bind visibility
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
                    "clicked": { "request": "usr.GenerateReportRequest" }
                }
            },

            // ================================================================
            // COMMISSION FILTERS CONTAINER
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrCommissionFiltersContainer",
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
                    "padding": { "top": "medium", "right": "none", "bottom": "medium", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 1
            },

            // Year-Month COMBOBOX
            {
                "operation": "insert",
                "name": "UsrYearMonthCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Year-Month",
                    "labelPosition": "auto",
                    "control": "$UsrYearMonth",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select month...",
                    "visible": true,
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 }
                },
                "parentName": "UsrCommissionFiltersContainer",
                "propertyName": "items",
                "index": 0
            },

            // Sales Group COMBOBOX
            {
                "operation": "insert",
                "name": "UsrSalesGroupCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Sales Group",
                    "labelPosition": "auto",
                    "control": "$UsrSalesGroup",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select group (optional)...",
                    "visible": true,
                    "layoutConfig": { "column": 2, "row": 1, "colSpan": 1, "rowSpan": 1 },
                    "mode": "List"
                },
                "parentName": "UsrCommissionFiltersContainer",
                "propertyName": "items",
                "index": 1
            },

            // ================================================================
            // CUSTOMER FILTER CONTAINER
            // ================================================================
            {
                "operation": "insert",
                "name": "UsrCustomerFilterContainer",
                "values": {
                    "type": "crt.GridContainer",
                    "columns": ["minmax(32px, 1fr)"],
                    "rows": "minmax(max-content, 32px)",
                    "gap": { "columnGap": "large", "rowGap": "none" },
                    "items": [],
                    "fitContent": true,
                    "visible": "$UsrShowCustomerFilter",
                    "color": "transparent",
                    "borderRadius": "none",
                    "padding": { "top": "medium", "right": "none", "bottom": "medium", "left": "none" }
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 2
            },

            // Customer COMBOBOX - bound to Account entity
            {
                "operation": "insert",
                "name": "UsrCustomerCombo",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Customer",
                    "labelPosition": "auto",
                    "control": "$UsrCustomer",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select customer...",
                    "visible": true,
                    "layoutConfig": { "column": 1, "row": 1, "colSpan": 1, "rowSpan": 1 }
                },
                "parentName": "UsrCustomerFilterContainer",
                "propertyName": "items",
                "index": 0
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[
            {
                "operation": "merge",
                "path": ["attributes"],
                "values": {
                    // Visibility flags
                    "UsrShowCommissionFilters": { "value": false },
                    "UsrShowCustomerFilter": { "value": false },
                    "UsrShowDateFilters": { "value": true },

                    // YearMonth - LOOKUP
                    "UsrYearMonth": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGYearMonth"
                        }
                    },

                    // SalesGroup - LOOKUP
                    "UsrSalesGroup": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.BGSalesGroup"
                        }
                    },

                    // SalesGroup list
                    "UsrSalesGroup_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{ "columnName": "BGSalesGroupName", "direction": "asc" }]
                            }
                        }
                    },

                    // Customer - LOOKUP bound to Account entity
                    "UsrCustomer": {
                        "modelConfig": {
                            "path": "UsrEntity_e7ac661DS.Account"
                        }
                    },

                    // Customer list (from Account)
                    "UsrCustomer_List": {
                        "isCollection": true,
                        "modelConfig": {
                            "sortingConfig": {
                                "default": [{ "columnName": "Name", "direction": "asc" }]
                            }
                        }
                    }
                }
            }
        ]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // Page init
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v42] Page initialized - DOM iframe + Account lookup");
                    hideLookerFrame(); // Ensure hidden on init
                    return;
                }
            },

            // Report selection
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    const bpmcsrf = getBpmcsrf();

                    if (request.attributeName === "LookupAttribute_0as4io2" && !request.silent) {
                        const ctx = request.$context;
                        let selectedReport = null;

                        try {
                            selectedReport = await ctx.LookupAttribute_0as4io2;
                        } catch (e) {
                            console.log("[v42] Error getting report:", e);
                        }

                        // Reset all
                        ctx.UsrShowCommissionFilters = false;
                        ctx.UsrShowCustomerFilter = false;
                        ctx.UsrShowDateFilters = true;
                        hideLookerFrame();

                        // Clear filter values
                        ctx.UsrYearMonth = null;
                        ctx.UsrSalesGroup = null;
                        ctx.UsrCustomer = null;

                        if (!selectedReport || !selectedReport.value) {
                            console.log("[v42] No report selected");
                            return next?.handle(request);
                        }

                        const reportName = (selectedReport.displayValue || "").toLowerCase();
                        console.log("[v42] Report selected:", selectedReport.displayValue);

                        // Check if Looker
                        let reportUrl = "";
                        try {
                            const r = await fetch("/0/odata/UsrReportesPampa(" + selectedReport.value + ")?$select=UsrURL", {
                                headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                            });
                            if (r.ok) {
                                const m = await r.json();
                                if (m && m.UsrURL) {
                                    reportUrl = m.UsrURL;
                                }
                            }
                        } catch (e) {}

                        if (reportName.includes("commission")) {
                            ctx.UsrShowCommissionFilters = true;
                            ctx.UsrShowDateFilters = false;
                            console.log("[v42] → Commission filters ON");

                        } else if (reportName.includes("items by customer")) {
                            ctx.UsrShowCustomerFilter = true;
                            ctx.UsrShowDateFilters = true;
                            console.log("[v42] → Customer (Account) lookup + Date filters ON");

                        } else if (reportUrl) {
                            // LOOKER: Show iframe via DOM
                            ctx.UsrShowDateFilters = true;
                            showLookerInPage(reportUrl);
                            console.log("[v42] → Looker iframe shown (DOM):", reportUrl);

                        } else {
                            ctx.UsrShowDateFilters = true;
                            console.log("[v42] → Date filters ON (Excel)");
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
                    console.log("[v42] Generate:", reportDisplayName);

                    // Check if Looker
                    let reportUrl = "", reportCode = "";
                    try {
                        const r = await fetch("/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=UsrURL,UsrCode", {
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        if (r.ok) {
                            const m = await r.json();
                            if (m) {
                                reportUrl = m.UsrURL || "";
                                reportCode = m.UsrCode || "";
                            }
                        }
                    } catch (e) {}

                    // LOOKER: Update iframe with filter params
                    if (reportUrl) {
                        let params = "";
                        try {
                            const filters = [];
                            const createdFrom = await ctx.CreatedFrom;
                            const createdTo = await ctx.CreatedTo;
                            const status = await ctx.LookupAttribute_tytkx09;

                            if (createdFrom) {
                                const d = new Date(createdFrom);
                                filters.push("CreatedOn ge datetime'" + d.toISOString().split("T")[0] + "'");
                            }
                            if (createdTo) {
                                const d = new Date(createdTo);
                                filters.push("CreatedOn le datetime'" + d.toISOString().split("T")[0] + "'");
                            }
                            if (status && status.displayValue && status.displayValue !== "All") {
                                filters.push("contains(BGStatus, '" + status.displayValue + "')");
                            }

                            if (filters.length > 0) {
                                params = '?params=%7B"ds0.additionalFilters":"' + filters.join(" and ") + '","ds0.top":"1000000"%7D';
                            }
                        } catch (e) {
                            console.log("[v42] Looker params error:", e);
                        }

                        const fullUrl = reportUrl + params;
                        showLookerInPage(fullUrl);
                        Terrasoft.showInformation("Looker report loaded");
                        return next?.handle(request);
                    }

                    // EXCEL: Find template
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
                            console.log("[v42] Template:", d.value[0].IntName);
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
                    const emptyGuid = "00000000-0000-0000-0000-000000000000";
                    let yearMonthId = emptyGuid;
                    let salesGroupId = emptyGuid;
                    let customerId = emptyGuid;
                    let customerName = "";
                    let dateFrom = null, dateTo = null, statusName = "";

                    // Always collect date filters
                    try { dateFrom = await ctx.CreatedFrom; } catch (e) {}
                    try { dateTo = await ctx.CreatedTo; } catch (e) {}
                    try {
                        const st = await ctx.LookupAttribute_tytkx09;
                        if (st && st.displayValue && st.displayValue !== "All") {
                            statusName = st.displayValue;
                        }
                    } catch (e) {}

                    console.log("[v42] Date filters | From:", dateFrom, "| To:", dateTo, "| Status:", statusName);

                    if (rLower.includes("commission")) {
                        try {
                            const ym = await ctx.UsrYearMonth;
                            if (ym && ym.value) {
                                yearMonthId = ym.value;
                                console.log("[v42] YearMonth:", ym.displayValue);
                            }
                        } catch (e) {}

                        try {
                            const sg = await ctx.UsrSalesGroup;
                            if (sg && sg.value) {
                                salesGroupId = sg.value;
                                console.log("[v42] SalesGroup:", sg.displayValue);
                            }
                        } catch (e) {}

                    } else if (rLower.includes("items by customer")) {
                        // Get Customer (Account) lookup value
                        try {
                            const cust = await ctx.UsrCustomer;
                            console.log("[v42] UsrCustomer raw value:", cust);

                            if (cust && cust.value) {
                                customerId = cust.value;
                                customerName = cust.displayValue || "";
                                console.log("[v42] Customer selected:", customerName, "| ID:", customerId);
                            } else if (cust && typeof cust === "string") {
                                // Maybe it's just a string value
                                customerName = cust;
                                console.log("[v42] Customer (string):", customerName);
                            } else {
                                console.log("[v42] No customer selected - will return all data");
                            }
                        } catch (e) {
                            console.log("[v42] Customer lookup error:", e);
                        }
                    }

                    // Generate
                    try {
                        Terrasoft.showInformation("Generating report...");

                        const requestBody = {
                            EsqString: intEsq,
                            ReportId: intExcelReportId,
                            RecordCollection: [],
                            YearMonthId: yearMonthId,
                            SalesRepId: salesGroupId,
                            CustomerId: customerId,
                            CustomerName: customerName,
                            CreatedFrom: toWcfDate(dateFrom),
                            CreatedTo: toWcfDate(dateTo),
                            StatusName: statusName
                        };

                        console.log("[v42] Request:", JSON.stringify(requestBody, null, 2));

                        const r = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify(requestBody)
                        });

                        const result = await r.json();
                        console.log("[v42] Result:", result);

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
                            const errorMsg = (result && result.message) || (result && result.errorMessage) || "Generation failed";
                            console.error("[v42] Failed:", errorMsg);
                            Terrasoft.showErrorMessage(errorMsg);
                        }
                    } catch (e) {
                        console.error("[v42] Error:", e);
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
