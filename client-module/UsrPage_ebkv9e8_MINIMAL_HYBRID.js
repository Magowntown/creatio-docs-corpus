/**
 * MINIMAL HYBRID HANDLER
 *
 * PURPOSE: Simple routing between Looker (URL) and Excel (no URL) reports.
 * No custom filters, no visibility changes - just proper routing.
 *
 * - If report HAS UsrURL → Open in new tab (original Looker behavior)
 * - If report has NO UsrURL → Call UsrExcelReportService (Excel download)
 *
 * Schema: UsrPage_ebkv9e8
 * Package: BGApp_eykaguu
 * PROD: https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972
 */
define("UsrPage_ebkv9e8", /**SCHEMA_DEPS*/["@creatio-devkit/common"]/**SCHEMA_DEPS*/, function/**SCHEMA_ARGS*/(sdk)/**SCHEMA_ARGS*/ {

    // Helper: Get BPMCSRF cookie for API calls
    function getBpmcsrf() {
        var value = "; " + document.cookie;
        var parts = value.split("; BPMCSRF=");
        if (parts.length === 2) return parts.pop().split(";").shift();
        return "";
    }

    return {
        viewConfigDiff: /**SCHEMA_VIEW_CONFIG_DIFF*/[]/**SCHEMA_VIEW_CONFIG_DIFF*/,
        viewModelConfigDiff: /**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/{}/**SCHEMA_VIEW_MODEL_CONFIG_DIFF*/,
        modelConfigDiff: /**SCHEMA_MODEL_CONFIG_DIFF*/{}/**SCHEMA_MODEL_CONFIG_DIFF*/,
        handlers: /**SCHEMA_HANDLERS*/[
            {
                // Intercept the OpenReport request from button click
                request: "OpenReport",
                handler: async (request, next) => {
                    console.log("[MINIMAL] OpenReport triggered");

                    try {
                        // Get the selected report
                        var selectedReport = await request.$context.LookupAttribute_0as4io2;
                        if (!selectedReport || !selectedReport.value) {
                            console.log("[MINIMAL] No report selected");
                            return next?.handle(request);
                        }

                        // Get report metadata (UsrURL)
                        var reportUrl = request.$context.attributes?.UsrURL;
                        console.log("[MINIMAL] Report:", selectedReport.displayValue, "URL:", reportUrl);

                        // ROUTING DECISION
                        if (reportUrl && reportUrl.trim() !== "") {
                            // HAS URL = Looker report → Let parent handle it (opens new tab)
                            console.log("[MINIMAL] Looker report - delegating to parent");
                            return next?.handle(request);
                        } else {
                            // NO URL = Excel report → Call UsrExcelReportService
                            console.log("[MINIMAL] Excel report - calling service");

                            // Get IntExcelReport ID for this report
                            var reportId = null;
                            try {
                                var model = await sdk.Model.create("IntExcelReport");
                                var results = await model.load({
                                    attributes: ["Id", "IntName"],
                                    parameters: [{
                                        type: sdk.ModelParameterType.Filter,
                                        value: sdk.Filter.contains("IntName", selectedReport.displayValue)
                                    }]
                                });
                                if (results && results.length > 0) {
                                    reportId = results[0].Id;
                                    console.log("[MINIMAL] Found IntExcelReport:", reportId);
                                }
                            } catch (e) {
                                console.error("[MINIMAL] IntExcelReport lookup error:", e);
                            }

                            if (!reportId) {
                                alert("Excel template not found for: " + selectedReport.displayValue);
                                return next?.handle(request);
                            }

                            // Call UsrExcelReportService/Generate
                            var payload = {
                                ReportId: reportId,
                                YearMonthId: "00000000-0000-0000-0000-000000000000",
                                SalesRepId: "00000000-0000-0000-0000-000000000000",
                                CustomerId: "00000000-0000-0000-0000-000000000000",
                                CustomerName: ""
                            };

                            try {
                                var response = await fetch("/0/rest/UsrExcelReportService/Generate", {
                                    method: "POST",
                                    headers: {
                                        "Content-Type": "application/json",
                                        "BPMCSRF": getBpmcsrf()
                                    },
                                    body: JSON.stringify(payload)
                                });

                                var result = await response.json();
                                console.log("[MINIMAL] Generate result:", result);

                                if (result.success && result.key) {
                                    // Download via hidden iframe
                                    var reportName = selectedReport.displayValue.replace(/[^a-zA-Z0-9]/g, "_");
                                    var downloadUrl = "/0/rest/UsrExcelReportService/GetReport/" +
                                                      result.key + "/" + reportName;

                                    var iframe = document.getElementById("reportDownloadFrame");
                                    if (!iframe) {
                                        iframe = document.createElement("iframe");
                                        iframe.id = "reportDownloadFrame";
                                        iframe.style.display = "none";
                                        document.body.appendChild(iframe);
                                    }
                                    iframe.src = downloadUrl;
                                    console.log("[MINIMAL] Download initiated:", downloadUrl);
                                } else {
                                    alert("Report generation failed: " + (result.message || "Unknown error"));
                                }
                            } catch (e) {
                                console.error("[MINIMAL] Generate error:", e);
                                alert("Error generating report: " + e.message);
                            }
                        }
                    } catch (e) {
                        console.error("[MINIMAL] Handler error:", e);
                    }

                    return next?.handle(request);
                }
            }
        ]/**SCHEMA_HANDLERS*/
    };
});
