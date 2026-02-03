/**
 * UsrPage_ebkv9e8 - v22 BARE MINIMUM
 * Package: BGApp_eykaguu
 *
 * APPROACH: Do as little as possible. No interceptors. No complex logic.
 * Just add Report dropdown + Generate button. That's it.
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/[]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/()/**SCHEMA_ARGS*/ {

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[
            // Hide parent's dropdown (we add our own)
            {
                "operation": "merge",
                "name": "GridContainer_oshnwh8",
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
            // Bind date filters container to visibility attribute
            {
                "operation": "merge",
                "name": "GridContainer_xdy25v1",
                "values": { "visible": "$UsrShowDateFilters" }
            },
            // Bind status filter container to visibility attribute
            {
                "operation": "merge",
                "name": "GridContainer_knkow5v",
                "values": { "visible": "$UsrShowDateFilters" }
            },
            // Report dropdown
            {
                "operation": "insert",
                "name": "ReportDropdown",
                "values": {
                    "type": "crt.ComboBox",
                    "label": "Report",
                    "labelPosition": "auto",
                    "control": "$LookupAttribute_0as4io2",
                    "listActions": [],
                    "showValueAsLink": true,
                    "controlActions": [],
                    "placeholder": "Select a report...",
                    "visible": true
                },
                "parentName": "MainContainer",
                "propertyName": "items",
                "index": 0
            }
        ]/**SCHEMA_VIEW_CONFIG_DIFF*/,

        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/{
            "attributes": {
                "UsrShowCommissionFilters": { "value": false },
                "UsrShowDateFilters": { "value": false },
                "UsrShowCustomerFilter": { "value": false }
            }
        }/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,
        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/[]/**SCHEMA_MODEL_CONFIG_DIFF*/,

        handlers: /**SCHEMA_HANDLERS*/[
            // Report selection change - update filter visibility
            {
                request: "crt.HandleViewModelAttributeChangeRequest",
                handler: async (request, next) => {
                    const result = await next?.handle(request);

                    if (request.attributeName === "LookupAttribute_0as4io2") {
                        const ctx = request.$context;
                        const report = request.value;

                        if (!report || !report.displayValue) {
                            ctx.UsrShowCommissionFilters = false;
                            ctx.UsrShowDateFilters = false;
                            ctx.UsrShowCustomerFilter = false;
                            return result;
                        }

                        const name = (report.displayValue || "").toLowerCase();
                        const isCommission = name.includes("commission");
                        const isItemsByCustomer = name.includes("items by customer");
                        const isLooker = false; // Will check URL in generate handler

                        ctx.UsrShowCommissionFilters = isCommission;
                        ctx.UsrShowDateFilters = !isCommission; // Date filters for non-Commission
                        ctx.UsrShowCustomerFilter = isItemsByCustomer;

                        console.log("[v22] Report changed:", report.displayValue,
                            "| Commission:", isCommission,
                            "| DateFilters:", !isCommission,
                            "| Customer:", isItemsByCustomer);
                    }

                    return result;
                }
            },
            // Generate button click
            {
                request: "usr.GenerateReportRequest",
                handler: async (request, next) => {
                    try {
                        // Get report
                        const ctx = request.$context;
                        const report = await ctx.LookupAttribute_0as4io2;

                        if (!report || !report.value) {
                            Terrasoft.showErrorMessage("Please select a report");
                            return;
                        }

                        const reportId = report.value;
                        const reportName = report.displayValue || "Report";

                        // Get CSRF token
                        const csrf = document.cookie.split('; ').find(c => c.startsWith('BPMCSRF='))?.split('=')[1] || '';

                        // Check if Looker
                        const metaResp = await fetch("/0/odata/UsrReportesPampa(" + reportId + ")?$select=UsrURL,UsrCode", {
                            headers: { "BPMCSRF": csrf }
                        });
                        const meta = await metaResp.json();

                        if (meta.UsrURL) {
                            window.open(meta.UsrURL, "_blank");
                            Terrasoft.showInformation("Report opened");
                            return;
                        }

                        // Find Excel template - search by UsrCode AND displayName (may differ)
                        const code = meta.UsrCode || "";
                        const name = reportName || "";
                        const esc = (s) => (s || "").replace(/'/g, "''");

                        // Build filter: try code, "Rpt code", name, "Rpt name"
                        const filters = [];
                        if (code) {
                            filters.push("IntName eq '" + esc(code) + "'");
                            filters.push("IntName eq 'Rpt " + esc(code) + "'");
                        }
                        if (name && name !== code) {
                            filters.push("IntName eq '" + esc(name) + "'");
                            filters.push("IntName eq 'Rpt " + esc(name) + "'");
                        }

                        const tplResp = await fetch("/0/odata/IntExcelReport?$filter=" + filters.join(" or ") + "&$select=Id,IntName&$top=1", {
                            headers: { "BPMCSRF": csrf }
                        });
                        const tpl = await tplResp.json();

                        if (!tpl.value || !tpl.value[0]) {
                            Terrasoft.showErrorMessage("Template not found: " + (code || name));
                            return;
                        }
                        console.log("[v22] Found template:", tpl.value[0].IntName, "| Id:", tpl.value[0].Id);

                        // Generate
                        console.log("[v22] Calling UsrExcelReportService/Generate...");
                        Terrasoft.showInformation("Generating...");

                        const requestBody = { ReportId: tpl.value[0].Id };
                        console.log("[v22] Request body:", JSON.stringify(requestBody));

                        const genResp = await fetch("/0/rest/UsrExcelReportService/Generate", {
                            method: "POST",
                            headers: { "Content-Type": "application/json", "BPMCSRF": csrf },
                            body: JSON.stringify(requestBody)
                        });

                        console.log("[v22] Response status:", genResp.status);
                        const resultText = await genResp.text();
                        console.log("[v22] Response text:", resultText);

                        let result;
                        try {
                            result = JSON.parse(resultText);
                        } catch (parseErr) {
                            console.error("[v22] JSON parse error:", parseErr);
                            Terrasoft.showErrorMessage("Invalid response from server");
                            return;
                        }

                        console.log("[v22] Parsed result:", result);

                        if (result.success && result.key) {
                            // Download
                            console.log("[v22] Downloading with key:", result.key);
                            const a = document.createElement("a");
                            a.href = "/0/rest/UsrExcelReportService/GetReport/" + result.key + "/" + encodeURIComponent(reportName);
                            a.download = reportName + ".xlsx";
                            a.click();
                            Terrasoft.showInformation("Downloaded: " + reportName);
                        } else {
                            console.error("[v22] Generation failed:", result);
                            Terrasoft.showErrorMessage(result.message || result.errorMessage || "Generation failed");
                        }
                    } catch (e) {
                        console.error("[v22] Exception:", e);
                        console.error("[v22] Stack:", e.stack);
                        Terrasoft.showErrorMessage("Error: " + (e.message || "Unknown error"));
                    }
                }
            }
        ]/**SCHEMA_HANDLERS*/,

        converters: /**SCHEMA_CONVERTERS*/{}/**SCHEMA_CONVERTERS*/,
        validators: /**SCHEMA_VALIDATORS*/{}/**SCHEMA_VALIDATORS*/
    };
});
