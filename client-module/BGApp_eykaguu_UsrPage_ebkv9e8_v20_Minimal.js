/**
 * UsrPage_ebkv9e8 - v20 Minimal (BGlobal Pattern)
 * Package: BGApp_eykaguu
 *
 * GOAL: Match BGlobal's BGIntExcelreportMixin as closely as possible.
 *
 * BGlobal's mixin interface:
 * - Sends: {EsqString, ReportId, RecordCollection}
 * - EsqString = serialized ESQ with filters already embedded
 * - RecordCollection = array of record IDs (can be empty)
 * - Downloads via UsrExcelReportService/GetReport/{key}/{filename}
 *
 * This handler:
 * - Adds Report dropdown (extends parent's filter controls)
 * - Generates report using IntExcelReport.IntEsq (BGlobal's template ESQ)
 * - NO complex filter visibility logic
 * - NO cascade filters
 * - Proper null guards everywhere
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {

    function getBpmcsrf() {
        var value = "; " + document.cookie;
        var parts = value.split("; BPMCSRF=");
        if (parts.length === 2) return parts.pop().split(";").shift();
        return "";
    }

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Hide parent's report dropdown (we use our own)
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
                "values": { "visible": false }
            },
            // Hide iframe container (we open Looker in new tab)
            {
                "operation": "merge",
                "name": "GridContainer_fh039aq",
                "values": { "visible": false }
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
            // INSERT: Report selector
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
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/[]/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,

        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // Page init - just log version
            {
                request: "crt.HandleViewModelInitRequest",
                handler: async (request, next) => {
                    await next?.handle(request);
                    console.log("[v20] Minimal handler - BGlobal pattern");
                    return;
                }
            },

            // Report generation - matches BGlobal's mixin pattern
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    const context = request.$context;
                    const bpmcsrf = getBpmcsrf();

                    // Get selected report with null guards
                    let selectedReport = null;
                    try {
                        selectedReport = await context.LookupAttribute_0as4io2;
                    } catch (e) {
                        console.log("[v20] Error getting selected report:", e);
                    }

                    if (!selectedReport) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    // Null guard for value property
                    const pampaReportId = selectedReport.value || null;
                    const reportDisplayName = selectedReport.displayValue || "Report";

                    if (!pampaReportId) {
                        Terrasoft.showErrorMessage("Please select a report");
                        return next?.handle(request);
                    }

                    console.log("[v20] Selected report:", reportDisplayName, "| ID:", pampaReportId);

                    // Fetch report metadata (URL for Looker, Code for template lookup)
                    let reportUrl = "";
                    let reportCode = "";
                    try {
                        const metaUrl = "/0/odata/UsrReportesPampa(" + pampaReportId + ")?$select=Id,Name,UsrURL,UsrCode";
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
                        console.log("[v20] Metadata lookup error:", e);
                    }

                    // --------------------------------------------------------
                    // LOOKER STUDIO PATH - Open in new tab
                    // --------------------------------------------------------
                    if (reportUrl && reportUrl.length > 0) {
                        console.log("[v20] Opening Looker:", reportDisplayName);
                        window.open(reportUrl, "_blank");
                        Terrasoft.showInformation("Report opened in new tab");
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // EXCEL PATH - Use BGlobal's pattern
                    // --------------------------------------------------------
                    console.log("[v20] Generating Excel:", reportDisplayName);

                    // Find IntExcelReport template by name
                    let intExcelReportId = null;
                    let intEsq = null;
                    try {
                        // Try exact name match first, then with "Rpt " prefix
                        const escapeName = (s) => (s || "").replace(/'/g, "''");
                        const odataUrl = "/0/odata/IntExcelReport?$filter=" +
                            "(IntName eq '" + escapeName(reportDisplayName) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportDisplayName) + "'" +
                            " or IntName eq '" + escapeName(reportCode) + "'" +
                            " or IntName eq 'Rpt " + escapeName(reportCode) + "')" +
                            "&$select=Id,IntName,IntEsq&$top=1";

                        const odataResp = await fetch(odataUrl, {
                            method: "GET",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf }
                        });
                        const odataResult = await odataResp.json();

                        if (odataResult.value && odataResult.value.length > 0) {
                            intExcelReportId = odataResult.value[0].Id;
                            intEsq = odataResult.value[0].IntEsq || null;
                            console.log("[v20] Found template:", odataResult.value[0].IntName);
                        } else {
                            Terrasoft.showErrorMessage("Excel template not found for: " + reportDisplayName);
                            return next?.handle(request);
                        }
                    } catch (e) {
                        Terrasoft.showErrorMessage("Error finding template: " + e.message);
                        return next?.handle(request);
                    }

                    // --------------------------------------------------------
                    // Generate report - BGlobal's mixin pattern:
                    // {EsqString, ReportId, RecordCollection}
                    // --------------------------------------------------------
                    try {
                        Terrasoft.showInformation("Generating report...");

                        // BGlobal's mixin sent the IntEsq as EsqString
                        // RecordCollection is usually empty for section reports
                        const requestData = {
                            EsqString: intEsq || "",
                            ReportId: intExcelReportId,
                            RecordCollection: []
                        };

                        console.log("[v20] Calling UsrExcelReportService.Generate");
                        const response = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
                            body: JSON.stringify(requestData)
                        });

                        const result = await response.json();
                        console.log("[v20] Service response:", result);

                        if (result && result.success && result.key) {
                            // Download - match BGlobal's pattern
                            const downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" +
                                result.key + "/" + encodeURIComponent(reportDisplayName);

                            // Use hidden iframe for download (same as our working approach)
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
                            const errorMsg = (result && result.message) ||
                                             (result && result.errorMessage) ||
                                             "Unknown error";
                            Terrasoft.showErrorMessage("Failed: " + errorMsg);
                        }
                    } catch (error) {
                        console.error("[v20] Error:", error);
                        Terrasoft.showErrorMessage("Error: " + (error.message || "Unknown error"));
                    }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
