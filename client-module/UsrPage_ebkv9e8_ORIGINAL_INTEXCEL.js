/**
 * ORIGINAL INTEXCEL HANDLER
 *
 * PURPOSE: Restore original Excel download behavior using IntExcelReportService
 * (the BGlobal/IntExcelExport package's original service).
 *
 * This handler:
 * 1. For reports WITH UsrURL (Looker): Delegates to parent (opens in new tab)
 * 2. For reports WITHOUT UsrURL (Excel): Uses IntExcelReportService endpoints
 *    - POST /0/rest/IntExcelReportService/GetExportFiltersKey
 *    - GET /0/rest/IntExcelReportService/GetExportFilteredData/{fileName}/{key}
 *
 * This is the ORIGINAL flow that worked before Freedom UI migration.
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

    // Helper: Build ESQ JSON for IntExcelReportService (mirrors Classic-era mixin)
    function buildReportEsq(rootSchemaName, executionId) {
        return {
            rootSchemaName: rootSchemaName,
            operationType: 0,
            includeProcessExecutionData: true,
            filters: {
                className: "Terrasoft.FilterGroup",
                items: executionId ? {
                    "execution-filter": {
                        className: "Terrasoft.CompareFilter",
                        filterType: 1,
                        comparisonType: 3,
                        isEnabled: true,
                        trimDateTimeParameterToDate: false,
                        leftExpression: {
                            className: "Terrasoft.ColumnExpression",
                            expressionType: 0,
                            columnPath: "BGExecutionId"
                        },
                        isAggregative: false,
                        key: "execution-filter",
                        dataValueType: 0,
                        leftExpressionCaption: "BGExecutionId",
                        rightExpression: {
                            className: "Terrasoft.ParameterExpression",
                            expressionType: 2,
                            parameter: {
                                className: "Terrasoft.Parameter",
                                dataValueType: 0,
                                value: executionId
                            }
                        }
                    }
                } : {},
                logicalOperation: 0,
                isEnabled: true,
                filterType: 6,
                rootSchemaName: rootSchemaName,
                key: ""
            },
            columns: { className: "Terrasoft.QueryColumns", items: {} },
            isDistinct: false,
            rowCount: -1,
            rowsOffset: -1,
            isPageable: false,
            allColumns: false,
            useLocalization: true,
            useRecordDeactivation: false,
            serverESQCacheParameters: { cacheLevel: 0, cacheGroup: "", cacheItemName: "" },
            queryOptimize: false,
            useMetrics: false,
            adminUnitRoleSources: 0,
            querySource: 0,
            ignoreDisplayValues: false,
            isHierarchical: false
        };
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
                    console.log("[INTEXCEL] OpenReport triggered");

                    try {
                        // Get the selected report from lookup
                        var selectedReport = await request.$context.LookupAttribute_0as4io2;
                        if (!selectedReport || !selectedReport.value) {
                            console.log("[INTEXCEL] No report selected - delegating to parent");
                            return next?.handle(request);
                        }

                        // Get report metadata (UsrURL determines Looker vs Excel)
                        var reportUrl = request.$context.attributes?.UsrURL;
                        console.log("[INTEXCEL] Report:", selectedReport.displayValue, "URL:", reportUrl);

                        // ROUTING DECISION
                        if (reportUrl && reportUrl.trim() !== "") {
                            // HAS URL = Looker report -> Let parent handle it (opens new tab with URL params)
                            console.log("[INTEXCEL] Looker report - delegating to parent handler");
                            return next?.handle(request);
                        }

                        // NO URL = Excel report -> Use original IntExcelReportService flow
                        console.log("[INTEXCEL] Excel report - using IntExcelReportService");

                        // Step 1: Find the IntExcelReport record for this report
                        var reportId = null;
                        var reportCode = null;
                        var rootSchemaName = null;

                        try {
                            // First get the report code from UsrReportesPampa
                            var pampaModel = await sdk.Model.create("UsrReportesPampa");
                            var pampaResults = await pampaModel.load({
                                attributes: ["Id", "Name", "UsrCode"],
                                parameters: [{
                                    type: sdk.ModelParameterType.PrimaryColumnValue,
                                    value: selectedReport.value
                                }]
                            });
                            if (pampaResults && pampaResults.length > 0) {
                                reportCode = pampaResults[0].UsrCode || selectedReport.displayValue;
                                console.log("[INTEXCEL] Report code:", reportCode);
                            }

                            // Then find IntExcelReport by name matching
                            var model = await sdk.Model.create("IntExcelReport");
                            var results = await model.load({
                                attributes: ["Id", "IntName", "IntEntitySchemaName"],
                                parameters: [{
                                    type: sdk.ModelParameterType.Filter,
                                    value: sdk.Filter.contains("IntName", selectedReport.displayValue)
                                }]
                            });

                            if (results && results.length > 0) {
                                reportId = results[0].Id;
                                // IntEntitySchemaName may be a lookup or string
                                var schemaName = results[0].IntEntitySchemaName;
                                if (typeof schemaName === "object" && schemaName) {
                                    rootSchemaName = schemaName.displayValue || schemaName.Name;
                                } else {
                                    rootSchemaName = schemaName;
                                }
                                console.log("[INTEXCEL] Found IntExcelReport:", reportId, "Schema:", rootSchemaName);
                            }
                        } catch (e) {
                            console.error("[INTEXCEL] IntExcelReport lookup error:", e);
                        }

                        if (!reportId) {
                            alert("Excel template not found for: " + selectedReport.displayValue);
                            return next?.handle(request);
                        }

                        // Step 2: Build the ESQ JSON (like Classic-era mixin)
                        // For now, use basic ESQ without BGExecutionId filter
                        // The IntExcelReportService should handle the filtering
                        var esqJson = buildReportEsq(rootSchemaName || "Order", null);

                        // Step 3: Call IntExcelReportService/GetExportFiltersKey (ORIGINAL endpoint)
                        var payload = {
                            EsqString: JSON.stringify(esqJson),
                            ReportId: reportId,
                            RecordCollection: []
                        };

                        console.log("[INTEXCEL] Calling GetExportFiltersKey...");

                        try {
                            var keyResponse = await fetch("/0/rest/IntExcelReportService/GetExportFiltersKey", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json",
                                    "BPMCSRF": getBpmcsrf()
                                },
                                body: JSON.stringify(payload)
                            });

                            var keyResult = await keyResponse.json();
                            console.log("[INTEXCEL] GetExportFiltersKey result:", keyResult);

                            // The key could be in different places depending on response format
                            var exportKey = keyResult.key || keyResult.Key || keyResult.exportKey ||
                                           keyResult.ExportFilterKey || keyResult;

                            if (typeof exportKey === "string" && exportKey.startsWith("ExportFilterKey_")) {
                                console.log("[INTEXCEL] Got export key:", exportKey);

                                // Step 4: Download via GetExportFilteredData (ORIGINAL endpoint)
                                var fileName = reportCode || selectedReport.displayValue.replace(/[^a-zA-Z0-9]/g, "_");
                                var downloadUrl = "/0/rest/IntExcelReportService/GetExportFilteredData/" +
                                                  encodeURIComponent(fileName) + "/" +
                                                  encodeURIComponent(exportKey);

                                console.log("[INTEXCEL] Download URL:", downloadUrl);

                                // Use hidden iframe for download (canonical approach)
                                var iframe = document.getElementById("reportDownloadFrame");
                                if (!iframe) {
                                    iframe = document.createElement("iframe");
                                    iframe.id = "reportDownloadFrame";
                                    iframe.style.display = "none";
                                    document.body.appendChild(iframe);
                                }
                                iframe.src = downloadUrl;
                                console.log("[INTEXCEL] Download initiated via hidden iframe");
                            } else {
                                console.error("[INTEXCEL] Invalid key format:", exportKey);
                                alert("Report generation failed - invalid key returned. Please contact support.");
                            }
                        } catch (e) {
                            console.error("[INTEXCEL] GetExportFiltersKey error:", e);
                            alert("Error generating report: " + e.message);
                        }
                    } catch (e) {
                        console.error("[INTEXCEL] Handler error:", e);
                    }

                    // Don't call next for Excel reports (we handled it)
                    return;
                }
            }
        ]/**SCHEMA_HANDLERS*/
    };
});
